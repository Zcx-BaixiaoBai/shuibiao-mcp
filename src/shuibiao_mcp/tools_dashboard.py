"""G2 总览看板"""
from __future__ import annotations

import asyncio
from datetime import date

from fastmcp import FastMCP

from .client import ShuibiaoClient


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def dashboard_charge_summary(year: int | None = None, buildingId: str = "") -> dict:
        """收费视窗汇总：净实收/总实收/总退费、应收(电/水)、其他收入、缴费方式占比、
        回收率、月度收应收序列、表计/房间/异常计数。year 默认当年。"""
        y = year or date.today().year
        base = "/hzeb-charge/ecochargerecord"
        q = {"customerId": "1", "buildingId": buildingId}
        qy = {**q, "year": y}
        receipts, receivable, annual, other, pay_cls, recovery, meter, room, abnormal = await asyncio.gather(
            client.request("GET", f"{base}/hydropowerReceipts", params=qy),
            client.request("GET", f"{base}/hydropowerReceivable", params=qy),
            client.request("GET", f"{base}/annualSummary/v2", params=qy),
            client.request("GET", f"{base}/otherIncome", params=qy),
            client.request("GET", f"{base}/payClassification", params=qy),
            client.request("GET", f"{base}/recoveryRate", params=qy),
            client.request("GET", f"{base}/meter/v2", params=q),
            client.request("GET", f"{base}/room", params=q),
            client.request("GET", f"{base}/abnormal", params=q),
        )
        return {"year": y, "receipts": receipts, "receivable": receivable,
                "monthlySummary": annual, "otherIncome": other, "payClassification": pay_cls,
                "recoveryRate": recovery, "meters": meter, "rooms": room, "abnormal": abnormal}

    @mcp.tool
    async def dashboard_collection_status(projectId: int = 1) -> dict:
        """采集运行状态：集中器/采集模块的在线、离线数量与在线率。"""
        return await client.request("GET", "/hzeb-collection/concentrator/statistics",
                                    params={"projectId": projectId})
