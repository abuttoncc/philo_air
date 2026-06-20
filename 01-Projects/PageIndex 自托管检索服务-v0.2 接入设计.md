---
title: PageIndex 自托管检索服务 · v0.2 多租户接入设计
type: project
status: draft
created: 2026-06-20
updated: 2026-06-20
tags: [project, infra, retrieval, pageindex, mcp, ablemind, portal]
owner: hanlin
supersedes: "v0.1 SRS 的 §7 鉴权 / §9 部署（鉴权模型由双 key 改为单 portal token 代理）"
---

# PageIndex 自托管检索服务 · v0.2 接入设计

> 配套：[[PageIndex 自托管检索服务-需求说明书]]（v0.1 功能/管线仍有效）。
> 本文只改一件事并改对：**接入与鉴权形态**——从"自造双 api-key"纠正为
> **复用 ablemind_portal 已有的「一枚 portal token + 姿势 A 代理」机制**。

---

## 0. 纠正：不造新 key，PageIndex = 挂在 Portal 后的第 4 个 per-user MCP

读 `ablemind_portal/skill-market` 源码后确认，你已有一套成熟机制，PageIndex 直接复用、零新增 key 体系：

- **一枚 portal install_token 走天下**：`sk_live_<hex>`，`sha256` 存哈希、明文只显一次、`/connect` 登录即回填（`api/skillhub/mcp-token`）。用户把这**同一枚** token 粘进 `mcp.json`，就能用全部后端 MCP。
- **Portal = 统一 MCP 网关（姿势 A：代理在前）**：后端 MCP 以 per-user 代理挂载，已挂 3 个——
  `ablemind-hub`(`/api/mcp`) · `ablework-fleet`(`/api/ablework/mcp`) · `heter-reason`(`/api/heter/mcp`)。
- **代理做身份翻译**：`verifyToken(token)` → `user.sub` → 换发**下游 per-user 凭证** → 转发到后端 `/mcp`。用户永远不碰下游短命 token（"密钥绝不进浏览器"）。
- **目录/发现**：`lib/mcp-catalog.ts` 文件型双源（`config/mcp.json` + `DATA_DIR/mcp.json` 覆盖 + `mcp-introspect.json` 工具清单）→ discover/connect UI。
- **私域闸门**：`server/access.ts` 的 `guardRead`——已登录会话 **或** 有效 token 才放行。

> **结论：PageIndex 就是第 4 个 MCP（`pageindex`，`/api/pageindex/mcp`）。** 不新建 key，不新建登录，不新建订阅 UI。你说的"公用的 / 每个人的 key"——其实是**同一枚 token 在服务端解析出不同 entitlement**，不是两把钥匙。

---

## 1. 两个现成范本，PageIndex 照哪个长

代码里有两种 per-user 代理姿势，PageIndex 取 **ablework 式**（因为它必须知道"你是谁"才能定位你的私库）：

| 范本 | 下游鉴权 | 后端知道用户吗 | 适用 |
|---|---|---|---|
| **ablework 式**(`server/ablework.ts`) | 独立 Casdoor app（`aud=ablework`）换发 per-user JWT，服务端按 `sub` 存储+按需刷新 | ✅ 知道 → 各自租户运行 | **PageIndex 选这个**（要分私库） |
| heter 式(`api/heter/mcp`) | 单一 `INTERNAL_TOKEN` + Portal 按 user_id 扣配额 | ❌ 不知道，纯共享 | 仅适合无租户的共享算力 |

**PageIndex 取 ablework 式**：自建一个 Casdoor application（`aud=pageindex`），Portal 代理按 `user.sub` 换发 per-user pageindex JWT，PageIndex 后端 `verify_casdoor_jwt` 认出用户 → scope 到「该用户私库 + 已订阅领域库」。

---

## 2. 总体架构（PageIndex 作为第 4 个 MCP）

```
用户的 Claude Code / ablework
  mcp.json 里粘一枚 portal install_token（/connect 回填）
        │  Bearer sk_live_...
        ▼
┌───────────── ablemind_portal (skill.ablemind.cc, heyun01) ─────────────┐
│  统一 MCP 网关 · Casdoor SSO · mcp-catalog · access 闸门 · 订阅          │
│   /api/mcp(hub)  /api/ablework/mcp  /api/heter/mcp  ▶ /api/pageindex/mcp │ ← 新增
│        代理: verifyToken→user.sub→换发 per-user pageindex JWT→转发         │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │ Bearer <per-user pageindex Casdoor JWT>
                                ▼  (内网 / Streamable-HTTP SSE 透传)
┌───────────────── PageIndex 自托管后端（你的额外机器，独立完整）─────────────┐
│  pi-serve  (在线 MCP 服务机, 轻)                                          │
│    verify_casdoor_jwt → sub → 解析 entitlement(私库 + 订阅领域库)          │
│    工具: search_corpus / locate / fetch / list_libs / describe / answer  │
│        ▲ 只读                                                            │
│  pi-store (存储): 对象存储(原件/归一化MD/树JSON) + 元数据库(per-tenant)     │
│        ▲ 写                                                              │
│  pi-build (离线算力机): OCR大模型 + 建树LLM(LiteLLM) + 管线 worker         │
└──────────────────────────────────────────────────────────────────────────┘
```

**独立完整性**：pi-serve 验的是 **Casdoor JWT（用 Casdoor JWKS 自验）**，不是 portal 的 DB token——所以 PageIndex 后端**在查询期不依赖 skill-market 应用**，只依赖 Casdoor（身份）。Portal 挂了，已链接用户的 JWT 在有效期内仍能查。这满足你"确保服务独立和完整"。

---

## 3. 鉴权链路（完全镜像 ablework，逐步）

1. 用户在 `/connect` 一次性 OAuth 授权 PageIndex 的 Casdoor app（与授权 ablework 同样的二次链接动作）；Portal 服务端按 `user.sub` 存其 refresh_token。
2. 用户把**同一枚 portal install_token** 粘进 `mcp.json` 的 `pageindex` 条目（`/connect` 直接给可粘配置）。
3. 运行时：Claude Code → `/api/pageindex/mcp`（带 portal token）→ 代理 `verifyToken` 得 `user.sub` → `getPageindexToken(sub)`（短命 JWT，按需 refresh）→ 转发 pi-serve。
4. pi-serve 验 JWT（`aud=pageindex`）→ `sub` → entitlement → scope 检索。
5. 失败不报 500：未链接/过期 → 回 JSON-RPC error / tool isError，带 `oauth_login` 引导链接（照搬 ablework 的 `linkGuidance`）。

---

## 4. 三级可见性 + 订阅复用 + 公用/私有

你说的"公用 + 每人"在这里落为**三级 entitlement**，全部由 pi-serve 按 `sub` 解析，不靠第二把 key：

| 级别 | 谁能查 | 对应你的话 |
|---|---|---|
| **私库** `user/{sub}` | 仅本人 | "每个人连自己的" |
| **公用领域库** `domain/{id}` (public) | 任何已链接用户 | "公用的" |
| **订阅领域库** `domain/{id}` (subscribed) | 订阅者 | 领域库的进阶/受控部分 |

**订阅复用**：把"一个领域库"在 skill-market 注册成一个可订阅条目（沿用现有入库/评测/订阅）。订阅事件 → webhook POST 到 pi-serve 的 admin API → pi-serve **本地** entitlements 表更新。
- 为什么本地缓存：保持 §2 的"查询期不依赖 portal"。Portal 是订阅/身份的 SoT，pi-serve 持订阅只读副本。
- 公用库 = entitlement 默认对所有已链接用户开；私库 = 仅 owner；订阅库 = 看副本。

---

## 5. 机器分配（用你的额外机器，落"独立完整"）

| 角色 | 机器 | 跑什么 | 负载 |
|---|---|---|---|
| **pi-build** | 额外机器①（算力/GPU） | OCR大模型 + LiteLLM 建树 + 管线 worker（采集/OCR/页保真归一化/建树/语料级树汇编） | 重，离线批，夜间可跑 |
| **pi-serve** | 额外机器②（或 heyun01 旁） | FastMCP streamable-http + JWT 验签 + entitlement 解析 + 检索推理 | 轻，常驻 |
| **pi-store** | 随 build 或独立 | 对象存储(MinIO/NAS/FS) + 元数据库(SQLite 起步→Postgres) | 中 |
| **portal 代理** | heyun01（现有） | `/api/pageindex/mcp` 一个路由文件 + catalog 一条目 | 零新机器 |

建树（重）与检索（轻）分机，互不挤占；存储独立分桶。Portal 侧只加**一个代理路由 + 一条 catalog**，不动现有三个 MCP。

---

## 6. Portal 代理路由（复用 ablework 代理的工程细节）

`skill-market/web/src/app/api/pageindex/mcp/route.ts`——以 `api/ablework/mcp/route.ts` 为模板，照搬这些**已被踩坑验证**的细节：
- **流式透传不缓冲**：直接 pipe `upstream.body`，设 `X-Accel-Buffering: no`（answer 可能跑数分钟，nginx 不能掐）。
- **回传 `mcp-session-id`**：FastMCP streamable-http 是有会话传输，initialize 的会话头要带回。
- **`maxDuration` 给足**：检索/answer 参照 ablework 给到数百秒（建树是离线的，不走这条）。
- **每方法注入下游 token**：若 pi-serve 像 ablework 那样所有方法都 gate，则每个转发方法都注 JWT。
- **（可选）配额**：领域库 answer 这类贵操作可仿 `server/quota.ts` 按 user_id 每日限额。

catalog 增条（`config/mcp.json`）：
```json
"pageindex": {
  "type": "http", "url": "https://skill.ablemind.cc/api/pageindex/mcp",
  "headers": { "Authorization": "Bearer ${PORTAL_TOKEN}" },
  "meta": { "name": "PageIndex 检索", "category": "data", "owner": "hanlin",
            "description": "无向量·推理式全文检索（私库 + 领域库）", "tags": ["rag","retrieval"] }
}
```

---

## 7. 灌库与租户命名

- **私库灌入**：用户经 pi-build CLI / 上传，写 `user/{sub}/` 命名空间；`doc_id` = 中文 slug。
- **领域库灌入**：维护者把高质量源（研报/财报/招股书/原典）灌进 `domain/{id}/`，注册成 skill-market 可订阅条目。
- **doc_id 对齐**：私库 `doc_id` 对齐用户自己 vault 的 `wiki/来源/{slug}`，于是其 `recall` 看到 `[[xxx]]` 来源节点可同名调本服务（延续 burrow 命名纪律）。
- **只读铁律**：PageIndex 永不写任何 vault；结构化沉淀仍独占给 `auto-wiki ingest`。

---

## 8. 分期

| 期 | 交付 | 验收 |
|---|---|---|
| **M0** | pi-build 跑通：一个公用领域库（金融研报）OCR→建树→语料级树→pi-store | 树合理、页码对得上 |
| **M1** | pi-serve 上线（JWT 验签 + entitlement）；Portal `/api/pageindex/mcp` 代理；catalog + /connect 接入 | 一枚 portal token 即可在 Claude Code 调通 search/locate/fetch |
| **M2** | 订阅 webhook → pi-serve 本地 entitlements；公用 vs 订阅领域库分级 | 订阅者可见、非订阅不可见 |
| **M3** | 私库：用户灌自己的源，`user/{sub}` 隔离 + doc_id 对齐其 vault | 私库硬隔离，跨租户零泄漏 |
| **M4** | phase-2 `answer`（多步推理 + 逐句引用） | 引用 100% 可溯源 |

---

## 9. 待你拍板
1. **PageIndex 用独立 Casdoor app（`aud=pageindex`）还是复用 ablework 的 app？** 我倾向独立（隔离 + 各自吊销），但要新建一个 Casdoor application + `/connect` 加一个授权按钮。
2. **pi-serve 用什么框架起 MCP？** 倾向 FastMCP（streamable-http，与 heter/ablework 上游同构，代理零改造）。
3. **pi-store 选型**：MinIO / NAS / 本地 FS；元数据库 SQLite 起步可否（与 skill-market 一致）？
4. **额外机器具体两台还是一台兼 build+store？** 给我机器规格我把 pi-build / pi-serve / pi-store 落到具体机器。
5. **公用领域库首发选哪个域**（金融研报 / 宏观 / 招股书 / 原典）做 M0？
