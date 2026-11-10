# 抽检批次：S1

> 由 `python tools/audit_prep.py sample` 生成，seed=42、rate=12%，可复现。
> 来源 8 个批次、共 80 条候选条目，抽 10 条（12.5%）；候选集构成由主控留档，不在本文件披露。
> **闭卷**：只给下列五元组，不要回读原文、卡片、其它批次或答案键。
> 快照 sha1: 7d1a204d54

## 合计

| 项 | 数 |
|---|---|
| 判定表总条目 | 131 |
| 候选条目 | 80 |
| 抽检条目 | 10 |
| 抽检比例 | 12.5% |

## 待判条目

### S01 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 相似性或检索机制 ・ p.2

- 论断：相似度度量采用以属性相对欧氏加权距离为基础的方法。
- 引文："To solve this problem and to be able to take into consideration everything important and necessary such as concurrence of quality, quantitative and fuzzy attributes and difference in dimension, this paper established a new similarity measure method based on the relative Euclidean weight distance of attributes (see expression (5))." (Zhang, 2006, p.2)

### S02 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 问题域 ・ p.1

- 论断：研究问题为高层建筑结构形式选型优化。
- 引文："High-rise structural form selection optimization is an important strategic problem concerning synthetic performance of building structure." (Zhang, 2006, p.1)

### S03 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 相似性或检索机制 ・ p.5

- 论断：两幅平面图签名之间的相似度用 χ2 距离计算。
- 引文："Let P and Q be the signatures of two diﬀerent ﬂoor plan images. Their similarity is calculated by means of the χ2 distance:" (de las Heras et al., 2014, p.5)

### S04 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 明确写出的局限 ・ p.9

- 论断：作者明确指出方法的弱点是只能找到实际存在的物理房间。
- 引文："Furthermore, a weak point of our approach is that it is only able to ﬁnd the physical existent rooms." (Ahmed et al., 2013, p.9)

### S05 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 案例或数据的表示形式 ・ p.1

- 论断：案例先按特征属性刻画、再转成目标案例。
- 引文："First, CBR needs to distinguish the characteristic attributes of the significant cases to form selection and then transforms them into target cases." (Zhang, 2006, p.1)

### S06 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 明确写出的局限 ・ p.20

- 论断：作者指出样本数量有限的数据集可能不足以代表所有建筑类型与设计风格，从而限制研究结论的普适性。
- 引文："Datasets with a limited number of samples may not adequately represent all possible building types and design styles, thereby constraining the generalizability of the research findings." (Ling et al., 2025, p.20)

### S07 ・ Gu2024_ShearWall_Diffusion ・ 评价方式 ・ p.10

- 论断：该研究主要以交并比（IoU）指标进行评价。
- 引文："The Intersection over Union (IoU) metric (Equation 11) was primarily employed in this study for evaluation." (Gu et al., 2024, p.10)

### S08 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 一句话主张 ・ p.1

- 论断：作者主张其新颖性在于把 CBR、精确图匹配与不精确图匹配组合在同一个系统中，用于建筑平面图检索。
- 引文："The novelty of our approach is that it combines CBR, exact, and inexact graph matching in one system in the domain of retrieval of architectural ﬂoor plans." (Sabri et al., 2017, p.1)

### S09 ・ AamodtPlaza1994_CBR_Foundations ・ 相似性或检索机制 ・ p.12

- 论断：PATDEX 使用一个依赖领域但全局的相似性度量，基于表层匹配来评估相似性。
- 引文："A domain-dependent, but global similarity metric is used to assess similarity based on surface match." (Aamodt and Plaza, 1994, p.12)

### S10 ・ Rodrigues2017_Clustering_FloorPlans ・ 明确写出的局限 ・ p.13

- 论断：作者明确写出 TD 描述子的一个局限：同一形状类型的设计可能因对外墙每次转折处线段尺寸的敏感度而被判为不同。
- 引文："Another issue was found with this descriptor. In some cases, when designs have the same shape type, it may consider distinct due to the sensitivity over the size of the segments in every turn of the exterior wall (see groups F and G in Fig. 9 as an example)." (Rodrigues et al., 2017, p.13)
