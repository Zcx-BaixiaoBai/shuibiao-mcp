"""配置加载：环境变量优先，其次 .env 文件。安装时通过 .env 引导配置。"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ENV_KEYS = {
    "SHUIBIAO_BASE_URL": "https://shuibiao.jinying.com",
    "SHUIBIAO_USERNAME": "",
    "SHUIBIAO_PASSWORD": "",
    "SHUIBIAO_DOWNLOAD_DIR": "",
    "SHUIBIAO_SESSION_FILE": "",
}


def _load_env_file() -> None:
    """把 .env（当前工作目录或包上三级项目根）里未设置的键注入 environ。"""
    candidates = [Path.cwd() / ".env", Path(__file__).resolve().parents[2] / ".env"]
    for path in candidates:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            os.environ.setdefault(key, val)
        break


@dataclass
class Config:
    base_url: str
    username: str
    password: str
    download_dir: Path
    session_file: Path

    def missing(self) -> list[str]:
        miss = []
        if not self.username:
            miss.append("SHUIBIAO_USERNAME（登录账号）")
        if not self.password:
            miss.append("SHUIBIAO_PASSWORD（登录密码）")
        return miss


def load_config() -> Config:
    _load_env_file()
    base_url = os.environ.get("SHUIBIAO_BASE_URL", ENV_KEYS["SHUIBIAO_BASE_URL"]).rstrip("/")
    project_root = Path(__file__).resolve().parents[2]
    download_dir = Path(os.environ.get("SHUIBIAO_DOWNLOAD_DIR") or project_root / "downloads")
    session_file = Path(os.environ.get("SHUIBIAO_SESSION_FILE") or project_root / ".session.json")
    return Config(
        base_url=base_url,
        username=os.environ.get("SHUIBIAO_USERNAME", ""),
        password=os.environ.get("SHUIBIAO_PASSWORD", ""),
        download_dir=download_dir,
        session_file=session_file,
    )
