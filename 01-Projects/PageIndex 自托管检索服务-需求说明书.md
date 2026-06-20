---
title: PageIndex 自托管检索服务 · 需求说明书
type: project
status: draft
created: 2026-06-20
updated: 2026-06-20
tags: [project, infra, retrieval, pageindex, mcp, cross-vault]
owner: hanlin
version: v0.1
---

# PageIndex 自托管检索服务 · 需求说明书 (SRS)

> 形态：**MCP 服务** ｜ 范围：**跨库统一语料** ｜ 检索：**两段式分期**
> 一句话定位：给所有 burrow 库（philo_air / valu_air / tech_air …）的**原始全文语料**配一个
> 不靠向量、靠"目录树 + LLM 推理"的自托管检索后端，作为 `wiki` 本体图谱之外的**第二条检索腿**。

---

## 0. 文档信息

| 项 | 值 |
|---|---|
| 文档状态 | Draft v0.1，待评审 |
| 决策前提 | 服务形态=MCP；语料范围=跨库统一（需语料级树）；检索=两段式分期 |
| 上游项目 | VectifyAI/PageIndex（开源建树引擎，复用）、pageindex-mcp（云端 MCP，不直接用） |
| 关联契约 | 各库 `auto-wiki` skill、`ref/text-sources.md`、`digest-inbox`、`08-Ops` 陋居层 |

---

## 1. 背景与目标

### 1.1 背景
burrow 范式的库把知识分三类：**思考**（Inbox→ingest）、**本体**（wiki 图谱）、**原始素材/语料**（原典全文、整本书、文字稿）。前两类有干净的生命周期，第三类——大块只读全文——一直**没有自己的检索器**：现在它们要么作为 `来源/` 节点背后一坨死的 backing text 躺着，要么整篇塞进上下文。

PageIndex 的理念与本库的 `wiki` 同源：**都拒绝"向量相似度"，改用"结构 + 推理"**。差别是 `wiki` 把全文**有损编译**成本体图谱，而 PageIndex 给全文盖一层**目录树**做**无损索引**，让 LLM 像查书目录一样推理钻取。两者互补，正好补齐第三类语料的检索。

### 1.2 目标（北极星）
让任意 burrow 库的 Agent（`recall` / `auto-wiki ingest` / `daily-routine` / `deep-dive`）在需要**精确引用原始全文某章节原句**时，通过一次 MCP 调用，**不靠向量、可溯源地**定位到正确文档的正确章节并取回原文，而不必把整本全文塞进上下文。

### 1.3 成功判据（可度量）
- **召回正确性**：在一组人工标注问句上，一期定位层 Top-3 文档命中率 ≥ 90%，章节定位 Top-3 命中率 ≥ 80%。
- **可溯源**：100% 的检索结果带 `doc_id + 节点路径 + 页码范围 + 来源出处`。
- **私有性**：素材与模型调用 100% 不出内网（自托管模型 base_url + 内网存储）。
- **集成无摩擦**：在一个库的 `.mcp.json` 注册后，`recall` 可零改造调用。

---

## 2. 范围

### 2.1 In Scope
- 跨库统一的**语料接入 → OCR/归一化 → 建树 → 语料级树汇编 → 存储**离线管线。
- **MCP 服务**：暴露检索工具，供各库 Agent 调用。
- **两段式检索**：一期"定位 + 取原文"，二期"端到端推理问答"。
- 与各库 `wiki/来源/` 节点的**主键对齐**（共享 slug）。

### 2.2 Out of Scope（明确不做）
- **不写 wiki**：本服务**只读**，绝不直写任何库的本体。结构化沉淀仍只能经 `auto-wiki ingest`（守"产出收口"原则）。
- 不做通用 Web 检索（那是各库 WebSearch / deep-research 的事）。
- 不替代 `wiki` 图谱推理；只补"全文精确引用"这一段。
- 一期不做端到端问答 Agent（推迟到二期）。

### 2.3 复用 vs 自建（边界交底）
| 模块 | 开源 PageIndex | 本项目 |
|---|---|---|
| 单文档建树（PDF/MD→JSON 树） | ✅ 直接复用 `run_pageindex.py` + `pageindex/` | 封装调用 |
| 模型可换（LiteLLM，指向自托管 LLM） | ✅ | 配置内网 base_url |
| 复杂 PDF OCR | ❌（云服务功能） | **自建**（用自托管 OCR 大模型）|
| 跨文档语料级树（File System） | ❌（云服务功能） | **自建** |
| 检索（多步推理 + 树搜索） | ⚠️ 仅 demo | **自建**（分两期）|
| MCP / 服务层 | ❌（开源版 CLI/库） | **自建** |
| 存储编排 / 增量 / 溯源 | ❌ | **自建** |

---

## 3. 术语
- **doc**：一份原始全文（一本书/一篇原典/一份文字稿）。
- **doc_id**：文档主键 = 中文 slug，**与该库 `wiki/{domain}/来源/` 节点 slug 同名**（命名纪律，靠 `aliases` 去重）。
- **per-doc 树**：单文档的 PageIndex 目录树（节点含 title / node_id / page_range / summary / children）。
- **语料级树 (corpus tree)**：所有 doc 的根节点 + doc 描述汇成的一棵"先选哪份文档"的树。
- **定位 (locate)**：沿树推理，返回节点路径 + 页码，不返答案。
- **取原文 (fetch)**：按节点/页码取回原文片段 + 引用元数据。

---

## 4. 角色与使用场景

| 角色 | 场景 | 触发 |
|---|---|---|
| 库的 `recall` | 讨论中要引坛经某品原句 / 财报某节原文 | 调 `locate`+`fetch`，把原文片段 + 引用喂进对话 |
| `auto-wiki ingest` | 编译时要核证某断言、补 `来源/` 节点原文锚 | 调 `locate` 定位章节，原文进 `来源/` 节点引文 |
| `daily-routine` / `deep-dive` | 缺口填充时在已有全文语料里先查 | 调 `search_corpus` 选文档再 `locate` |
| 维护者（人） | 灌新原典、查建树质量、巡检语料覆盖 | CLI / 管理接口 |

> **用户故事示例**：`recall` 在 philo_air 讨论"见路不走"时，需要金刚经"凡所有相皆是虚妄"原句 →
> `search_corpus("金刚经 相 虚妄", vault=philo_air)` 命中 `金刚经` doc → `locate("相 虚妄", doc_id=金刚经)`
> 返回"第十四分"节点 + 页码 → `fetch` 取回该分原文 + `[[金刚经]]#第十四分` 引用。全程零向量、可溯源。

---

## 5. 总体架构

```
┌─────────────────────── 离线接入管线 (批处理) ───────────────────────┐
│  采集层        OCR/归一化层         建树层            汇编层          │
│  ─────         ──────────          ─────            ─────           │
│ 各库 03-       PDF有文本层→直解     run_pageindex    语料级树         │
│ Resources/     扫描/图片→OCR大模型   (LiteLLM→自托管  (汇所有 doc     │
│ 原典/、         逐页→页标记 markdown  LLM)→per-doc 树   根+描述)       │
│ text-sources   归一化+sha256         JSON                            │
│ 拉取、用户PDF                                                        │
└──────────────────────────────┬─────────────────────────────────────┘
                               ▼
              ┌──────────── 存储层 ────────────┐
              │ 对象存储: 原件 / 归一化MD / 树JSON │
              │ 元数据库: documents / nodes 表    │
              └──────────────┬─────────────────┘
                             ▼
┌──────────────────── 在线检索服务 (常驻 MCP) ───────────────────────┐
│  一期 (定位层)                      二期 (问答层, 叠加)              │
│  search_corpus → locate → fetch     answer (多步推理 Agent)         │
│  describe / list                    复用一期工具做内部步骤           │
└──────────────────────────────┬─────────────────────────────────────┘
                               ▼
        各库 .mcp.json 注册 → recall / auto-wiki / daily-routine 调用
```

**关键不变量**：检索服务**只读存储**；管线**只写存储、不写任何 wiki**；wiki 的写入仍独占给 `auto-wiki`。

---

## 6. 功能需求 (FR)

### 6.1 接入与管线（离线，一期必做）

- **FR-1 采集**：支持三种来源——① 各库 `03-Resources/原典/` 等目录下的 md/txt/pdf；② `ref/text-sources.md` 按 URL 拉取的全文；③ 维护者手投 PDF。每份登记为一个 doc，分配 `doc_id`（中文 slug，与目标库 `来源/` 节点对齐）。
- **FR-2 OCR/归一化**：
  - PDF 有文本层 → 直接解析（pypdf/pdfplumber）。
  - 扫描件/图片 PDF → 调**自托管 OCR 大模型**逐页识别为 markdown。
  - **页保真（硬约束）**：归一化输出必须保留**每页边界标记**（如 `<!-- page:N -->`），否则建树拿不到 `page_range`，溯源链断。
  - 输出统一为"带页标记的 markdown" + 文档级 `sha256`。
- **FR-3 建树**：调用 PageIndex 引擎（`--md_path` 或 `--pdf_path`），LiteLLM `base_url` 指向自托管 LLM；产 per-doc 树 JSON，节点含 `title / node_id / page_range / summary / children`。建树参数（`--max-pages-per-node` / `--max-tokens-per-node` / `--if-add-node-summary` 等）可配。
- **FR-4 语料级树汇编**：把所有 per-doc 树的根 + doc 描述汇成一棵 corpus tree，**按 库 → 域 → 作者/类别**分组（让 LLM 先在小范围里选文档）。新增/更新 doc 时增量重建受影响子树。
- **FR-5 增量与幂等**：以 `sha256` 判重（对齐 `digest-inbox` 的 SHA256-skip）；源未变则跳过重建；变更则**新版本树 + 旧版保留**（对齐"退役不删除"，溯源可回放）。
- **FR-6 灌库 CLI**：`ingest <path|url> --vault <v> --domain <d> [--doc-id <slug>]`，批量、可重跑、出建树质量报告（节点数 / 页覆盖 / 异常页）。

### 6.2 检索服务 · 一期（定位 + 取原文）

以 MCP 工具暴露（契约见 §7）：
- **FR-7 search_corpus**：输入自然语言 query（可带 `vault` / `domain` 过滤）→ LLM 在 corpus tree 上推理 → 返回候选 doc 列表（`doc_id` + 选它的理由 + 置信）。
- **FR-8 locate**：输入 query + `doc_id` → LLM 在该 doc 的 per-doc 树上推理遍历 → 返回 1~N 个**节点路径 + 页码范围 + 节点摘要**。**不返最终答案。**
- **FR-9 fetch**：输入 `doc_id` + `node_id`（或页码范围）→ 返回该节原文片段 + **引用元数据**（`doc_id`、节点路径、页码、来源出处 URL/书目）。
- **FR-10 describe / list**：列语料清单、看某 doc 的树结构与元数据（供维护者与 Agent 自检）。

### 6.3 检索服务 · 二期（端到端问答，叠加）

- **FR-11 answer**：输入 query（可带 scope）→ 内部编排 `search_corpus → locate → fetch → 多步推理` → 返回**带逐句引用的答案**。复用一期工具作为内部步骤，不另起炉灶。
- **FR-12 跨文档综合**：answer 支持跨多 doc 取证并标注每条引用来自哪个 doc/节点（对齐本库"溯源记作者+著作+章节"）。

---

## 7. 接口需求（MCP 工具契约）

> 传输：MCP（stdio 或 streamable-http）。命名前缀 `pageindex_`，便于在 `.mcp.json` 与其它 MCP 区隔。

| 工具 | 期 | 入参 | 出参（要点） |
|---|---|---|---|
| `pageindex_search_corpus` | 一 | `query`, `vault?`, `domain?`, `top_k=5` | `[{doc_id, title, reason, score}]` |
| `pageindex_locate` | 一 | `query`, `doc_id`, `top_k=3` | `[{node_id, node_path, page_range, summary, score}]` |
| `pageindex_fetch` | 一 | `doc_id`, `node_id` \| `page_range` | `{text, citation:{doc_id,node_path,page_range,source}}` |
| `pageindex_describe` | 一 | `doc_id` | `{title, aliases, vault, domain, source, tree}` |
| `pageindex_list` | 一 | `vault?`, `domain?` | `[{doc_id, title, status, pages, updated}]` |
| `pageindex_answer` | 二 | `query`, `scope?` | `{answer, citations:[{doc_id,node_path,page_range,quote}]}` |

**数据模型（存储层）**：
- `documents`：`doc_id`(PK, 中文 slug) · `title` · `aliases[]` · `vault` · `domain` · `source_url` · `sha256` · `pages` · `tree_path` · `status` · `created` · `updated`。
- `nodes`（可选加速）：`doc_id` · `node_id` · `node_path` · `page_start` · `page_end` · `title` · `summary`。
- 对象存储：`{原件} / {归一化MD} / {per-doc 树JSON} / {corpus 树JSON}`，按 `vault/domain/doc_id` 分桶。

> **主键对齐纪律**：`doc_id` 必须等于目标库 `wiki/{domain}/来源/{slug}` 的 slug。于是 `recall` 在 wiki 里看到 `[[金刚经]]` 这个 `来源/` 节点，可无缝拿同名 `doc_id` 调本服务取全文。**单一中文 slug 全栈唯一**，延续 burrow 命名纪律。

---

## 8. 非功能需求 (NFR)

- **NFR-1 可溯源（一等公民）**：任何检索结果必须可回放到"哪份文档/哪个节点/哪几页/什么出处"。无引用的结果视为缺陷。
- **NFR-2 私有/离线**：素材、归一化文本、模型调用全程内网；LLM/OCR 走自托管 base_url；服务可在断外网下运行（原典、私有材料刚需）。
- **NFR-3 性能**：建树为离线批处理，不计入在线 SLA；在线一期 `locate` P95 ≤ 数秒（含 1~2 次 LLM 调用）。`fetch` 不调 LLM，P95 ≤ 数百 ms。
- **NFR-4 成本可控**：建树是 LLM 密集的一次性成本（可夜间批跑）；检索按调用计费，二期 answer 的多步推理需设步数/Token 上限。
- **NFR-5 可解释**：`search_corpus` / `locate` 返回"为什么选这条"的推理理由，不做黑箱。
- **NFR-6 幂等/可重跑/不丢**：管线任一步可安全重跑；版本化树（退役不删除），支持回放。
- **NFR-7 可观测**：建树质量报告 + 检索调用日志（query / 命中 / 耗时 / Token），落各库 `08-Ops/runs/` 留痕。
- **NFR-8 模型可插拔**：LLM 与 OCR 模型经配置切换（LiteLLM 统一 LLM；OCR 走独立适配器），不绑死单一供应商。

---

## 9. 部署拓扑（自托管）

```
[ 服务器 ]
 ├─ 管线 Worker（批处理；夜间/手动触发建树）
 │    ├─ OCR 适配器 ── HTTP ──▶ [ 自托管 OCR 大模型 ]
 │    └─ PageIndex 引擎 ─ LiteLLM ─▶ [ 自托管 LLM (base_url) ]
 ├─ MCP 服务（常驻；stdio / streamable-http）
 │    └─ 只读存储
 └─ 存储
      ├─ 对象存储（原件 / MD / 树 JSON）
      └─ 元数据库（SQLite 起步，量大转 Postgres）
```
- **各库接线**：在 `philo_air/.mcp.json`、`valu_air/.mcp.json` … 注册同一个 MCP endpoint，用 `vault` 入参隔离视图。
- **触发**：管线手动/夜间批跑（一期）；后续可挂 `08-Ops` 定时器（launchd）做"新原典落库自动建树"。

---

## 10. 分期与验收

| 期 | 交付 | 验收 |
|---|---|---|
| **M0 PoC** | 拿坛经/矛盾论各建一棵树，跑通"自托管 LLM 建树" | 树 JSON 节点合理、页码对得上原文 |
| **M1 管线** | 接入+OCR+建树+语料级树+存储+灌库 CLI；灌入 philo_air 全部原典 | FR-1~6 通过；建树质量报告达标 |
| **M2 一期检索** | MCP 服务上线，`search_corpus/locate/fetch/describe/list`；接入 philo_air `.mcp.json` | §1.3 成功判据；`recall` 实测可零改造调用 |
| **M3 跨库** | 灌入 valu_air / tech_air，corpus tree 跨库分组 | 跨库检索 `vault` 过滤正确、命中率达标 |
| **M4 二期问答** | `pageindex_answer` 端到端多步推理 + 逐句引用 | FR-11~12；引用 100% 可溯源 |

---

## 11. 风险与开放问题

- **R-1 页保真**：OCR→归一化→建树若丢页边界，`page_range` 失真、溯源断。**缓解**：页标记贯穿，建树后抽样核页。
- **R-2 建树成本/质量**：长书（69 万字小说）建树 Token 消耗大、章节切分可能不理想。**缓解**：分卷建树、调 `max-tokens-per-node`、人工抽检。
- **R-3 中文/无目录文档**：PageIndex 偏好有 ToC 的专业文档；纯叙事文本（小说）天然章节弱。**开放问题**：小说类是否值得建树，还是仍走 wiki 编译为主？（建议 M1 用一本小说试，看树是否有用）
- **R-4 OCR 模型接口**：自托管 OCR 大模型的输入/输出格式需适配器抽象。**开放问题**：用哪个 OCR 模型、是否需逐页 vision 推理。
- **R-5 与 wiki 主键漂移**：`doc_id` 与 `来源/` slug 若不同步会断引用。**缓解**：灌库时校验目标库是否已有同名 `来源/` 节点，不一致则报人工。
- **R-6 二期推理步数失控**：answer 多步推理可能发散。**缓解**：硬上限步数/Token，超限降级为一期定位结果。

---

## 12. 待你拍板（写进 v0.2 前）
1. **OCR 模型**：具体用哪个自托管 OCR 大模型？是否需要 vision 逐页？
2. **建树 LLM**：自托管的哪个模型走 LiteLLM？上下文窗口多大（决定 `max-tokens-per-node`）？
3. **存储选型**：对象存储用什么（MinIO / 本地 FS / NAS）？元数据库 SQLite 起步可否？
4. **小说类语料**（豆豆三部曲）：进不进 PageIndex？还是只让 wiki 编译，PageIndex 只收"有章节结构的原典/财报/讲义"？
5. **MCP 传输**：stdio（本机随 Claude Code 起）还是 streamable-http（服务器常驻、多客户端共享）？跨库共享更适合后者。

---

> 来源参考：[VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex) · [pageindex-mcp](https://github.com/VectifyAI/pageindex-mcp)
