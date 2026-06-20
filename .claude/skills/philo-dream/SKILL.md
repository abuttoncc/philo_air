---
name: philo-dream
version: 0.1.0
description: |
  拾遗员 · 捕获泵：会话结束/夜间，把 Claude Code 对话里**会蒸发的 conviction**
  抽成 ≤5 条候选，落进 Inbox(捕获免费),交给 digest-inbox 晋升(晋升收紧)。
  这是飞轮缺的「进料口」—— 让知识库从日常对话自己长,而不是等人手喂。

  触发词：拾遗、捕获本场、capture session、philo-dream、把这次对话存下来、
  存入对话、夜间捕获、/philo-dream、留痕、别让这次对话蒸发。

  本 skill 不写 wiki 正典 —— 只产候选;晋升委托 digest-inbox + 08-Ops 信任闸。
  确定性层(读转写)走 capture.py;LLM 层(抽候选)是本 SKILL 的活。
---

# 拾遗员 · 捕获泵 (philo-dream)

> 用户说「捕获本场 / 把这次对话存下来」时触发,或被 launchd 夜间 headless 调起。
> 把一段会话里**值得长期记的判断**拾起来,落成 Inbox 候选,让它进入 `digest-inbox → wiki` 的既有管线。

**与 dpagt 的 Dream 同构(刻意为之)**：dpagt 后端的 `dream.py`「offline right-brain consolidation」读 finalized 对话→小 LLM「值得长期记吗」→≤5 候选→走 ingest 闸,**只写候选不写正典**。本 skill 是它在 philo_air(原型库)里的对等件。**在这儿先把它跑通、验准,再移植回 dpagt 的 Dream 调度器**——原型证明,产品照搬。

## 核心理念

- **降熵发生在「存入」之前先要有「捕获」**。digest-inbox 是把 Inbox 压成低熵存量的泵;但 Inbox 本身靠人手喂。拾遗员补的是更上游那一环:**把对话自动变成 Inbox 候选**。没有它,飞轮没有进料口,会话结束即蒸发(1.0 病)。
- **捕获免费、晋升收紧(陋居四原则)**。捕获要廉价、低摩擦、宁滥勿缺地落**候选层**(Inbox,未 `compiled`);晋升进 wiki 正典走 **既有信任闸**(digest-inbox 的 auto-wiki 纪律 + 08-Ops review)。**拾遗员一行正典都不写。**
- **产出收口**。LLM 抽的候选可能脏/脱靶——一律落候选,人/digest 复核才晋升。绝不直写 wiki、绝不退役、绝不合并数值。
- **选择性,不是录音机**。一场对话大半是工具拉扯、实现细节、元讨论;只拾**耐用的判断**(机制/立场/原则/决策),其余丢掉。见下「脱靶闸」。

## 脱靶闸(借 dpagt Dream 的 system prompt,kimi「脱靶」警告的现成防线)

候选**必须**同时满足:
1. **领域锚定**——落在本库某个域(metaphysics / epistemology / ethics / capital-allocation / product-philosophy)。**不是**工具调试 / Claude Code 用法 / 文件 file:line 接线 / 颜色像素 / ADR 编号这类实现噪声。
2. **耐用**——是个跨时仍成立的判断(T1 立场 / T2 论证或原则 / T3 实体关系),不是一句即时调侃。
3. **可溯源**——带 `source-session`(会话 id)+ 一句 `why-long-term`(为什么值得长期记)。

> 拿不准领域锚定与否 → **丢掉**(宁缺毋滥比污染候选层好)。本会话级的元讨论(怎么改 dpagt 代码、怎么接 /recall)正是该被丢的典型。

## 执行流程

### Step 0 — 读转写(确定性,走 capture.py)
- `python3 .claude/skills/philo-dream/capture.py --list` 看今天哪些会话、够不够实质(`user_turns ≥ 3`)、是否已捕获。
- 选目标会话 → `capture.py --dump <SID|latest>` 拿压实后的「人说+我说」对话文本。**这步零 LLM。**
- 被 launchd 调起时:`capture.py --check`(退出码 10=有待捕获才唤醒 LLM 层),再对每个未捕获会话 `--dump`。

### Step 1 — 抽候选(LLM,本 SKILL 的活)
通读 dump,抽 **≤5 条** conviction 候选。每条:
- **claim**:一句话把这个判断说清(人话,不是术语堆)。
- **why-long-term**:为什么这值得跨会话记(一句)。
- **candidate-domain**:猜它属哪个域(product-philosophy / capital-allocation / …)。
- **时间档提示**:T1 立场 / T2 原则·论证 / T3 实体关系(给 digest 的 ingest 当线索)。
- **连接提示**(可选):它该 `develops`/`grounds`/`references` 哪个已有节点(如「乔布斯心智模型网」)——给 digest 省力。
- 过**脱靶闸**;没满 5 条就少写,**绝不凑数**。

### Step 2 — 落候选(写 Inbox,一会话一文件)
写 `Inbox/conv_<date>_<topic-slug>.md`(对应 dpagt 的 `conv_*.md`),frontmatter:
```yaml
---
tags: [拾遗, capture-candidate]
type: conviction-candidate     # 注意:不是 capture(那会被 scan-inbox 跳过);不写 compiled,好让 digest 认领
created: <date>
source-session: <sid 前 8 位>
status: open
candidate-domains: [product-philosophy, capital-allocation]
---
```
正文 = ≤5 条候选,每条带 claim / why-long-term / 时间档 / 连接提示 + 一段对话原文摘录(溯源)。**这是候选不是定论**,正文首行写明「待 digest-inbox 分诊晋升」。

### Step 3 — 留痕(写 run 档,补上 §7 契约)
在 `08-Ops/runs/` 建 `type: run` 档(`routine: capture`):飞轮步进 + outputs(捕获 N 条候选去哪)+ budget + escalations。**交互被调起同样要建**——这正是 §7 说的「留痕是契约固定收尾步」。

### Step 4 — 记账防重(走 capture.py)
- `capture.py --mark <SID>` 把会话写进 `08-Ops/.capture-log.md`,下次 `--check` 不再重复捕获。
- 更新 `08-Ops/routines/拾遗员.md` 的 `last-run` / `last-result`。
- (可选)把「本次捕获 N 条候选」回写当天 `05-Daily/<date>.md`。

### Step 5 — 汇报
```
拾遗完成(as-of <date> · session <sid8>):
- 扫 <n> 会话 → 捕获 <m> 条候选 → Inbox/conv_<date>_<slug>.md
- 候选域:<product-philosophy ×k / capital-allocation ×j>
- 脱靶丢弃:<x 条实现噪声/元讨论>
- 下一步:跑 /digest-inbox 把候选分诊晋升(拾遗员不自己晋升)
```

## 防扩散与纪律

- **只产候选,不写正典**:wiki/data.db 一行不碰;晋升 100% 委托 digest-inbox + 08-Ops 闸。
- **≤5 条/会话**,宁缺毋滥;脱靶闸把实现噪声/元讨论挡在外面。
- **幂等**:`--mark` 过的会话不重复捕获;同会话重跑只在已有 conv 文件上补，不另起。
- **源 immutable**:候选是新文件,不动 transcript、不动既有 Inbox。
- **领域可空**:本库当前 5 域;材料若不锚定任何域 → 丢弃,不硬塞。

## 与其它 skill / 工具的关系

| 职责 | 委托给 |
|---|---|
| 读会话转写 / 压实 / 记账(确定性层) | 本 skill 的 `capture.py` |
| 抽候选(LLM 层) | 本 SKILL |
| 候选 → 分诊 → wiki(晋升) | `digest-inbox`(它再委托 `auto-wiki`) |
| 高危写入闸(newnode/xedge/retire/数值) | `08-Ops/审批账本.md` + review |
| 夜间触发(检测层) | launchd `com.philovault.philo-dream`(见同目录 plist) |
| 串进每日例行 | `daily-routine`(在「消化 Inbox」前插「拾遗」) |

## 陋居接线(08-Ops)

- 拾遗 = 飞轮的 stage ⓪(捕获),喂 stage ①(`分诊员`/digest-inbox)。在 CLAUDE.md §三 的生命周期里排在「①发散提问」之前。
- 收尾必建 run 档 + 更新 `拾遗员.md` 契约 last-run。无人值守(launchd)与交互被调起,**两模式都留痕**。
- 默认开关保守:launchd 先灰度(plist 默认装好不启,或只对本人账号),验候选质量一周再常开。
