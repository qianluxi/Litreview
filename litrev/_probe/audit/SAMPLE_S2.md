# 抽检批次：S2

> 由 `python tools/audit_prep.py sample` 生成，seed=71、rate=9%，可复现。
> 来源 8 个批次、共 128 条候选条目，抽 12 条（9.4%）；候选集构成由主控留档，不在本文件披露。
> **闭卷**：只给下列五元组，不要回读原文、卡片、其它批次或答案键。
> 快照 sha1: 8cf4be2cc9

## 合计

| 项 | 数 |
|---|---|
| 判定表总条目 | 138 |
| 候选条目 | 128 |
| 抽检条目 | 12 |
| 抽检比例 | 9.4% |

## 待判条目

### S01 ・ Borner1993_StructuralSimilarity_CBR ・ 一句话主张 ・ p.10

- 论断：作者的核心主张是，只有在存在可据以把旧解正确改编到当前问题的知识时，才进行结构相似性评估。
- 引文："Structural similarity is assessed if and only if there is knowledge available to adapt old solutions correctly to the current problem of interest" (Borner, 1993, p.10)

### S02 ・ Liao1998_SimilarityMeasures_CBR ・ 系统形态 ・ p.13

- 论断：有一个 CBR 系统正在开发中，用于存储失效分析。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)

### S03 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11

- 论断：作者指出，由于剪力墙样本有限，过拟合更容易避免。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)

### S04 ・ MaherGomez1996_CBR_StructuralDesign ・ 案例或数据的表示形式 ・ p.6

- 论断：案例以属性-值对（attribute-value pair）来描述。
- 引文："The differences between CaseCAD’s and CADsyn’s case representations lie in the attribute-value pairs and the decomposition into subcases." (Maher and Gomez, 1996, p.6)

### S05 ・ Liao1998_SimilarityMeasures_CBR ・ 相似性或检索机制 ・ p.17

- 论断：对模糊值采用「面积比方法」（area ratio method）计算两个模糊值之间的相似度。
- 引文："The area ratio method calculates the similarity between two fuzzy" (Liao et al., 1998, p.17)

### S06 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 评价方式 ・ p.5

- 论断：选型结果与工程实践相同。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)

### S07 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 评价方式 ・ p.15

- 论断：评价中请七位建筑师从自身角度指明若干属性对基于手绘图纸检索的重要性。
- 引文："Seven architects were asked to specific the importance of certain properties for searching based on freehand drawings from their point of view." (Roith et al., 2017, p.15)

### S08 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 相似性或检索机制 ・ p.52

- 论断：提出两阶段匹配与检索，即房间布局匹配与房间装饰匹配。
- 引文："A two phase matching and retrieval, Room Layout Matching (RLM) and Room Decor Matching (RDM) is proposed." (Sharma, 2018, p.52)

### S09 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 相似性或检索机制 ・ p.5

- 论断：检索由 Caspian 执行，索引检索完成后可运行两种模式，启用案例匹配器时程序扫描案例子集并找出权重值最高的案例。
- 引文："After the index search has been completely successfully, Caspian can be run in two different modes: with or without case matcher. If the case matcher is invoked, the program scans the subset of cases to ﬁnd the one with the highest weight value." (Soibelman et al., 2000, p.5)

### S10 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 评价方式 ・ p.143

- 论断：在 ROBIN 数据集上以 Mean Average Precision（MAP）评价；仅考虑房间布局时，检索得到的 MAP 值为 0.247。
- 引文："The Mean Average Precision (MAP) value obtained during retrieval on the ROBIN dataset was observed to be 0.247 in case only room layout was considered while retrieval, on the other hand incorporating both room layout and room decor features made retrieval quite specific." (Sharma, 2018, p.143)

### S11 ・ Rodrigues2017_Clustering_FloorPlans ・ 评价方式 ・ p.1

- 论断：在 72 个合成平面图构成的数据集上，将聚类结果与参考聚类比较，并以 Rand 指数衡量，Tangent Distance 的 Rand 指数为 0.873。
- 引文："A hierarchical agglomerative clustering algorithm is used to cluster a synthetic dataset of 72 ﬂoor plans. When compared to a reference clustering, despite good perceptual results with the use of the Point Distance and Turning Function representations, the Tangent Distance descriptor (Rand index of 0.873) provides the best results." (Rodrigues et al., 2017, p.1)

### S12 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 相似性或检索机制 ・ p.8

- 论断：机制是用 GNN 预测边标签：输入特征先经 GraphSAGE 层，再由 MLP 以每条边及其两个对应节点的组合特征值为输入来预测边特征。
- 引文："The process of predicting edge labels using the GNN comprises passing the input features through GraphSAGE algorithm layers, followed by the application of an MLP to predict the edge features using the combined feature values of each edge and its two corresponding nodes as input. Finally, the feature information for each edge is processed using a classification algorithm to yield the corresponding predicted values." (Xia et al., 2025, p.8)
