---
title: PageIndex 检索服务 · 完整开发提示词（交付 able_portal 侧 agent）
type: project
status: ready-to-build
created: 2026-06-20
updated: 2026-06-20
tags: [project, infra, retrieval, pageindex, mcp, ablemind, build-brief]
owner: hanlin
audience: "ablemind_portal 仓库里的开发 agent（Claude Code / ablework）"
related: ["[[PageIndex 自托管检索服务-需求说明书]]", "[[PageIndex 自托管检索服务-v0.2 接入设计]]"]
---

# PageIndex 检索服务 · 完整开发提示词

> **致开发 agent**：这是一份自包含的 build brief。你不需要读任何历史对话。按本文从 0 构建
> 一个自托管的「无向量·推理式全文检索服务」，并把它作为**第 4 个 per-user MCP** 接进
> `ablemind_portal` 平台。**先读懂第 1 节（它能做什么）和第 4 节（MCP 工具契约）——那是本服务的全部价值；鉴权和建库是支撑，不是核心。**

---

## 1. 这个服务能做什么（先读这节）

**一句话**：把任意一堆「有结构的长文档」，变成一个可被 LLM 推理导航、可逐字溯源引用、可选择性装载进上下文的「活书库」。它不是搜索框，是「给 agent 用的、会查目录的图书管理员」。

**它做这些事（每条对应一个 MCP 工具，见 §4）：**
1. **文档地图**：把一份 300 页文档转成目录树（每节带标题/页码/摘要），人和 agent 都能用它导航。
2. **跨文档选择**：5000 份里先推理锁定「该读哪几份」。
3. **推理定位**：按「相关」而非「相似」钻到具体章节（向量 RAG 做不到的：措辞不像但相关的段落也能抓到）。
4. **精确取原文**：取回逐字原句 + 页码引用（不是改写、不是幻觉，可审计）。
5. **断言取证**：给一个论断 → 回答语料「支持 / 反驳 / 查无」+ 落到哪一页。这是事实核查原语。
6. **选择性装载上下文**：不把 200 页塞进 context，只把命中的那 1 节装进去——**省 token、不撑爆窗口、答得更准**。这是它对所有 agent 工作流的底层提效。
7. **（二期）端到端问答 / 跨文档·跨版本对比**：直接给带逐句引用的答案；或并排比对 A/B 文档、同文档新旧版本。

**它的能力天花板 = 让「源」对 LLM 变得可推理导航、可逐字溯源、可选择性装载。** 仅此而已——见 §12 边界。

---

## 2. 全局架构：两个构建面

```
用户 Claude Code/ablework ──portal token──► ablemind_portal（网关）──per-user JWT──► PageIndex 后端
                                          [构建面 B：本仓库]            [构建面 A：独立服务+额外机器]
```

| 面 | 在哪 | 你建什么 | 技术栈 |
|---|---|---|---|
| **A · PageIndex 后端** | 独立 repo + 额外机器（**不在 ablemind_portal monorepo**） | `pi-build`(灌库管线) + `pi-serve`(FastMCP 服务) + `pi-store`(存储) | Python + FastMCP + 复用 VectifyAI/PageIndex |
| **B · Portal 集成** | `ablemind_portal/skill-market/web` | 代理路由 + per-user token 服务 + catalog 条目 + connect 授权 | 现有 Next.js，**照搬 ablework 模式** |

**两面解耦**：A 是个独立完整的 Python 服务（自己的存储、自己的 MCP、自己的机器）；B 只是把它挂到网关后面。A 验的是 Casdoor JWT，**查询期不依赖 Portal 应用**——Portal 挂了，已链接用户仍能查。

---

## 3. 必须复用的既有代码（构建面 B：先读这些文件再动手）

`ablemind_portal` 已经把同样的事干过 3 遍（hub / ablework / heter 三个 per-user MCP）。**照搬，别新造。**

| 读这个文件 | 学什么 / 照搬什么 |
|---|---|
| `skill-market/web/src/app/api/ablework/mcp/route.ts` | **代理路由范本**：verifyToken→user.sub→换发下游 token→流式透传。你的 `/api/pageindex/mcp` 复制它。 |
| `skill-market/web/src/server/ablework.ts` | **per-user 下游 JWT 服务范本**：独立 Casdoor app OIDC、按 sub 存 refresh_token、按需刷新。你写 `server/pageindex.ts` 照抄。 |
| `skill-market/web/src/server/tokens.ts` | portal install_token 的 `verifyToken` / `tokenFromRequest`（直接 import 用）。 |
| `skill-market/web/src/lib/mcp-catalog.ts` + `config/mcp.json` | **catalog 机制**：加一条 `pageindex` 条目就出现在 discover/connect。 |
| `skill-market/web/src/app/connect/page.tsx` | connect 页：加一个「授权 PageIndex」按钮（同 ablework 的二次授权姿势）。 |
| `skill-market/web/src/server/access.ts` | 读权限闸门（`guardRead`）。 |
| `skill-market/web/src/server/quota.ts` | （可选）给贵操作（answer）按 user_id 每日限额。 |

**踩坑点必须照搬（ablework 已验证）**：① 流式透传**绝不缓冲**，直接 pipe `upstream.body`，设 `X-Accel-Buffering: no`；② 回传 `mcp-session-id`；③ `maxDuration` 给足（answer 可能数分钟）；④ 鉴权失败回 JSON-RPC error / tool isError + oauth 引导链接，**绝不 500**。

---

## 4. MCP 工具契约（本服务的核心 = 能做什么落到接口）

pi-serve 用 FastMCP（streamable-http）暴露下列工具。每个调用的身份从 JWT 的 `sub` 解析，自动 scope 到「该用户私库 + 公用/已订阅领域库」。**一期做 1–6，二期做 7–8。**

```
# ── 一期 ──
pageindex_list_libs()
  → [{ lib_id, type:"user"|"domain", name, doc_count, scope:"private"|"public"|"subscribed" }]
  我能查哪些库。

pageindex_outline(doc_id, depth?=∞)
  → { doc_id, title, tree:[{ node_id, title, page_range:[s,e], summary, children[] }] }
  取一份文档的目录树（文档地图）。

pageindex_search_corpus(query, lib_id?=all_entitled, top_k?=5)
  → [{ doc_id, lib_id, title, reason, score }]
  跨文档推理选「该读哪几份」。

pageindex_locate(query, doc_id, top_k?=3)
  → [{ node_id, node_path, page_range, summary, reason }]
  在一份文档里推理定位到相关章节（返路径+页码+为什么，不返答案）。

pageindex_fetch(doc_id, node_id | page_range)
  → { text, citation:{ doc_id, title, node_path, page_range, source } }
  取逐字原文 + 引用元数据。fetch 不调 LLM。

pageindex_ground(claim, lib_id? | doc_id?)
  → { verdict:"supported"|"contradicted"|"not_found",
      evidence:[{ doc_id, node_path, page_range, quote }] }
  断言取证：语料支不支持这个论断、在哪一页。

# ── 二期 ──
pageindex_answer(query, scope?)
  → { answer, citations:[{ doc_id, node_path, page_range, quote }] }
  端到端多步推理问答（内部编排 search_corpus→locate→fetch），带逐句引用。

pageindex_compare(query, doc_ids[] | { doc_id, versions[] })
  → { dimensions:[{ aspect, per_doc:[{ doc_id, finding, citation }] }] }
  跨文档 / 同文档跨版本对比（如两公司分部披露、新旧财报口径 diff）。
```

> 工具描述里写清「按相关而非相似检索、结果必带页码引用」，让调用方 LLM 知道何时用它。
> 工具命名统一前缀 `pageindex_`，与 hub/ablework/heter 区隔。

---

## 5. 构建面 A：PageIndex 后端规格

### 5.1 pi-build（灌库管线，离线批处理，跑在额外算力机）
按顺序，每份文档跑一遍，**幂等**（按 `sha256` 跳过未变的）：
1. **采集**：吃 PDF / md / txt（私库走用户上传；领域库走维护者灌入）。登记为一个 `doc`，分配 `doc_id`（中文 slug）。
2. **OCR / 归一化**：有文本层的 PDF 直接解析；扫描/图片 PDF 调**自托管 OCR 大模型**逐页识别。
   - **页保真（硬约束）**：输出的 markdown 必须带每页边界标记（如 `<!-- page:N -->`）。否则建树拿不到 `page_range`，**溯源链断 = 整个服务的卖点没了**。
3. **建树**：复用 `VectifyAI/PageIndex`（`run_pageindex.py` / `pageindex` 包），用 **LiteLLM** 把模型指向**自托管 LLM**（`base_url`）。产 per-doc 树 JSON（节点含 title/node_id/page_range/summary/children）。
4. **语料级树汇编**：把所有 per-doc 树的根 + doc 描述，按 `库→域→作者/类别` 汇成一棵 corpus tree（供 `search_corpus` 先选文档）。增量更新。
5. **写 pi-store**：原件 / 归一化MD / per-doc树 / corpus树，按租户命名空间分桶。
- 提供 CLI：`ingest <path|url> --lib <user:{sub}|domain:{id}> [--doc-id <slug>]`，出建树质量报告（节点数 / 页覆盖 / 异常页）。

### 5.2 pi-serve（在线 MCP 服务，跑在轻量常驻机）
- FastMCP streamable-http server，暴露 §4 工具。
- 入口：`verify_casdoor_jwt`（用 Casdoor JWKS 自验，`aud=pageindex`）→ `sub` → 解析 entitlement（私库 `user/{sub}` + 公用领域库 + 本地订阅副本里该用户订阅的领域库）。
- 检索推理：`search_corpus`/`locate` 是 LLM 在树上推理；`fetch` 纯读不调 LLM；`ground`/`answer` 多步推理（设步数/Token 上限）。
- 只读 pi-store。

### 5.3 pi-store（存储）
- 对象存储：原件 / 归一化MD / 树JSON（MinIO 或 NAS 或本地 FS，按 `lib/{tenant}/{doc_id}/` 分桶）。
- 元数据库（SQLite 起步，量大转 Postgres）：
  - `documents(doc_id PK, lib_id, title, aliases[], source, sha256, pages, tree_path, status, created, updated)`
  - `nodes(doc_id, node_id, node_path, page_start, page_end, title, summary)` —— 加速 locate/fetch
  - `entitlements(sub, lib_id, scope, since)` —— 订阅只读副本，由 Portal webhook 同步
  - `libs(lib_id, type, name, visibility)` —— public / subscribed / private

---

## 6. 构建面 B：Portal 集成规格（在 ablemind_portal）

1. **`server/pageindex.ts`**（照抄 `server/ablework.ts`）：PageIndex 自己的 Casdoor app 的 OIDC（authorizeUrl / exchangeCode / refresh）+ 按 `user.sub` 存取 token + `getPageindexToken(sub)`（按需刷新）+ `pageindexMcpForward(...)`。
2. **`app/api/pageindex/mcp/route.ts`**（照抄 `app/api/ablework/mcp/route.ts`）：`verifyToken`→`user.sub`→`getPageindexToken`→转发 pi-serve `/mcp`；流式透传 + session-id + maxDuration + 鉴权失败引导。
3. **`config/mcp.json` 加条目**：
   ```json
   "pageindex": {
     "type":"http", "url":"https://skill.ablemind.cc/api/pageindex/mcp",
     "headers": { "Authorization":"Bearer ${PORTAL_TOKEN}" },
     "meta": { "name":"PageIndex 检索", "category":"data", "owner":"hanlin",
               "description":"无向量·推理式全文检索（私库 + 领域库），结果带页码溯源",
               "tags":["rag","retrieval","citation"] }
   }
   ```
   并跑 introspect 生成工具清单（`config/mcp-introspect.json`）。
4. **`app/connect/page.tsx`**：加「授权 PageIndex」按钮（同 ablework 二次授权），登录后回填同一枚 portal token 的可粘配置。
5. **订阅同步 webhook**：用户在 skill-market 订阅/退订一个领域库 → POST 到 pi-serve 的 admin API → 更新 pi-serve 本地 `entitlements`。（Portal 是订阅 SoT，pi-serve 持只读副本以保独立性。）
6. **（可选）`server/quota.ts`**：给 `pageindex_answer` 按 user_id 每日限额。

---

## 7. 鉴权链路（支撑，简版）

一枚 portal token 走天下 → 代理换发 per-user Casdoor JWT(`aud=pageindex`) → pi-serve 自验 JWT → 按 `sub` 解析 entitlement。**三级可见性**：私库 `user/{sub}`（仅本人）· 公用领域库（全员）· 订阅领域库（订阅者）。用户全程只碰那一枚 portal token，不碰下游 JWT。详见 [[PageIndex 自托管检索服务-v0.2 接入设计]]。

---

## 8. 构建顺序与验收

| 里程碑 | 交付 | 验收（硬标准） |
|---|---|---|
| **M0** pipeline | pi-build 跑通：1 个公用领域库（金融研报）OCR→建树→corpus树→pi-store | 树结构合理；随机抽 10 节，`page_range` 与原文实际页码一一对得上 |
| **M1** serve+接入 | pi-serve（JWT+entitlement）；Portal `/api/pageindex/mcp` 代理 + catalog + connect | 一枚 portal token 粘进 Claude Code，`list_libs/outline/search_corpus/locate/fetch` 全调通；结果 100% 带页码引用 |
| **M2** 取证+订阅分级 | `pageindex_ground`；订阅 webhook→本地 entitlements；公用 vs 订阅分级 | 给一条真/假论断各 3 条，verdict + 证据页码正确；订阅者可见、非订阅不可见 |
| **M3** 私库 | 用户灌自己的源到 `user/{sub}`，doc_id 对齐其 vault `来源/` slug | 私库硬隔离：A 用户的 token 取不到 B 的任何节点 |
| **M4** 二期 | `pageindex_answer` + `pageindex_compare` | answer/compare 的每条引用可回放到具体文档/节点/页 |

---

## 9. 必须守的纪律

- **页保真**：OCR→归一化→建树全程保留页边界，否则溯源断（M0 验收就卡这条）。
- **只读铁律**：本服务**永不写任何 vault / 知识库**。结构化沉淀、建本体、记立场——**不是它的事**（那是 auto-wiki）。它只读 pi-store、只返检索结果。
- **不编造**：查不到就 `not_found` / 留空标「待补」，绝不臆造页码或原文。
- **doc_id 对齐**：私库 `doc_id` = 用户 vault 里 `wiki/来源/{slug}` 同名 slug，跨译名靠 `aliases`。
- **租户硬隔离**：任何查询都不得跨租户；审计每次调用（哪个 sub / 哪个 lib / 哪个 doc）。

---

## 10. 已拍板的默认（除非用户另行推翻，按这些建）

- **Casdoor**：PageIndex 用**独立** application（`aud=pageindex`），不复用 ablework 的。
- **pi-serve 框架**：FastMCP（streamable-http，与上游 heter/ablework 同构，代理零改造）。
- **pi-store**：对象存储起步用本地 FS / MinIO；元数据库 SQLite 起步（与 skill-market 一致），量大转 Postgres。
- **建树模型**：复用 VectifyAI/PageIndex，LiteLLM 指向自托管 LLM；OCR 用自托管 OCR 大模型。
- **首发公用领域库**：金融研报（AbleMind 甜区，PageIndex 战绩即 FinanceBench 98.7%）。
- **机器**：pi-build 上算力机、pi-serve 上轻量常驻机、pi-store 随 build 或独立。具体机器规格待用户填，先按这个角色划分。

---

## 11. 边界：**不要**建这些（建了就是越界）

| 不建 | 因为那是谁的活 |
|---|---|
| 抽取事实 / 建知识本体 / 记关系 | `auto-wiki ingest` |
| 沉淀 conviction / 立场账本 | 用户的 wiki / AbleMind 账本（moat） |
| 数值计算 / 财务聚合 | Tushare / 财务工具 |
| 实时 / 联网检索 | WebSearch / deep-research |
| 弱结构文档（纯叙事小说）强行建树 | 这类走 wiki 编译，不进本服务 |
| 海量短文本模糊召回 | 那是向量的活，不是树的活 |

**记死：本服务是「原文层的检索器与上下文供给器」——把源喂得准、引得到、装得省。理解、沉淀、计算、判断都发生在它之外。**

---

## 12. 起步动作（你现在就可以做）

1. 读 §3 列的 7 个文件，确认 ablework 模式。
2. 在独立 repo 起 pi-serve 骨架（FastMCP + §4 工具桩 + JWT 验签桩），先返 mock 数据。
3. 在 ablemind_portal 起构建面 B：复制 `ablework/mcp/route.ts`→`pageindex/mcp/route.ts`、`server/ablework.ts`→`server/pageindex.ts`，改 endpoint/aud，加 catalog 条目。
4. 端到端打通「Claude Code 粘 token → 经 Portal → pi-serve mock」后，再回头做 pi-build 真实灌库（M0）。
5. 有疑问先问用户，**不要编造**机器 IP / 模型名 / Casdoor client_id（这些是部署期填的 env）。
