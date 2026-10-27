"""HTTP 客户端：SSRF 防护 + 会话管理（JWT 请求头模式）。

安全约束：仅允许 http/https；每次请求前校验 host，拒绝 localhost、环回、
私有与保留地址（含 DNS 解析后的全部 IP）；不跟随重定向。
"""
from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import socket
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx

from .config import Config

_dns_cache: dict[str, tuple[float, list[str]]] = {}


class UnsafeUrlError(Exception):
    """目标地址不在允许范围（非 http/https 或指向环回/私有/保留地址）。"""


class NeedLoginError(Exception):
    """会话缺失或已过期：请先调用 auth_get_captcha + auth_login。"""


class ApiError(Exception):
    def __init__(self, code, msg: str):
        super().__init__(f"[{code}] {msg}")
        self.code = code
        self.msg = msg


def _ip_unsafe(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True
    return (
        addr.is_loopback or addr.is_private or addr.is_reserved
        or addr.is_link_local or addr.is_multicast or addr.is_unspecified
    )


def assert_safe_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UnsafeUrlError(f"仅允许 http/https，收到: {parsed.scheme!r}")
    host = (parsed.hostname or "").lower().rstrip(".")
    if not host:
        raise UnsafeUrlError("URL 缺少 host")
    if host == "localhost" or host.endswith(".localhost"):
        raise UnsafeUrlError("拒绝 localhost")
    try:
        ipaddress.ip_address(host)
        if _ip_unsafe(host):
            raise UnsafeUrlError(f"拒绝环回/私有/保留地址: {host}")
        return
    except ValueError:
        pass  # 域名，走 DNS 校验
    now = time.time()
    hit = _dns_cache.get(host)
    if hit and now - hit[0] < 60:
        ips = hit[1]
    else:
        try:
            infos = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
        except socket.gaierror as exc:
            raise UnsafeUrlError(f"DNS 解析失败: {host} ({exc})") from exc
        ips = sorted({i[4][0] for i in infos})
        _dns_cache[host] = (now, ips)
    if not ips or any(_ip_unsafe(ip) for ip in ips):
        raise UnsafeUrlError(f"拒绝解析到环回/私有/保留地址的域名: {host} -> {ips}")


@dataclass
class Session:
    token: str = ""
    userid: str = ""
    username: str = ""
    customerid: str = ""
    customername: str = ""  # 原文，发请求时 URL 编码
    roletype: str = ""
    remoteadd: str = ""
    expire_at: float = 0.0

    def alive(self) -> bool:
        return bool(self.token) and time.time() < self.expire_at - 30

    def headers(self) -> dict[str, str]:
        from urllib.parse import quote
        return {
            "token": self.token,
            "username": self.username,
            "userid": self.userid,
            "customerid": self.customerid,
            "customername": quote(self.customername),
            "roletype": self.roletype,
            "remoteadd": self.remoteadd,
            "accept": "application/json, text/plain, */*",
        }


@dataclass
class ShuibiaoClient:
    cfg: Config
    session: Session = field(default_factory=Session)
    _http: httpx.AsyncClient | None = None
    _pending_check_key: int | None = None

    # ---- 基础设施 ----
    def http(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=30.0, follow_redirects=False)
        return self._http

    async def aclose(self) -> None:
        if self._http is not None:
            await self._http.aclose()
            self._http = None

    def load_session(self) -> Session:
        if self.session.alive():
            return self.session
        try:
            raw = json.loads(self.cfg.session_file.read_text(encoding="utf-8"))
            sess = Session(**{k: raw[k] for k in Session.__dataclass_fields__ if k in raw})
            if sess.alive():
                self.session = sess
        except (OSError, ValueError, TypeError, KeyError):
            pass
        return self.session

    def save_session(self) -> None:
        self.cfg.session_file.parent.mkdir(parents=True, exist_ok=True)
        self.cfg.session_file.write_text(
            json.dumps(self.session.__dict__, ensure_ascii=False), encoding="utf-8")

    # ---- 认证 ----
    async def public_ip(self) -> str:
        assert_safe_url("https://checkip.amazonaws.com/")
        r = await self.http().get("https://checkip.amazonaws.com/")
        return r.text.strip()

    async def fetch_captcha(self) -> dict:
        """返回 {checkKey, imageBase64}；imageBase64 为纯 base64（不含 data: 前缀）。"""
        check_key = int(time.time() * 1000)
        url = f"{self.cfg.base_url}/hzeb-base/sys/user/randomImage/{check_key}"
        assert_safe_url(url)
        r = await self.http().get(url)
        payload = r.json() if r.headers.get("content-type", "").startswith("application/json") else None
        if payload is not None:
            img = payload.get("result") or payload.get("data") or ""
            if isinstance(img, dict):
                img = img.get("captcha") or img.get("img") or next(iter(img.values()), "")
        else:
            img = "data:image/jpeg;base64," + base64.b64encode(r.content).decode()
        if isinstance(img, str) and img.startswith("data:"):
            img = img.split(",", 1)[1]
        self._pending_check_key = check_key
        return {"checkKey": check_key, "imageBase64": img}

    async def login(self, captcha: str, check_key: int | None = None) -> dict:
        if not self.cfg.username or not self.cfg.password:
            raise NeedLoginError("未配置 SHUIBIAO_USERNAME / SHUIBIAO_PASSWORD，请在 .env 中配置后重启 MCP")
        ck = check_key if check_key is not None else self._pending_check_key
        if ck is None:
            raise NeedLoginError("checkKey 缺失：请先调用 auth_get_captcha")
        # MD5 为服务端登录协议强制要求（抓包确认 userPassword=base64(md5hex(密码))），非本地安全选型
        md5hex = hashlib.md5(self.cfg.password.encode()).hexdigest()
        body = {
            "userName": self.cfg.username,
            "userPassword": base64.b64encode(md5hex.encode()).decode(),
            "checkKey": ck,
            "captcha": captcha,
            "loginIp": await self.public_ip(),
        }
        url = f"{self.cfg.base_url}/hzeb-base/sys/user/login"
        assert_safe_url(url)
        r = await self.http().post(url, json=body, headers={"remoteadd": body["loginIp"]})
        data = r.json()
        if data.get("code") != 200:
            raise ApiError(data.get("code"), data.get("msg") or "登录失败")
        d = data["data"]
        user = d.get("userObj") or {}
        roles = user.get("roleTypes") or [{}]
        cust = (d.get("customerList") or [{}])[0]
        self.session = Session(
            token=d["token"],
            userid=str(d.get("userId")),
            username=d.get("userName") or self.cfg.username,
            customerid=str(cust.get("customerId", "1")),
            customername=d.get("customerName_1") or cust.get("customerName", ""),
            roletype=str(roles[0].get("roleType", "")),
            remoteadd=body["loginIp"],
            expire_at=time.time() + float(d.get("expire", 10800)),
        )
        self.save_session()
        return {"username": self.session.username, "customer": self.session.customername,
                "expireSeconds": d.get("expire")}

    # ---- 业务请求 ----
    async def request(self, method: str, path: str, *, params=None, json_body=None,
                      raw: bool = False):
        sess = self.load_session()
        if not sess.alive():
            raise NeedLoginError("会话未建立或已过期：请调用 auth_get_captcha 获取验证码图，识别后调用 auth_login")
        url = self.cfg.base_url + path
        assert_safe_url(url)
        r = await self.http().request(method, url, params=params, json=json_body, headers=sess.headers())
        if r.status_code == 401:
            raise NeedLoginError("token 被服务端拒绝(401)：请重新走验证码登录流程")
        if raw:
            return r
        if r.status_code in (502, 503, 504):
            raise ApiError(r.status_code, "上游微服务不可用（网关 502/503/504）：该服务在当前部署未运行或暂故障")
        try:
            data = r.json()
        except ValueError:
            raise ApiError(r.status_code, f"非 JSON 响应: {r.text[:200]}")
        code = data.get("code", data.get("status"))
        msg = data.get("msg") or data.get("message") or ""
        if code in (401, "401") or "token" in str(msg).lower() and code != 200:
            raise NeedLoginError(f"会话失效({msg})：请重新走验证码登录流程")
        if code not in (200, 0, "200", None) and data.get("success") is not True:
            raise ApiError(code, msg)
        return data.get("data", data.get("result", data))


def unwrap_rows(payload) -> dict:
    """统一分页响应：兼容 {records,total} / {list,total} / 裸 list。"""
    if isinstance(payload, list):
        return {"rows": payload, "total": len(payload)}
    if isinstance(payload, dict):
        for key in ("records", "list", "rows", "content"):
            if key in payload:
                return {"rows": payload[key], "total": payload.get("total", len(payload[key])), "raw": payload}
    return {"rows": [], "total": 0, "raw": payload}
