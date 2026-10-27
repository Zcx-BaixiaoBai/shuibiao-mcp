"""G4 抄表与采集（参数名对齐生产抓包：startdate/enddate 带时分秒、energyTypeID、appType 等）"""
from __future__ import annotations

from datetime import date, datetime, timedelta

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows

WATER, ELEC = "01002", "01001"


def _dt_range(startDate: str, endDate: str) -> tuple[str, str]:
    sd = startDate or date.today().isoformat()
    ed = endDate or sd
    return f"{sd} 00:00:00", f"{ed} 23:59:59"


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def metering_reading_water(page: int = 1, limit: int = 20, startDate: str = "",
                                     endDate: str = "", buildingId: str = "1",
                                     meterNo: str = "") -> dict:
        """抄表数据(水)分页：日冻结水量明细 + 区间合计。日期 YYYY-MM-DD，默认当天。"""
        sd, ed = _dt_range(startDate, endDate)
        base = "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water"
        q = {"startdate": sd, "enddate": ed, "energyTypeID": WATER, "buildingID": buildingId,
             "page": page, "limit": limit, "appType": "1", "type": "1", "comAddress": meterNo}
        data = await client.request("GET", base, params=q)
        out = unwrap_rows(data)
        out["total_amount"] = await client.request("GET", base + "/total", params=q)
        return out

    @mcp.tool
    async def metering_reported_data(page: int = 1, limit: int = 20, buildingId: str = "1",
                                     meterNo: str = "") -> dict:
        """上报数据查询（表计原始上报报文记录）。"""
        data = await client.request(
            "GET", "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterList",
            params={"page": page, "limit": limit, "buildingId": buildingId,
                    "energy": WATER, "comAddress": meterNo})
        return unwrap_rows(data)

    @mcp.tool
    async def metering_success_rate(startDate: str = "", endDate: str = "",
                                    buildingId: str = "1") -> dict:
        """抄表成功率：按日列表 + 区间合计。默认近 30 天。"""
        ed = endDate or date.today().isoformat()
        sd = startDate or (date.today() - timedelta(days=30)).isoformat()
        sdt, edt = _dt_range(sd, ed)
        base = "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRate"
        q = {"type": "1", "appType": "1", "limit": 100, "page": 1, "buildingId": buildingId,
             "energy": WATER, "customerId": "1", "startdate": sdt, "enddate": edt}
        lst = await client.request("GET", f"{base}/list", params=q)
        total = await client.request("GET", f"{base}/total", params=q)
        return {"list": unwrap_rows(lst), "total": total}

    @mcp.tool
    async def metering_frozen_loss(page: int = 1, limit: int = 20, month: str = "",
                                   buildingId: str = "1") -> dict:
        """冻损/缺失表计列表（手工补录依据）。month 格式 YYYYMM，默认当月。"""
        m = month or datetime.now().strftime("%Y%m")
        data = await client.request(
            "GET", "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenLossMeter/v2",
            params={"page": page, "limit": limit, "appType": "1", "buildingId": buildingId,
                    "energy": WATER, "type": "1", "date": m})
        return unwrap_rows(data)

    @mcp.tool
    async def metering_remote_control(meterNos: list[str], action: str, confirm: bool = False,
                                      reason: str = "") -> dict:
        """⚠️ 远程阀控：对水/电表执行通断控制（action=open 合闸/开阀, close 拉闸/关阀）。
        影响实际供水供电！confirm=false 时仅返回待执行清单预览；确认执行需 confirm=true。"""
        if action not in ("open", "close"):
            raise ApiError(400, "action 仅支持 open/close")
        preview = {"action": action, "meterCount": len(meterNos), "meterNos": meterNos[:50],
                   "warning": "该操作将远程断水/断电或恢复供应"}
        if not confirm:
            return {"needConfirm": True, **preview}
        return await client.request(
            "POST", "/hzeb-charge/comEspecialtask/emergencyControlBatch",
            json_body={"meterNos": meterNos, "controlType": action, "reason": reason})

    @mcp.tool
    async def metering_control_records(page: int = 1, limit: int = 20, buildingId: str = "",
                                       startDate: str = "", endDate: str = "") -> dict:
        """远程控制/应急控制流水分页。"""
        data = await client.request(
            "GET", "/hzeb-charge/comEspecialtask/controlList",
            params={"page": page, "limit": limit, "buildingId": buildingId,
                    "startTime": startDate, "endTime": endDate})
        return unwrap_rows(data)
