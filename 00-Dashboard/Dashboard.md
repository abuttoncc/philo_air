---
cssclasses:
  - dashboard
  - hlb
  - hide-all
---

> [!abstract]
> ```dataviewjs
> const h = new Date().getHours();
> const period = h < 6 ? "深夜好" : h < 12 ? "早上好" : h < 18 ? "下午好" : "晚上好";
> const date = dv.date("today").toFormat("yyyy.MM.dd EEEE");
> const skip = p => !p.file.path.startsWith("00-Dashboard") && !p.file.path.startsWith("06-Templates") && !p.file.path.startsWith("09-Attachments") && !p.file.path.startsWith(".");
> const all = dv.pages().where(skip);
> const para = all.where(p => !p.file.path.startsWith("wiki/"));
> const ib = dv.pages('"Inbox"').where(p => p.file.name !== "README" && p.file.name !== "plan" && p.compiled !== true).length;
> const pj = dv.pages('"01-Projects"').where(p => p.status === "active").length;
> const op = para.file.tasks.where(t => !t.completed).length;
> const dn = para.file.tasks.where(t => t.completed).length;
> const pct = (op + dn) > 0 ? Math.round(dn / (op + dn) * 100) : 0;
> const ORDER = ["人物","学派","著作","概念","论证","事件","分析","来源"];
> const HUBS = new Set(["形而上学","认识论","伦理学"]);
> const nodes = dv.pages('"wiki"').where(p => p.type && p.type != "ontology" && p.type != "registry" && !p.file.name.startsWith("_") && !HUBS.has(p.file.name) && p.file.name != "log");
> const cnt = {}; for (const p of nodes) { const s = p.file.folder.split("/").pop(); cnt[s] = (cnt[s]||0)+1; }
> const LABELS = new Set(["问题","应用议题","义务论","后果主义","美德伦理","一元论","二元论"]);
> const contested = nodes.where(p => p.confidence == "contested" || p.confidence == "low").length;
> const noSrc = nodes.where(p => p.type != "source" && (!p.sources || p.sources.length == 0)).length;
> const orphan = nodes.where(p => p.type != "source" && p.type != "analysis" && p.file.inlinks.length == 0).length;
> let broken = 0; for (const p of nodes) { for (const l of (p.file.outlinks || [])) { if (!l.path) continue; const nm = l.path.split("/").pop().replace(/\.md$/, ""); if (LABELS.has(nm)) continue; if (!dv.page(l.path)) broken++; } }
> const ok = (contested + noSrc + orphan + broken) == 0;
> const stat = (v, l) => `<div class="hlb-stat"><b>${v}</b><span>${l}</span></div>`;
> const types = ORDER.filter(k => cnt[k]).map(k => `<span class="ht">${k}<b>${cnt[k]}</b></span>`).join("");
> const health = ok ? "健康 · 无断链 / 孤儿 / 争议" : "待治理 " + (contested+noSrc+orphan+broken);
> const root = dv.el("div", ""); root.className = "hlb-hero";
> root.innerHTML = `<div class="hlb-hero-main"><span class="hlb-badge">KNOWLEDGE BASE</span><h1>PHILO <em>VAULT</em></h1><div class="hlb-greet">${period} · ${date}</div></div>`
>   + `<div class="hlb-hero-mid"><div class="hlb-mid-lbl">哲学本体 · 当前构成（全域合计）</div><div class="hlb-types">${types}</div><span class="hlb-badge2 ${ok ? "ok" : "warn"}">${health}</span></div>`
>   + `<div class="hlb-hero-stats">${stat(nodes.length,"本体节点")}${stat(para.length,"笔记")}${stat(ib,"待消化")}${stat(op,"待办")}${stat(pj,"项目")}${stat(pct+"%","完成")}</div>`;
> ```
> <span class="hlb-flow"><em>信息流</em> `0 待消化` → `1 发散` → `2 行动` → `3 编译` → `4 看板`</span>[[wiki/metaphysics/形而上学|形而上学]] · [[wiki/epistemology/认识论|认识论]] · [[wiki/ethics/伦理学|伦理学]] · [[01-Projects/|项目]] · [[05-Daily/|日记]] · [[Inbox/README|收集箱]] · [[00-Dashboard/MOC|MOC]]

> [!note] 1 发散 · INBOX
> ```dataview
> TABLE WITHOUT ID file.link AS 思考专题, choice(compiled, "✅", "🔴") AS 消化, triage AS 分诊, status AS 状态
> FROM "Inbox"
> WHERE file.name != "README" AND file.name != "plan"
> SORT compiled ASC, created ASC
> ```

> [!warning] 0 待消化 · 领先指标
> ```dataviewjs
> const pend = dv.pages('"Inbox"').where(p => p.file.name !== "README" && p.file.name !== "plan" && p.compiled !== true);
> const n = pend.length;
> let oldest = -1, oldestName = "";
> for (const p of pend) {
>   if (!p.created) continue;
>   const c = (typeof p.created === "string") ? dv.date(p.created) : p.created;
>   const d = Math.floor(dv.date("today").diff(c, "days").days);
>   if (d > oldest) { oldest = d; oldestName = p.file.name; }
> }
> if (n === 0) { dv.paragraph("✅ **收集箱已排空** —— 无未消化项，泵跟上了进料。"); }
> else {
>   const urgent = (oldest >= 3 || n >= 5);
>   dv.paragraph(`${urgent ? "🔴" : "🟡"} **${n}** 篇待消化 · 最老 **${oldest}** 天（${oldestName}）`);
>   dv.paragraph("→ 跑 `/digest-inbox` 排空；这两个数往上走 = 进料超过消化，熵在赢。");
> }
> ```

> [!example] ⚡ 控制台 · CONSOLE
> ```dataviewjs
> // 一键唤起 Claude 跑 skill。优先 terminal 插件集成终端（cmdId）；没加载到就回退弹 Terminal.app。
> try {
>   const ACTIONS = [
>     { label: "🧹 消化 Inbox", cmd: "/digest-inbox",  cmdId: "terminal:open-terminal.claudeDigest.root",            desc: "扫散文 → 编译进 wiki → 打 compiled 标记" },
>     { label: "🔁 今日例行",   cmd: "/daily-routine", cmdId: "terminal:open-terminal.claudeRoutine.root",           desc: "跑 07-QA 动态问答库并回写 Daily" },
>     { label: "⌨️ 终端",       cmd: "",               cmdId: "terminal:open-terminal.darwinIntegratedDefault.root", desc: "在库根开一个空的集成终端" },
>   ];
>   const CLAUDE = "/Users/jameslee/.local/bin/claude";
>   const ad = app.vault.adapter;
>   const vault = ad.getBasePath ? ad.getBasePath() : ad.basePath;
>   const run = (a) => {
>     const reg = app.commands && app.commands.commands;
>     if (a.cmdId && reg && reg[a.cmdId]) {
>       app.commands.executeCommandById(a.cmdId);
>       new Notice("集成终端 · " + (a.cmd || "shell"));
>       return;
>     }
>     try {
>       const { spawn } = require("child_process");
>       const sh = a.cmd ? `cd '${vault}' && ${CLAUDE} '${a.cmd}'` : `cd '${vault}' && ${CLAUDE}`;
>       spawn("osascript", ["-e", `tell application "Terminal" to do script "${sh}"`, "-e", 'tell application "Terminal" to activate']);
>       new Notice("外部终端 · " + (a.cmd || "shell") + "（集成 profile 未加载，重启 Obsidian 后启用）");
>     } catch (e) { new Notice("启动失败：" + (e && e.message || e)); }
>   };
>   const bar = dv.el("div", "");
>   bar.style.cssText = "display:flex;flex-wrap:wrap;gap:8px;margin:6px 0";
>   for (const a of ACTIONS) {
>     const b = bar.createEl("button", { text: a.label, attr: { title: a.desc } });
>     b.style.cssText = "cursor:pointer;padding:6px 14px;border-radius:8px;border:1px solid var(--background-modifier-border);background:var(--interactive-normal);font-size:13px;font-weight:500";
>     b.addEventListener("mouseenter", () => { b.style.background = "var(--interactive-hover)"; });
>     b.addEventListener("mouseleave", () => { b.style.background = "var(--interactive-normal)"; });
>     b.addEventListener("click", () => run(a));
>   }
>   dv.el("div", "点击 = 在集成终端（或回退弹 Terminal.app）发起命令；进度、合并守闸、权限确认都在终端里答。", { attr: { style: "font-size:11px;color:var(--text-muted);margin-top:2px" } });
> } catch (e) {
>   dv.paragraph("⚠️ CONSOLE 渲染失败：" + (e && e.message || e));
> }
> ```

> [!todo] 2 行动 · 待办
> **今日**
> ```dataviewjs
> const todayStr = dv.date("today").toFormat("yyyy-MM-dd");
> const page = dv.page("05-Daily/" + todayStr) || dv.page(todayStr);
> const open = page ? (page.file.tasks || []).filter(t => !t.completed) : [];
> if (page && open.length > 0) { dv.taskList(open, false); }
> else if (page) { dv.paragraph("今日已清空"); }
> else { dv.paragraph("还没有今天的日记"); }
> ```
> **活跃项目**
> ```dataview
> TABLE WITHOUT ID file.link AS 项目, due-date AS 截止
> FROM "01-Projects"
> WHERE status = "active"
> SORT due-date ASC
> ```

> [!info] 3 编译 · 进 WIKI
> ```dataview
> TABLE WITHOUT ID file.link AS 节点, type AS 类型
> FROM "wiki"
> WHERE type != "ontology" AND type != "registry" AND file.name != "形而上学" AND file.name != "认识论" AND file.name != "伦理学" AND file.name != "log"
> SORT file.mtime DESC
> LIMIT 7
> ```

> [!success] 4 看板 · GRAPH
> ```dataviewjs
> const HUBS = new Set(["形而上学","认识论","伦理学"]);
> const nodes = dv.pages('"wiki"').where(p => p.type && p.type != "ontology" && p.type != "registry" && p.type != "source" && p.type != "analysis" && !p.file.name.startsWith("_") && !HUBS.has(p.file.name) && p.file.name != "log");
> const norm = t => String((t && t.target !== undefined) ? t.target : t).replace(/[\[\]]/g, "").split("|")[0].trim();
> const inb = {};
> for (const p of nodes) for (const r of (p.relations || [])) { const n = norm(r); if (n) inb[n] = (inb[n] || 0) + 1; }
> const rows = nodes.map(p => ({ link: p.file.link, name: p.file.name, deg: (p.relations || []).length + (inb[p.file.name] || 0) }))
>   .array().filter(r => r.deg > 0).sort((a, b) => b.deg - a.deg || a.name.localeCompare(b.name)).slice(0, 8);
> dv.paragraph("打开 **Graph** `⌘/Ctrl+G` 按类型配色看全局 · 中心 [[实在]] · [[知识]] · [[道德]]");
> dv.table(["枢纽节点", "度 (入+出)"], rows.map(r => [r.link, "●".repeat(Math.min(r.deg, 12)) + "  " + r.deg]));
> dv.paragraph("度 = 入边 + 出边 · 越高越接近图谱中心");
> ```

> [!quote] © 2026 HLB_ / PHILO VAULT · [[00-Dashboard/MOC|MOC]]
