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

## 2026-06-15 — 事件去孤儿（exemplifies 放宽，evidences 决策落地为"复用"）
- 决策: evidences 缺口选项 A —— 放宽 `exemplifies` 从「案例→概念」到「**案例/事件**→概念」，不新增词类（母本…本域 _ontology 同步）
- data.db: relations +4（1997-回归→聚焦即说不、2007-iPhone→一句话定义、2005-演讲→连点成线/死亡过滤器，皆 exemplifies）
- 复验: scan 孤儿 4→0（product-philosophy 3 事件去孤儿）；皆有事件页内容依据（"奠基性实证"/"教科书演示"/三个故事）
- Conflicts: none

## 2026-06-17 — ingest：固收工具产品原型设计实践复盘（新话题）
- Source: 来源/2026-06-17-固收工具产品设计对谈（讨论纪要；HTML 原型存库外 ~/Documents/fixed-income-cockpit）
- 裁决: 注册表第 0 步命中既有 product-philosophy → **不建新域**（避免与"产品设计"重复）；话题落 分析/，概念落 概念/
- Created: 9 页 — 概念 5（渐进式披露/图主导/磁力对齐/影响前后呈现/不可替代性拷问）· 案例 1（固收资产过程管理工具）· 分析 1（固收工具原型设计实践复盘）· 事件 1（2026-06-16-固收工具四方红队评审）· 来源 1
- Revised: 分析/乔布斯产品哲学映射智能体工作区3.0（+「控制面投影范式」段：投影范式从图谱搬到债券组合）—— 控制面投影并入此页，不单独建概念
- data.db: facts +4（案例决策序列 T1：MVP优先级/目标口径/主视觉/信息架构范式，1 条 caused_by 红队事件）· events +1 · relations +28（exemplifies 5 + changed_by 1 + develops 5 + part_of 5 + references 12）
- 接入乔布斯网络: 渐进式披露→隐形工艺、图主导→设计即如何运作、影响前后呈现/磁力对齐→从用户体验倒推、不可替代性拷问→死亡过滤器（皆 develops）
- 防扩散: 数据时效悖论/主动vs被动偏离/三套色分离/操作从左到右 留复盘正文，不单独建概念（用户选「精选核心6」→实建 5 + 控制面投影并页）
- 审批: newnode（交互会话，用户 AskUserQuestion 裁决"精选核心6个"+"控制面投影并入3.0分析"即批准）
- Conflicts: none

## 2026-06-17 — lint（结构档）：固收复盘 ingest 后体检
- 范围: product-philosophy 全域（43 页 < 50，全量）
- Validation: schema 全过（来源页 source_type 讨论→一手 已修）
- Broken Link: 0（新增/修改页 wikilink 全解析）
- Orphan: 0 真洞；新概念/案例/分析 deg 4–8，已接入乔布斯网络
- 治理: 红队事件原 deg=1 挂件 → 补 exemplifies→不可替代性拷问（事件实证该原则，沿 2026-06-15 放宽）→ relations 92→93
- 越界关系边: 0（exemplifies/develops/references/changed_by/part_of 皆受控词）
- 残留: 来源页 deg=1（source 天然叶子，正常，不强织）
- 健康度: 良好
- Conflicts: none

## 2026-06-21 — digest-inbox：AbleMind 三候选结晶（飞轮/护城河/多模型护城河）
- Source: Inbox/conv_2026-06-20_ablemind飞轮 + conv_2026-06-21_ablemind护城河 + conv_2026-06-21_ablemind多模型护城河（三场讨论记录，互引、同锚母题 [[AbleMind 的一句话定位]]）
- Created: 1 页 — 分析/AbleMind护城河与飞轮分析（派生视图，跨域 capital-allocation；AbleMind/3.0 工作区防扩散不本体化）
- relations: 6 条 references（→竞争优势模式[跨域]/不可替代性拷问/死亡过滤器/隐形工艺/设计即如何运作/乔布斯产品哲学映射智能体工作区3.0）
- 防扩散：通用概念（先发优势 / 多模型=生存基底 / 累积型护城河）作 newnode 候选报人工裁决，未自动建节点
- Validation: schema 44/44 PASSED；Broken Link 0（跨域 references 解析正常）
- Conflicts: none
