# 资本配置领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-13
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-13 — 首次 ingest（域奠基）
- Source: 来源/2026-06-13-局外人-GitHub笔记 + 来源/2026-06-13-高质量投资-GitHub笔记（均二手·GitHub 读书笔记，原文留存 Inbox）
- Created: 39 页 — 人物 10 / 公司 8 / 著作 2 / 概念 12 / 案例 3 / 事件 1 / 分析 1 / 来源 2
- data.db: data_points 10（8 家公司年化回报、特利丹回购比例、ABC 对价，confidence=medium）；facts 6（T2 耐用逻辑）；events 1（2012-巴菲特推荐《局外人》）；relations 52
- 防扩散：《高质量投资》案例公司（SGS/Costco/爱马仕/孟山都等）不建页；跨域 grounds 边仅列候选（见 分析/资本配置与质量投资框架综述），未写入
- Conflicts: none

## 2026-06-14 — 横向因果链织入（expand --scan 驱动 + T5 词表扩展）
- 触发: expand --scan 报本域 5 概念为"挂件"；读内容发现框架已 part_of 织好（scan 误报干净树叶），真缺口=横向因果边，而词表无概念→概念因果边
- T5 本体变更: 母本 metaphysics/_ontology.md + CLAUDE.md 受控词表 **新增 `enables`(概念→概念，因果/增强)**；用户裁决"加，全库通用"
- Created: 0 页（纯织边，无新节点）
- data.db: relations +4（品牌力→定价权、定价权→增长来源、经常性收入→资本回报、竞争优势模式→资本回报，皆 enables）
- 复盘: scan 在此为假阳性（干净分类树叶 deg=1 必然），已记入待优化（scan 应区分"已 part_of 归位"与"真未织入"）
- Conflicts: none

## 2026-06-15 — 事件去孤儿（exemplifies 放宽）
- 决策 A 落地: 放宽 `exemplifies` 允许 事件→概念（本域 _ontology 同步）
- data.db: relations +1（《局外人》→changed_by→2012-巴菲特推荐《局外人》——2012 背书事件特例，连书不连概念）
- 复验: scan 孤儿（capital-allocation 侧 2012 事件）去孤儿
- Conflicts: none

## 2026-06-15 — 补全局外人 8 CEO 案例集（anysearch 驱动，补弱连接公司）
- 触发: scan 报 5 家公司弱连接（TCI/伯克希尔/华盛顿邮报/罗尔斯顿/通用影院，仅 led_by）；用户「用 anysearch 补案例」
- Source: 来源/2026-06-15-局外人五案例-anysearch调研（二手·多源：Thorndike 解读/HBS/Commoncog/Quartr）
- Created: 6 页 — 案例 5（TCI杠杆税盾/华盛顿邮报回购/罗尔斯顿回购/通用影院多元化/伯克希尔浮存金）+ 来源 1；案例集补全为 8/8
- data.db: relations +21（每案例 exemplifies→概念 + involves→公司/CEO + appears_in→《局外人》）；data_points +3（回购比例 40%/60%、跑赢标普 11x，verified）
- 复验: scan 弱连接 14→9（5 公司脱离）；schema 45/45 PASSED
- 防扩散: 案例集封顶 8（=书中 8 CEO），不再扩；CEO/公司复用既有节点
- 审批: newnode 9→10（交互会话，用户指令即裁决）
- Conflicts: none
