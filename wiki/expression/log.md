# 表达领域 · ingest 日志

> 每次 ingest 追加一行：日期 · 源材料 · 新增/更新节点 · 关系边 · 校验结果。

## 2026-07-05
- 域创建（new_domain.py 脚手架）。
- ingest（核心批·框架骨架）：
  - Source: 来源/2026-07-05-叙事结构研究、来源/2026-07-05-金字塔原理摘录
  - Created 框架(7)：勾立转收 · 救猫咪十五拍 · 起承转合 · 相声四段式 · 三幕结构 · 金字塔原理 · SCQA
  - Created 概念(4)：勾 · 立 · 转 · 收（各承载跨传统对应）
  - Created 人物(3)：芭芭拉·明托 · 布莱克·斯奈德 · 杨载
  - Created 著作(3)：《金字塔原理》·《Save the Cat!》·《诗法家数》
  - Created 分析(1)：表达双轴与叙事结构综述（references 产品哲学，跨域）
  - Relations：51（思想边 30：对应/proposed_by/authored_by/appears_in/part_of/instance_of/references；facet 分类边 21）
  - 签名边 对应：勾立转收↔起承转合/相声四段式/金字塔原理、起承转合↔相声四段式、转↔SCQA
  - schema 校验：20/20 PASS
  - 待补：结论先行/MECE/悬念/包袱/三翻四抖等概念、产品表达案例（乔布斯发布会）、第4叙事镜（麦基《故事》）
  - Conflicts: none
- ingest（应用综述）：
  - Created 分析(1)：中文语境如何写好故事-四体裁表达工程（公文/研报/科技博客/公众号）
  - 依据：双轴模型落地 + 中文语境层（凤头猪肚豹尾·元乔吉、文气与势、去翻译腔）+ 公文三段式(缘由→事项→要求) verified
  - Relations：references→勾立转收/金字塔原理/SCQA/起承转合/表达双轴综述 + facet 2；schema PASS
