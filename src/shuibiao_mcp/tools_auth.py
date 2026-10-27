"""G1 认证与会话"""
from __future__ import annotations

import time

from fastmcp import FastMCP

from .client import ShuibiaoClient


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def auth_get_captcha() -> dict:
        """获取登录图形验证码。返回 base64 图片（imageBase64）与 checkKey。

        请识别图中 4 位字母（不区分大小写通常可接受，按原样提交），
        然后调用 auth_login(captcha=识别结果, checkKey=本返回值)。
        """
        return await client.fetch_captcha()

    @mcp.tool
    async def auth_login(captcha: str, checkKey: int | None = None) -> dict:
        """用验证码完成登录（账号密码取自服务端配置）。成功返回用户与客户信息。"""
        return await client.login(captcha, checkKey)

    @mcp.tool
    async def auth_status() -> dict:
        """查看当前会话状态：是否已登录、用户、客户、剩余有效期；未配置凭据时给出配置指引。"""
        miss = client.cfg.missing()
        if miss:
            return {"loggedIn": False, "needConfig": miss,
                    "guide": "在项目 .env 中设置 SHUIBIAO_USERNAME / SHUIBIAO_PASSWORD / SHUIBIAO_DOWNLOAD_DIR 后重启 MCP"}
        sess = client.load_session()
        if not sess.alive():
            return {"loggedIn": False, "needLogin": True,
                    "guide": "调用 auth_get_captcha 获取验证码图并识别，再调用 auth_login"}
        return {"loggedIn": True, "username": sess.username, "customer": sess.customername,
                "remainingSeconds": int(sess.expire_at - time.time())}
