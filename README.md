# 水表 MCP（shuibiao-mcp）

南京金鹰·智慧能源管理平台（智能水表/电表，https://shuibiao.jinying.com/）的 MCP 服务器。
10 组 **64 tools**（含 20 个写操作）+ 1 resource + 1 prompt：认证、看板、档案、抄表采集、
报警消息、收费账单、能耗分析、报表、系统管理、表单写操作。
设计文档：`docs/mcp-tools-design.md`；接口清单：`docs/api-inventory.md`。

## 安装与配置（三步）

### 1. 配置凭据与下载目录
```bash
cp .env.example .env
# 编辑 .env，填写：
#   SHUIBIAO_USERNAME  登录账号
#   SHUIBIAO_PASSWORD  登录密码
#   SHUIBIAO_DOWNLOAD_DIR  报表导出落盘目录
```

### 2. 注册到 MCP 客户端（stdio）
ZCode / Claude Desktop 配置示例：
```json
{
  "mcpServers": {
    "shuibiao": {
      "command": "uv",
      "args": ["--directory", "/Users/bai/金鹰/努力工作/智能水表/水表开发", "run", "shuibiao-mcp"]
    }
  }
}
```

### 3. 首次登录（验证码流程）
平台登录需要 4 位字母图形验证码，MCP 不内置 OCR：
1. 调用 `auth_get_captcha` → 返回 `imageBase64`（验证码图）与 `checkKey`
2. 识别图中 4 位字母
3. 调用 `auth_login(captcha="识别结果", checkKey=...)`
会话约 3 小时有效，缓存于 `.session.json`，过期后重复上述流程。
自检：`auth_status` 或读取资源 `shuibiao://config/status`。

## 使用约定
- **写入确认强制策略**：所有写操作 tool 带 `confirm` 参数。第一次调用必须 `confirm=false`
  取得预览（回显 endpoint + 请求体）；Agent 须把预览展示给用户并获得明确同意后，
  才能以 `confirm=true`、相同参数重放。服务端 instructions 已内置该约束。
- 列表类 tool 统一 `page/limit` 分页 + 业务过滤参数。
- `reports_export` 将 Excel 下载到 `SHUIBIAO_DOWNLOAD_DIR`，返回本地绝对路径。
- 安装/配置引导：调用 prompt `setup_guide`。

## 开发
```bash
uv sync                 # 安装依赖
uv run shuibiao-mcp     # stdio 启动
```
接口抓取脚本与原始存档在 `capture/`（puppeteer-core harness + 479 个 webpack chunk + 遍历 JSONL）。

## 安全
- 出站请求仅 http/https；每次请求前校验 host，拒绝 localhost/环回/私有/保留地址（含 DNS 解析结果）；不跟随重定向。
- 密码仅存本地 `.env`；会话 token 存本地 `.session.json`。
