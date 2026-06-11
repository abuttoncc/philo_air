---
tags: [ops]
type: index
created: 2026-06-11
---

# 审核队列 (08-Ops/review)

> 无人值守 agent 的**高危写入候选**落在这里（产出收口原则）。每张卡一个文件，命名
> `YYYY-MM-DD-{gate}-{对象slug}.md`。裁决入口：终端说「**处理审核队列**」，或在 Dashboard 控制台点「裁决队列」。

## 候选卡 frontmatter 规范

```yaml
type: candidate
gate: newnode | retire | disputed | xedge | t0-merge
status: pending          # → approved / rejected / contested
target: 物自体           # 中文 slug
domain: metaphysics
routine: daily-routine   # 投递 agent
created: 2026-06-12
decided:                 # 裁决日期，裁决时回填
```

正文三节：`## 变更`（diff 式：+新值 / -旧值 / 事件盖章）· `## 来源`（溯源 + confidence + fact-check 结果）· `## 裁决记录`（append）。

## 裁决语义

- **批准** → Agent 按 ingest 协议原子执行（退役走六步），审批账本 streak+1。
- **驳回** → 不落库，审批账本 streak 清零（已 auto 的 gate 降级）。
- **contested** → 按争议记录进本体（confidence: contested），审批账本不加不清。

```dataview
TABLE WITHOUT ID file.link AS 候选, gate AS 闸, routine AS 投递 agent, created AS 日期, status AS 状态
FROM "08-Ops/review"
WHERE type = "candidate"
SORT status DESC, created DESC
```
