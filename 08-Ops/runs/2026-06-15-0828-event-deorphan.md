---
type: run
routine: compile
run-id: 2026-06-15-0828
started: 2026-06-15T00:05
finished: 2026-06-15T00:20
status: ok
outputs: "evidences 决策落地为选项 A：放宽 exemplifies（案例→案例/事件，两域 _ontology 同步），不新增词类；5 条事件实证边（pp 4 exemplifies + ca 1 changed_by）；scan 孤儿 4→0；两域 schema 全过"
budget-spent: —
escalations: 0
---

# RUN 2026-06-15-0828 · 事件去孤儿（evidences 决策 = 复用 exemplifies）

> 上轮留的 evidences 本体决策落地。用户选 A：复用 exemplifies 而非新增 evidences 词类（克制，避免词表两天涨三类）。

## 飞轮

- 00:05 ✓ 决策 · evidences 缺口 → 选项 A：放宽 exemplifies「案例→概念」为「案例/事件→概念」；母本注释 + 两域 _ontology 同步
- 00:10 ✓ 定边 · 读 3 事件页确认页内依据（1997"奠基性实证"/2007"教科书演示"/2005 三故事）；2012 特例=背书事件连书不连概念
- 00:14 ✓ 织边 · pp +4 exemplifies（1997→聚焦即说不、2007→一句话定义、2005→连点成线/死亡过滤器）；ca +1（《局外人》→changed_by→2012）；双写 frontmatter+db
- 00:18 ✓ 复验 · scan 孤儿 4→0（真洞 18→14，剩 14 全是弱连接实体）
- 00:20 ✓ 收尾 · 两域 schema 全过；位置编码+报告 ×2；两 Hub footer；两 log；账本 t5-vocab 行

## 备注

- 克制原则：能复用就不新增词类（对比上次 enables 是真新增——因为概念→概念因果当时无任何边可复用；本次 exemplifies 已存在、只需放宽 domain）。
- 剩余真洞=14 弱连接实体（公司/书/人），是内容缺口（缺案例/关系），非边类型问题——下一步若做需读材料补案例，成本更高。
- Conflicts: none。
