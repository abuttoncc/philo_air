---
title: 原典文本源仓清单
type: reference
created: 2026-06-12
updated: 2026-06-13
tags: [ref, text-sources, ingest]
---

# 原典文本源仓清单（供自动探索时临时拉取）

> 用途：deep-dive / ingest / 答题员 routine 需要原典全文时，按本清单 `curl` 临时拉取到 `Inbox/`。
> 纪律：① 拉取后必须做完整性核验（见每条的「核验锚」——grep 关键句确认非 404/残本）；
> ② 临时拉取的文件用完按需决定去留，正式 ingest 的留 `Inbox/` 进 git；
> ③ raw URL 模式：`https://raw.githubusercontent.com/{owner}/{repo}/master/{path}`，中文路径直接放引号内即可。

## 已验证可用（2026-06-12 实测）

### 毛泽东选集（Markdown，逐篇独立文件）
- **仓库**: https://github.com/weiyinfu/MaoZeDongAnthology
- 拉取模式:
  ```bash
  curl -sL "https://raw.githubusercontent.com/weiyinfu/MaoZeDongAnthology/master/src/016-实践论.md" -o Inbox/实践论.md
  curl -sL "https://raw.githubusercontent.com/weiyinfu/MaoZeDongAnthology/master/src/017-矛盾论.md" -o Inbox/矛盾论.md
  ```
- 篇目索引: `src/` 下按 `NNN-篇名.md` 编号，覆盖毛选全卷（目录可浏览仓库 src/ 列表按需取篇）
- 核验锚: 实践论→"你要有知识，你就得参加变革现实的实践"；矛盾论→"矛盾的普遍性"（应 20+ 次命中）
- 已拉取: `Inbox/实践论.md`（32KB）、`Inbox/矛盾论.md`（81KB），2026-06-12 核验通过；**已 ingest**（epistemology，2026-06-12）
- **备用镜像**: https://github.com/echonoshy/Maozedong-xuanji （同样的 `016-实践论.md` / `017-矛盾论.md` 命名）

### 《金刚经》（鸠摩罗什译本，三十二分品，Markdown）
- **仓库**: https://github.com/HanYouyang/Diamond-Sutra
- 拉取模式:
  ```bash
  curl -sL "https://raw.githubusercontent.com/HanYouyang/Diamond-Sutra/master/《金刚经》.md" -o Inbox/金刚经.md
  ```
- 同仓还有: 中英对照、讲记等多版本 .md
- 核验锚: "凡所有相，皆是虚妄。若见诸相非相，即见如来"（[[见路不走]]引文升级的目标原句）
- 已拉取: `Inbox/金刚经.md`（20KB），2026-06-12 核验通过；**已 ingest**（metaphysics，2026-06-12）
- **辅助仓**（解读，非原典，引用时注意 source_type 降为 二手）:
  - https://github.com/gitlore/jin-gang-jing （南怀瑾相关）
  - https://github.com/vinjn/diamond-sutra-101 （解读版）

### 《改造我们的学习》（毛选，同上仓）
- 路径: `src/059-改造我们的学习.md`；核验锚: ""实事"就是客观存在着的一切事物"
- 已拉取: `Inbox/改造我们的学习.md`（16KB），2026-06-12 核验通过；**已 ingest**（epistemology）

### 《坛经》（宗宝本，LaTeX 源）
- **仓库**: https://github.com/YinJC/TanJing （TanJing.tex，216KB，简体宗宝本+编者白话译文）
- 处理: 无干净 md 仓；从 .tex 剥离 LaTeX 标记得纯文本（脚本见 run 档案）；引用仅取经文原文段
- 核验锚: "应无所住而生其心"（行由品开悟段）、"无念为宗，无相为体，无住为本"（定慧品）
- 已拉取: `Inbox/坛经.md`（71K字，十品完整），2026-06-12 核验通过；**已 ingest**（metaphysics）
- 探索副产物: GitHub 搜"坛经/六祖坛经"无干净原典 md 仓（多为讲记/录音稿，2026-06-12 结论）

### 投资经典读书笔记（二手，非原典——引用时 source_type 一律标 二手）
- **仓库**: https://github.com/ketanarlulkar/Book_Summaries （多本投资/商业书的结构化笔记）
- **辅助仓**: https://github.com/ever-works/awesome-startup-books （details/ 下按书逐篇详细总结）
- 拉取模式:
  ```bash
  curl -sL "https://raw.githubusercontent.com/ketanarlulkar/Book_Summaries/master/The_OUTSIDERS.md" -o Inbox/xxx.md
  curl -sL "https://raw.githubusercontent.com/ever-works/awesome-startup-books/master/details/the-outsiders.md" -o Inbox/xxx.md
  ```
- 核验锚: The Outsiders→"Singleton"/"Murphy"；Quality Investing→"capital allocation"
- 已拉取（2026-06-13 核验通过；**已 ingest**，capital-allocation 域奠基，2026-06-13）:
  - `Inbox/The Outsiders（局外人）最佳笔记.md`（13KB，双源合并：资本配置五选项 + Outsider Checklist + 8 位 CEO 案例）
  - `Inbox/Quality Investing（高质量投资）最佳笔记.md`（48KB，Building Blocks / Competitive Advantage / Pitfalls / Implementation）

### 乔布斯思维框架（二手提炼，Skill 形态）
- **主仓**: https://github.com/alchaincyf/steve-jobs-skill （SKILL.md，27KB：6 心智模型 + 8 决策启发式 + 表达 DNA，基于 Isaacson 传记/Stanford 演讲/Lost Interview 提炼）
- **辅助仓**: https://github.com/K-Dense-AI/mimeographs （注意路径双层：`mimeographs/steve-jobs/SKILL.md` + `AGENTS.md`，默认分支 main）
- **一手档案**（未拉取，在线阅读）: https://book.stevejobsarchive.com/ （Make Something Wonderful，官方演讲/邮件档案——升级引文 confidence 时用这里）
- 核验锚: 主仓→"聚焦/说不/现实扭曲"；mimeographs→"craftsmanship"
- 已拉取: `Inbox/乔布斯产品设计思维（Steve Jobs）最佳资料.md`（51KB，三仓合并+用户资料地图），2026-06-13 核验通过；**已 ingest**（product-philosophy 域奠基，2026-06-13）

## 已知不可得（避免重复探索浪费）

- **韦伯《中国的宗教：儒教与道教》**: GitHub 无干净全文 md/txt 主仓（多为 PDF 或片段，2026-06-12 探索结论）。
  路径：等用户提供 PDF 转换，或按商务印书馆王容芬译本做定点摘录（对勘只需结论章"儒教与清教"）。

## 候选探索方向（未验证，自动探索时可先试这些关键词）

| 目标文本 | 对应 wiki 缺口 | 探索关键词 |
|---|---|---|
| 《道德经》全文（王弼本） | [[道法自然]]原典充实 | `github 道德经 markdown`（此类仓库极多，注意选带章节号的） |
| 《坛经》 | 佛学谱系线（五台山论道背景） | `github 六祖坛经 markdown` |
| 龙树《中论》 | [[自指反驳论证]]"去二着一"语汇 | `github 中论 鸠摩罗什 txt` |
| 鲁迅全集（阿Q正传/狂人日记/娜拉走后怎样） | [[国民性批判]]原典充实 | `github 鲁迅全集 markdown` |
| 马克思《关于费尔巴哈的提纲》《〈政治经济学批判〉序言》 | [[历史唯物主义]]原典充实 | `github 马克思恩格斯选集 markdown` |
| 《卡拉马佐夫兄弟》宗教大法官章 | [[救世主情结]]西方对勘 | 中译本版权敏感，优先找公版英译或片段 |

## 拉取后的标准动作

1. `file`/`head` 看编码（GitHub raw 一般已是 UTF-8；本地书源常是 GB18030，需转码）。
2. grep 核验锚句 → 记录到本页「已拉取」行。
3. 正式编译走 auto-wiki ingest 协议（来源页标 source_type: 一手 + 版本/译本注记）。
