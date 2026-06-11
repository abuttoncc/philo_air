---
name: daily-routine
version: 0.1.0
description: |
  每日例行任务编排器：扫 07-QA 问答库，对到期的动态问题站在当前时点作答（复盘+推演），
  建立连接，缺口则向外界获取（deep-dive）并 ingest 回 wiki，最后追加答案并回写 Daily。

  触发词：执行今日例行任务、今日例行、例行任务、每日例行、跑问答库、
  刷新本周预测、daily routine、run routine、跑例行。

  本 skill 是编排器，不自己实现 recall/ingest/lint —— 委托给 auto-wiki；取材用
  WebSearch / 网页阅读（SEP / IEP / PhilPapers）。
---

# 每日例行任务 (daily-routine)

> 用户打开 Claude Code 说「执行今日例行任务」时触发。把 `07-QA/` 问答库里**到期的动态问题**跑一遍标准流水线。

## 核心理念

- **问题是模板，答案是时间序列**：动态问题每次站在 `as-of=今天` 重答，旧答案 append 保留，绝不覆盖（对齐 wiki 的 T0 观测值 / 退役不删除）。
- **站在时间点上**：周初问"本周怎么看"，要**先复盘上周已发生**（数据/事件/价格落地了没），**再推演本周**（基准/上行/下行情景 + 概率 + 一句话）。
- **闭环**：能用 wiki 回答的先 recall 回答；wiki 缺/过期的，才向外界 deep-dive，并把新知识 ingest 回 wiki，让下次 recall 更强。

## 执行流程

### Step 0 — 定位时点与 Daily
- `as-of = 系统 currentDate`（今天）。判断今天是周几（周初触发 weekly 类问题）。
- 确保 `05-Daily/<today>.md` 存在；不存在按 [[06-Templates/Daily Note]] 建。

### Step 1 — 扫问答库，挑出到期问题
- 读 `07-QA/` 下每个 `type: qa` 文件的 frontmatter。
- **到期判据**：`mode: dynamic` 且满足任一 —— `cadence` 周期已到（weekly: 距 `last-run` ≥ 上个周一；monthly: 跨月）/ `status: due` / `last-run` 为空 / 用户点名。
- `static` 问题默认跳过（除非用户显式要求刷新）。
- 列出本次要跑的问题清单，先报给用户。

### Step 2 — 对每个到期问题作答（流水线）
1. **recall**：按该问题 `recall-scope`（如 `[metaphysics]`）加载 wiki 本体上下文 —— 委托 auto-wiki recall（读 `wiki/{domain}/` hub + data.db 摘要 + 相关节点）。
2. **复盘**：站在 as-of，总结上一周期**已发生**的关键变化（新读的文本、T4 事件、立场切换），并**对照上一次答案**——"上周我怎么判断、兑现了没"。
3. **推演**：对本周期给出**基准 / 上行 / 下行**情景 + 触发条件 + 一句话结论。用「立场研判（轻）」结构：当前立场 + 最强支持论证 + 最强反驳（steelman）+ 一句话结论。
4. **建立连接**：答案内回链 wiki 节点、[[02-Areas/哲学研究]]、来源页（`wiki/{domain}/来源/`）、上一次答案。
5. **缺口检测**：委托 auto-wiki lint(Coverage) —— 列出回答时 wiki 里**缺/过期**的节点（断链、单来源、陈旧数据、被引未建页）。
6. **外部获取（若有缺口）**：deep-dive —— 用 WebSearch / 网页阅读（SEP / IEP / PhilPapers）取材 →（关键缺口）按 auto-wiki ingest 协议补进 `wiki/{domain}/`（建节点/事件、数值进 data.db、补关系边）→ 用新知识**补全答案**。每个缺口最多搜 3 次，搜不到标"未能补全"。
7. **写回答案**：把本次答案作为 `### <as-of> (as-of)` 块 **append 进该问题文件「## 答案历史」的顶部**；更新 frontmatter `last-run: <today>`、`status: fresh`、`last-summary: <一句话结论>`（供 Dashboard QA 时间线读取）。

### Step 3 — 回写 Daily
- 在 `05-Daily/<today>.md` 的「## 笔记/阅读」记：跑了哪些问题 + 各自一句话结论 + 触发的 deep-dive/ingest 动作。

### Step 4 —（可选）更新 Area 跟踪指标
- 若复盘取到更新读数，同步 [[02-Areas/投资研究]] 的「回顾与跟踪指标」表。

### Step 5 — 汇报
```
今日例行任务完成（as-of <today>）：
- 作答 N 题：<问题> → <一句话结论> …
- deep-dive：<缺口> → <补了什么> / <未能补全>
- ingest：wiki/{domain} 新增/更新 <节点/事件/数值>
- 待人工确认：<冲突/存疑项>
```

## 防扩散与纪律

- **append-only**：答案只增不改；发现旧答案判断错了，不改旧块，在新块里写"修正：上周判断X，实际Y"。
- **ingest 守协议**：建事件/退役旧结论一律走 auto-wiki 的「退役不删除六步」，数值进 data.db 不进正文。
- **链接会过期**：网络来源溯源记"标题+站点+日期"；原典溯源记"作者+著作+章节"。
- **可控范围**：默认只跑到期的 dynamic 问题；一次最多 deep-dive 10 个缺口。

## 与其它 skill / 工具的关系

| 职责 | 委托给 |
|---|---|
| recall / ingest / lint(Coverage) | `auto-wiki`（wiki/{domain} 本体） |
| SEP / IEP / PhilPapers / 公开网页 | WebSearch / 网页阅读 |


## 陋居接线（08-Ops，2026-06-12 起）

- **无人值守 run**（launchd，暂未接线；接线后生效）：开跑在 `08-Ops/runs/` 建 run 档（status: running），结束补全「## 飞轮」步进 / outputs / status；**产出收口**：高危写入（newnode / retire / disputed / xedge=grounds 族）先查 `08-Ops/审批账本.md`——gate `state: auto` 直写并在审计日志 append 记账，其余落 `08-Ops/review/` 候选卡。
- **交互 run**（用户在终端）：高危写入当场问用户，裁决即记审批账（批准 streak+1 / 驳回清零 / contested 原地记）；跑完更新 `08-Ops/routines/答题员.md` 的 `last-run` / `last-result`。
- **「处理审核队列」**：读 `08-Ops/review/` 全部 pending 候选 → 逐张报卡（gate + diff + 来源 + 审批账本上下文）→ 按裁决执行写入 / 翻卡 / 记账。