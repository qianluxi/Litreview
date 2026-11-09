# 人工基准标签 v1（先标后测，审计员不可见）

标定时间：2026-11-09 09:55，在派出审计 agent **之前**写定，避免"看完机器判定再改答案"。
依据：`AUDIT_CONTRACT.md` 第三节五条规则 + 原文措辞。

| id | 支撑 | 自足 | 判定理由（引文原词） |
|---|---|---|---|
| 01 | SUPPORTED | SELF | `BIM-based variant retrieval` + `early design phases` 与论断逐项对应；论断省略 CBR/PM 不算越界（少说不等于多说） |
| 02 | SUPPORTED | SELF | `graph pattern matching` / `Based on a pattern query, matching graphs are selected from a case base` 与"按模式查询由案例库选出匹配图"对应。**边界项**：原文 `is a possibility to find` 被写成"方法是"，可争辩为轻微情态升级，但仍落在方法陈述范围内 |
| 03 | PARTIAL | SELF | `IFC data structure` 被写成"IFC 标准"（术语替换）；`can be defined` 被写成"分别定义"（情态升级） |
| 04 | SUPPORTED | SELF | `distributed retrieval system MetisCBR` + `architectural design domain` 逐项对应 |
| 05 | SUPPORTED | SELF | `user queries built with a semantic description model Semantic Fingerprint`，主语在引文内 |
| 06 | SUPPORTED | SELF | `container-based structure` / `autonomous multi-agent sub-system that is nested inside a parent MAS` 逐项对应。**边界项**：`can be seen as` 被写成"是"，属理论主张的表述差异，未改变命题 |
| 07 | SUPPORTED | SELF | `Two major considerations ... representations of design cases and process models for recalling and adapting design cases` 逐项对应 |
| 08 | SUPPORTED | DEPENDENT | 论断补出主语 design-case recall（规则 5：补主语不算越界），但引文以 `it` 开头、指代在引号外，学术上不可直接引用 |
| 09 | SUPPORTED | SELF | `Indexing identifies the features a previous design should have` 逐项对应 |
| 10 | PARTIAL | SELF | 引文只支撑"对两个备选变体做相似度比较"；"没有给出文献篇数或样本条数"是**缺席命题**（规则 4），单条引文无法证明 |
| 11 | PARTIAL | SELF | 引文支撑"变体数量相当有限"；但不支撑"没有给出具体数量/文献篇数/样本条数"（规则 4） |
| 12 | PARTIAL | SELF | 引文支撑"取值落在 0 到 1 之间"；"只定义了"（排他）与"没有报告准确率"（缺席）无依据（规则 4） |
| 13 | PARTIAL | SELF | 引文支撑"差异为零对应相似度一"；同 12，缺席与排他成分无依据；"差异为一对应零"此句未提 |

## 汇总

- 支撑：SUPPORTED 9 / PARTIAL 4 / UNSUPPORTED 0
- 自足：SELF 12 / DEPENDENT 1

## 这套标签自身的弱点（先说清，免得把吻合当成正确性证明）

1. **单标**：只有我一个人标，没有第二人独立标。所以"吻合率"的上限是"与我的口径一致"，不是"与真理一致"。
2. **02 / 06 是边界项**：判 SUPPORTED 有争议空间。若审计员判 PARTIAL，不宜直接记为错判，应单独列为"口径分歧"。
3. **10–13 的判法有解释选择**：我把它们判 PARTIAL（而非专门造一个"答非所问"码），理由是论断里混入了缺席命题。若换成"条目不回答被指派命题"这个维度，它们会是另一类失败。两种判法都成立，本轮只测第一种。
