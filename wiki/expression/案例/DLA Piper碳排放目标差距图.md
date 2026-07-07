---
title: DLA Piper碳排放目标差距图
type: concept
durability: medium
created: '2026-07-07'
updated: '2026-07-07'
sources: [2026-07-07-案例调研-增减目标归纳]
confidence: medium
classified_as: [可视化的视觉表达]
relations:
  - {target: 目标差距→差距柱, type: exemplifies}
tags: [案例, 表达, 可视化的视觉表达]
---

# DLA Piper碳排放目标差距图

- **来源**：DLA Piper《Impact Summary 2024》第 14 页。官方直链被反爬拦截，改用 [Wayback Machine 存档](http://web.archive.org/web/20250324181114/https://www.dlapiper.com/-/media/project/dlapiper-tenant/dlapiper/about-us/sustainability/sustainability-report-23-24/impact-summary-2024.pdf)核实内容真实，如实标注为存档链接。
- **页标题(论点)**："Decarbonising our business operations in line with 1.5°C"；正文："our emissions are trending down and are ahead of our projected reduction pathway…"
- **逻辑类型**：目标差距（bullet chart 的时间序列变体）
- **视觉形式**：FY20-FY24 五年堆叠柱（Scope 1/2/3 分色），柱顶标实测值，叠加两条蓝色虚线分别标注 2030/2040 目标值，柱高与虚线的垂直距离即差距。
- **为什么是这个形状**：论点要同时呈现逐年趋势、两个未来锚点、以及两者差距，把 bullet chart 的语法拉伸到多期序列，比多张独立 bullet graph 更省版面、更易看出差距是收敛还是扩大。
- **复现要点**：
  1. 目标线用虚线+独立标签浮动，与柱体分层，避免和堆叠色混淆
  2. 实际值直接标在柱顶，减少眼动往返
  3. 多个目标叠在同一张图而非拆图
- **常见做坏的方式**：目标线做成和数据柱同色同粗的实线，被误读成"又一根数据柱"，分不清实际与目标。
