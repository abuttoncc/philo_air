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

## 2026-07-07
- 本体扩展（非 ingest，未建节点）：注册第 4 个 facet **可视化的视觉表达**（讲得一眼看懂）——
  _ontology.md §0.5/§4、表达.md、meta.yaml keywords 已更新；[[金字塔原理]] 标记为未来双 facet 节点（思想表达 + 可视化的视觉表达），尚未改其 frontmatter。
- 文献调研（P0，未产出节点）：Minto 金字塔原理"页序/页内结构"机制细化、Zelazny 五种数据关系、
  Abela Chart Chooser（19 终端节点，全部为数据图，非逻辑图扩展；Stephen Few "Abela's Folly" 批评其顶层四分类不 MECE）、
  Duarte 六大图形族(Flow/Structure/Cluster/Radiate/Pictorial/Data，与其 Diagrammer 工具实际用的 Flow/Network/Stack/Segment/Join 五分类不一致)、
  Alley Assertion-Evidence（修辞纪律，非图形选择表）、久恒启一図解思考（图先于逻辑成型，与前四者"逻辑先行"相反）。
- 待办：逐一为 Zelazny/Duarte/Abela/Alley/久恒启一 建 人物+著作+框架 节点；
  为已产出的 12 种"逻辑类型→视觉形式"映射 + 待补 6 种建 概念 节点对；分析/ 建总表；案例/ 待拆解卡。
- Conflicts: none
