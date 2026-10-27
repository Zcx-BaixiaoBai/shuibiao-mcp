"""G9 系统管理"""
from __future__ import annotations

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def system_user_list(page: int = 1, limit: int = 20, username: str = "") -> dict:
        """操作用户分页（系统管理→用户权限→用户管理），含角色下拉字典。"""
        data = await client.request("GET", "/hzeb-base/sys/user/list",
                                    params={"pageNo": page, "pageSize": limit, "username": username})
        out = unwrap_rows(data)
        out["roleOptions"] = await client.request("GET", "/hzeb-base/sys/role/down/list")
        return out

    @mcp.tool
    async def system_user_write(action: str, user: dict, confirm: bool = False) -> dict:
        """⚠️ 操作用户写操作。action: save 新增 / update 修改 / delete 删除(user 传 {userId}) /
        resetPassword 重置密码(user 传 {userId, newPassword})。confirm=false 仅预览。"""
        paths = {"save": "/hzeb-base/sys/user/save", "update": "/hzeb-base/sys/user/update",
                 "delete": "/hzeb-base/sys/user/delete", "resetPassword": "/hzeb-base/sys/user/resetPassword"}
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "action": action, "user": user}
        method = "POST" if action in ("save", "update") else "PUT" if action == "resetPassword" else "DELETE"
        return await client.request(method, paths[action], json_body=user)

    @mcp.tool
    async def system_role_list(page: int = 1, limit: int = 20, roleName: str = "") -> dict:
        """角色分页 + 可授权菜单树。"""
        data = await client.request("GET", "/hzeb-base/sys/role/list",
                                    params={"page": page, "limit": limit, "customerId": "1",
                                            "roleName": roleName})
        out = unwrap_rows(data)
        try:
            out["menuTree"] = await client.request(
                "GET", "/hzeb-base/sys/menu/getAllMenu/tree", params={"customerId": "1"})
        except ApiError:
            out["menuTree"] = None
        return out

    @mcp.tool
    async def system_role_write(action: str, role: dict, confirm: bool = False) -> dict:
        """⚠️ 角色写操作。action: save / update / delete。confirm=false 仅预览。"""
        paths = {"save": "/hzeb-base/sys/role/save", "update": "/hzeb-base/sys/role/update",
                 "delete": "/hzeb-base/sys/role/delete"}
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "action": action, "role": role}
        return await client.request("POST", paths[action], json_body=role)

    @mcp.tool
    async def system_log_list(page: int = 1, limit: int = 20, username: str = "",
                              startDate: str = "", endDate: str = "") -> dict:
        """系统操作日志分页（增删改/远程控制等操作追溯）。优先 base 域 queryPage，失败回退 charge 域 list。"""
        params = {"pageNo": page, "pageSize": limit, "page": page, "limit": limit,
                  "username": username, "startTime": startDate, "endTime": endDate,
                  "starttime": startDate, "endtime": endDate}
        try:
            data = await client.request("GET", "/hzeb-base/ecoSyslog/queryPage", params=params)
        except ApiError:
            data = await client.request("GET", "/hzeb-charge/ecosyslog/list", params=params)
        return unwrap_rows(data)

    @mcp.tool
    async def system_params() -> dict:
        """系统参数集合：客户信息/服务包/收费配置/业务选项（只读）。"""
        import asyncio
        cust, pack, cfg, opt = await asyncio.gather(
            client.request("GET", "/hzeb-base/sys/parameter/get/customer/info", params={"customerId": 1}),
            client.request("GET", "/hzeb-base/sys/parameter/get/service/pack"),
            client.request("GET", "/hzeb-charge/customerconfig/info"),
            client.request("GET", "/hzeb-charge/systemoption/systemoption/getOption"),
            return_exceptions=True)
        return {k: (v if not isinstance(v, Exception) else str(v))
                for k, v in (("customer", cust), ("servicePack", pack), ("chargeConfig", cfg), ("options", opt))}
