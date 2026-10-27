"""G10 表单填写类写操作（请求体对齐生产前端 bundle 抓包分析）。

确认策略：所有 tool 默认 confirm=False 仅回显将要提交的请求体预览；
Agent 必须把预览展示给用户、获得用户明确同意后，才能以 confirm=True 重放同一参数。
"""
from __future__ import annotations

from fastmcp import FastMCP

from .client import ApiError, ShuibiaoClient, unwrap_rows

CONFIRM_HINT = "confirm=False 仅预览；须经用户明确确认后以 confirm=True 调用"


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    # ---- 抄表补录与策略下发 ----
    @mcp.tool
    async def metering_manual_entry(form: dict, confirm: bool = False) -> dict:
        """⚠️ 手工补录抄表数据（水/电冻损补录）。form 示例:
        {"type": "daily"|"monthly"|"hourly", "date": "YYYY-MM-DD 或 YYYY-MM",
         "data": [{"meterid": 1000, "dataitemvalue": "123.4", ...}]}
        data 行结构可先由 metering_frozen_loss 读取后修改得到。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "endpoint": "/supervision/beforecalc/frozen/addFrozenData", "body": form}
        try:
            return await client.request("POST", "/supervision/beforecalc/frozen/addFrozenData", json_body=form)
        except ApiError:
            return await client.request(
                "POST", "/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/addFrozenData",
                json_body=form)

    @mcp.tool
    async def metering_time_programme_list(page: int = 1, limit: int = 20) -> dict:
        """校时/参数方案列表（只读）。"""
        data = await client.request("GET", "/hzeb-collection/time/programme/list",
                                    params={"page": page, "limit": limit})
        return unwrap_rows(data)

    @mcp.tool
    async def metering_time_programme_save(form: dict, programmeId: int | None = None,
                                           confirm: bool = False) -> dict:
        """⚠️ 保存/更新校时方案。form 示例:
        {"programmeName": str, "type": "1"|"2", "customerId": 1, "oneValue": str, "twoValue": str}；
        传 programmeId 则走更新。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "body": form, "programmeId": programmeId}
        path = "/hzeb-collection/time/programme/update" if programmeId else "/hzeb-collection/time/programme/save"
        body = {**form, "id": programmeId} if programmeId else form
        return await client.request("POST", path, json_body=body)

    @mcp.tool
    async def metering_dispatch(idList: list[int], kind: str = "time", form: dict | None = None,
                                confirm: bool = False) -> dict:
        """⚠️ 向采集设备下发指令。kind=time 校时下发(anew/distribution, type: 1 校时 2 重启)；
        kind=param 参数下发(parameter/distribution, form 为方案参数体)。""" + CONFIRM_HINT
        if kind == "time":
            body = {"idList": idList, "type": (form or {}).get("type", "1")}
            path = "/hzeb-collection/time/programme/anew/distribution"
        elif kind == "param":
            body = form or {}
            path = "/hzeb-collection/time/programme/parameter/distribution"
        else:
            raise ApiError(400, "kind 仅支持 time/param")
        if not confirm:
            return {"needConfirm": True, "endpoint": path, "body": body}
        return await client.request("POST", path, json_body=body)

    # ---- 收费类表单 ----
    @mcp.tool
    async def charge_bill_adjust(form: dict, confirm: bool = False) -> dict:
        """⚠️ 账单调整（费率调整/调账）。form 为调账表单完整对象（可先读 charge_bill_list 行修改）。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/customerefldj/customerefldj/adjustBills", "body": form}
        return await client.request("POST", "/hzeb-charge/customerefldj/customerefldj/adjustBills", json_body=form)

    @mcp.tool
    async def charge_fee_insert_save(form: dict, confirm: bool = False) -> dict:
        """⚠️ 其他账单录入（saveFeeInsert）。form 为账单表单对象。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/customerfee/customerfee/saveFeeInsert", "body": form}
        return await client.request("POST", "/hzeb-charge/customerfee/customerfee/saveFeeInsert", json_body=form)

    @mcp.tool
    async def charge_fee_insert_list(page: int = 1, limit: int = 20, buildingId: str = "") -> dict:
        """其他账单录入记录列表（只读）。"""
        data = await client.request("GET", "/hzeb-charge/customerfee/customerfee/feeInsertList",
                                    params={"page": page, "limit": limit, "buildingId": buildingId})
        return unwrap_rows(data)

    @mcp.tool
    async def charge_notice_update(form: dict, confirm: bool = False) -> dict:
        """⚠️ 收费通知单配置更新（billnoticeUpdate）。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/customerbillnotice/billnoticeUpdate", "body": form}
        return await client.request("POST", "/hzeb-charge/customerbillnotice/billnoticeUpdate", json_body=form)

    @mcp.tool
    async def charge_balance_alarm_setting(buildingId: int, enable: bool, confirm: bool = False) -> dict:
        """⚠️ 设置房间/建筑低余额提醒开关。""" + CONFIRM_HINT
        body = {"buildingId": buildingId, "isBalancealarm": 1 if enable else 0}
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/customer/buildinginfo/updateIsBalancealarm", "body": body}
        return await client.request("POST", "/hzeb-charge/customer/buildinginfo/updateIsBalancealarm", json_body=body)

    @mcp.tool
    async def charge_settle_refresh(form: dict, confirm: bool = False) -> dict:
        """⚠️ 结算数据刷新/重算（ecodatasettle/refresh）。form 为结算筛选对象。""" + CONFIRM_HINT
        if not confirm:
            return {"needConfirm": True, "endpoint": "/hzeb-charge/ecodatasettle/refresh", "body": form}
        return await client.request("POST", "/hzeb-charge/ecodatasettle/refresh", json_body=form)

    @mcp.tool
    async def charge_settle_bill_list(page: int = 1, limit: int = 20, kind: str = "bill",
                                      buildingId: str = "") -> dict:
        """结算账单分页（只读）。kind: bill 结算账单 / trade 交易账单。"""
        base = "/hzeb-charge/ecodatasettle"
        path = f"{base}/billList/page" if kind == "bill" else f"{base}/tradeBillList/page"
        data = await client.request("GET", path, params={"page": page, "limit": limit,
                                                         "buildingId": buildingId})
        return unwrap_rows(data)

    # ---- 档案类表单 ----
    @mcp.tool
    async def archives_building_write(action: str, form: dict, confirm: bool = False) -> dict:
        """⚠️ 建筑档案写操作。action: add 新增 / update 修改 / delete 删除(form 传 {buildingId}) /
        matchTable 配表(binding 表计)。form 为建筑表单完整对象。""" + CONFIRM_HINT
        paths = {"add": "/hzeb-charge/customer/buildinginfo/add",
                 "update": "/hzeb-charge/customer/buildinginfo/update",
                 "matchTable": "/hzeb-charge/customer/buildinginfo/match/table"}
        if action == "delete":
            if not confirm:
                return {"needConfirm": True, "endpoint": "/hzeb-charge/customer/buildinginfo/delete", "params": form}
            return await client.request("DELETE", "/hzeb-charge/customer/buildinginfo/delete", params=form)
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths) + ['delete']}")
        if not confirm:
            return {"needConfirm": True, "endpoint": paths[action], "body": form}
        return await client.request("POST", paths[action], json_body=form)

    @mcp.tool
    async def archives_meter_write(action: str, form: dict, confirm: bool = False) -> dict:
        """⚠️ 计量设备写操作。action: updateQc 起度/阈值修改(updateQcvalue) / dismantle 拆表。
        form 为表计对象（含 meterid 等，可先读 archives_meter_list 行修改）。""" + CONFIRM_HINT
        paths = {"updateQc": "/hzeb-charge/customermeterinfo/customermeterinfo/updateQcvalue",
                 "dismantle": "/hzeb-charge/customermeterinfo/customermeterinfo/dismantleMeter"}
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "endpoint": paths[action], "body": form}
        return await client.request("POST", paths[action], json_body=form)

    @mcp.tool
    async def archives_collector_write(action: str, form: dict, confirm: bool = False) -> dict:
        """⚠️ 采集设备写操作。action: add 新增 / delete 删除(form 传集中器编号对象) /
        activation 激活。""" + CONFIRM_HINT
        paths = {"add": "/hzeb-collection/concentrator/add/concentrator",
                 "delete": "/hzeb-collection/concentrator/delete/concentrator",
                 "activation": "/hzeb-collection/concentrator/activation"}
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "endpoint": paths[action], "body": form}
        return await client.request("POST", paths[action], json_body=form)

    @mcp.tool
    async def archives_share_building_write(action: str, form: dict, confirm: bool = False) -> dict:
        """⚠️ 公摊建筑/公摊组写操作。action: add / update / remove(form 传 {id})。""" + CONFIRM_HINT
        paths = {"add": "/hzeb-charge/shareBuilding/shareBuilding/add",
                 "update": "/hzeb-charge/shareBuilding/shareBuilding/update",
                 "remove": "/hzeb-charge/shareBuilding/shareBuilding/remove"}
        if action not in paths:
            raise ApiError(400, f"action 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "endpoint": paths[action], "body": form}
        method = "DELETE" if action == "remove" else "POST"
        if method == "DELETE":
            return await client.request(method, paths[action], params=form) if confirm else {}
        return await client.request("POST", paths[action], json_body=form)

    # ---- 配置类表单 ----
    @mcp.tool
    async def system_config_update(kind: str, form: dict, confirm: bool = False) -> dict:
        """⚠️ 业务配置更新。kind: customer 客户配置(customerconfig/update) /
        timing 定时配置(update/timing) / chargeWay 缴费方式(updateChargeWay) /
        loopName 回路名(updateLoopName) / messageConfig 消息配置(systemMessageconfig/update)。""" + CONFIRM_HINT
        paths = {"customer": "/hzeb-charge/customerconfig/update",
                 "timing": "/hzeb-charge/customerconfig/update/timing",
                 "chargeWay": "/hzeb-charge/customerconfig/updateChargeWay",
                 "loopName": "/hzeb-charge/customerconfig/updateLoopName",
                 "messageConfig": "/hzeb-charge/systemMessageconfig/update"}
        if kind not in paths:
            raise ApiError(400, f"kind 仅支持 {list(paths)}")
        if not confirm:
            return {"needConfirm": True, "endpoint": paths[kind], "body": form}
        return await client.request("POST", paths[kind], json_body=form)
