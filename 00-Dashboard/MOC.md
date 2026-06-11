---
tags: [moc]
---

# 内容地图 (MOC)

> [[00-Dashboard/Dashboard|← 返回仪表盘]]

所有笔记的导航入口，按区域分类。使用 Dataview 自动聚合。

---

## 知识本体 wiki（编译产物）

> 按领域组织的结构化本体。打开 **Graph 视图**（已配色）看完整知识网。域注册表见 [[wiki/_index|_index]]。

- 领域 Hub：[[wiki/metaphysics/形而上学|metaphysics · 形而上学]] · 中心实体 [[实在]] · 契约 [[wiki/metaphysics/_ontology|_ontology]]
- 领域 Hub：[[wiki/epistemology/认识论|epistemology · 认识论]] · 中心实体 [[知识]] · 契约 [[wiki/epistemology/_ontology|_ontology]]
- 领域 Hub：[[wiki/ethics/伦理学|ethics · 伦理学]] · 中心实体 [[道德]] · 契约 [[wiki/ethics/_ontology|_ontology]]

```dataview
TABLE WITHOUT ID file.link AS 节点, type AS 类型, dateformat(file.mtime, "MM-dd") AS 更新
FROM "wiki"
WHERE type != "ontology" AND type != "registry" AND file.name != "形而上学" AND file.name != "认识论" AND file.name != "伦理学" AND file.name != "log"
SORT file.mtime DESC
LIMIT 12
```

## 陋居自动化层 08-Ops

> agent 契约 / run 记录 / 审核队列 / [[08-Ops/审批账本|审批账本]]。入口 [[08-Ops/README|README]]。

```dataview
TABLE WITHOUT ID file.link AS agent, status AS 状态, last-run AS 最近运行, last-result AS 最近产出
FROM "08-Ops/routines"
WHERE type = "routine"
SORT sort ASC
```

## 收集箱 Inbox

```dataview
TABLE WITHOUT ID file.link AS Note, status AS Status, type AS Type
FROM "Inbox"
WHERE file.name != "README"
SORT created DESC
```

## 问答库 07-QA

> 动态问题（如「我当前对 X 的立场」）的答案是时间序列。说「执行今日例行任务」刷新到期问题。

```dataview
TABLE WITHOUT ID file.link AS 问题, mode AS 模式, cadence AS 节奏, last-run AS 上次作答
FROM "07-QA"
WHERE type = "qa"
SORT last-run ASC
```

## 项目 Projects

```dataview
LIST
FROM "01-Projects"
SORT file.name ASC
```

## 领域 Areas

```dataview
LIST
FROM "02-Areas"
SORT file.name ASC
```

## 资源 Resources

```dataview
LIST
FROM "03-Resources"
SORT file.name ASC
```

## 知识工作流

- [[06-Templates/Research Note|研究笔记模板]] · [[06-Templates/Book Note|读书笔记模板]]
- [[Inbox/README|收集箱入口]]
- auto-wiki：`/auto-wiki recall` · `/auto-wiki ingest` · `/auto-wiki lint`

## 归档 Archive

```dataview
LIST
FROM "04-Archive"
SORT file.name ASC
```

## 日记 Daily Notes

```dataview
LIST
FROM "05-Daily"
SORT file.name DESC
LIMIT 14
```

---
*提示：新笔记推荐先放入 Inbox，再定期整理到对应 PARA 文件夹。*
