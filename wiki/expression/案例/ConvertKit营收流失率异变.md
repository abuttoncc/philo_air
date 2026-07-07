---
title: ConvertKit营收流失率异变
type: concept
durability: low
created: '2026-07-07'
updated: '2026-07-07'
sources: [2026-07-07-案例调研-筛选交集趋势]
confidence: contested
classified_as: [可视化的视觉表达]
relations:
  - {target: 趋势异变→折线+标注, type: exemplifies}
tags: [案例, 表达, 可视化的视觉表达, 争议]
---

# ConvertKit营收流失率异变

> [!warning] 视觉形式与映射定义有出入
> 三轮搜索未能找到"真实公司+可访问URL+图上确有标注(箭头/文本框)"三者同时满足的案例——本案例的异变原因写在图表**下方紧邻文字**里，而非图上标注，是可得的最接近案例而非干净确证。标注为 contested，不当作已验证案例使用。

- **来源**：Nathan Barry（ConvertKit/Kit 创始人）公开运营数据页 [nathanbarry.com/metrics](https://nathanbarry.com/metrics/)，非幻灯片，是持续更新的公开网页。
- **页标题(论点)**：图表下方原文："The drop in revenue churn you see above is because the contraction from annual plans is now outside the rolling 30 day window."
- **逻辑类型**：趋势异变
- **视觉形式**：Revenue Churn % 折线图出现明显下降拐点，但异变原因写在图表下方文字，图表本身未画箭头/文本框标注。
- **为什么是这个形状**：论点结构是"指标出现反直觉转折→必须给出因果解释，否则读者会误判业务变好"，折线呈现转折点，紧邻文字把转折翻译成原因（统计口径效应而非真实业务变化）。
- **复现要点**：
  1. 折线只保留能体现转折的最小时间窗口
  2. 解释紧贴转折点位置，不要放到文末（本案例恰恰没做到这点）
  3. 给出统计机制层面的原因，不能只说"业务变好/变坏"
- **常见做坏的方式**：只画折线不给任何解释，最常见的错误猜测是把统计口径变化误读成真实业务趋势。
- **待补**：本域仍缺一个"图上确有标注"的干净案例，建议下一轮直接人工打开 Baremetrics/ChartMogul 官方博客或 Duolingo/Airbnb investor day PDF 逐页核实。
