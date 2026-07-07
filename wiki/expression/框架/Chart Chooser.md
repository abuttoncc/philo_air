---
title: Chart Chooser
type: concept
durability: medium
aliases: [Extreme Presentation Method, 图表选择器]
created: '2026-07-07'
updated: '2026-07-07'
sources: [2026-07-07-Abela与Duarte调研, 2026-07-07-ExtremePresentation官方ChartChooser原始PDF, 2026-07-07-StephenFew的AbelasFolly博客原文]
confidence: medium
classified_as: [可视化的视觉表达]
preconditions: [数据可被归入 Relationship/Comparison/Distribution/Composition 四类之一]
falsifiable_by: ["顶层四分类若不满足 MECE 则决策树的入口本身站不住——Stephen Few《Abela's Folly》已提出此批评（Comparison=活动性质、Distribution=统计属性、Composition=结构属性、Relationship=泛化关系，四者不在同一维度；且\"随时间变化\"同时出现在 Comparison 与 Composition 分支下）"]
relations:
  - {target: Andrew Abela, type: proposed_by}
  - {target: 《Advanced Presentations by Design》, type: appears_in}
  - {target: Zelazny五种数据关系图表选择法, type: develops}
tags: [框架, 表达, 可视化的视觉表达]
---

# Chart Chooser

**一句话**：单页放射状决策树，从"你想展示什么"出发，经 Relationship/Comparison/Distribution/Composition 四向分支，终止于 19 种具体图表类型（21 个终端节点）。

Abela 本人承认直接受 [[Zelazny五种数据关系图表选择法]] 启发，是把 Zelazny 的关系判断操作化、细颗粒度化的决策树，而非独立框架。**关键限定**：21 个终端节点全部是数据图表，没有一个是流程图/组织图/权衡矩阵——**没有把选图方法扩展到逻辑图领域**，这是本域待补总表要面对的真实缺口，而非可以直接照抄 Abela 的地方。

> [!warning] 顶层分类受外部批评
> Stephen Few《Abela's Folly》公开指出四分类不满足 MECE，本域采用该框架时应带着这层保留，不视为已解决的干净分类基座。
