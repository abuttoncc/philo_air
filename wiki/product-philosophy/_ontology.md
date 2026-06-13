---
title: 产品哲学领域本体契约
type: ontology
domain: product-philosophy
direction: 实践哲学
created: '2026-06-13'
updated: '2026-06-13'
schema_version: "2.0"
central_entity: 产品哲学
tags: [ontology, contract]
---

# Philo Vault · 产品哲学领域本体契约

> `wiki/product-philosophy/` 的本体定义。`ingest`/`recall` 前先读本页。引擎规范见 `.claude/skills/auto-wiki/`，
> 与 [[wiki/metaphysics/_ontology|metaphysics 母本]] **共用同一套 6 档时间模型、退役不删除协议与三分铁律**——
> **本页只声明 产品哲学 领域特有的节点类型与受控关系词表**，其余一律以引擎 + metaphysics 母本契约为准。

## 0. 总原则（同母本）
1. **节点 / 数据 / 边 三分**：数值绝不是节点（进 data.db）；关系是边不是页；分类标签是边不是页。
2. **编译单向**：`Inbox(散文) → ingest → wiki(本体)`。严谨只用在已结晶的知识。
3. **退役不删除**：T1/T2/T3 任何变化都是「旧行封 valid_to + 插新行」，永不 DELETE，必有 T4 事件盖章。

## 1. 节点判据（同母本的「能不能指向就是这一个」）
能用手指指向「就是这一个」、明年同名还指同一个 → **实体**；必须先讲一段机理才懂 → **概念**。

## 2. 节点类型（=目录=图谱着色）
| 类型 | 子目录 | 判据 | 例子 |
|---|---|---|---|
| 实体·人物 | `人物/` | 有专名的产品人/思想源头，能指向就是这一个 | 史蒂夫·乔布斯、乙川弘文、埃德温·兰德、艾伦·凯 |
| 实体·公司 | `公司/` | 有专名的企业 | 苹果 |
| 实体·著作 | `著作/` | 有专名的文本，书名号《》开头命名 | 《史蒂夫·乔布斯传》《Make Something Wonderful》 |
| 概念 | `概念/` | 必须先讲定义/机理才懂；有专名的心智模型/启发式归此 | 聚焦即说不、端到端控制、现实扭曲力场、死亡过滤器 |
| 案例 | `案例/` | 有专名的产品决策实践样本：可指认主体+时段，功能是例证/反驳某概念 | iPhone砍实体键盘案例 |
| 事件 | `事件/` | 有日期+施动者，发生即固定 | 1997-乔布斯回归苹果、2005-斯坦福毕业演讲 |
| 分析 | `分析/` | 研究课题派生视图（删了不影响本体） | 乔布斯产品哲学综述 |
| 来源 | `来源/` | 提炼笔记/演讲文字稿/访谈摘录（注明 source_type） | 2026-06-13-乔布斯-GitHub技能笔记 |

> 易踩的坑：「现实扭曲力场」「连点成线」有故事性、像案例——但它们是**有专名的心智模型**，归 `概念/`；
> 「1997 砍掉 90% 产品线」是 **T4 事件 + T0 数值**（350→10 进 data.db），不单独建概念页；
> 「乔布斯执掌苹果」是一条 **`led_by` 边**（带时态），不是页。

## 3. 受控关系词表（product-philosophy 特有；通用词沿用母本）

本域特有增量（与 capital-allocation 共用同三词）：
- `led_by`（公司 → 人物）：经营/掌舵，T3 关系带时态。例：苹果 →led_by→ 史蒂夫·乔布斯。
- `exemplifies`（案例 → 概念）：案例例证某心智模型。例：iPhone砍实体键盘案例 →exemplifies→ 聚焦即说不。
- `involves`（案例 → 人物/公司）：案例涉及的主体。

沿用母本：`proposed_by`(概念→人物) · `authored_by`(著作→人物) · `appears_in` · `supports`/`critiques` ·
`develops`(后继人物/概念→前驱，思想师承用此) · `instance_of` · `part_of` · `classified_as` ·
`created_by`/`changed_by`(→事件) · `references`(分析/来源→任意)。

> lint 时以本表对照；双写：页面 `frontmatter.relations[]` + `data.db relations 表`。

## 4. 跨域连接
本域作为驱动层时，用 `references` 边连到其他域的「分析/节点」（如 product-philosophy/分析 → equity/公司）。
跨域 wikilink 直接写对方 slug 即可。
