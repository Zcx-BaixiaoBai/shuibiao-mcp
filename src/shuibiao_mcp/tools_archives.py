"""G3 档案管理"""
from __future__ import annotations

from fastmcp import FastMCP

from .client import ShuibiaoClient, unwrap_rows


def register(mcp: FastMCP, client: ShuibiaoClient) -> None:
    @mcp.tool
    async def archives_building_tree(domain: str = "charge", buildingType: str = "") -> list:
        """建筑/区域树。domain=charge 收费域(含房间层级) / collection 采集域。"""
        if domain == "collection":
            return await client.request("GET", "/hzeb-collection/buildinginfo/getTreeAll")
        return await client.request(
            "GET", "/hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal",
            params={"buildingType": buildingType})

    @mcp.tool
    async def archives_building_list(page: int = 1, limit: int = 20, buildingName: str = "",
                                     buildingId: str = "2", buildingType: str = "23028",
                                     buildingLevel: str = "2") -> dict:
        """建筑档案分页列表。buildingType: 23028 房间/23025/23027 等建筑类型编码；buildingLevel 层级。"""
        data = await client.request(
            "GET", "/hzeb-charge/customer/buildinginfo/list2/v2",
            params={"page": page, "limit": limit, "customerId": "1", "buildingId": buildingId,
                    "buildingType": buildingType, "buildingLevel": buildingLevel,
                    "buildingName": buildingName})
        return unwrap_rows(data)

    @mcp.tool
    async def archives_meter_list(page: int = 1, limit: int = 20, buildingId: str = "",
                                  meterType: str = "", meterNo: str = "") -> dict:
        """计量设备（水表/电表）分页列表。meterType 用水/电类型编码，meterNo 表号模糊。"""
        data = await client.request(
            "GET", "/hzeb-collection/customermeterinfo/customermeterinfo/list",
            params={"pageNo": page, "pageSize": limit, "buildingId": buildingId,
                    "equipmentType": meterType, "meterNo": meterNo})
        return unwrap_rows(data)

    @mcp.tool
    async def archives_meter_types() -> list:
        """计量设备类型字典（水/电表型号类别）。"""
        return await client.request(
            "GET", "/hzeb-collection/customermeterinfo/customermeterinfo/getAllEquipmentType")

    @mcp.tool
    async def archives_collector_list(page: int = 1, limit: int = 20, buildingId: str = "") -> dict:
        """采集设备（集中器）分页列表。"""
        data = await client.request(
            "GET", "/hzeb-collection/concentrator/list",
            params={"pageNo": page, "pageSize": limit, "buildingId": buildingId})
        return unwrap_rows(data)

    @mcp.tool
    async def archives_tenant_merchant_list(page: int = 1, limit: int = 20, kind: str = "tenant",
                                            buildingId: str = "", name: str = "") -> dict:
        """住户档案(kind=tenant)/商户档案(kind=merchant)分页列表。"""
        data = await client.request(
            "GET", "/hzeb-charge/customer/buildinginfo/list",
            params={"page": page, "limit": limit, "buildingId": buildingId,
                    "customerType": kind, "name": name})
        return unwrap_rows(data)

    @mcp.tool
    async def archives_resident_list(page: int = 1, limit: int = 20, buildingId: str = "",
                                     kind: str = "tenant") -> dict:
        """住户/商户的房间绑定用户分页（用户管理→住户/商户）。"""
        data = await client.request(
            "GET", "/hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/list/v2",
            params={"customerId": "1", "buildingType": "23028", "jdqzt": "-1",
                    "inRate": "0", "loadMode": "1", "buildingId": buildingId, "type": kind})
        return unwrap_rows(data)
