---
tags: [ops, moc]
type: index
created: 2026-06-11
---

# 陋居自动化层 (08-Ops)

> 隐喻：陋居（The Burrow）——毛衣针自己织毛衣、搅拌器自己搅拌。**人做深度思考和全局掌控；
> 「当 X 发生 → 做 Y」的模式化劳动交给 agent（受契约约束的 routine）。**
> 蓝图见 `ref/burrow-workspace-blueprint.md`；本目录是它在 Obsidian 库里的文件化落地。

## 四条原则（叠在库的 8 条不变量之上）

1. **产出收口** — agent 在**无人值守**运行时永远不直写高危正典知识，只投递候选（`review/`）。毛衣针可以织毛衣，不能重新布置房间。
2. **捕获免费、晋升收紧** — Inbox 和对话零摩擦；类型校验只发生在晋升（ingest 闸门）时刻。
3. **审批权限分级** — 自动批准范围由 [[审批账本]] 治理：某类写入连续 N 次人工批准零驳回 → 进自动批准白名单；一次驳回 → 清零降级。
4. **确定性优先** — 能用纯代码完成的 agent 绝不用 LLM（schema.py 校验、scan-inbox.py 扫描、晋升执行的退役六步）。

## 目录结构

| 子目录/文件 | 内容 | 谁写 |
|---|---|---|
| `routines/` | agent 契约注册表，每个 agent 一页（trigger/scope/budget/escalation） | 人（改契约=改 agent 权限） |
| `runs/` | 飞轮记录，每次无人值守 run 一页（步进 + 产出 + 预算消耗） | agent（run 开始建、结束补全） |
| `review/` | 审核队列：高危写入候选卡片（status: pending → approved/rejected/contested） | agent 投递，人裁决 |
| [[审批账本]] | 信任账本：每类写入一条进度（streak/threshold/state）+ 审计日志 | 裁决时记账 |

## 高危写入分级（gate）

| gate | 含义 | 初始状态 |
|---|---|---|
| `t0-merge` | T0 verified 数值合并补充（fact-check 通过） | counting 0/10 |
| `newnode` | 新建本体节点 | counting 0/20 |
| `xedge` | 跨域边（grounds 族） | counting 0/20 |
| `retire` | 退役触发（T1/T2 当前态改变） | **永久人工**（设计决定：改变世界当前态的写入不开放自动批准） |
| `disputed` | fact-check 数值分歧 | 永久人工（逐例裁决） |

## 两种运行模式

- **交互会话**（你在终端里）：高危写入当场问你 → 你的批准/驳回**即时记入审批账本**（裁决记账），批准后直写。
- **无人值守**（launchd，本库暂未接定时器）：gate 处于 `auto` 状态的直写并在审批账本审计日志记账；其余一律落 `review/` 候选，等你晨读裁决。

## 裁决流程（晨读 ≤3 分钟）

1. 打开 [[00-Dashboard/Dashboard|Dashboard]] → 北极星条扫一眼 → Agent 状态钟看运行状态 → QA 时间线读结论。
2. 审核队列有 pending → 终端说「**处理审核队列**」：Agent 逐张报卡（diff + 来源 + 审批账本上下文），你说 批准/驳回/contested。
3. 批准 → Agent 按 ingest 协议原子执行写入（退役走六步）→ 候选卡 status 翻转 → 审批记账（streak+1 或清零）。

## 自动聚合

```dataview
TABLE WITHOUT ID file.link AS agent, status AS 状态, trigger AS 触发, budget AS 预算
FROM "08-Ops/routines"
WHERE type = "routine"
SORT sort ASC
```

```dataview
TABLE WITHOUT ID file.link AS 候选, gate AS 闸, status AS 状态, created AS 投递
FROM "08-Ops/review"
WHERE type = "candidate"
SORT status DESC, created DESC
LIMIT 10
```
