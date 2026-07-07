---
title: McKinseyDECC英国用电量瀑布图
type: concept
durability: high
created: '2026-07-07'
updated: '2026-07-07'
sources: [2026-07-07-案例调研-增减目标归纳]
confidence: high
classified_as: [可视化的视觉表达]
relations:
  - {target: 增减构成→瀑布图, type: exemplifies}
tags: [案例, 表达, 可视化的视觉表达]
---

# McKinseyDECC英国用电量瀑布图

- **来源**：McKinsey 为英国能源与气候变化部(DECC)撰写的报告，2012 年经 gov.uk 官方发布，[PDF 第 6 页已核实](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/65626/7035-capturing-full-elec-eff-potential-edr.pdf)。
- **页标题(论点)**："Underlying U.K. electricity demand is projected to be ~411 TWh in 2030, excluding the impact of current or future policy"
- **逻辑类型**：增减构成
- **视觉形式**：6 根柱子的浮动瀑布图，虚线连接柱顶/柱底——起点锚 328→浮动加项+27→中间锚355→浮动加项+56→深色高亮终值411→浮动减项-54→终点锚357。
- **为什么是这个形状**：论点是"排除政策影响后需求会到多少、政策又把它压低多少"，本质是从实际值出发经若干可归因分量、最终落到预测值的因果链，浮动柱+虚线直接画出"净变化被拆成几个分量"。
- **复现要点**：
  1. 中间柱"浮动"（柱底不落x轴，从上一累计高度画起），虚线横杠连接前后柱顶
  2. 只给关键锚点深色强调，过渡分量浅色弱化
  3. 柱顶直接标数值，不用图例查表
- **常见做坏的方式**：所有分量柱同色同重量，读者要逐个读x轴文字才能拼出"先加后减"的故事，图没替论点做功。
