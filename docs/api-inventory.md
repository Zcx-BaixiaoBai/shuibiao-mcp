# 智慧能源管理平台 API 清单（水表 MCP 依据）

- 站点: https://shuibiao.jinying.com/ （深圳合众致达·智慧能源管理平台）
- 抓取方式: 静态 webpack chunk 扫描（577 端点） + 动态菜单遍历（52 个观测端点）
- 静态发现但页面未触发 = 标记 `[静态]`；动态观测到 = 带方法/参数/响应示例

## 0. 认证与会话机制

| 项 | 值 |
|---|---|
| 登录 | `POST /hzeb-base/sys/user/login` |
| 登录体 | `{userName, userPassword: base64(md5hex(密码)), checkKey: 验证码时间戳, captcha, loginIp}` |
| 验证码 | `GET /hzeb-base/sys/user/randomImage/{timestamp}` 返回 base64 图片 |
| 会话 | 无 cookie；token(JWT HS512, 约3h) 存 sessionStorage.SESSIONOBJECT |
| 请求头 | `token`, `username`, `userid`, `customerid`, `customername`(URL编码), `roletype`, `remoteadd` |
| 客户 | customerId=1 南京金鹰国际物业集团有限公司 |

## 1. 接口总览（按服务/业务模块）

### address / getTree （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/address/getTree`

### address / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/address/list`

### api / devices （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/api/devices/concentrator/config/info`
- `[静态]` `/hzeb-collection/api/devices/concentrator/info`

### api / pay （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/api/pay/jlNotify`

### archives / alone （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/alone/save/formula`

### archives / bind （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/bind/point/list`

### archives / cancel （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/cancel/bind`

### archives / config （观测 0，仅静态 13）

- `[静态]` `/hzeb-energy/archives/config/batch/setting/price`
- `[静态]` `/hzeb-energy/archives/config/delete`
- `[静态]` `/hzeb-energy/archives/config/energy/threshold`
- `[静态]` `/hzeb-energy/archives/config/export`
- `[静态]` `/hzeb-energy/archives/config/get/archives/building`
- `[静态]` `/hzeb-energy/archives/config/import`
- `[静态]` `/hzeb-energy/archives/config/importInfo`
- `[静态]` `/hzeb-energy/archives/config/importRecord`
- `[静态]` `/hzeb-energy/archives/config/list`
- `[静态]` `/hzeb-energy/archives/config/save`
- `[静态]` `/hzeb-energy/archives/config/select`
- `[静态]` `/hzeb-energy/archives/config/share`
- `[静态]` `/hzeb-energy/archives/config/share/username/list`

### archives / downLoad （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/downLoad`

### archives / get （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/get/building/formula`

### archives / getMatching （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/getMatching/tree`

### archives / hlv （观测 0，仅静态 7）

- `[静态]` `/hzeb-energy/archives/hlv/delete`
- `[静态]` `/hzeb-energy/archives/hlv/import`
- `[静态]` `/hzeb-energy/archives/hlv/list`
- `[静态]` `/hzeb-energy/archives/hlv/save`
- `[静态]` `/hzeb-energy/archives/hlv/save/build`
- `[静态]` `/hzeb-energy/archives/hlv/select`
- `[静态]` `/hzeb-energy/archives/hlv/update`

### archives / import （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/import`

### archives / importInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/importInfo`

### archives / importRecord （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/importRecord`

### archives / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/list`

### archives / list2 （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/list2`

### archives / match （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/match/table`

### archives / new （观测 0，仅静态 2）

- `[静态]` `/hzeb-energy/archives/new/building/sub/list`
- `[静态]` `/hzeb-energy/archives/new/point/list`

### archives / option （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/option/list`

### archives / power （观测 0，仅静态 4）

- `[静态]` `/hzeb-energy/archives/power/list`
- `[静态]` `/hzeb-energy/archives/power/save`
- `[静态]` `/hzeb-energy/archives/power/select`
- `[静态]` `/hzeb-energy/archives/power/update`

### archives / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/save/formula`

### archives / topologytree （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/topologytree/meter/list`

### archives / tree （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/tree`

### archives / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/update/up/parentid`

### archives / updateBuildingOrder （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/archives/updateBuildingOrder`

### archives / 能耗档案 （观测 0，仅静态 7）

- `[静态]` `/hzeb-energy/archives/archives/add`
- `[静态]` `/hzeb-energy/archives/archives/delete`
- `[静态]` `/hzeb-energy/archives/archives/info`
- `[静态]` `/hzeb-energy/archives/archives/list`
- `[静态]` `/hzeb-energy/archives/archives/sync`
- `[静态]` `/hzeb-energy/archives/archives/topologyTree`
- `[静态]` `/hzeb-energy/archives/archives/update`

### authorize / getpower （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/authorize/getpower`
- `[静态]` `/hzeb-energy/authorize/getpower`

### authorize / saveorupdate （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/authorize/saveorupdate`
- `[静态]` `/hzeb-energy/authorize/saveorupdate`

### big / power （观测 1，仅静态 3）

- `GET /hzeb-collection/big/power/list`
  - query: `{"page": "1", "limit": "100000"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100000,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表
- `[静态]` `/hzeb-collection/big/power/delete`
- `[静态]` `/hzeb-collection/big/power/save`
- `[静态]` `/hzeb-collection/big/power/update`

### build / buildcompare （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/build/buildcompare`

### build / energy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/build/energy/consumption`

### build / get （观测 0，仅静态 2）

- `[静态]` `/hzeb-energy/build/get/allBuild`
- `[静态]` `/hzeb-energy/build/get/energyvalue`

### build / getamount （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/build/getamount`

### build / time （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/build/time/sharing/compare`

### build / timecompare （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/build/timecompare`

### buildinginfo / activationBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/activationBatch`

### buildinginfo / active （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/active`

### buildinginfo / activeBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/activeBatch`

### buildinginfo / buildinginfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/buildinginfo`

### buildinginfo / changeMeter （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/changeMeter`

### buildinginfo / downLoad （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/downLoad`

### buildinginfo / energy （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/energy/getTreeAll`

### buildinginfo / get （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/get/energy/model/list`

### buildinginfo / getAllTree （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/getAllTree`

### buildinginfo / getBuildGropuName （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/getBuildGropuName`

### buildinginfo / getTree （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/getTree`

### buildinginfo / getTreeAll （观测 2，仅静态 0）

- `GET /hzeb-collection/buildinginfo/getTreeAll`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"buildingid":1,"buildinglevel":1,"buildingname":"南京金鹰国际物业集团有限公司","aliasName":"南京金鹰国际物业集团有限公司","parentid":0,"isleaf":0,"orderNum":1,"comAddress":null,"equipmentNum":null,"buildingNo":"dfbfa3d08c034d7bab8804e4e2361edd","list":[{"buildingid":2,"buildinglevel":3,"building`
  - 菜单: 设备与采集 > 设备档案 > 建筑档案；设备与采集 > 设备档案 > 建筑配表；设备与采集 > 设备档案 > 采集设备
- `GET /hzeb-collection/buildinginfo/getTreeAll/search`
  - query: `{"energyTypeID": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"buildingid":1,"buildinglevel":1,"buildingname":"南京金鹰国际物业集团有限公司","aliasName":"南京金鹰国际物业集团有限公司","parentid":0,"isleaf":0,"orderNum":1,"comAddress":null,"equipmentNum":null,"buildingNo":"dfbfa3d08c034d7bab8804e4e2361edd","list":[{"buildingid":2,"buildinglevel":3,"building`
  - 菜单: 设备与采集 > 设备远程抄控 > 手工点抄；设备与采集 > 设备远程抄控 > 远程控制

### buildinginfo / import （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/import`

### buildinginfo / importInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/importInfo`

### buildinginfo / importRecord （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/importRecord`

### buildinginfo / interchangeMeter （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/interchangeMeter`

### buildinginfo / new （观测 1，仅静态 7）

- `GET /hzeb-collection/buildinginfo/new/building/list`
  - query: `{"buildingId": "1", "page": "1", "limit": "100"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"buildingId":1,"buildingName":"南京金鹰国际物业集团有限公司","buildingLevel":1,"aliasName":"南京金鹰国际物业集团有限公司","buildingArea":null,"totalPersonal":null,"contacts":null,"contactsPhone":null,"orderNum":1},{"buildingId":2,"buildingName":"金鹰中心","buildingLevel":3,"aliasName":"金鹰`
  - 菜单: 设备与采集 > 设备档案 > 建筑档案
- `[静态]` `/hzeb-collection/buildinginfo/new/building/add`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/batch/add`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/delete`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/import`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/info`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/sub/list`
- `[静态]` `/hzeb-collection/buildinginfo/new/building/update`

### buildinginfo / removeCircuit （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/removeCircuit`

### buildinginfo / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/update/up/parentid`

### buildinginfo / updateBuildingName （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/updateBuildingName`

### buildinginfo / updateBuildingOrder （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/buildinginfo/updateBuildingOrder`

### charge / get （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/get/bill/list`

### charge / subsidyBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/subsidyBatch`

### charge / subsidyBatchStu （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/subsidyBatchStu`

### charge / subsidyExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/subsidyExport`

### charge / subsidyImport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/subsidyImport`

### charge / 账单 （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/charge/billList`

### comEspecialtask / communicationExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/communicationExport`

### comEspecialtask / communicationQuery （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/communicationQuery`

### comEspecialtask / configDownload （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/configDownload`

### comEspecialtask / deleteOrReload （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/deleteOrReload`

### comEspecialtask / emergencyControl （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/emergencyControl`

### comEspecialtask / emergencyControlBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/emergencyControlBatch`

### comEspecialtask / getItemID （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/getItemID`

### comEspecialtask / getResultByMeterId （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/getResultByMeterId`

### comEspecialtask / getTypeSecond （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/getTypeSecond`

### comEspecialtask / needList （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/needList`

### comEspecialtask / needListExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/needListExport`

### comEspecialtask / readValue （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/readValue`

### comEspecialtask / reissueLast （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/reissueLast`

### comEspecialtask / reissueTask （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/reissueTask`

### comEspecialtask / specialList （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/specialList`

### comEspecialtask / specialListExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/comEspecialtask/specialListExport`

### comEspecialtask / 远程控制 （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/comEspecialtask/controlList`
- `[静态]` `/hzeb-charge/comEspecialtask/controlListExport`

### comedatareadtask / comedatareadtask （观测 0，仅静态 5）

- `[静态]` `/hzeb-collection/comedatareadtask/comedatareadtask/delete`
- `[静态]` `/hzeb-collection/comedatareadtask/comedatareadtask/getItemID/v2`
- `[静态]` `/hzeb-collection/comedatareadtask/comedatareadtask/getResult`
- `[静态]` `/hzeb-collection/comedatareadtask/comedatareadtask/getResultExport`
- `[静态]` `/hzeb-collection/comedatareadtask/comedatareadtask/update`

### concentrator / activation （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/activation`

### concentrator / add （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/add/concentrator`

### concentrator / and （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/concentrator/and/meter/export`
- `[静态]` `/hzeb-collection/concentrator/and/meter/list`

### concentrator / batch （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/batch/collection/activation`

### concentrator / check （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/check/concentrator/number`

### concentrator / delete （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/delete/concentrator`

### concentrator / exportExcel （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/exportExcel`

### concentrator / get （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/get/down/list`

### concentrator / homepageexport （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/homepageexport`

### concentrator / list （观测 1，仅静态 0）

- `GET /hzeb-collection/concentrator/list`
  - query: `{"pageSize": "9999", "pageNo": "1", "buildingId": "1", "projectId": "1"}`
  - status: 200
  - resp: `{"success":true,"message":"操作成功！","code":200,"result":{"records":[{"address":"户内","equipmentTypeName":"无线水表采集器","moduleOrConcentrator":2,"equipmentNum":"000002001","circuitId":"49c3dbfd2d32404b8591a9a93b1c0622","buildingId":"69","lastLoginTime":null,"upCommunicationMode":null,"isOnLine":1,"activeSta`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表；设备与采集 > 设备档案 > 采集设备；设备与采集 > 设备档案 > 计量设备

### concentrator / model （观测 1，仅静态 1）

- `GET /hzeb-collection/concentrator/model/list`
  - query: `{"projectId": "1"}`
  - status: 200
  - resp: `{"success":true,"message":"操作成功！","code":200,"result":[{"equipmentTypeName":"无线水表采集器","productModelName":"HZZD-NB"}],"timestamp":1791972386901}`
  - 菜单: 设备与采集 > 设备档案 > 采集设备
- `[静态]` `/hzeb-collection/concentrator/model/statistics`

### concentrator / monitor （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/monitor/list`

### concentrator / second （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/concentrator/second/activationCircuit`
- `[静态]` `/hzeb-collection/concentrator/second/batch/activationCircuit`

### concentrator / statistics （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/statistics`

### concentrator / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/concentrator/update`

### customer / buildinginfo （观测 2，仅静态 22）

- `GET /hzeb-charge/customer/buildinginfo/list`
  - query: `{"customerId": "1", "buildingType": "23028"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"buildingtype":"23028","buildingid":2,"buildingname":"南京金鹰国际物业集团有限公司","list":null,"isleaf":0,"isOpen":0,"isBindMeter":null,"buildinglevel":1,"parentName":null,"buildingarea":0.00,"parentid":0,"buildingcode":null,"orderNum":1,"thirdId":null}]}`
  - 菜单: 收费管理 > 档案管理 > 住户档案；收费管理 > 档案管理 > 商户档案
- `GET /hzeb-charge/customer/buildinginfo/list2/v2`
  - query: `{"limit": "100", "page": "1", "customerId": "1", "buildingId": "2", "buildingType": "23028", "buildingLevel": "2"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 收费管理 > 档案管理 > 住户档案；收费管理 > 档案管理 > 商户档案
- `[静态]` `/hzeb-charge/customer/buildinginfo/add`
- `[静态]` `/hzeb-charge/customer/buildinginfo/batch/update/building/type`
- `[静态]` `/hzeb-charge/customer/buildinginfo/batchQrCode/base64`
- `[静态]` `/hzeb-charge/customer/buildinginfo/delete`
- `[静态]` `/hzeb-charge/customer/buildinginfo/downLoad`
- `[静态]` `/hzeb-charge/customer/buildinginfo/export`
- `[静态]` `/hzeb-charge/customer/buildinginfo/exportHf`
- `[静态]` `/hzeb-charge/customer/buildinginfo/getQrCode`
- `[静态]` `/hzeb-charge/customer/buildinginfo/import`
- `[静态]` `/hzeb-charge/customer/buildinginfo/importHf`
- `[静态]` `/hzeb-charge/customer/buildinginfo/importInfo`
- `[静态]` `/hzeb-charge/customer/buildinginfo/importRecord`
- `[静态]` `/hzeb-charge/customer/buildinginfo/list2`
- `[静态]` `/hzeb-charge/customer/buildinginfo/match/table`
- `[静态]` `/hzeb-charge/customer/buildinginfo/maxBuildingCode`
- `[静态]` `/hzeb-charge/customer/buildinginfo/new/building/sub/list`
- `[静态]` `/hzeb-charge/customer/buildinginfo/point/list`
- `[静态]` `/hzeb-charge/customer/buildinginfo/select`
- `[静态]` `/hzeb-charge/customer/buildinginfo/syncBuild`
- `[静态]` `/hzeb-charge/customer/buildinginfo/update`
- `[静态]` `/hzeb-charge/customer/buildinginfo/update/up/parentid`
- `[静态]` `/hzeb-charge/customer/buildinginfo/updateIsBalancealarm`

### customerShareFee / customerShareFee （观测 0，仅静态 6）

- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/addConfigure`
- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/getAllMeterType`
- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/getConfigure`
- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/getList`
- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/getMeasuringPointPage`
- `[静态]` `/hzeb-charge/customerShareFee/customerShareFee/removeFee`

### customerShift / add （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerShift/add`

### customerShift / delete （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerShift/delete`

### customerShift / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerShift/list`

### customerShift / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerShift/update`

### customerTeam / add （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeam/add`

### customerTeam / delete （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeam/delete`

### customerTeam / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeam/list`

### customerTeam / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeam/update`

### customerTeamConfig / config （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeamConfig/config`

### customerTeamConfig / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerTeamConfig/list`

### customerTeamConfig / team （观测 0，仅静态 2）

- `[静态]` `/hzeb-energy/customerTeamConfig/team/energy/data/list`
- `[静态]` `/hzeb-energy/customerTeamConfig/team/energy/data/list/export`

### customerWorkday / info （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerWorkday/info`

### customerWorkday / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customerWorkday/save`

### customeraccount / customeraccount （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/customeraccount/customeraccount/openUserBatch`
- `[静态]` `/hzeb-charge/customeraccount/customeraccount/settlePreview`

### customeralarmconfig / getEarlyWarningMsgMeterList （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customeralarmconfig/getEarlyWarningMsgMeterList`

### customeralarmconfig / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customeralarmconfig/list`

### customeralarmconfig / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/customeralarmconfig/save`

### customerbillnotice / 账单 （观测 1，仅静态 3）

- `GET /hzeb-charge/customerbillnotice/billnoticeStatus`
  - query: `{"buildingId": "2", "projectModel": "0"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"billnotices":[],"isEnable":0}}`
  - 菜单: 收费管理 > 账单管理 > 收费通知单
- `[静态]` `/hzeb-charge/customerbillnotice/billnoticeEnable`
- `[静态]` `/hzeb-charge/customerbillnotice/billnoticeInfo`
- `[静态]` `/hzeb-charge/customerbillnotice/billnoticeUpdate`

### customerbuildinginfo / 建筑档案 （观测 4，仅静态 17）

- `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"buildingid":2,"buildingname":"南京金鹰国际物业集团有限公司","isleaf":0,"list":[],"buildinglevel":1,"buildingtype":"23028,23025,23027","isOpen":0,"parentid":0,"orderNum":1,"aliasname":null}]}`
  - 菜单: 收费管理 > 档案管理 > 水电单价管理；收费管理 > 用户管理 > 住户；收费管理 > 用户管理 > 商户
- `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotalNoRoom`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"buildingid":2,"buildingname":"南京金鹰国际物业集团有限公司","isleaf":0,"list":[],"buildinglevel":1,"buildingtype":"23028,23025,23027","isOpen":0,"parentid":0,"orderNum":1,"aliasname":null}]}`
  - 菜单: 收费管理 > 系统设置 > 参数配置
- `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/list/v2`
  - query: `{"customerId": "1", "buildingType": "23028", "jdqzt": "-1", "inRate": "0", "loadMode": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"buildingNum":0,"buildingNumIsOpen":0,"buildingNumNoOpen":0,"buildingareaTotal":0,"receivableFee":0,"list":[],"openRate":0,"idleRate":0,"buildingNumIsFull":null,"buildingNumNoFull":null}}`
  - 菜单: 收费管理 > 用户管理 > 住户；收费管理 > 用户管理 > 商户
- `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/listByNotice`
  - query: `{"limit": "100", "page": "1", "buildingId": "2"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 收费管理 > 账单管理 > 收费通知单
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/authorizeData`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/configSubMch`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/configThreshold`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/getAuthorizeData`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTree`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeAndMeter`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/export/v2`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/info`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/list`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/subMchList`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/update`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/updateBuildingOrder`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/updateInstalledCapacity`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/updatePersonalBatch`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/updateblacklist`
- `[静态]` `/hzeb-charge/customerbuildinginfo/customerbuildinginfo/userImport`

### customerbuildinguser / customerbuildinguser （观测 0，仅静态 8）

- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/batchAdd`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/batchClear`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/batchDel`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/batchUpdate`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/changeRoom`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/getCustomerBuildingUser`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/saveOrDeleteCustomerUser`
- `[静态]` `/hzeb-charge/customerbuildinguser/customerbuildinguser/update`

### customerconfig / info （观测 1，仅静态 0）

- `GET /hzeb-charge/customerconfig/info`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"config":{"configId":1,"customerId":1,"customerName":"南京金鹰国际物业集团有限公司","createTime":"2023-07-07 16:14:06","updateTime":null,"customerPhone":null,"printMode":0,"printUser":0,"isPrivate":0,"submchId":null,"submchName":null,"commissionMode":2,"commissionRatio":0.60,"deMode`
  - 菜单: 收费管理 > 档案管理 > 住户档案；收费管理 > 档案管理 > 商户档案；收费管理 > 收退费查询 > 收费查询

### customerconfig / openAutoWithdraw （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/customerconfig/openAutoWithdraw`

### customerconfig / update （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/customerconfig/update`
- `[静态]` `/hzeb-charge/customerconfig/update/timing`

### customerconfig / updateChargeWay （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/customerconfig/updateChargeWay`

### customerconfig / updateLoopName （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/customerconfig/updateLoopName`

### customerconfig / updateSubMch （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/customerconfig/updateSubMch`

### customerdaymonitor / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerdaymonitor/list`

### customeredskz / customeredskz （观测 1，仅静态 3）

- `GET /hzeb-collection/customeredskz/customeredskz/down/list`
  - query: `{"customerid": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"dcId":1,"dcMc":"不启用定时控制"}]}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表
- `[静态]` `/hzeb-collection/customeredskz/customeredskz/`
- `[静态]` `/hzeb-collection/customeredskz/customeredskz/delete`
- `[静态]` `/hzeb-collection/customeredskz/customeredskz/list`

### customerefldj / customerefldj （观测 1，仅静态 7）

- `GET /hzeb-charge/customerefldj/customerefldj/fldjConfigList`
  - query: `{"buildingId": "2"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"fldjid":1,"fldjmc":"默认电价方案","energytypeid":"01001","multiRate":1,"priceFirstOne":1.0000000000,"priceFirstTwo":1.0000000000,"priceFirstThree":1.0000000000,"priceFirstFour":1.0000000000,"jtFirst":null,"isConvertFirst":0,"changeTime":"2126-10-14 11:03:37","multiRateSeco`
  - 菜单: 收费管理 > 档案管理 > 水电单价管理
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/adjustBills`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/adjustMeterStatus/page`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/adjustMeterStatus/total`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/adjustMeterStatusExport`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/fldjConfigDelete`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/fldjConfigHistory`
- `[静态]` `/hzeb-charge/customerefldj/customerefldj/fldjConfigOption`

### customereqfdd / customereqfdd （观测 0，仅静态 5）

- `[静态]` `/hzeb-charge/customereqfdd/customereqfdd/delete`
- `[静态]` `/hzeb-charge/customereqfdd/customereqfdd/list`
- `[静态]` `/hzeb-charge/customereqfdd/customereqfdd/listS`
- `[静态]` `/hzeb-charge/customereqfdd/customereqfdd/save`
- `[静态]` `/hzeb-charge/customereqfdd/customereqfdd/update`

### customerfee / customerfee （观测 0，仅静态 8）

- `[静态]` `/hzeb-charge/customerfee/customerfee/feeBillExport`
- `[静态]` `/hzeb-charge/customerfee/customerfee/feeBillList/page`
- `[静态]` `/hzeb-charge/customerfee/customerfee/feeBillList/total`
- `[静态]` `/hzeb-charge/customerfee/customerfee/feeInsertList`
- `[静态]` `/hzeb-charge/customerfee/customerfee/otherBillExport`
- `[静态]` `/hzeb-charge/customerfee/customerfee/otherBillList/page`
- `[静态]` `/hzeb-charge/customerfee/customerfee/otherBillList/total`
- `[静态]` `/hzeb-charge/customerfee/customerfee/saveFeeInsert`

### customerhourmonitor / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerhourmonitor/list`

### customerkf / list （观测 1，仅静态 0）

- `GET /hzeb-charge/customerkf/list`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[]}`
  - 菜单: 系统管理 > 系统参数 > 参数配置

### customerkf / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/customerkf/save`

### customerloadrecordmonitor / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerloadrecordmonitor/list`

### customermaxdemandmonitor / measurepoint （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customermaxdemandmonitor/measurepoint/energy/list`

### customermeterinfo / customermeterinfo （观测 2，仅静态 11）

- `GET /hzeb-collection/customermeterinfo/customermeterinfo/getAllEquipmentType`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN15)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN25卧式)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN20)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN32)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN50)"}]}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表
- `GET /hzeb-collection/customermeterinfo/customermeterinfo/list`
  - query: `{"buildingId": "1", "energy": "01002", "page": "1", "limit": "100"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"meterid":1038,"comaddress":"102609100596","mtequipmentversioncode":"HS.CLHQW.DKWF8-NG811","mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN25卧式)","ratio":1.00,"currentRatio":1.00,"voltageRatio":1.00,"energytypeid":"01002","buildingid":98,"customerid":1,"useStatus`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/dismantleMeter`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/getMatchMeterList`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/getMeterStatusExport`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/getMeterStatusList`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/getRemoteConRecExport`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/refreshSettle`
- `[静态]` `/hzeb-charge/customermeterinfo/customermeterinfo/updateQcvalue`
- `[静态]` `/hzeb-collection/customermeterinfo/customermeterinfo/export`
- `[静态]` `/hzeb-collection/customermeterinfo/customermeterinfo/getEnergyStatus`
- `[静态]` `/hzeb-collection/customermeterinfo/customermeterinfo/getEquipment`
- `[静态]` `/hzeb-collection/customermeterinfo/customermeterinfo/useUpdate`

### customermonthmonitor / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customermonthmonitor/list`

### customerpecmrelation / enable （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerpecmrelation/enable`

### customerpecmrelation / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerpecmrelation/list`

### customerpecmrelation / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerpecmrelation/update`

### customerproblem / 故障报修 （观测 1，仅静态 3）

- `GET /hzeb-charge/customerproblem/customerproblem/list`
  - query: `{"page": "1", "limit": "100", "applyStartDate": "2026-09-14 00:00:00", "applyEndDate": "2026-10-14 23:59:59", "solveStatuss": "待处理,已审核，处理中,待用户缴费,待确认,处理完成,无效报修已作废"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 系统管理 > 运维管理 > 故障报修管理
- `[静态]` `/hzeb-charge/customerproblem/customerproblem/export`
- `[静态]` `/hzeb-charge/customerproblem/customerproblem/info`
- `[静态]` `/hzeb-charge/customerproblem/customerproblem/solve`

### customerrealtimecyclemonitor / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/customerrealtimecyclemonitor/list`

### dataitem / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/dataitem/list`

### dict / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/dict/list`

### ecaBalancedaily / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecaBalancedaily/export`

### ecaBalancedaily / 报表 （观测 1，仅静态 0）

- `GET /hzeb-collection/ecaBalancedaily/report/v2`
  - query: `{"type": "1", "limit": "100", "page": "1", "buildingId": "1", "energy": "01002", "startdate": "2026-09-13 00:00:00", "enddate": "2026-10-13 23:59:59", "customerId": "1", "isFuzzy": "0", "fuzzyDay": "30"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"page":{"records":[{"meterID":1038,"aliasName":"冷水表-金鹰中心A座B1F北美咖啡","comAddress":"102609100596","dateCycle":"2026-09-13~2026-10-13","cycleType":"区间","meterratio":1.00,"sdataitemvalue":null,"sdataitemvalueone":null,"sdataitemvaluetwo":null,"sdataitemvaluethree":null,"sda`
  - 菜单: 设备与采集 > 抄表数据查询 > 用水结算报表

### ecaWorktimedata / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/ecaWorktimedata/export`

### ecaWorktimedata / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/ecaWorktimedata/list`

### ecabalancealarm / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecabalancealarm/export`

### ecabalancealarm / handleAlarm （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecabalancealarm/handleAlarm`

### ecabalancealarm / handleAlarmBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecabalancealarm/handleAlarmBatch`

### ecabalancealarm / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecabalancealarm/list`

### ecabalancedaily / energy （观测 2，仅静态 1）

- `GET /hzeb-charge/ecabalancedaily/energy/energyRank`
  - query: `{"limit": "100", "page": "1", "buildingId": "2", "energyId": "01001", "dataType": "1", "orderRule": "desc", "value": "0", "timeType": "2", "topRank": "50", "timePoint": "2026-09"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"totalCount":0,"pageSize":100,"totalPage":0,"currPage":1,"list":[]}}`
  - 菜单: 收费管理 > 报表管理 > 用能排名
- `GET /hzeb-charge/ecabalancedaily/energy/enertyType`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[]}`
  - 菜单: 收费管理 > 账户查询 > 表计状态监测；收费管理 > 报表管理 > 用能排名
- `[静态]` `/hzeb-charge/ecabalancedaily/energy/energyRankExport`

### ecabalancedaily / queryEDataExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecabalancedaily/queryEDataExport`

### ecabalancedaily / queryEDataInfoByBuildingID （观测 0，仅静态 3）

- `[静态]` `/hzeb-charge/ecabalancedaily/queryEDataInfoByBuildingID`
- `[静态]` `/hzeb-charge/ecabalancedaily/queryEDataInfoByBuildingID/page`
- `[静态]` `/hzeb-charge/ecabalancedaily/queryEDataInfoByBuildingID/total`

### ecadealarm / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecadealarm/export`

### ecadealarm / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecadealarm/list`

### ecamessagelist / 报警消息 （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/ecamessagelist/ecamessagelist/list`
- `[静态]` `/hzeb-collection/ecamessagelist/ecamessagelist/readed/`

### ecoChangemeter / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoChangemeter/export`

### ecoChangemeter / list （观测 1，仅静态 0）

- `GET /hzeb-collection/ecoChangemeter/list`
  - query: `{"page": "1", "limit": "100", "buildingId": "1", "changeType": "1", "startTime": "2025-10-14 00:00:00", "endTime": "2026-10-14 23:59:59"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 设备与采集 > 设备档案 > 设备更换日志

### ecoEdaydata / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEdaydata/export`

### ecoEdaydata / falilist （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEdaydata/falilist`

### ecoEeventdata / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEeventdata/export`

### ecoEeventdata / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEeventdata/list`

### ecoEhourdata / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEhourdata/export`

### ecoEhourdata / falilist （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEhourdata/falilist`

### ecoEhourdata / lastHourData （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEhourdata/lastHourData`

### ecoEhourdata / statistics （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEhourdata/statistics`

### ecoEmonthdata / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEmonthdata/export`

### ecoEmonthdata / falilist （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/ecoEmonthdata/falilist`

### ecoEsinglerealtimedata / ecoEsinglerealtimedata （观测 6，仅静态 18）

- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water`
  - query: `{"startdate": "2026-10-14 00:00:00", "enddate": "2026-10-14 23:59:59", "energyTypeID": "01002", "buildingID": "1", "page": "1", "appType": "1", "limit": "100", "type": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"itemid":1,"meterid":1000,"aliasName":"冷水表-金鹰中心B座负一楼瑞幸咖啡","comAddress":"102609100177","mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN15)","errorcase":null,"ratio":1.00,"operationResult":0,"buildingId":119,"buildingLevel":8,"meterValue":null,"dataItemValue":null,`
  - 菜单: 设备与采集 > 抄表数据查询 > 抄表数据(水)
- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water/total`
  - query: `{"startdate": "2026-10-14 00:00:00", "enddate": "2026-10-14 23:59:59", "energyTypeID": "01002", "buildingID": "1", "page": "1", "appType": "1", "limit": "100", "type": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":"成功：0条，失败：0条，执行中：0条，未执行：58条，成功率：0%"}`
  - 菜单: 设备与采集 > 抄表数据查询 > 抄表数据(水)
- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenLossMeter/v2`
  - query: `{"limit": "100", "page": "1", "appType": "1", "buildingId": "1", "energy": "01002", "type": "1", "date": "202610"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"meterid":1000,"comaddress":"102609100177","loopNum":1,"buildingname":"金鹰中心B座负一楼瑞幸咖啡"},{"meterid":1001,"comaddress":"102609100176","loopNum":1,"buildingname":"金鹰中心B座负一楼王春春鸡汤饭"},{"meterid":1002,"comaddress":"102609100538","loopNum":1,"buildingname":"金鹰中心B座B8`
  - 菜单: 设备与采集 > 抄表数据查询 > 手工补录(水)
- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterList`
  - query: `{"limit": "100", "page": "1", "buildingId": "1", "energy": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"buildingname":"金鹰中心A座B7F3AM-1（表1）","comaddress":"102609100325","mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN20)","energytypeid":"01002","createTime":null,"ljyl":null,"dcdl":null,"nbxh":null,"status":null,"rssi":null,"rsrp":null,"sinr":null,"sbdate":null},{"bu`
  - 菜单: 设备与采集 > 抄表数据查询 > 上报数据查询
- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRate/list`
  - query: `{"type": "1", "appType": "1", "limit": "100", "page": "1", "buildingId": "1", "energy": "01002", "customerId": "1", "startdate": "2026-09-14 00:00:00", "enddate": "2026-10-14 23:59:59"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"seqNum":null,"aliasName":"南京金鹰国际物业集团有限公司","dataType":"日冻结","dataItemValueTime":"2026-10-14","dataItemValueTimeDate":"2026-10-14 00:00:00","equipmentTotalNum":58,"realEquipmentTotalNum":58,"totalNum":58,"successNum":0,"failNum":58,"successRate":"0.00"}],"to`
  - 菜单: 设备与采集 > 抄表数据查询 > 抄表成功率
- `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRate/total`
  - query: `{"type": "1", "appType": "1", "limit": "100", "page": "1", "buildingId": "1", "energy": "01002", "customerId": "1", "startdate": "2026-09-14 00:00:00", "enddate": "2026-10-14 23:59:59"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"seqNum":null,"aliasName":null,"dataType":null,"dataItemValueTime":null,"dataItemValueTimeDate":null,"equipmentTotalNum":58,"realEquipmentTotalNum":null,"totalNum":58,"successNum":0,"failNum":58,"successRate":"0.00"}}`
  - 菜单: 设备与采集 > 抄表数据查询 > 抄表成功率
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/addFrozenData`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/addFrozenDataImport`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/ele`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/ele/exportExcel`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/ele/total`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water/exportExcel`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/exportExcel`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/failData`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/failDataExport`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenLossData`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenLossDataExport`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenRecord`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/hot/cold/exportExcel`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterDataExport`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterDataList`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterExport`
- `[静态]` `/hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRateExport`

### ecoOrderline / ecoOrderline （观测 0，仅静态 3）

- `[静态]` `/hzeb-charge/ecoOrderline/ecoOrderline/auditWithdrawOrder`
- `[静态]` `/hzeb-charge/ecoOrderline/ecoOrderline/queryWithdrawOrderExport`
- `[静态]` `/hzeb-charge/ecoOrderline/ecoOrderline/queryWithdrawOrderList`

### ecoSyslog / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-base/ecoSyslog/export`

### ecoSyslog / queryPage （观测 0，仅静态 1）

- `[静态]` `/hzeb-base/ecoSyslog/queryPage`

### ecoaccountflow / exportAll （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoaccountflow/exportAll`

### ecoaccountflow / flowExeclExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoaccountflow/flowExeclExport`

### ecoaccountflow / flowPdfExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoaccountflow/flowPdfExport`

### ecoaccountflow / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoaccountflow/list`

### ecoaccountflow / listAll （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoaccountflow/listAll`

### ecochangemeter / change （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/ecochangemeter/change/info`
- `[静态]` `/hzeb-charge/ecochangemeter/change/meter`

### ecochangemeter / get （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/ecochangemeter/get/collection/meter/list`
- `[静态]` `/hzeb-charge/ecochangemeter/get/energy/model/list`

### ecochangemeter / handleChange （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochangemeter/handleChange`

### ecochangemeter / interchange （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/ecochangemeter/interchange`
- `[静态]` `/hzeb-charge/ecochangemeter/interchange/info`

### ecochangemeter / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochangemeter/list`

### ecochangemeter / testandverify （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochangemeter/testandverify`

### ecochargerecord / abnormal （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/abnormal`

### ecochargerecord / abnormalInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/abnormalInfo`

### ecochargerecord / abnormalInfoExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/abnormalInfoExport`

### ecochargerecord / annualInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/annualInfo/v2`

### ecochargerecord / annualInfoExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/annualInfoExport/v2`

### ecochargerecord / annualSummary （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/annualSummary/v2`

### ecochargerecord / getAnnunCharge （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/getAnnunCharge`

### ecochargerecord / hydropowerReceipts （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/hydropowerReceipts`

### ecochargerecord / hydropowerReceivable （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/hydropowerReceivable`

### ecochargerecord / meter （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/meter/v2`

### ecochargerecord / meterOffline （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/meterOffline/v2`

### ecochargerecord / meterOfflineExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/meterOfflineExport/v2`

### ecochargerecord / otherIncome （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/otherIncome`

### ecochargerecord / payClassification （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/payClassification`

### ecochargerecord / recoveryRate （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/recoveryRate`

### ecochargerecord / room （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/room`

### ecochargerecord / roomProtection （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/roomProtection`

### ecochargerecord / roomProtectionExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecochargerecord/roomProtectionExport`

### ecochargerecord / 收费统计看板 （观测 2，仅静态 31）

- `GET /hzeb-charge/ecochargerecord/ecochargerecord/findRealList/page`
  - query: `{"limit": "100", "page": "1", "buildingId": "2", "beginTime": "2026-10-01", "endTime": "2026-10-14"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 收费管理 > 财务管理 > 账目盘点
- `GET /hzeb-charge/ecochargerecord/ecochargerecord/findRealList/total`
  - query: `{"limit": "100", "page": "1", "buildingId": "2", "beginTime": "2026-10-01", "endTime": "2026-10-14"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"subsidyMoney":0.00,"aliasname":"合计","payMoney":0.00,"totalMoney":0.00,"backMoney":0.00,"reFundMoney":0.00}}`
  - 菜单: 收费管理 > 财务管理 > 账目盘点
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/arrearsCall`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/arrearsSummaryExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/arrearsSummaryList`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/batteryLowExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/batteryLowList`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeRecordExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeRecordList`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeRecordList/page`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeRecordList/total`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeSummaryExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeSummaryList/page`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/chargeSummaryList/total`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/deleteDe`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/findRealExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/findSummaryExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/findSummaryList/page`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/incomeMonthDay`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/incomeSummary`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/longTimeNoChargeExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/longTimeNoChargeList`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/noPayBillSummary`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/overdrawSummary`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/refundRecordExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/refundRecordList/page`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/refundRecordList/total`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/todoSummary`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/updateUp`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/usageThresholdExport`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/usageThresholdList`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/userSummary`
- `[静态]` `/hzeb-charge/ecochargerecord/ecochargerecord/warnSummary`

### ecoclearmeter / clearBatch （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoclearmeter/clearBatch`

### ecoclearmeter / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoclearmeter/export`

### ecoclearmeter / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoclearmeter/list`

### ecocloseaccountrecord / ecocloseaccountrecord （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/export`
- `[静态]` `/hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/list`

### ecodatasettle / refresh （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecodatasettle/refresh`

### ecodatasettle / tradeBillExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecodatasettle/tradeBillExport/v2`

### ecodatasettle / tradeBillList （观测 0，仅静态 2）

- `[静态]` `/hzeb-charge/ecodatasettle/tradeBillList/page`
- `[静态]` `/hzeb-charge/ecodatasettle/tradeBillList/total`

### ecodatasettle / 账单 （观测 0，仅静态 3）

- `[静态]` `/hzeb-charge/ecodatasettle/billExport`
- `[静态]` `/hzeb-charge/ecodatasettle/billList/page`
- `[静态]` `/hzeb-charge/ecodatasettle/billList/total`

### ecoeday / queryDayDataByMeters （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecoeday/queryDayDataByMeters`

### ecosyslog / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecosyslog/export`

### ecosyslog / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/ecosyslog/list`

### electricity / findBalanceValue （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/electricity/findBalanceValue`

### electricity / findResaultMessage （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/electricity/findResaultMessage`

### electricity / get （观测 0，仅静态 5）

- `[静态]` `/hzeb-energy/electricity/get/collection/ele/data/list/export`
- `[静态]` `/hzeb-energy/electricity/get/collection/loadrecord/list`
- `[静态]` `/hzeb-energy/electricity/get/collection/loadrecord/list/export`
- `[静态]` `/hzeb-energy/electricity/get/collection/peak/list`
- `[静态]` `/hzeb-energy/electricity/get/collection/peak/list/export`

### electricity / lineloss （观测 0，仅静态 2）

- `[静态]` `/hzeb-energy/electricity/lineloss`
- `[静态]` `/hzeb-energy/electricity/lineloss/export`

### electricity / loadrecord （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/electricity/loadrecord/list`

### equipment / building （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/building/config/table`

### equipment / check （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/check/equipmentNum`

### equipment / export （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/export`

### equipment / fkms （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/fkms/equipment/list`

### equipment / get （观测 1，仅静态 0）

- `POST /hzeb-collection/equipment/get/project/check/status`
  - body: `{"projectId": "1"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"checkStatus":1}}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表；设备与采集 > 设备档案 > 采集设备

### equipment / homepageexport （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/homepageexport`

### equipment / list （观测 2，仅静态 1）

- `GET /hzeb-collection/equipment/list/total/v2`
  - query: `{"buildingId": "1", "energy": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"totalNum":58,"onLineNum":0,"offLineNum":58,"onLineRate":"0.00%"}}`
  - 菜单: 设备与采集 > 设备档案 > 计量设备
- `GET /hzeb-collection/equipment/list/v2`
  - query: `{"limit": "100", "page": "1", "buildingId": "1", "energy": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"equipmentId":1038,"equipmentNum":"102609100596","meterName":"冷水表-金鹰中心A座B1F北美咖啡","buildingId":98,"energy":"01002","productModel":"HS.CLHQW.DKWF8-NG811","productName":"物联网4G阀控冷水表(ZZ-DN25卧式)","ratio":1.00,"currentRatio":1.00,"voltageRatio":1.00,"communication`
  - 菜单: 设备与采集 > 设备档案 > 计量设备
- `[静态]` `/hzeb-collection/equipment/list`

### equipment / meter （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/meter/model/list`

### equipment / model （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/model/statistics`

### equipment / monitor （观测 0，仅静态 5）

- `[静态]` `/hzeb-collection/equipment/monitor/count/quantity`
- `[静态]` `/hzeb-collection/equipment/monitor/ele/info`
- `[静态]` `/hzeb-collection/equipment/monitor/ele/list`
- `[静态]` `/hzeb-collection/equipment/monitor/water/info`
- `[静态]` `/hzeb-collection/equipment/monitor/water/list`

### equipment / school （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/school/model/list`

### equipment / statistics （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/statistics`

### equipment / timing （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/timing`

### equipment / timingList （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/timingList`

### equipment / xfmy （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/equipment/xfmy/equipment/list`

### formula / list （观测 0，仅静态 2）

- `[静态]` `/hzeb-energy/formula/list`
- `[静态]` `/hzeb-energy/formula/list/export`

### home / carbonEmissions （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/carbonEmissions`

### home / getEnergyRank （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getEnergyRank`

### home / getEnergyRankEnergy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getEnergyRankEnergy`

### home / getLeakageMonthly （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getLeakageMonthly`

### home / getLiveAlarm （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getLiveAlarm`

### home / getLiveAlarmEnergy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getLiveAlarmEnergy`

### home / getMeterInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getMeterInfo`

### home / getOfflineMeterInfo （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getOfflineMeterInfo`

### home / getYearlyMount （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getYearlyMount`

### home / getYearlyMountEnergy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/getYearlyMountEnergy`

### home / offlineMeterInfoExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/offlineMeterInfoExport`

### home / subitem （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/subitem/list`

### home / timecompareEnergy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/home/timecompareEnergy`

### 收费服务 / (根) （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge`

### 采集服务 / (根) （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection`

### 能耗服务 / (根) （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy`

### maxdemand / monitor （观测 0，仅静态 3）

- `[静态]` `/hzeb-energy/maxdemand/monitor/info`
- `[静态]` `/hzeb-energy/maxdemand/monitor/list`
- `[静态]` `/hzeb-energy/maxdemand/monitor/list/export`

### option / list （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/option/list`

### power / supply （观测 0，仅静态 4）

- `[静态]` `/hzeb-collection/power/supply/add`
- `[静态]` `/hzeb-collection/power/supply/building/list`
- `[静态]` `/hzeb-collection/power/supply/delete`
- `[静态]` `/hzeb-collection/power/supply/update`

### report / energyExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/energyExport`

### report / energyGenerate （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/energyGenerate`

### report / energyList （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/energyList`

### report / revenueExport （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/revenueExport`

### report / revenueGenerate （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/revenueGenerate`

### report / revenueList （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/report/revenueList`

### report / 报表 （观测 0，仅静态 4）

- `[静态]` `/hzeb-energy/report/reportDelete`
- `[静态]` `/hzeb-energy/report/reportDetail`
- `[静态]` `/hzeb-energy/report/reportDown`
- `[静态]` `/hzeb-energy/report/reportList`

### servicesummary / finddataitem （观测 0，仅静态 1）

- `[静态]` `/hzeb-collection/servicesummary/finddataitem`

### servicesummary / getDataItem （观测 1，仅静态 0）

- `POST /hzeb-collection/servicesummary/getDataItem/v2`
  - body: `{"equipmentNums": [], "optionType": 1, "energy": "01002"}`
  - status: 200
  - resp: `{"code":500,"msg":"请选择建筑/设备","data":null}`
  - 菜单: 设备与采集 > 设备远程抄控 > 手工点抄；设备与采集 > 设备远程抄控 > 远程控制

### servicesummary / getEquipmentVersionByEnergyType （观测 1，仅静态 1）

- `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyType/01001`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"mtequipmentversionid":"D.*D*.F**B*-**01","mtequipmentversionname":"单相费控智能表"},{"mtequipmentversionid":"D.*D*.F**B*-**51","mtequipmentversionname":"单相智能电表"},{"mtequipmentversionid":"D.*D*.F**B*-**54","mtequipmentversionname":"单相智能电表(多费率)"},{"mtequipmentversionid":"D.*T`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表
- `[静态]` `/hzeb-collection/servicesummary/getEquipmentVersionByEnergyType/`

### servicesummary / getEquipmentVersionByEnergyTypeAndAppType （观测 1，仅静态 0）

- `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyTypeAndAppType`
  - query: `{"energyTypeID": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN15)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN25卧式)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN20)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN32)"},{"mtequipmentversionname":"物联网4G阀控冷水表(ZZ-DN50)"}]}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表；设备与采集 > 设备档案 > 计量设备；设备与采集 > 设备远程抄控 > 手工点抄

### servicesummary / queryDataItems （观测 1，仅静态 0）

- `GET /hzeb-collection/servicesummary/queryDataItems`
  - query: `{"energyTypeID": "01002"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"dataItem":"累计用水量","dataItemId":"P-14-0030"},{"dataItem":"累计流量","dataItemId":"P-16-0030"},{"dataItem":"累计用水量","dataItemId":"P-01-0030"},{"dataItem":"保水"},{"dataItem":"解除保水"},{"dataItem":"欠费关阀","dataItemId":"P-01-0050"},{"dataItem":"冲正开阀","dataItemId":"P-01-0049"},{"da`
  - 菜单: 设备与采集 > 抄表数据查询 > 抄表数据(水)

### setting / get （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/setting/get/energy/setinging`

### setting / getCarbonDisclosure （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/setting/getCarbonDisclosure`

### setting / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/setting/save/energy/setinging`

### setting / saveCarbonDisclosure （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/setting/saveCarbonDisclosure`

### shareBuilding / shareBuilding （观测 0，仅静态 3）

- `[静态]` `/hzeb-charge/shareBuilding/shareBuilding/add`
- `[静态]` `/hzeb-charge/shareBuilding/shareBuilding/remove`
- `[静态]` `/hzeb-charge/shareBuilding/shareBuilding/update`

### subitem / energy （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/energy/type/list`

### subitem / onyear （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/onyear/with/energy`

### subitem / poject （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/poject/subitem/list`

### subitem / save （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/save/point/itemname`

### subitem / statistics （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/statistics/with/energy`

### subitem / summarize （观测 0，仅静态 1）

- `[静态]` `/hzeb-energy/subitem/summarize/with/energy`

### sys / external （观测 0，仅静态 2）

- `[静态]` `/hzeb-base/sys/external/interface/update/loading`
- `[静态]` `/hzeb-base/sys/external/interface/uploadImage`

### sys / pipeNetwork （观测 0，仅静态 1）

- `[静态]` `/hzeb-base/sys/pipeNetwork/getPipeNetwork`

### sys / 用户与认证 （观测 2，仅静态 15）

- `GET /hzeb-base/sys/user/info`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"user":{"userid":3,"username":"jygjgly","mobile":"18021798901","status":1,"createuserid":2,"roleid":"3","roleaname":"超级管理员","rigtofbuildings":null,"buildingname":null,"rightofdeparts":null,"depname":null,"createtime":"2026-10-14 16:25:59","customerids":"1","lastip":null,"des`
  - 菜单: 收费管理 > 用户管理 > 住户；收费管理 > 用户管理 > 商户
- `GET /hzeb-base/sys/user/list`
  - query: `{"limit": "100", "page": "1", "customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 系统管理 > 用户权限 > 用户管理
- `[静态]` `/hzeb-base/sys/user/altPasswd`
- `[静态]` `/hzeb-base/sys/user/getjfmodeandly`
- `[静态]` `/hzeb-base/sys/user/infoLinkedMenuUpdate`
- `[静态]` `/hzeb-base/sys/user/login`
- `[静态]` `/hzeb-base/sys/user/logout`
- `[静态]` `/hzeb-base/sys/user/queryAllUsername`
- `[静态]` `/hzeb-base/sys/user/queryCustomerSysconfig`
- `[静态]` `/hzeb-base/sys/user/randomImage/`
- `[静态]` `/hzeb-base/sys/user/restart/password`
- `[静态]` `/hzeb-base/sys/user/save`
- `[静态]` `/hzeb-base/sys/user/send/hzeb/sms`
- `[静态]` `/hzeb-base/sys/user/thirdlogin`
- `[静态]` `/hzeb-base/sys/user/update`
- `[静态]` `/hzeb-base/sys/user/update/hzeb/phone`
- `[静态]` `/hzeb-base/sys/user/updatepasswordbyphone`

### sys / 系统参数 （观测 2，仅静态 4）

- `GET /hzeb-base/sys/parameter/get/customer/info`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"isMulti":0,"defaultImageFlag":1,"projectModel":0,"imageUrl":"","defaultLeaderFlag":1,"customerId":1,"customerName":"南京金鹰国际物业集团有限公司"}}`
  - 菜单: 收费管理 > 账单管理 > 收费通知单；系统管理 > 系统参数 > 参数配置
- `GET /hzeb-base/sys/parameter/get/service/pack`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"records":[],"total":0,"size":20,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 系统管理 > 系统参数 > 服务包管理
- `[静态]` `/hzeb-base/sys/parameter/get/interface/List`
- `[静态]` `/hzeb-base/sys/parameter/get/interface/info`
- `[静态]` `/hzeb-base/sys/parameter/get/pay/info`
- `[静态]` `/hzeb-base/sys/parameter/save/customer/info`

### sys / 系统日志 （观测 0，仅静态 2）

- `[静态]` `/hzeb-collection/sys/log/exportRecords`
- `[静态]` `/hzeb-collection/sys/log/getRecords`

### sys / 菜单权限 （观测 1，仅静态 3）

- `GET /hzeb-base/sys/menu/getAllMenu/tree`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":[{"menuId":101,"parentId":0,"parentName":null,"name":"收费管理","url":"","perms":null,"type":0,"icon":"","orderNum":1,"open":null,"rolecheck":null,"list":null,"id":null,"level":null,"path":null,"childList":[{"menuId":101101,"parentId":101,"parentName":null,"name":"首页","ur`
  - 菜单: 系统管理 > 用户权限 > 角色管理
- `[静态]` `/hzeb-base/sys/menu/bigclass`
- `[静态]` `/hzeb-base/sys/menu/getLeafChildMenu`
- `[静态]` `/hzeb-base/sys/menu/getMenu`

### sys / 角色权限 （观测 2，仅静态 4）

- `GET /hzeb-base/sys/role/down/list`
  - query: `{"customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":[]}`
  - 菜单: 系统管理 > 用户权限 > 用户管理；系统日志 > 用户权限 > 用户管理
- `GET /hzeb-base/sys/role/list`
  - query: `{"limit": "100", "page": "1", "customerId": "1"}`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 系统管理 > 用户权限 > 角色管理
- `[静态]` `/hzeb-base/sys/role/delete`
- `[静态]` `/hzeb-base/sys/role/save`
- `[静态]` `/hzeb-base/sys/role/show`
- `[静态]` `/hzeb-base/sys/role/update`

### sysDictItem / getDictItem （观测 0，仅静态 1）

- `[静态]` `/hzeb-base/sysDictItem/getDictItem`

### system / phenotypeDataitem （观测 0，仅静态 4）

- `[静态]` `/hzeb-collection/system/phenotypeDataitem/issue/up/and/dataitem/v2`
- `[静态]` `/hzeb-collection/system/phenotypeDataitem/list`
- `[静态]` `/hzeb-collection/system/phenotypeDataitem/meter/list`
- `[静态]` `/hzeb-collection/system/phenotypeDataitem/save`

### systemMessage / getUnConfirm （观测 2，仅静态 1）

- `GET /hzeb-charge/systemMessage/getUnConfirm`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"general":0,"emergency":0,"urgency":0}}`
  - 菜单: 系统管理 > 系统消息；系统日志 > 系统参数 > 参数配置；系统日志 > 系统消息
- `GET /hzeb-collection/systemMessage/getUnConfirm`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"general":0,"emergency":0,"urgency":0}}`
  - 菜单: 系统管理 > 系统消息；系统日志 > 系统参数 > 参数配置；系统日志 > 系统消息
- `[静态]` `/hzeb-energy/systemMessage/getUnConfirm`

### systemMessage / listMessage （观测 1，仅静态 0）

- `POST /hzeb-charge/systemMessage/listMessage`
  - body: `{"buildingId": 2, "confirmTimeStart": "", "confirmTimeEnd": "", "happenTimeStart": "2026-09-14 00:00:00", "happenTimeEnd": "2026-10-14 23:59:59", "eventLevel": 3, "confirmStatus": "0", "alarmType": "", "eventType": "", "handler": "", "meterNameOrNo": "", "page": 1, "limit": 100, "buildingType": "230`
  - status: 200
  - resp: `{"msg":"操作成功","code":200,"data":{"records":[],"total":0,"size":100,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":0}}`
  - 菜单: 系统管理 > 系统消息

### systemMessageconfig / info （观测 1，仅静态 0）

- `GET /hzeb-charge/systemMessageconfig/info`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[{"id":null,"alarmType":1,"eventType":1001,"eventLevel":1,"thresholdValue":null,"customerId":1},{"id":null,"alarmType":1,"eventType":1002,"eventLevel":1,"thresholdValue":null,"customerId":1},{"id":null,"alarmType":2,"eventType":2001,"eventLevel":1,"thresholdValue":null,`
  - 菜单: 系统管理 > 消息管理 > 消息类型

### systemMessageconfig / update （观测 0，仅静态 1）

- `[静态]` `/hzeb-charge/systemMessageconfig/update`

### systemoption / systemoption （观测 1，仅静态 1）

- `GET /hzeb-charge/systemoption/systemoption/getOption`
  - query: `{"ChoiceID": "16"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":[]}`
  - 菜单: 收费管理 > 收退费查询 > 收费查询；收费管理 > 收退费查询 > 退费查询；收费管理 > 账单管理 > 水费账单
- `[静态]` `/hzeb-charge/systemoption/systemoption/getType/16`

### time / programme （观测 1，仅静态 10）

- `GET /hzeb-collection/time/programme/list`
  - query: `{"type": "1", "page": "1", "limit": "100000"}`
  - status: 200
  - resp: `{"code":200,"msg":null,"data":{"records":[{"createTime":"2026-10-14 11:03:37","id":2,"programmeName":"单一时区方案","userName":"creat_by_ypt"}],"total":1,"size":100000,"current":1,"orders":[],"optimizeCountSql":true,"searchCount":true,"countId":null,"maxLimit":null,"pages":1}}`
  - 菜单: 设备与采集 > 设备档案 > 建筑配表；设备与采集 > 设备档案 > 计量设备
- `[静态]` `/hzeb-collection/time/programme/anew/distribution`
- `[静态]` `/hzeb-collection/time/programme/delete`
- `[静态]` `/hzeb-collection/time/programme/especialtask/delete`
- `[静态]` `/hzeb-collection/time/programme/especialtask/export`
- `[静态]` `/hzeb-collection/time/programme/especialtask/list`
- `[静态]` `/hzeb-collection/time/programme/parameter/distribution`
- `[静态]` `/hzeb-collection/time/programme/parameter/read`
- `[静态]` `/hzeb-collection/time/programme/save`
- `[静态]` `/hzeb-collection/time/programme/show`
- `[静态]` `/hzeb-collection/time/programme/update`

## 2. 菜单 → 接口 视图（动态遍历）

- **收费管理 > 报表管理 > 低余额提醒报表**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 定额超限报表**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 应急控制报表**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 清零记录查询**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 用能异常统计**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 用能报表（水）**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 用能排名**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/ecabalancedaily/energy/energyRank`
  - `GET /hzeb-charge/ecabalancedaily/energy/enertyType`
- **收费管理 > 报表管理 > 远程控制流水**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 报表管理 > 销户结算报表**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 收退费查询 > 收费查询**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerconfig/info`
  - `GET /hzeb-charge/systemoption/systemoption/getOption`
- **收费管理 > 收退费查询 > 退费查询**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerconfig/info`
  - `GET /hzeb-charge/systemoption/systemoption/getOption`
- **收费管理 > 档案管理 > 住户档案**
  - `GET /hzeb-charge/customer/buildinginfo/list`
  - `GET /hzeb-charge/customer/buildinginfo/list2/v2`
  - `GET /hzeb-charge/customerconfig/info`
- **收费管理 > 档案管理 > 商户档案**
  - `GET /hzeb-charge/customer/buildinginfo/list`
  - `GET /hzeb-charge/customer/buildinginfo/list2/v2`
  - `GET /hzeb-charge/customerconfig/info`
- **收费管理 > 档案管理 > 水电单价管理**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerefldj/customerefldj/fldjConfigList`
- **收费管理 > 用户管理 > 住户**
  - `GET /hzeb-base/sys/user/info`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/list/v2`
- **收费管理 > 用户管理 > 商户**
  - `GET /hzeb-base/sys/user/info`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/list/v2`
- **收费管理 > 系统设置 > 参数配置**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotalNoRoom`
  - `GET /hzeb-charge/customerconfig/info`
- **收费管理 > 系统设置 > 票据格式**
  - `GET /hzeb-charge/customerconfig/info`
- **收费管理 > 财务管理 > 充值统计**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 财务管理 > 欠费统计**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 财务管理 > 账目盘点**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/ecochargerecord/ecochargerecord/findRealList/page`
  - `GET /hzeb-charge/ecochargerecord/ecochargerecord/findRealList/total`
- **收费管理 > 账单管理 > 其他账单**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/systemoption/systemoption/getOption`
- **收费管理 > 账单管理 > 收费通知单**
  - `GET /hzeb-base/sys/parameter/get/customer/info`
  - `GET /hzeb-charge/customerbillnotice/billnoticeStatus`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/listByNotice`
- **收费管理 > 账单管理 > 水电收支账单**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **收费管理 > 账单管理 > 水费账单**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/systemoption/systemoption/getOption`
- **收费管理 > 账户查询 > 表计状态监测**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/ecabalancedaily/energy/enertyType`
- **收费管理 > 账户查询 > 账户监测**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
- **用户管理 > 系统消息**
  - `GET /hzeb-charge/systemMessage/getUnConfirm`
  - `GET /hzeb-collection/systemMessage/getUnConfirm`
- **系统日志 > 用户权限 > 用户管理**
  - `GET /hzeb-base/sys/role/down/list`
- **系统日志 > 系统参数 > 参数配置**
  - `GET /hzeb-charge/systemMessage/getUnConfirm`
  - `GET /hzeb-collection/systemMessage/getUnConfirm`
- **系统日志 > 系统消息**
  - `GET /hzeb-charge/systemMessage/getUnConfirm`
  - `GET /hzeb-collection/systemMessage/getUnConfirm`
- **系统管理 > 消息管理 > 消息类型**
  - `GET /hzeb-charge/systemMessageconfig/info`
- **系统管理 > 用户权限 > 用户管理**
  - `GET /hzeb-base/sys/role/down/list`
  - `GET /hzeb-base/sys/user/list`
- **系统管理 > 用户权限 > 角色管理**
  - `GET /hzeb-base/sys/menu/getAllMenu/tree`
  - `GET /hzeb-base/sys/role/list`
- **系统管理 > 系统参数 > 参数配置**
  - `GET /hzeb-base/sys/parameter/get/customer/info`
  - `GET /hzeb-charge/customerkf/list`
- **系统管理 > 系统参数 > 服务包管理**
  - `GET /hzeb-base/sys/parameter/get/service/pack`
- **系统管理 > 系统消息**
  - `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`
  - `GET /hzeb-charge/systemMessage/getUnConfirm`
  - `GET /hzeb-collection/systemMessage/getUnConfirm`
  - `POST /hzeb-charge/systemMessage/listMessage`
- **系统管理 > 运维管理 > 故障报修管理**
  - `GET /hzeb-charge/customerproblem/customerproblem/list`
- **设备与采集 > 抄表数据查询 > 上报数据查询**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/nbwaterList`
- **设备与采集 > 抄表数据查询 > 手工补录(水)**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/frozenLossMeter/v2`
- **设备与采集 > 抄表数据查询 > 抄表成功率**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRate/list`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/successRate/total`
- **设备与采集 > 抄表数据查询 > 抄表数据(水)**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water`
  - `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/dataList/water/total`
  - `GET /hzeb-collection/servicesummary/queryDataItems`
- **设备与采集 > 抄表数据查询 > 用水结算报表**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecaBalancedaily/report/v2`
- **设备与采集 > 设备档案 > 建筑档案**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/buildinginfo/new/building/list`
- **设备与采集 > 设备档案 > 建筑配表**
  - `GET /hzeb-collection/big/power/list`
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/concentrator/list`
  - `GET /hzeb-collection/customeredskz/customeredskz/down/list`
  - `GET /hzeb-collection/customermeterinfo/customermeterinfo/getAllEquipmentType`
  - `GET /hzeb-collection/customermeterinfo/customermeterinfo/list`
  - `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyType/01001`
  - `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyTypeAndAppType`
  - `GET /hzeb-collection/time/programme/list`
  - `POST /hzeb-collection/equipment/get/project/check/status`
- **设备与采集 > 设备档案 > 计量设备**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/concentrator/list`
  - `GET /hzeb-collection/equipment/list/total/v2`
  - `GET /hzeb-collection/equipment/list/v2`
  - `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyTypeAndAppType`
  - `GET /hzeb-collection/time/programme/list`
- **设备与采集 > 设备档案 > 设备更换日志**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/ecoChangemeter/list`
- **设备与采集 > 设备档案 > 采集设备**
  - `GET /hzeb-collection/buildinginfo/getTreeAll`
  - `GET /hzeb-collection/concentrator/list`
  - `GET /hzeb-collection/concentrator/model/list`
  - `POST /hzeb-collection/equipment/get/project/check/status`
- **设备与采集 > 设备远程抄控 > 手工点抄**
  - `GET /hzeb-collection/buildinginfo/getTreeAll/search`
  - `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyTypeAndAppType`
  - `POST /hzeb-collection/servicesummary/getDataItem/v2`
- **设备与采集 > 设备远程抄控 > 远程控制**
  - `GET /hzeb-collection/buildinginfo/getTreeAll/search`
  - `GET /hzeb-collection/servicesummary/getEquipmentVersionByEnergyTypeAndAppType`
  - `POST /hzeb-collection/servicesummary/getDataItem/v2`
