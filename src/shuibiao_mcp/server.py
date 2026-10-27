"""水表 MCP 服务入口：FastMCP stdio。"""
from __future__ import annotations

from fastmcp import FastMCP

from . import (tools_alarm, tools_archives, tools_auth, tools_charge, tools_dashboard,
               tools_energy_reports, tools_metering, tools_system, tools_writes)
from .client import ShuibiaoClient
from .config import load_config

mcp = FastMCP(
    "shuibiao-mcp",
    instructions=(
        "南京金鹰智慧能源管理平台（智能水表/电表）MCP。"
        "首次使用或会话过期时：先 auth_get_captcha 取验证码图（base64），识别 4 位字母后 auth_login。"
        "【写入确认强制策略】任何带 confirm 参数的写操作 tool：第一次调用必须 confirm=False 取得预览；"
        "随后必须把预览内容（endpoint + body）原样展示给用户并询问是否执行；"
        "只有在用户明确回复同意后，才允许以 confirm=True、相同参数再次调用。禁止跳过用户确认直接写。"
        "导出类 tool 将文件下载到配置的 SHUIBIAO_DOWNLOAD_DIR 并返回本地绝对路径。"
    ),
)

_client = ShuibiaoClient(load_config())

for mod in (tools_auth, tools_dashboard, tools_archives, tools_metering, tools_alarm,
            tools_charge, tools_energy_reports, tools_system, tools_writes):
    mod.register(mcp, _client)


@mcp.prompt
def setup_guide() -> str:
    """安装配置引导：凭据、下载目录、MCP 注册与首次登录流程。"""
    cfg = _client.cfg
    miss = cfg.missing()
    lines = [
        "水表 MCP 安装引导：",
        f"1. 配置文件 .env（当前项目根）需包含：SHUIBIAO_USERNAME、SHUIBIAO_PASSWORD、SHUIBIAO_DOWNLOAD_DIR。"
        f"当前缺失：{miss if miss else '无'}",
        f"2. 当前生效配置：base_url={cfg.base_url} download_dir={cfg.download_dir}",
        "3. 在 ZCode/Claude Desktop 的 MCP 设置中加入：",
        '   {"mcpServers": {"shuibiao": {"command": "uv", "args": ["--directory", "<项目绝对路径>", "run", "shuibiao-mcp"]}}}',
        "4. 首次登录：auth_get_captcha → 识别 4 位字母 → auth_login(captcha, checkKey)。",
        "5. 自检：auth_status 或资源 shuibiao://config/status。",
    ]
    return "\n".join(lines)


@mcp.resource("shuibiao://config/status")
async def resource_config_status() -> str:
    """配置与会话状态（安装自检用）。"""
    miss = _client.cfg.missing()
    sess = _client.load_session()
    lines = [f"base_url={_client.cfg.base_url}",
             f"download_dir={_client.cfg.download_dir}",
             f"configured={'yes' if not miss else 'missing: ' + ', '.join(miss)}",
             f"session_alive={'yes' if sess.alive() else 'no'}"]
    return "\n".join(lines)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
