# Philo Vault — 项目说明（给 Agent 读的指令文件）

Obsidian 个人哲学知识库，覆盖**理论哲学 + 实践哲学两大方向**（理论哲学是实践哲学的奠基层）。**两层架构**（与姊妹库 `valu_air` 同范式）：

- **PARA 工作层**（人写人看，按行动/时效组织）：散文式思考、阅读笔记、讨论记录、日记。
- **知识本体层 `wiki/`**（编译产物，按**领域 domain** 组织）：结构化本体，进 git、进 Obsidian 图谱。

**编译方向单向**：`Inbox(散文思考/讨论) → /auto-wiki ingest → wiki(结构化本体)`。wiki 只反向被 `recall` 消费，不反向生成 PARA 目录。**严谨用在已结晶的知识（wiki），不用在正在结晶的知识（Inbox）。**

> 权威真相源是每个领域的 `wiki/{domain}/_ontology.md`（v2 本体契约）。`ingest`/`recall` 前先读它。本文件是整库导航，本体细节以 `_ontology.md` 为准。

---

## 一、PARA 工作层 — 文件夹结构

| 文件夹 | 用途 |
|--------|------|
| `00-Dashboard/` | 仪表盘与导航 |
| `01-Projects/` | 活跃项目（如：读完某本书、写一篇论文式笔记） |
| `02-Areas/` | 持续关注的哲学领域 |
| `03-Resources/` | 参考资料（SEP 条目摘录、讲义、书单） |
| `04-Archive/` | 已完成/归档 |
| `05-Daily/` | 每日笔记 |
| `06-Templates/` | 模板（含研究笔记、读书笔记模板） |
| `08-Ops/` | **陋居自动化层**：agent 契约 / run 记录 / 审核队列 / 审批账本（详见第七节） |
| `09-Attachments/` | 附件（图片、PDF），编号 09 排在最后 |
| `Inbox/` | 收集箱：散文式思考、困惑、讨论记录、读书摘记，每条独立文件 |

这一层是「人写散文」的地方，不要求本体严谨。思考在 Inbox 用研究笔记模板写「困惑 / 目标 / 思路 / 线索」，讨论/阅读完成后用 `/auto-wiki ingest` 编译进 `wiki/`。

---

## 二、知识本体层 `wiki/` — auto-wiki v2 本体化系统

本仓库已安装 **auto-wiki** skill（知识编译器），引擎在 `.claude/skills/auto-wiki/`，脚本在其 `references/`（`schema.py` 校验 frontmatter、`store.py` 操作 `data.db`）。

### 按领域组织，不按课题

`wiki/` **按领域（domain）** 切分：`wiki/{domain}/`。**研究课题（topic）不单独建目录**，降级为该领域 `分析/` 下的一页（派生视图，删了不影响本体）。

### 两大方向 × 多域（扁平）+ 切换 + 拓展

库分 **理论哲学 / 实践哲学** 两个方向（`direction`）。**方向是 `meta.yaml` 的字段，不是目录层级**——域一律扁平并列在 `wiki/` 下，以免破坏 `wiki/{domain}/data.db` 路径假设与「图谱按节点类型着色」的规则。当前 3 个域：

| 方向 | 域 | 中心实体 | 说明 |
|---|---|---|---|
| 理论哲学 | `wiki/metaphysics/` | 实在 | 形而上学：存在、因果、心身、自由意志 |
| 理论哲学 | `wiki/epistemology/` | 知识 | 认识论：知识、信念、辩护、怀疑论 |
| 实践哲学 | `wiki/ethics/` | 道德 | 伦理学与政治哲学：规范、价值、正义 |

**切换（路由）**：`wiki/_index.md` 是**自动生成的域注册表**（扫所有 `meta.yaml` 的 `direction/hub/keywords` 生成）。**`ingest`/`recall` 第 0 步先读 `_index.md`**，按「路由关键词」把材料/问题命中到域；横跨多域则双写 + 跨域连边。**勿手改 `_index.md`**，改 `meta.yaml` 后重建。

**拓展（建新域）**：一条命令——
```
python .claude/skills/auto-wiki/references/new_domain.py <name> \
  --direction <方向> --central <中心实体> --hub <中文名> --desc "<范围>" \
  --types "类型1,类型2,..." --keywords "kw1,kw2,..." --validator none --coverage none
```
它克隆骨架、`store.py init` 建 data.db、写 meta/本体/Hub/log、重建 `_index.md`。**建完必须手填 `wiki/{name}/_ontology.md` 的类型判据表 + 受控关系词表，再 ingest**。只重建注册表用 `new_domain.py --reindex`。候选新域：`mind`（心灵哲学，若 AI 意识讨论变多可从 metaphysics 拆出）、`language`（语言哲学）、`aesthetics`（美学）。

**继承式本体**：引擎（schema.py/store.py/6 档/退役协议）是公共底座，**metaphysics 是本库参考母本**（声明哲学通用的节点类型与关系词表），epistemology/ethics 的 `_ontology.md` 只声明自己特有的增量。

**跨方向奠基边**：理论哲学不是孤岛，是实践哲学的上游。理论域用签名边 `grounds`（理论哲学节点 → 任意域节点，跨域）表达「形而上学/认识论立场 → 伦理/政治后果」（例：自由意志怀疑论 →grounds→ 道德责任）；**同一专名物（如康德）全库只建一次**，另一域连边引用（命名纪律：单一中文 slug 全库唯一）。

### 五个模式（按用户意图自动路由）

| 模式 | 触发 | 说明 |
|------|------|------|
| `recall` | 「打开 wiki」「根据积累回答」「之前讨论过」 | 加载 `wiki/{domain}/` 本体上下文，后续问题先查 wiki 再答 |
| `ingest` | 提供文件/大段文本，「编译」「整理这篇」「加进知识库」 | 读源材料 → 查 canonical 合并或建节点 → 写 6 档时间表 → 退役协议 → 校验 |
| `query` | 「wiki 里怎么说」「查查看」 | 单次从 wiki 取答案并综合 |
| `lint` | 「检查 wiki」「有没有矛盾」「健康度」 | 扫断链、越界关系边、矛盾、覆盖率 |
| `deep-dive` | 「深度研究」「查漏补缺」「上强度」 | 非独立模式 = `lint(Coverage)` 找缺口 + `ingest`(搜索填充) 的组合管道 |

路由：无新材料但提到 wiki/领域知识 → `recall`；提供了文件或大段文本 → `ingest`；说「上强度」→ `deep-dive`；不确定就问。**选哪个域**：先读 `wiki/_index.md` 按关键词命中（横跨多域则双写 + 跨域连边）。

### 节点类型与判据：实体（individual） vs 概念（class）

> **核心判据**：「能不能用手指指向『就是这一个』、明年用同名还指同一个东西？」
> 能 → **实体（individual）**；必须先讲一段「它怎么定义/怎么运作」才听得懂 → **概念（class）**。
> 哲学域易踩的坑：「电车难题」「中文房间」有具体场景描述，像实体——但它们是**有专名的论证/思想实验**，归 `论证/`；「功利主义」「物自体」必须先讲定义 → **概念**；「康德」「《纯粹理性批判》」「维也纳学圈」能指向就是这一个 → 实体。

节点类型（=目录=图谱着色），以 `wiki/metaphysics/` 为样板：

| 类型 | 子目录 | 例子 |
|---|---|---|
| 实体·人物 | `人物/` | 康德、亚里士多德、维特根斯坦 |
| 实体·学派 | `学派/` | 斯多亚学派、维也纳学圈、法兰克福学派 |
| 实体·著作 | `著作/` | 《纯粹理性批判》《正义论》 |
| 概念 | `概念/` | 自由意志、物自体、功利主义、心身问题（问题型概念，`classified_as` 问题） |
| 论证（有专名的论证/思想实验） | `论证/` | 电车难题、中文房间、葛梯尔反例、知识论证 |
| 事件 | `事件/` | 1781-纯粹理性批判出版、1929-达沃斯之辩 |
| 分析（研究课题=派生视图） | `分析/` | 自由意志与道德责任全景、AI 意识问题综述 |
| 来源 | `来源/` | SEP 条目摘录、播客访谈纪要、课程讲义 |

三分铁律：
- **数值绝不是节点** → 进 `data.db`（哲学域 T0 少，但如「PhilPapers 调查中物理主义支持率」这类调查数据进 `data_points`）。
- **关系是边不是页** → 「康德写了《纯粹理性批判》」是一条 `authored_by` 边。
- **分类标签是边不是页** → 大陆/分析、一元论/二元论、义务论/后果主义是贴在概念/人物上的 `classified_as` 边，可按它分桶着色，但不建页。

### 受控关系词表（关系是一等公民，但仍是边）

`type` 不许自由文本，从下表选，越界边被 `lint` 拒绝。双写：页面 `frontmatter.relations[]`（给 Obsidian 连边）+ `data.db relations 表`，两者一致。

`proposed_by`(概念/论证→人物) · `authored_by`(著作→人物) · `belongs_to`(人物→学派) · `appears_in`(概念/论证→著作) · `responds_to`(论证→概念[问题]) · `supports`/`critiques`(论证/人物→概念/论证) · `develops`(后继概念/人物→前驱概念) · `instance_of`(论证→概念) · `part_of`(概念→概念) · `classified_as`(→分类标签) · `created_by`/`changed_by`(→事件) · `grounds`(理论哲学节点→任意域节点，跨域签名边) · `references`(分析/来源→任意，只溯源)。

### 6 档时间模型 + 退役不删除

「时变 vs 永久」是一根变化速率连续轴，切成 6 档，每档记录方式不同：

| 档 | 是什么 | 哲学域的对应 | 记在哪 |
|---|---|---|---|
| **T0 观测值** | 某指标某时点一次测量 | PhilPapers 调查支持率、某书引用数 | `data_points` |
| **T1 状态/制度态** | 一段时间恒真、被有日期的事件切换的命题 | 「学界主流立场=物理主义」「我当前接受的立场=相容论」 | `facts` 拉链表 |
| **T2 耐用逻辑** | 跨时代论证/定义，可被反驳但不随日历变 | 论证页正文、概念定义 + `durability` 字段 |
| **T3 实体/近永久关系** | 客观存在物及本质归属 | 人物/著作/学派页 + `relations`（带时态） |
| **T4 事件** | 有日期+施动者、发生即固定 | 出版、讲座、论战、调查发布 | `events` 表/页，只增不改 |
| **T5 类型公理** | 约束「别的知识长什么样」 | `_ontology.md` + DB CHECK 约束 |

> 关键裁决：「我目前对自由意志的立场=相容论」是 **T1**（facts，立场会被某次讨论/某本书切换，切换必有 T4 事件盖章）；「弗兰克福案例反驳『可供取舍可能性原则』」是 **T2**（耐用论证）。两种物，记录方式必须不同。**个人立场变化是这个库最有价值的时间序列——立场切换永不删旧行。**

**退役不删除**：覆盖原值只允许在 T0 同 period 纠错；跨到 T1/T2/T3 的任何「变化」都是「旧行封 `valid_to` + 插新行」，**永不 DELETE**。每条断言双时态：`valid_from/valid_to`（何时为真/何时持有）+ `recorded_at`（哪次讨论/哪本书记的），两轴绝不混。一切当前态（T1/T2）的改变必须追溯到一个 T4 事件页（`caused_by_event`，事件盖章）。

### data.db（每领域一个，双时态）

每领域一个 `data.db`（SQLite，由 `store.py` 操作）。核心表：`data_points`(T0) / `facts`(T1+T2 拉链) / `events`(T4 append-only) / `relations`(T3 带时态)。

**命名纪律**：**单一中文 slug = 文件名 = `[[wikilink]]` = `data.db` 主键**。不另起英文 id。著作用书名号《》开头命名；跨译名去重靠 `aliases:` 字段（维特根斯坦=Wittgenstein、《纯批》=《纯粹理性批判》）。

### 校验器

本库 `meta.yaml` 里 `validator: none`（FIBO 是金融本体，不适用哲学域）。`lint` 只做引擎内置校验：断链、越界关系边、矛盾、覆盖率。未来若接入哲学本体 MCP（如 InPhO），再按域改 `validator` 字段。

### 可视化与图谱

`schema.py --report` 生成 `wiki/{domain}/_report.html`（图谱按节点类型着色；若存在 `_positions.json` 则默认**校准布局**——y=本体抽象层级、x=拉普拉斯谱坐标，由 `position_encoding.py` 重算，可一键切回力导向）。Obsidian Graph 指向 `wiki/` 看本体；颜色按 `path:人物/` 等着色，`graph.json` 别放 `path:wiki` catch-all 灰色规则（会盖掉所有颜色）。

---

## 三、编译生命周期（知识看板如何形成）

① **发散提问**：在 Inbox 用研究笔记模板写「困惑/目标/思路/线索」。
② **研究发散**：读原典/SEP/讲义/播客，或直接与 Agent 对谈，边讨论边记。
③ **编译（ingest）**：读源材料 → 先查 canonical（含 aliases）合并 or 按决策树建节点 → 给每条知识定 6 档时间档写对应表 → 补受控关系边 → 走退役协议 → 研究综述落 `分析/` → 更新 Hub（`{hub}.md`）+ `log.md` → 跑 `schema.py` 校验 → 刷新位置编码（`position_encoding.py` + `--report`）。
④ **新知识看板**：编译产物 = `wiki/{domain}/` 本体（节点 + data.db + 关系），在 Obsidian Graph / `_report.html` 呈现为「中心实体辐射的知识网」；后续 `recall` 站在它上面继续讨论。

### Agent ingest 操作清单

0. **先读 `wiki/_index.md` 注册表，按关键词把材料命中到域**（横跨 理论/实践 多域则双写 + 跨域 `grounds`/`references` 连边）。
1. 读 SKILL.md：`.claude/skills/auto-wiki/SKILL.md`；按操作加载对应 reference（ingest → ingest-protocol.md）。
2. 先读目标领域 `wiki/{domain}/_ontology.md`（本体契约）+ Hub 页。
3. 逐项抽名词 → 查现有页（含 aliases）→ 已存在则合并/按退役协议更新 data.db；不存在则走分类决策树定类型建页。
4. 按 6 档时间档写对应表；补/退役受控关系边。
5. 综述落 `分析/` + 更新 Hub + 追加 `log.md` + 跑 `schema.py` 校验。
6. 刷新位置编码：`python references/position_encoding.py wiki/{domain}` + `schema.py --report`。

---

## 四、取材通道

本库**不接金融 MCP**（`.mcp.json` 留空）。哲学材料取材通道：

| 通道 | 用途 |
|------|------|
| `web`（WebSearch / 网页阅读） | SEP（Stanford Encyclopedia of Philosophy，首选权威源）、IEP、PhilPapers |
| **原典源仓**（`ref/text-sources.md`） | 已验证的 GitHub 原典全文仓清单（毛选/金刚经等），含 curl 拉取模式与核验锚——需要原典全文时**先查此清单**再自行探索 |
| 用户提供 | 原典片段、读书摘记、课程讲义、播客文字稿 |
| 与 Agent 对谈 | 苏格拉底式讨论本身就是源材料：讨论记录落 `Inbox/`，结晶后 ingest |

> **讨论即研究**：这个库的特色工作流是「用户与 Agent 就某哲学问题对谈 → 对谈中的论证、立场、引用落 Inbox → `/digest-inbox` 或 `/auto-wiki ingest` 编译进 wiki」。Agent 在讨论中应主动充当「严肃的对话者」：给出最强反驳（steelman）、追问前提、标注哪些断言值得进 wiki。溯源记「作者+著作+章节」，网络来源记「标题+站点+日期」。

---

## 五、同步约定

- **`.claude/`（skill 引擎）+ `wiki/`（本体）都进 git**，别人 pull 即得。仅 `.claude/settings.local.json` 排除（个人本机设置）。
- `wiki/` **必须可见**（不是 `.wiki/` dotfolder——Obsidian 隐藏 dot 开头目录，dotfolder 不会进图谱），进 git，出现在 Obsidian Graph。skill 一律称 `auto-wiki`。
- `obsidian-git` 自动提交与推送（备份）。运行产物 `data.db-wal/-shm` 不入库。

---

## 六、每日例行任务（07-QA 问答库）

`07-QA/` 是**问答库**：一组站着不动的问题，动态问题（`mode: dynamic`）的答案是**时间序列**（append-only，每次站在 `as-of=今天` 重答、旧答案不删）。

哲学库的动态问题形如：「我当前对 X 的立场是什么、为什么、和上次比变了没有」——立场的演化轨迹本身就是这个库的核心产出。

**触发**：用户说「**执行今日例行任务**」（或"今日例行/跑问答库"）→ 调用 `daily-routine` skill（`.claude/skills/daily-routine/`）。它扫 `07-QA/` 挑出到期的动态问题，对每个跑：
`recall(加载 wiki 本体) → 复盘(上次立场) → 推演(当前立场+一句话理由) → 建立连接 → lint 缺口检测 → 缺口则 deep-dive 外部获取并 ingest 回 wiki → 追加答案 → 回写 Daily`。

**答案 append 不覆盖；ingest 守退役不删除协议。**

---

## 七、陋居自动化层（08-Ops）

> 蓝图：`ref/burrow-workspace-blueprint.md`。隐喻：陋居（The Burrow）——人做深度思考与全局掌控，「当 X 发生 → 做 Y」的模式化劳动交给受契约约束的 agent（routine）。

在库的 8 条不变量之上加四条原则：**产出收口**（无人值守 agent 不直写高危正典，只投递候选）· **捕获免费、晋升收紧** · **连续批准升级 · 一次驳回降级**（审批账本）· **确定性优先**（能纯代码绝不用 LLM）。

| 落点 | 内容 |
|---|---|
| `08-Ops/routines/` | agent 契约注册表（分诊员/答题员/研究员/结构巡检员/编译裁决员），契约 = trigger/scope/budget/escalation，**改契约 = 改权限** |
| `08-Ops/runs/` | 无人值守 run 记录：开跑建档（status: running）、结束补全飞轮步进/产出/预算 |
| `08-Ops/review/` | 审核队列：高危写入候选卡（pending → approved/rejected/contested） |
| `08-Ops/审批账本.md` | 信任账本：每类写入 streak/threshold/state + append-only 审计日志 |

**高危写入 gate**：`newnode`(新建节点) / `xedge`(跨域 grounds 边) / `t0-merge`(verified 数值合并) 可通过连续批准升为自动批准；`retire`(退役触发) 与 `disputed`(数值分歧) **永久人工**。规则：连续 threshold 次批准零驳回 → `state: auto`（无人值守可直写但仍记账）；**一次驳回 streak 清零**、已 auto 降级。

**模式区分**：交互会话 = 高危写入当场问用户，**裁决即记账**；无人值守（launchd，本库暂未接定时器；接线后同规则生效）= 非 auto gate 一律落 `review/` 候选。

**触发语**：「**处理审核队列**」→ 读全部 pending 候选 → 逐张报卡（gate + diff + 来源 + 审批账本上下文）→ 按用户裁决三步走：执行写入（退役走六步）/ 翻转卡片 status / 审批记账。

**Dashboard**（00-Dashboard，按例外优先级排）：北极星条 → Agent 状态钟 + Agent 清单 → 审核队列 → 运行轨迹 → 审批账本 → QA 时间线。答题员答完每题把一句话结论回写 QA frontmatter `last-summary` 供时间线读取。
