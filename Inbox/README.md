---
tags: [inbox]
type: capture
created: 2026-06-11
cssclasses:
  - inbox
---

# 收集箱 (Inbox)

> 所有待处理想法、哲学困惑、讨论记录、读书摘记的快速落脚点。
> 每条内容一个文件，消化后编译进 wiki / 路由到 PARA。

## 待处理

-

## 灵感 & 想法

-

## 稍后阅读 / 链接

-

## 使用方法

| 操作 | 怎么做 |
|------|--------|
| **快速捕捉** | 在此文件添加一行，或直接在 `Inbox/` 下新建笔记 |
| **思考专题** | 使用 `Research Note` 模板，创建为 `Inbox/专题名.md` |
| **与 Agent 对谈** | 就某哲学问题讨论，把对谈中的论证/立场/引用记成一篇 Inbox 笔记 |
| **消化（推荐）** | `/digest-inbox` —— 逐篇分诊（结晶/参考/速朽）→ 编译进 wiki + 路由到 PARA + 打 `compiled` 标记，一步排空 |
| **只编译进 wiki** | `/auto-wiki ingest` 将思考产出持久化（digest-inbox 内部会委托它） |

> **消化闭环**：每篇笔记 frontmatter 有 `compiled` 字段。`false`/缺失 = 未消化（熵）；`/digest-inbox`
> 处理后置 `true` 并写 `digested` / `triage` / `sinks`。**源文件不移动**，靠标记区分已消化，
> 不破坏 wikilink。

```dataview
TABLE WITHOUT ID file.link AS Note, choice(compiled, "✅已消化", "🔴待消化") AS 消化, triage AS 分诊, status AS Status, dateformat(created, "MM-dd") AS Created
FROM "Inbox"
WHERE file.name != "README"
SORT compiled ASC, created ASC
```

---
*提示：保持此文件简洁，思考内容写在独立文件中。定期清空本页。*
