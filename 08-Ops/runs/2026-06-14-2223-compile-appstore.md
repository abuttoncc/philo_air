---
type: run
routine: compile
run-id: 2026-06-14-2223
started: 2026-06-14T22:00
finished: 2026-06-14T22:23
status: ok
outputs: "App Store 发布史补厚 + 去孤儿：事件/2008-App-Store开放 富化（机器=iPhone 3G·三日期·设计理念）；来源 +1；T0 +4（SDK 10万/首发 500/首周 1000万/累计 10亿，verified）；relations +2（聚焦即说不、端到端控制 →changed_by→ 事件，去孤儿）；schema 34/34 全过。首次 expand 驱动的 recall→补全闭环"
budget-spent: —
escalations: 0
---

# RUN 2026-06-14-2223 · App Store 补厚（expand 驱动 · 交互会话）

> 第一次 **expand 工具驱动的研究回合**：expand.py 查出 `2008-App-Store开放` 为孤儿节点（0 邻居）→ anysearch 拉一手事实 → ingest 补厚 + 去孤儿。验证了"遍历驱动研究"而非"语义聚光驱动"。

## 飞轮

- 22:00 ✓ expand recall · `expand.py 2008-App-Store开放 --depth 2` → **0 邻居 = 孤儿**；prose 里被两概念引用、图上却无边 · 缺口锁定
- 22:05 ✓ anysearch · 3 组查询命中 Apple Newsroom 一手新闻稿（2008-07-10/07-14、2008-03-06）+ Wikipedia 核验 · 来源 1（confidence=high）
- 22:12 ✓ 答用户 · 机器=iPhone 3G（2008-07-11 出厂带）；SDK 2008-03-06（<1周10万下载）；涌入两波（首周1000万→2009-04 累计10亿）；设计理念=受控的开放
- 22:16 ✓ 富化事件 · 三日期弧线 + 设计理念（端到端控制向第三方延伸/70/30/It just works）写入事件页
- 22:18 ✓ 去孤儿 · 聚焦即说不、端到端控制 →changed_by→ 事件（双写 frontmatter+db）；局限条款从 prose 升级为真边 · relations +2
- 22:20 ✓ db · 来源页 upsert；T0 ×4（verified，挂事件页）；pages 33→34、dp 6→10、rel 52→54
- 22:23 ✓ 收尾 · schema 34/34 PASSED；位置编码刷新；_report 重生成；Hub+log+账本 newnode 8→9；**expand 复验事件现有 2 邻居（去孤儿成功）**

## 备注

- 防扩散：iPhone 3G 不建节点（设备，留事件正文）；SDK 不另建事件（并入 + T0）。
- 高危：仅来源 1（newnode 8→9，交互当场批准）；T0 为新增 verified 非合并；edges 域内非 xedge；零驳回。
- 方法论意义：这是「expand 查孤儿 → 外部补料 → ingest 去孤儿」的第一个完整样板，正是 A 选项要演示的 auto-research 第一回合。
- Conflicts: none。
