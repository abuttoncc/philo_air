# 产品哲学领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-06-13
- 域创建（new_domain.py 脚手架）。待首次 ingest。

## 2026-06-13 — 首次 ingest（域奠基）
- Source: 来源/2026-06-13-乔布斯-GitHub技能笔记（二手·双仓提炼，原文留存 Inbox）
- Created: 26 页 — 人物 5 / 公司 1 / 著作 2 / 概念 11 / 案例 1 / 事件 4 / 分析 1 / 来源 1
- data.db: data_points 4（产品线 350→10、Mac 团队、iPhone 周期）；facts 6（T2 核心命题+局限条款）；events 4；relations 35
- 防扩散：表达 DNA / Agentic 工作流 / 完整时间线不本体化（留 Inbox）；Tim Cook/Jony Ive/铃木俊隆等仅叙事；跨域 grounds 边（应无所住→连点成线 等）仅列候选未写入
- Conflicts: none

## 2026-06-13 — deep-dive：印度之行与禅修考证
- Source: 来源/2026-06-13-乔布斯禅修考证-Web调研（二手·权威，Isaacson 引文多源核验）
- Created: 4 页 — 事件/1974-乔布斯印度之行、概念/直觉优于智识、分析/乔布斯禅修与思想定型考、来源 1
- Revised: 人物/史蒂夫·乔布斯（印度线/禅线拆分）、人物/乙川弘文（关系细节 confidence→high）；metaphysics/应无所住 grounds 边证据加固
- data.db: data_points +2（verified）；facts +4（含「性质判定：非佛教闭关」「思想定型分期」）；events +1；relations +9
- 前提修正: 「印度佛教闭关修炼」不成立——印度教朝圣（扑空）与日本曹洞禅（回美后）是两条线
- Conflicts: none

## 2026-06-14 — ingest：乔布斯产品哲学 → 智能体工作区 3.0 映射
- Source: 来源/2026-06-14-乔布斯设计原则-anysearch调研（二手·anysearch 联网多源；NYT 2003 / WWDC 1997 / 2011 iCloud）
- Created: 3 页 — 概念/设计即如何运作、来源 1、分析/乔布斯产品哲学映射智能体工作区3.0
- data.db: facts +1（设计即如何运作核心命题，T2 durable）；relations +8（概念 proposed_by/part_of 2 + 分析 references 6）
- 防扩散: 「智能体工作区 3.0」**不本体化**（用户工具/项目，非哲学知识）——留项目记忆 + 分析页派生视图；「极简/It just works」归入既有 [[聚焦即说不]]/[[隐形工艺]]，不另建概念；无跨域 grounds 边（3.0 非他域节点）
- 审批: newnode 7→8（交互会话，用户指令「b」即裁决）
- Conflicts: none

## 2026-06-14 — ingest：App Store 发布史补厚 + 去孤儿（expand 驱动）
- 触发: expand.py 查出 [[2008-App-Store开放]] 为孤儿节点（0 邻居）；用户问"哪款机器/何时开发者涌入"
- Source: 来源/2026-06-14-AppStore发布史-anysearch调研（二手·权威，命中 Apple Newsroom 一手新闻稿）
- Revised: 事件/2008-App-Store开放（机器=iPhone 3G 2008-07-11；SDK 2008-03-06；设计理念=受控的开放）
- Created: 来源 1
- data.db: data_points +4（SDK 10万/首发 500/首周 1000万/累计 10亿，verified）；relations +2（聚焦即说不、端到端控制 →changed_by→ 事件，**去孤儿**）
- 防扩散: iPhone 3G 不建节点（设备，留事件正文）；不另建 SDK 事件（并入本事件 + T0）
- 审批: newnode 8→9（来源 1；交互会话，用户指令「a」+ 提问即裁决）；T0 为新增 verified 非合并、edges 为域内非 xedge
- Conflicts: none

## 2026-06-14 — 乔布斯心智模型横向织入（enables，scan 驱动）
- 触发: expand --scan（改进版）报乔布斯簇 12 概念"可富化"（part_of 已归位、缺横向思想边）；用户指令"用 enables 织乔布斯那簇"
- Created: 0 页（纯织边）
- data.db: relations +6（死亡过滤器→聚焦即说不、聚焦即说不→隐形工艺/一句话定义、A级人才密度→隐形工艺、端到端控制→设计即如何运作、科技与人文交汇→从用户体验倒推，皆 enables）
- 纪律: 6 边皆有概念页内容依据（Rock Tumbler/It just works/从理解出发设计…）；现实扭曲力场/直觉优于智识（依据偏薄）、销售驱动腐化（反模式）**留可富化池不硬织**
- 复验: scan 可富化 15→6，掉出的 9 个正是所织概念 → 闭环自洽
- Conflicts: none
