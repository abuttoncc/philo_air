---
title: Appcues onboarding漏斗
type: concept
durability: medium
created: '2026-07-07'
updated: '2026-07-07'
sources: [2026-07-07-案例调研-筛选交集趋势]
confidence: medium
classified_as: [可视化的视觉表达]
relations:
  - {target: 筛选→漏斗, type: exemplifies}
tags: [案例, 表达, 可视化的视觉表达]
---

# Appcues onboarding漏斗

- **来源**：Appcues 官方博客 ["How to set up Mixpanel funnels for user onboarding success"](https://www.appcues.com/blog/mixpanel-funnels-user-onboarding)。公司数据真实，但这是分析工具(Mixpanel)原生截图，不是设计过的 deck 页。
- **页标题(论点)**：原文："This is real data that we collected from one of our onboarding flows at Appcues. Since we saw the largest drop-off between steps 2 and 3, we decided to start investigating here."
- **逻辑类型**：筛选
- **视觉形式**：Mixpanel Funnel Report——5 个 onboarding 步骤按序排列的递减条形，优化前后两版对比呈现。
- **为什么是这个形状**：论点是"用户逐级流失，要找到流失最大的一级"，条形逐级变窄直接把"每一步留下多少人"翻译成长度对比，最长落差=最大问题所在。
- **复现要点**：
  1. 每一级标绝对转化率，不只是相对上一级的百分比
  2. 优化前/优化后并排放，让改进一眼可见
  3. 只在流失最大的一级加视觉强调，别让每级同等着色
- **常见做坏的方式**：把漏斗做成纯装饰性梯形图标，不标真实数字，只剩"感觉在变窄"的暗示，读者拿不到可执行的诊断信息。
