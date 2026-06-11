---
tags: [qa, moc]
type: index
created: 2026-06-11
---

# 问答库 (07-QA)

> 一组**站着不动的问题**。动态问题的答案是**时间序列**——同一问题每次站在提问时点重答，旧答案不删、新答案追加（append-only）。
> 哲学库的典型动态问题：「我当前对 X 的立场是什么、理由是什么、和上次比变了没有」——**立场的演化轨迹本身就是这个库的核心产出**。

## 触发方式

打开 Claude Code，说 **「执行今日例行任务」** → `daily-routine` skill 自动：
扫本目录 → 挑出**到期**的动态问题 → 对每个跑
`recall(加载 wiki 本体) → 复盘(上次立场) → 推演(当前立场+一句话理由) → 建立连接 → 缺口检测 → 缺口则 deep-dive 外部获取并 ingest → 追加答案 → 回写 Daily`。

## 问题清单

| 问题 | 模式 | 节奏 | recall 域 | 上次作答 |
|---|---|---|---|---|
| （暂无——按下方字段约定新建） | | | | |

## 字段约定（每个问题文件的 frontmatter）

- `mode`：`dynamic`（答案随时间变，每次新增一块）/ `static`（答案相对固定，变化走更新）
- `cadence`：`weekly` / `monthly` / `adhoc`（到期才被例行任务挑中）
- `recall-scope`：作答时加载哪些 wiki 领域（如 `[metaphysics, ethics]`）
- `last-run`：最近一次作答日期（由 daily-routine 更新）
- `status`：`due`（待答）/ `fresh`（今日已答）

示例问题（可直接建）：「我当前对自由意志的立场」`recall-scope: [metaphysics, ethics]`、
「本月读的哲学文本中最强的一个论证」`cadence: monthly`。

## 自动聚合

```dataview
TABLE mode AS 模式, cadence AS 节奏, last-run AS 上次作答, status AS 状态
FROM "07-QA"
WHERE type = "qa"
SORT last-run ASC
```

---
*新问题：在 `07-QA/` 下按字段约定新建一个文件即可，下次例行任务会自动纳入。*
