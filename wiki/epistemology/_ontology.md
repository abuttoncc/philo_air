---
title: 认识论领域本体契约
type: ontology
domain: epistemology
direction: 理论哲学
created: '2026-06-11'
updated: '2026-06-11'
schema_version: "2.0"
central_entity: 知识
tags: [ontology, contract]
---

# Philo Vault · 认识论领域本体契约

> `wiki/epistemology/` 的本体定义。`ingest`/`recall` 前先读本页。
> 与 [[wiki/metaphysics/_ontology|metaphysics 母本]] **共用同一套节点类型判据、受控关系词表、
> 6 档时间模型与退役不删除协议**——本页只声明 epistemology 特有的增量，其余一律以母本为准。

## 1. 节点类型（同母本 8 类：人物/学派/著作/概念/论证/事件/分析/来源）

判据同母本。本域典型例子：

| 子目录 | 本域例子 |
|---|---|
| `人物/` | 葛梯尔、笛卡尔、休谟、奎因、威廉姆森 |
| `学派/` | 经验主义、理性主义（作为历史学派建页；作为分类标签则走 `classified_as`，二者择一，默认标签） |
| `著作/` | 《人类理解论》《知识及其限度》 |
| `概念/` | 知识、信念、辩护、真理、先验、归纳问题（问题型概念） |
| `论证/` | 葛梯尔反例、缸中之脑、笛卡尔妖、归纳怀疑论论证 |
| `事件/` | 1963-葛梯尔论文发表 |
| `分析/` | 知识的定义之争全景、AI 时代的证言知识 |
| `来源/` | SEP 条目摘录、讨论纪要 |

> 本域易踩的坑：「经验主义」既可指历史学派（洛克-贝克莱-休谟谱系，实体）也可指立场标签（概念分类）。
> 裁决：**默认作分类标签走 `classified_as`，不建页**；只有当需要记录学派成员/时段等 T3 关系时才在 `学派/` 建页。

## 2. 受控关系词表

**全部沿用母本**：`proposed_by` · `authored_by` · `belongs_to` · `appears_in` · `responds_to` ·
`supports` · `critiques` · `develops` · `instance_of` · `part_of` · `classified_as` ·
`created_by`/`changed_by` · `grounds`（本域属理论哲学，可发出跨域奠基边）· `references`。

本域无特有关系词。例：葛梯尔反例 →critiques→ 知识（JTB 定义）；可靠主义 →responds_to→ 葛梯尔反例引出的辩护问题。

## 3. 跨域连接
- 向 ethics：认识论立场 →grounds→ 伦理后果（例：证据主义 →grounds→ 信念伦理学）。
- 向 metaphysics：共享人物/概念不重复建页，直接 wikilink + 连边（单一中文 slug 全库唯一）。
