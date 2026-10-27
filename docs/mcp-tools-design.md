# 水表 MCP — tools 分组设计（检查点①：请审核）

> **实现状态（2026-10-14）**：分组已按用户决策定稿并实现完毕。
> - 决策：写操作全纳入+confirm 二次确认；验证码由 Agent 看图识别；导出落盘到 `SHUIBIAO_DOWNLOAD_DIR`，安装时引导配置账号/密码/下载路径。
> - 代码：`src/shuibiao_mcp/`（FastMCP + httpx，stdio），注册 **48 tools + 1 resource**。
> - smoke 测试：45 项中 41 通过；`energy_*` 4 项因生产侧 `hzeb-energy` 微服务网关 502（裸 curl 同样 502，非代码问题），服务恢复后自动可用。
> - 已实测链路：验证码识别→登录→看板/档案/抄表/报警/收费/系统各读接口→导出 xlsx 落盘。
> - 安装与接入见 `README.md`（ZCode 配置片段 therein）。

站点：https://shuibiao.jinying.com/ （智慧能源管理平台·深圳合众致达）
依据：`docs/api-inventory.md`（静态 577 端点 + 动态遍历 68 菜单页 / 52 观测端点）

## 设计原则
1. **1 个 tool = 1 个业务动作**，内部聚合多个后端接口；不暴露裸 HTTP。
2. 所有 list 类 tool 统一支持 `page/limit` 与业务过滤参数（对齐真实 query）。
3. 建筑树（getTreeTotal/getTreeAll）是多数页面的前置依赖 → 由 client 层缓存，不作为独立 tool 暴露（提供 `archives_building_tree` 供按需查询）。
4. 写操作（远程控制、充值、补录、开户/销户、报警处理）单独标注 ⚠️，默认带 `confirm` 参数二次确认。
5. 会话：MCP 内部维护 token；过期自动走验证码登录流程（见 G1）。

## 分组总览（9 组 / 42 tools）

| 组 | 域 | tools 数 | 读写 |
|---|---|---|---|
| G1 auth | 认证与会话 | 3 | 写(登录) |
| G2 dashboard | 总览看板 | 2 | 读 |
| G3 archives | 档案管理 | 6 | 读 |
| G4 metering | 抄表与采集 | 6 | 读+⚠️写 |
| G5 alarm | 报警与消息 | 4 | 读+⚠️写 |
| G6 charge | 收费与账单 | 8 | 读+⚠️写 |
| G7 energy | 能耗分析 | 5 | 读 |
| G8 reports | 报表查询 | 3 | 读(含导出) |
| G9 system | 系统管理 | 5 | 读+⚠️写 |

---

## G1 auth 认证与会话
| tool | 说明 | 后端接口 |
|---|---|---|
| `auth_get_captcha` | 获取图形验证码（返回 base64 图 + checkKey），供多模态 Agent 识别 | `GET /hzeb-base/sys/user/randomImage/{ts}` |
| `auth_login` | 提交验证码完成登录；密码自动 base64(md5hex)；会话持久化 | `POST /hzeb-base/sys/user/login` |
| `auth_status` | 当前会话状态/登录用户信息 | `GET /hzeb-base/sys/user/info` |

> 验证码为 4 位字母图（已验证可识别）。MCP 不内置 OCR，由调用方 Agent 看图填码——与 Agent 使用场景天然契合。

## G2 dashboard 总览看板
| tool | 说明 | 后端接口 |
|---|---|---|
| `dashboard_charge_summary` | 收费视窗汇总：实收/应收/其他收入/缴费方式/回收率/月度序列 | `GET /hzeb-charge/ecochargerecord/{hydropowerReceipts, hydropowerReceivable, annualSummary/v2, otherIncome, payClassification, recoveryRate, meter/v2, room, abnormal}` |
| `dashboard_collection_status` | 采集在线率：集中器/模块在线离线统计 | `GET /hzeb-collection/concentrator/statistics` |

## G3 archives 档案管理
| tool | 说明 | 后端接口 |
|---|---|---|
| `archives_building_tree` | 建筑/区域树（收费域或采集域） | `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/getTreeTotal`；`GET /hzeb-collection/buildinginfo/getTreeAll` |
| `archives_building_list` | 建筑档案分页 | `GET /hzeb-charge/customer/buildinginfo/list2/v2` |
| `archives_meter_list` | 计量设备（水/电表）分页 + 设备类型字典 | `GET /hzeb-collection/customermeterinfo/customermeterinfo/list`、`getAllEquipmentType` |
| `archives_collector_list` | 采集设备/集中器分页 + 型号字典 | `GET /hzeb-collection/concentrator/list`、`concentrator/model/list` |
| `archives_tenant_merchant_list` | 住户/商户档案分页 | `GET /hzeb-charge/customer/buildinginfo/list` |
| `archives_resident_list` | 住户/商户用户（房间绑定）分页 | `GET /hzeb-charge/customerbuildinginfo/customerbuildinginfo/jxlyxy/list/v2` |

## G4 metering 抄表与采集
| tool | 说明 | 后端接口 |
|---|---|---|
| `metering_reading_data` | 抄表数据查询（水/电、冻结/实时、上报数据） | `GET /hzeb-collection/ecoEsinglerealtimedata/ecoEsinglerealtimedata/{dataList/water, nbwaterList}` 等 |
| `metering_success_rate` | 抄表成功率（列表+合计） | `GET .../successRate/list`、`.../successRate/total` |
| `metering_frozen_loss` | 冻损/缺失表计（手工补录依据） | `GET .../frozenLossMeter/v2` |
| `metering_manual_entry` ️ | 手工补录抄表数 | 表单提交端点待二次抓取（遍历未触发） |
| `metering_remote_control` ⚠️️ | 远程阀控/通断（单表/批量）——断水断电级操作 | `POST /hzeb-charge/comEspecialtask/emergencyControl(Batch)` |
| `metering_control_records` | 远程控制/应急控制流水 | `GET /hzeb-charge/comEspecialtask/controlList` |

## G5 alarm 报警与消息
| tool | 说明 | 后端接口 |
|---|---|---|
| `alarm_balance_list` | 低余额报警分页；`handle` 子动作处理/批量处理 ⚠️ | `GET /hzeb-charge/ecabalancealarm/list`；`POST .../handleAlarm(Batch)` |
| `alarm_usage_event_list` | 异常用能事件分页 | `GET /hzeb-collection/ecoEeventdata/list` |
| `alarm_message_list` | 报警消息分页 / 标记已读 | `GET /hzeb-collection/ecamessagelist/ecamessagelist/list`；`GET .../readed/{id}` |
| `alarm_fault_repair_list` | 故障报修工单分页 | `GET /hzeb-charge/customerproblem/customerproblem/list` |

## G6 charge 收费与账单
| tool | 说明 | 后端接口 |
|---|---|---|
| `charge_price_list` | 水电单价/费率配置 | `GET /hzeb-charge/customerefldj/customerefldj/fldjConfigList` |
| `charge_bill_list` | 账单查询（水费/电费/公摊/其他/收支，billType 区分） | `GET /hzeb-charge/customerfee/customerfee/{feeBillList, otherBillList}/page+total`、`charge/billList`、`charge/get/bill/list` |
| `charge_notice_list` | 收费通知单状态/列表 | `GET /hzeb-charge/customerbillnotice/billnoticeStatus`、`customerbuildinginfo/listByNotice` |
| `charge_payment_query` | 收费/退费查询（实收流水分页+合计） | `GET /hzeb-charge/ecochargerecord/ecochargerecord/findRealList/page+total` |
| `charge_recharge_stats` | 充值统计/欠费统计/账目盘点 | `GET /hzeb-charge/ecochargerecord/*`（部分待二次抓取确认） |
| `charge_recharge` ⚠️ | 账户充值（线下记账/线上发起） | 表单提交端点待二次抓取 |
| `charge_account_open_close` ⚠️ | 开户/销户（批量） | `POST /hzeb-charge/customeraccount/customeraccount/openUserBatch`；`GET /hzeb-charge/ecocloseaccountrecord/ecocloseaccountrecord/list` |
| `charge_low_balance_report` | 低余额提醒报表 | `GET /hzeb-charge/ecabalancealarm/list`（报表视图） |

## G7 energy 能耗分析
| tool | 说明 | 后端接口 |
|---|---|---|
| `energy_overview` | 能耗总概览/拓扑树 | `GET /hzeb-energy/archives/topologyTree` 等 |
| `energy_building` | 建筑用能（含同比/环比） | `GET /hzeb-energy/build/{energy, time, buildcompare, timecompare}` |
| `energy_branch_elec` | 支路用电 + 线损分析 | `/hzeb-energy/...`（静态端点，页面参数待二次抓取） |
| `energy_branch_water` | 支路用水 + 漏水分析 | 同上 |
| `energy_rank` | 用能排名 | `GET /hzeb-charge/ecabalancedaily/energy/energyRank`、`enertyType` |

## G8 reports 报表查询
| tool | 说明 | 后端接口 |
|---|---|---|
| `reports_energy` | 用能报表（水/电）、用能异常统计、定额超限 | `/hzeb-charge|collection/...report...`（静态） |
| `records_control_and_close` | 远程控制流水、应急控制、销户结算、清零记录 | `comEspecialtask/controlList`、`ecocloseaccountrecord/list` 等 |
| `reports_export` | 任一报表导出（99 个 export/import 端点按 reportType 路由），返回文件落盘路径 | `*/export`、`*/downLoad` |

## G9 system 系统管理
| tool | 说明 | 后端接口 |
|---|---|---|
| `system_user_list` | 操作用户分页（含角色下拉） | `GET /hzeb-base/sys/user/list`、`sys/role/down/list` |
| `system_user_write` ⚠️ | 用户新增/改/删/重置密码 | `POST /hzeb-base/sys/user/{save, update, delete...}`（静态） |
| `system_role_list_write` ⚠️ | 角色 CRUD + 菜单树 | `GET /hzeb-base/sys/role/list`、`sys/menu/getAllMenu/tree`、`role/{save, update, delete}` |
| `system_log_list` | 系统操作日志分页/导出 | `GET /hzeb-base/ecoSyslog/...`、`export` |
| `system_params` | 客户参数/服务包/收费参数/票据配置 | `GET /hzeb-base/sys/parameter/get/customer/info`、`get/service/pack`、`/hzeb-charge/customerconfig/info`、`systemoption/getOption` |

---

## 待你拍板的 3 个问题
1. **写操作范围**：G4/G5/G6/G9 的 ⚠️ 写 tool（尤其远程阀控、充值）是否纳入第一版？还是第一版纯只读，写操作后加？
2. **验证码流程**：`auth_get_captcha` 返回 base64 由 Agent 识别（推荐）；是否接受？
3. **导出类接口**（99 个 export/import）：MCP 内下载后返回本地文件路径（推荐），还是 base64 内联？

## 已知缺口（实现期补齐）
- 表单提交类写端点（手工补录、充值、开户/销户）遍历未触发 → 实现期用浏览器二次抓取表单提交确认请求体。
- G7 能耗分支页面参数结构待二次抓取。
- socket.io 实时通道（报警推送）第一版不接入 MCP，留作后续。

---

## 增补（2026-10-15）：G10 表单填写类写操作 + 确认策略强化

应用户要求补齐表单提交类接口（读写全纳入），请求体通过对 479 个前端 chunk 的
表单提交代码静态分析获得（不碰生产表单，避免脏数据）。新增 16 tools，总计 **64 tools**。

**写入确认强制策略**（服务端 instructions 级约束）：
任何写 tool 第一次调用必须 `confirm=False` 取得预览（回显 endpoint + body）；
Agent 必须把预览原样展示给用户并询问；仅当用户明确同意后才允许 `confirm=True` 重放同一参数。

### G10 表单写操作（16 tools，全部 ⚠️ confirm 流程，除标注只读）
| tool | 说明 | 后端接口 |
|---|---|---|
| `metering_manual_entry` | 手工补录抄表数 `{type, date, data[]}` | `POST /supervision/beforecalc/frozen/addFrozenData`（404 回退 hzeb-collection 同名） |
| `metering_time_programme_list` | 校时/参数方案列表（只读） | `GET /hzeb-collection/time/programme/list` |
| `metering_time_programme_save` | 校时方案保存/更新 | `POST time/programme/save|update` |
| `metering_dispatch` | 校时下发 / 参数下发 | `POST time/programme/anew/distribution、parameter/distribution` |
| `charge_bill_adjust` | 账单调整/调账 | `POST customerefldj/adjustBills` |
| `charge_fee_insert_save` | 其他账单录入 | `POST customerfee/saveFeeInsert` |
| `charge_fee_insert_list` | 其他账单录入记录（只读） | `GET customerfee/feeInsertList` |
| `charge_notice_update` | 收费通知单配置更新 | `POST customerbillnotice/billnoticeUpdate` |
| `charge_balance_alarm_setting` | 低余额提醒开关 | `POST customer/buildinginfo/updateIsBalancealarm` |
| `charge_settle_refresh` | 结算重算 | `POST ecodatasettle/refresh` |
| `charge_settle_bill_list` | 结算/交易账单分页（只读） | `GET ecodatasettle/billList|tradeBillList/page` |
| `archives_building_write` | 建筑 add/update/delete/matchTable | `POST customer/buildinginfo/add|update|match/table`、`DELETE .../delete` |
| `archives_meter_write` | 表计起度阈值修改/拆表 | `POST customermeterinfo/updateQcvalue|dismantleMeter` |
| `archives_collector_write` | 集中器 add/delete/activation | `POST concentrator/add|delete|activation` |
| `archives_share_building_write` | 公摊组 add/update/remove | `POST shareBuilding/add|update`、`DELETE remove` |
| `system_config_update` | 客户/定时/缴费方式/回路名/消息配置更新 | `POST customerconfig/update*、systemMessageconfig/update` |

### 既有 tool 修正
- `charge_recharge` 改为真实端点 `POST /hzeb-charge/comechargetask/comechargetask/chargeEnergy`，
  请求体 `{buildingId, chargeAmount, chargeWay, chargeType}`（chunk 抓包确认）。
- 新增 prompt `setup_guide`：安装时引导配置账号/密码/下载目录 + MCP 注册 + 首次登录流程。
