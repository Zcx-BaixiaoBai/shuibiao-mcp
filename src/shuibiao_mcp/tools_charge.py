"""G6 收费与账单"""
from __future__ import annotations

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def charge_price_list() -> dict:
        """水电单价/费率配置列表（含阶梯/分时费率结构）。"""
        data = await client.request("GET", "/hzeb-charge/customerefldj/customerefldj/fldjConfigList")
        return {"configs": data} if isinstance(data, list) else data

    @mcp.tool
    async def charge_bill_list(billType: str = "water", page: int = 1, limit: int = 20,
                               buildingId: str = "", roomNo: str = "", status: str = "",
                               startDate: str = "", endDate: str = "") -> dict:
        """账单分页查询。billType: water 水费 / elec 电费 / share 公摊 / other 其他 /
        income 水电收支。status: 未支付/已支付 等。"""
        if billType in ("water", "elec"):
            path = "/hzeb-charge/customerfee/customerfee/feeBillList/page"
            tpath = "/hzeb-charge/customerfee/customerfee/feeBillList/total"
            energy = "01002" if billType == "water" else "01001"
            params = {"pageNo": page, "pageSize": limit, "buildingId": buildingId,
                      "roomNo": roomNo, "status": status, "energyType": energy,
                      "startTime": startDate, "endTime": endDate}
        elif billType == "other":
            path = "/hzeb-charge/customerfee/customerfee/otherBillList/page"
            tpath = "/hzeb-charge/customerfee/customerfee/otherBillList/total"
            params = {"pageNo": page, "pageSize": limit, "buildingId": buildingId,
                      "startTime": startDate, "endTime": endDate}
        elif billType == "income":
            path = "/hzeb-charge/charge/billList"
            tpath = None
            params = {"page": page, "limit": limit, "buildingId": buildingId,
                      "startTime": startDate, "endTime": endDate}
        else:  # share 公摊
            path = "/hzeb-charge/charge/get/bill/list"
            tpath = None
            params = {"page": page, "limit": limit, "buildingId": buildingId,
                      "billType": billType, "startTime": startDate, "endTime": endDate}
        data = await client.request("GET", path, params=params)
        out = unwrap_rows(data)
        if tpath:
            out["total_amount"] = await client.request("GET", tpath, params=params)
        return out

    @mcp.tool
    async def charge_notice_status(buildingId: str = "") -> dict:
        """收费通知单启用状态与按通知单的建筑列表。"""
        status = await client.request("GET", "/hzeb-charge/customerbillnotice/billnoticeStatus")
        lst = await client.request(
            "GET", "/hzeb-charge/customerbuildinginfo/customerbuildinginfo/listByNotice",
            params={"buildingId": buildingId})
        return {"noticeStatus": status, "buildings": unwrap_rows(lst)}

    @mcp.tool
    async def charge_payment_query(page: int = 1, limit: int = 20, startDate: str = "",
                                   endDate: str = "", buildingId: str = "2", payWay: str = "") -> dict:
        """收费查询：实收流水分页 + 合计（财务对账→收费查询）。日期 YYYY-MM-DD，默认本月。"""
        from datetime import date as _d
        sd = startDate or _d.today().replace(day=1).isoformat()
        ed = endDate or _d.today().isoformat()
        q = {"page": page, "limit": limit, "buildingId": buildingId,
             "beginTime": sd, "endTime": ed, "payWay": payWay}
        data = await client.request("GET", "/hzeb-charge/ecochargerecord/ecochargerecord/findRealList/page", params=q)
        out = unwrap_rows(data)
        out["total_amount"] = await client.request(
            "GET", "/hzeb-charge/ecochargerecord/ecochargerecord/findRealList/total", params=q)
        return out

    @mcp.tool
    async def charge_finance_stats(kind: str = "recharge", startDate: str = "",
                                   endDate: str = "", buildingId: str = "2") -> dict:
        """财务统计。kind: recharge 充值统计(实收合计) / arrears 欠费统计 / inventory 账目盘点(流水分页)。"""
        from datetime import date as _d
        sd = startDate or _d.today().replace(day=1).isoformat()
        ed = endDate or _d.today().isoformat()
        q = {"buildingId": buildingId, "beginTime": sd, "endTime": ed}
        if kind == "recharge":
            return await client.request("GET", "/hzeb-charge/ecochargerecord/ecochargerecord/findRealList/total", params=q)
        if kind == "arrears":
            return await client.request("GET", "/hzeb-charge/ecochargerecord/ecochargerecord/noPayBillSummary", params=q)
        if kind == "inventory":
            page = await client.request("GET", "/hzeb-charge/ecochargerecord/ecochargerecord/findRealList/page", params={**q, "page": 1, "limit": 20})
            return unwrap_rows(page)
        raise ApiError(400, "kind 仅支持 recharge/arrears/inventory")

    @mcp.tool
    async def charge_recharge(buildingId: int, chargeAmount: float, chargeWay: str = "offline",
                              chargeType: str = "1", confirm: bool = False) -> dict:
        """⚠️ 账户充值（chargeEnergy）。chargeWay: offline 线下 / wechat 微信；
        chargeType: 1 按金额 2 按电量等（以平台表单为准）。
        confirm=false 仅返回预览；涉及资金，必须经用户明确确认后 confirm=true。"""
        body = {"buildingId": buildingId, "chargeAmount": chargeAmount,
                "chargeWay": chargeWay, "chargeType": chargeType}
        preview = {**body, "warning": "该操作将向账户写入余额/电量"}
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/comechargetask/comechargetask/chargeEnergy", "body": preview}
        return await client.request(
            "POST", "/hzeb-charge/comechargetask/comechargetask/chargeEnergy", json_body=body)

    @mcp.tool
    async def charge_account_open(roomIds: list[str], confirm: bool = False) -> dict:
        """⚠️ 批量开户。confirm=false 仅预览。"""
        if not confirm:
            return {"needConfirm": True, "roomIds": roomIds}
        return await client.request(
            "POST", "/hzeb-charge/customeraccount/customeraccount/openUserBatch",
            json_body={"roomIds": roomIds})

    @mcp.tool
    async def charge_close_account_list(page: int = 1, limit: int = 20, buildingId: str = "") -> dict:
        """销户结算记录分页（销户管理/销户结算报表）。"""
        data = await client.request(
            "GET", "/hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/list",
            params={"pageNo": page, "pageSize": limit, "buildingId": buildingId})
        return unwrap_rows(data)

    @mcp.tool
    async def charge_low_balance_report(page: int = 1, limit: int = 20, buildingId: str = "") -> dict:
        """低余额提醒报表（预付费余额不足房间清单）。"""
        data = await client.request(
            "GET", "/hzeb-charge/ecabalancealarm/list",
            params={"pageNo": page, "pageSize": limit, "buildingId": buildingId})
        return unwrap_rows(data)
