# 抽检批次：S1

> 由 `python tools/audit_prep.py sample` 生成，seed=42、rate=12%，可复现。
> 来源 8 个批次、共 81 条候选条目，抽 10 条（12.3%）；候选集构成由主控留档，不在本文件披露。
> **闭卷**：只给下列五元组，不要回读原文、卡片、其它批次或答案键。
> 快照 sha1: 0ff8391a63

## 合计

| 项 | 数 |
|---|---|
| 判定表总条目 | 131 |
| 候选条目 | 81 |
| 抽检条目 | 10 |
| 抽检比例 | 12.3% |

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

### S05 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 问题域 ・ p.4

- 论断：问题域是结构设计，尤其是其中不适合纯算法求解、常呈病构性的设计问题。
- 引文："structural design are not amenable to purely algorithmic solutions. These problems are often ill-" (Sriram et al., 1985, p.4)

### S06 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 一句话主张 ・ p.1

- 论断：该文全面梳理建筑平面图检索所依赖的语义、空间、形状、纹理四类特征（合称 3ST 特征）。
- 引文："This paper presents a comprehensive exploration of four primary features essential for the retrieval of building floor plans: semantic features, spatial features, shape features, and texture features (collectively referred to as 3ST features)." (Ling et al., 2025, p.1)

### S07 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 案例或数据的表示形式 ・ p.6

- 论断：平面图被抽取出的语义以带顶点与边的图 G 表示。
- 引文："The extracted semantics are represented as a graph G ¼ ðV; EÞ." (Ahmed et al., 2013, p.6)

### S08 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 明确写出的局限 ・ p.12

- 论断：作者明确写出过滤器式 agent 的一项局限：输入集需要通过网络复制到 agent。
- 引文："Another limitation of filters is that the input set needs to be copied over the network into the agent." (Roith et al., 2017, p.12)

### S09 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 评价方式 ・ p.8

- 论断：评价时将系统结果与三套 ground truth 模型对比并报告平均精度均值，对照 gtA、gtB、gtAB 的 mAP 分别为 0.67、0.63 和 0.66。
- 引文："In retrieval terms, the mean average precision (mAP) obtained also varies depending on the ground truth model. Thus, the mAP scores are 0.67 when compared to gtA, 0.63 to gtB, and 0.66 to gtAB." (de las Heras et al., 2014, p.8)

### S10 ・ Rodrigues2017_Clustering_FloorPlans ・ 一句话主张 ・ p.13

- 论断：作者主张四种描述子的感知分析中，Tangent Distance（TD）能更好地刻画平面图形状且离群更少。
- 引文："The perceptual analysis carried out on the four descriptors shows that Tangent Distance (TD) captures better ﬂoor plan shapes and presents fewer outliers." (Rodrigues et al., 2017, p.13)
