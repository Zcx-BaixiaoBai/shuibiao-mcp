"""G7 能耗分析 + G8 报表查询"""
from __future__ import annotations

from pathlib import Path

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    # ---- G7 能耗 ----
    @mcp.tool
    async def energy_overview() -> dict:
        """能耗总概览：能耗档案拓扑树 + 概览指标。"""
        tree = await client.request("GET", "/hzeb-energy/archives/topologyTree")
        return {"topologyTree": tree}

    @mcp.tool
    async def energy_building(buildingId: str, startDate: str, endDate: str,
                              energyType: str = "water") -> dict:
        """建筑用能分析：区间用量 + 同比/环比。energyType: water/elec。"""
        q = {"buildingId": buildingId, "startTime": startDate, "endTime": endDate,
             "energyType": energyType}
        usage = await client.request("GET", "/hzeb-energy/build/energy", params=q)
        compare = await client.request("GET", "/hzeb-energy/build/buildcompare", params=q)
        return {"usage": usage, "compare": compare}

    @mcp.tool
    async def energy_branch_elec(buildingId: str, startDate: str, endDate: str) -> dict:
        """支路用电 + 线损分析。"""
        q = {"buildingId": buildingId, "startTime": startDate, "endTime": endDate}
        branch = await client.request("GET", "/hzeb-energy/build/time", params=q)
        loss = await client.request("GET", "/hzeb-energy/build/timecompare", params=q)
        return {"branch": branch, "lineLoss": loss}

    @mcp.tool
    async def energy_branch_water(buildingId: str, startDate: str, endDate: str) -> dict:
        """支路用水 + 漏水分析（夜间最小流量法）。"""
        q = {"buildingId": buildingId, "startTime": startDate, "endTime": endDate}
        branch = await client.request("GET", "/hzeb-energy/archives/hlv/list", params=q)
        return {"branch": unwrap_rows(branch)}

    @mcp.tool
    async def energy_rank(buildingId: str = "2", month: str = "", energyType: str = "water",
                          topRank: int = 50, orderRule: str = "desc") -> dict:
        """用能排名（房间/表计用量排行）。month 格式 YYYY-MM，默认上月；
        energyType: water/elec；orderRule: desc/asc。"""
        from datetime import date, timedelta
        m = month or (date.today().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
        q = {"page": 1, "limit": topRank, "buildingId": buildingId,
             "energyId": "01002" if energyType == "water" else "01001",
             "dataType": "1", "orderRule": orderRule, "value": "0",
             "timeType": "2", "topRank": topRank, "timePoint": m}
        rank = await client.request("GET", "/hzeb-charge/ecabalancedaily/energy/energyRank", params=q)
        return {"rank": unwrap_rows(rank)}

    # ---- G8 报表 ----
    @mcp.tool
    async def reports_energy(energyType: str = "water", startDate: str = "", endDate: str = "",
                             buildingId: str = "1", page: int = 1, limit: int = 20) -> dict:
        """用能报表（水/电）分页：日冻结用量汇总 + 合计。日期 YYYY-MM-DD，默认当天。"""
        from datetime import date as _d
        sd = startDate or _d.today().isoformat()
        ed = endDate or sd
        base = "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList"
        path = f"{base}/water" if energyType == "water" else f"{base}/ele"
        q = {"startdate": f"{sd} 00:00:00", "enddate": f"{ed} 23:59:59",
             "energyTypeID": "01002" if energyType == "water" else "01001",
             "buildingID": buildingId, "page": page, "limit": limit, "appType": "1", "type": "1"}
        data = await client.request("GET", path, params=q)
        out = unwrap_rows(data)
        out["total_amount"] = await client.request("GET", path + "/total", params=q)
        return out

    @mcp.tool
    async def reports_records(kind: str = "control", page: int = 1, limit: int = 20,
                              buildingId: str = "", startDate: str = "", endDate: str = "") -> dict:
        """记录类报表。kind: control 远程控制流水 / emergency 应急控制 / close 销户结算 /
        change 换表记录(清零)。"""
        paths = {
            "control": "/hzeb-charge/comEspecialtask/controlList",
            "emergency": "/hzeb-charge/comEspecialtask/controlList",
            "close": "/hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/list",
            "change": "/hzeb-collection/ecoChangemeter/list",
        }
        if kind not in paths:
            raise ApiError(400, f"kind 仅支持 {list(paths)}")
        data = await client.request(
            "GET", paths[kind],
            params={"pageNo": page, "pageSize": limit, "page": page, "limit": limit,
                    "buildingId": buildingId, "startTime": startDate, "endTime": endDate})
        return unwrap_rows(data)

    @mcp.tool
    async def reports_export(reportType: str, startDate: str = "", endDate: str = "",
                             buildingId: str = "") -> dict:
        """导出报表为 Excel，下载到配置的 SHUIBIAO_DOWNLOAD_DIR，返回本地绝对路径。
        reportType: balanceAlarm 低余额 / usageEvent 异常用能 / closeAccount 销户结算 /
        controlList 控制流水 / feeBill 费用账单 / syslog 系统日志。"""
        paths = {
            "balanceAlarm": "/hzeb-charge/ecabalancealarm/export",
            "usageEvent": "/hzeb-collection/ecoEeventdata/export",
            "closeAccount": "/hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/export",
            "controlList": "/hzeb-charge/comEspecialtask/controlListExport",
            "feeBill": "/hzeb-charge/customerfee/customerfee/feeBillExport",
            "syslog": "/hzeb-base/ecoSyslog/export",
        }
        if reportType not in paths:
            raise ApiError(400, f"reportType 仅支持 {list(paths)}")
        r = await client.request("GET", paths[reportType],
                                 params={"startTime": startDate, "endTime": endDate,
                                         "buildingId": buildingId}, raw=True)
        client.cfg.download_dir.mkdir(parents=True, exist_ok=True)
        ext = ".xlsx" if "spreadsheet" in r.headers.get("content-type", "") or r.content[:2] == b"PK" else ".bin"
        target: Path = client.cfg.download_dir / f"{reportType}_{startDate or 'all'}_{endDate or 'now'}{ext}"
        target.write_bytes(r.content)
        return {"path": str(target), "bytes": len(r.content)}
