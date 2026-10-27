"""G5 报警与消息"""
from __future__ import annotations

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def alarm_balance_list(page: int = 1, limit: int = 20, buildingId: str = "",
                                 status: str = "") -> dict:
        """低余额报警分页（余额不足预警清单）。status 过滤处理状态。"""
        data = await client.request(
            "GET", "/hzeb-charge/ecabalancealarm/list",
            params={"pageNo": page, "pageSize": limit, "buildingId": buildingId, "status": status})
        return unwrap_rows(data)

    @mcp.tool
    async def alarm_balance_handle(alarmIds: list[str], handleType: str = "confirm",
                                   confirm: bool = False) -> dict:
        """⚠️ 处理低余额报警（单条/批量）。confirm=false 仅预览。"""
        if not confirm:
            return {"needConfirm": True, "alarmIds": alarmIds, "handleType": handleType}
        if len(alarmIds) == 1:
            return await client.request("POST", "/hzeb-charge/ecabalancealarm/handleAlarm",
                                        json_body={"id": alarmIds[0], "handleType": handleType})
        return await client.request("POST", "/hzeb-charge/ecabalancealarm/handleAlarmBatch",
                                    json_body={"ids": alarmIds, "handleType": handleType})

    @mcp.tool
    async def alarm_usage_event_list(page: int = 1, limit: int = 20, buildingId: str = "",
                                     eventType: str = "", startDate: str = "", endDate: str = "") -> dict:
        """异常用能事件分页（漏水/窃水/超量等事件）。日期 YYYY-MM-DD，默认近 30 天。"""
        from datetime import date as _d, timedelta as _td
        ed = endDate or _d.today().isoformat()
        sd = startDate or (_d.today() - _td(days=30)).isoformat()
        data = await client.request(
            "GET", "/hzeb-collection/ecoEeventdata/list",
            params={"page": page, "limit": limit, "buildingId": buildingId,
                    "eventType": eventType, "startdate": sd, "enddate": ed, "isRead": 0})
        return unwrap_rows(data)

    @mcp.tool
    async def alarm_message_list(page: int = 1, limit: int = 20, domain: str = "charge",
                                 confirmStatus: str = "0", eventLevel: int | None = None,
                                 alarmType: str = "", eventType: str = "",
                                 startDate: str = "", endDate: str = "",
                                 buildingId: int | None = None) -> dict:
        """系统/报警消息分页（报警、断电、断水、通讯异常等）。
        domain: charge/collection/energy；confirmStatus: 0 未确认 1 已确认（空=全部）；
        eventLevel: 1 一般 2 紧急 3 严重；默认近 30 天。"""
        from datetime import date, timedelta
        ed = endDate or date.today().isoformat()
        sd = startDate or (date.today() - timedelta(days=30)).isoformat()
        body = {
            "buildingId": buildingId if buildingId is not None else 2,
            "confirmTimeStart": "", "confirmTimeEnd": "",
            "happenTimeStart": f"{sd} 00:00:00", "happenTimeEnd": f"{ed} 23:59:59",
            "eventLevel": eventLevel if eventLevel is not None else 3,
            "confirmStatus": confirmStatus, "alarmType": alarmType, "eventType": eventType,
            "handler": "", "meterNameOrNo": "", "page": page, "limit": limit,
            "buildingType": "23028,23025,23027",
        }
        data = await client.request("POST", f"/hzeb-{domain}/systemMessage/listMessage", json_body=body)
        return unwrap_rows(data)

    @mcp.tool
    async def alarm_message_mark_read(messageId: str) -> dict:
        """将一条报警消息标记为已读。"""
        return await client.request(
            "GET", f"/hzeb-collection/ecamessagelist/ecamessagelist/readed/{messageId}")

    @mcp.tool
    async def alarm_fault_repair_list(page: int = 1, limit: int = 100, solveStatus: str = "") -> dict:
        """故障报修工单分页。solveStatus 如 待处理/已处理。"""
        data = await client.request(
            "GET", "/hzeb-charge/customerproblem/customerproblem/list",
            params={"page": page, "limit": limit, "solveStatus": solveStatus})
        return unwrap_rows(data)

    @mcp.tool
    async def alarm_unread_count() -> dict:
        """各服务未确认系统消息计数（收费域+采集域）。"""
        import asyncio
        a, b = await asyncio.gather(
            client.request("GET", "/hzeb-charge/systemMessage/getUnConfirm"),
            client.request("GET", "/hzeb-collection/systemMessage/getUnConfirm"),
            return_exceptions=True)
        out = {}
        for k, v in (("charge", a), ("collection", b)):
            out[k] = v if not isinstance(v, Exception) else str(v)
        return out
