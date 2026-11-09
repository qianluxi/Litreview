# C4 剩余支撑轴审计批次 B2（17 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节口径修订）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词） | 缺什么/需补的一句 |
|----|------|------|--------------------------------|--------------------|

### R2-01 ・ AamodtPlaza1994_CBR_Foundations ・ 问题域 ・ p.7

- 论断：本文讨论的是案例推理的通用方法论，作者指出并不存在适用于每一个应用领域的通用案例推理方法。
- 引文："As for AI in general, there are no universal CBR methods suitable for every domain of application." (Aamodt and Plaza, 1994, p.7)
- 源文件：第 11 行

### R2-02 ・ AamodtPlaza1994_CBR_Foundations ・ 明确写出的局限 ・ p.10

- 论断：作者明确指出，这种索引方式会随案例数量的增加而轻易导致索引的爆炸式增长。
- 引文："This may easily lead to an explosive growth of indices with increased number of cases." (Aamodt and Plaza, 1994, p.10)
- 源文件：第 31 行

### R2-03 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 案例或数据的表示形式 ・ p.6

- 论断：平面图被抽取出的语义以带顶点与边的图 G 表示。
- 引文："The extracted semantics are represented as a graph G ¼ ðV; EÞ." (Ahmed et al., 2013, p.6)
- 源文件：第 15 行

### R2-04 ・ Gu2024_ShearWall_Diffusion ・ 评价方式 ・ p.10

- 论断：该研究主要以交并比（IoU）指标进行评价。
- 引文："The Intersection over Union (IoU) metric (Equation 11) was primarily employed in this study for evaluation." (Gu et al., 2024, p.10)
- 源文件：第 27 行

### R2-05 ・ Maher1987_ExpertSystems_StructuralDesign ・ 相似性或检索机制 ・ p.16

- 论断：STRUPLE 的相似性度量由一组匹配准则构成，这些准则界定匹配建筑与输入建筑应共享的重要共同方面。
- 引文："The similarity metric is described by a set of criteria, also called matching criteria, which define what significant common aspects the matching buildings and the input building should share." (Maher, 1987, p.16)
- 源文件：第 19 行

### R2-06 ・ Rodrigues2017_Clustering_FloorPlans ・ 案例或数据的表示形式 ・ p.6

- 论断：每种描述子都表示成长度相同的数值向量（100 个值），因此表示类型不影响算法性能。
- 引文："As the vector in every clustering process had the same length (100 values), the type of shape representation did not affect the performance of the algorithm." (Rodrigues et al., 2017, p.6)
- 源文件：第 15 行

### R2-07 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 问题域 ・ p.2

- 论断：面向建筑设计过程，系统让用户以在手绘或多点触控设备上绘制的建筑草图检索相似的建筑模型。
- 引文："This paper describes an information retrieval system that allows users to search for building models that are similar to a hand-drawn sketch of a building or parts of a building on a multi-touch device to support the design process of architects." (Roith et al., 2017, p.2)
- 源文件：第 11 行

### R2-08 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 明确写出的局限 ・ p.12

- 论断：作者明确写出过滤器式 agent 的一项局限：输入集需要通过网络复制到 agent。
- 引文："Another limitation of filters is that the input set needs to be copied over the network into the agent." (Roith et al., 2017, p.12)
- 源文件：第 31 行

### R2-09 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 一句话主张 ・ p.1

- 论断：作者主张其新颖性在于把 CBR、精确图匹配与不精确图匹配组合在同一个系统中，用于建筑平面图检索。
- 引文："The novelty of our approach is that it combines CBR, exact, and inexact graph matching in one system in the domain of retrieval of architectural ﬂoor plans." (Sabri et al., 2017, p.1)
- 源文件：第 7 行

### R2-10 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 评价方式 ・ p.7

- 论断：评价采用定性分析，请参与者观察三种检索方法在 10 个查询上的结果。
- 引文："For this qualitative analysis we asked different participants to observe the results of each of the three retrieval methods, corresponding to each of the 10 queries." (Sabri et al., 2017, p.7)
- 源文件：第 27 行

### R2-11 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 系统形态 ・ p.21

- 论断：论文还提出了交互式图形用户界面，帮助用户选择、分析并检索相似平面图。
- 引文："An interactive graphical user interface to aid users to select, analyse and retrieve similar floor plans is also proposed in this thesis." (Sharma, 2018, p.21)
- 源文件：第 23 行

### R2-12 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 相似性或检索机制 ・ p.5

- 论断：检索由 Caspian 执行，索引检索完成后可运行两种模式，启用案例匹配器时程序扫描案例子集并找出权重值最高的案例。
- 引文："After the index search has been completely successfully, Caspian can be run in two different modes: with or without case matcher. If the case matcher is invoked, the program scans the subset of cases to ﬁnd the one with the highest weight value." (Soibelman et al., 2000, p.5)
- 源文件：第 19 行

### R2-13 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 问题域 ・ p.1

- 论断：问题域是建筑平面图的特征检索，并置于建筑工程项目管理与执行的语境中。
- 引文："Feature retrieval technology for building floor plans has garnered significant attention in recent years due to its critical role in the efficient management and execution of construction projects." (Ling et al., 2025, p.1)
- 源文件：第 11 行

### R2-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 一句话主张 ・ p.1

- 论断：作者提出将剪力墙与梁的耦合潜在位置统一表示为图，并用图神经网络（GNN）驱动剪力墙与梁的协同设计。
- 引文："This study constructed a graph representation of the coupled potential positions for shear walls and beams and proposed a co-design method driven by a graph neural network (GNN)." (Xia et al., 2025, p.1)
- 源文件：第 7 行

### R2-15 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 评价方式 ・ p.13

- 论断：评价采用与工程师设计对比的交并比（SIoU、BIoU）：协同设计方法的 SIoU 为 0.625、BIoU 为 0.548，顺序设计方法分别为 0.544 与 0.404。
- 引文："The SIoU and BIoU obtained using the proposed co-design method were 0.625 and 0.548, respectively, whereas those obtained using the successive design method were 0.544 and 0.404, respectively." (Xia et al., 2025, p.13)
- 源文件：第 27 行

### R2-16 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 系统形态 ・ p.3

- 论断：系统形态是查询示例（query by example）式的检索框架。
- 引文："The retrieval model proposed is a query by example framework." (de las Heras et al., 2014, p.3)
- 源文件：第 23 行

### R2-17 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 相似性或检索机制 ・ p.5

- 论断：SSIG 被表述为基于 IoU 的相似度与基于 nGED 的相似度之间的加权平均。
- 引文："Coined as SSIG (Structural Similarity by IoU and GED), 7 essentially computes a weighted average between a IoU-based and a nGED-based similarity metric." (van Engelenburg et al., 2023, p.5)
- 源文件：第 19 行
