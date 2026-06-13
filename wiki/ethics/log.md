# 伦理学领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-11
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-12 — ingest（首次）
- Source: 来源/2026-06-12-遥远的救世主（豆豆《遥远的救世主》，全25章，约35万字）
- Created entity: 人物/豆豆、著作/《遥远的救世主》
- Created concept: 概念/文化属性、概念/强势文化、概念/弱势文化、概念/救世主情结、概念/得救之道（共5页）
- Created argument: 论证/文化决定论论证、论证/得救悖论、论证/扶贫悖论（共3页）
- Created analysis: 分析/遥远的救世主-文化伦理主题综述
- Relations: 18条（authored_by / appears_in / proposed_by / part_of / supports / critiques）
- Cross-domain grounds: 天道(形而上学) →grounds→ 文化属性/强势文化/弱势文化（伦理学）
- Facts(T2): 文化属性核心命题 / 强势文化定义 / 弱势文化定义（3条，valid_from 2005-01）
- Conflicts: none
- Schema: pending（见下方校验步骤）

## 2026-06-12 — deep-dive（理论沿革）
- Source: 来源/2026-06-12-理论沿革深挖（二手·权威，Agent 知识综合 SEP/IEP 与标准哲学史文献）
- **引用纪律生效**：直引仅限可核验原典/标准中译；外文转译标原文段落（GM I §10 / Ethica E4 Praef. 等）；不确定即转述
- Created entity: 人物/尼采、人物/韦伯、人物/马克思、人物/鲁迅；著作/《论道德的谱系》、著作/《新教伦理与资本主义精神》
- Created concept: 概念/主人道德与奴隶道德、概念/新教伦理论题、概念/历史唯物主义、概念/国民性批判
- Created analysis: 分析/文化属性论的理论沿革谱系（六条谱系线证据分级）
- Updated（回填 develops 边+沿革章节）: 强势文化、弱势文化、文化属性、救世主情结、文化决定论论证
- Relations: +21条（authored_by/proposed_by/appears_in/develops/references）
- Facts(T2): 尼采平行判定、韦伯平行判定、马克思倒转判定、国民性批判承袭判定（4条，confidence 如实标注）
- Events(T4): 1859-政治经济学批判序言发表、1887-论道德的谱系出版、1904-新教伦理发表、1918-狂人日记发表
- Conflicts: none；修正上次遗留：神即道论证页自环 instance_of 边（仅 frontmatter，db 无）、蒂利希名误（詹姆斯→保罗）

## 2026-06-12 — ingest（《背叛》+《天幕红尘》，三部曲补全）
- Source: 来源/2026-06-12-背叛（OCR 扫描版 15章）、来源/2026-06-12-天幕红尘（OCR 版 51章）；引文全部 grep 逐字核验+章节定位核验
- Created entity: 著作/《背叛》、著作/《天幕红尘》
- Created concept: 概念/坦然、概念/输血与造血
- Created argument: 论证/道德熔点论证
- Created analysis: 分析/天道三部曲思想演化（内部演化弧：毁灭→孤独→殉道）
- Updated: 豆豆（+2 著作）、得救之道（+develops 输血与造血、三部曲演化节）、历史唯物主义（天幕红尘小说化阐释）
- Relations: +20条
- Facts(T2): 救世主情结三部曲首现判定、弱势文化诗化前身判定、历史唯物主义天幕红尘姿态判定（3条）
- Events(T4): 2013-天幕红尘出版
- Conflicts: none

## 2026-06-12 — deep-dive 第二轮（民主论节点 + 张力分析 + lint）
- Source: 引用 来源/2026-06-12-天幕红尘（民主论引文 7 条全部 grep 核验+章节定位）
- Created concept: 概念/民主的因果论（政治哲学首批）、概念/立场（豆子之喻/立场悖论）
- Created analysis: 分析/豆豆体系的内在张力（六张力：is-ought三级跳/决定论vs方法论/坦然vs无住/住因果相/外天道vs内自性/知场不免于场；steelman+反驳+裁决）
- Lint 修复: 清除首轮 28 条方向颠倒/互为重复的 frontmatter 边（著作→appears_in→概念、人物→authored_by→著作、互相 develops 等）；补写 26 条缺失正向边入 db；frontmatter↔db diff 清零
- Relations: +14 · Facts(T2): 六张力裁决（1条）
- Conflicts: none
