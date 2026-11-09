# C4 剩余支撑轴审计批次 B5（17 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节口径修订）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词） | 缺什么/需补的一句 |
|----|------|------|--------------------------------|--------------------|

### R5-01 ・ AamodtPlaza1994_CBR_Foundations ・ 系统形态 ・ p.6

- 论断：系统形态是理论性的描述框架，用两个互补的模型来代表对案例推理的两种视角。
- 引文："The two models are complementary and represent two views on case-based reasoning." (Aamodt and Plaza, 1994, p.6)
- 源文件：第 23 行

### R5-02 ・ Gu2024_ShearWall_Diffusion ・ 案例或数据的表示形式 ・ p.4

- 论断：该文用图像中的颜色编码不同构件与剪力墙。
- 引文："Different components and shear walls can be encoded using the colors in the image." (Gu et al., 2024, p.4)
- 源文件：第 15 行

### R5-03 ・ Maher1987_ExpertSystems_StructuralDesign ・ 问题域 ・ p.6

- 论断：问题域是结构设计的初步阶段，即做出结构体系类型、材料与位置决策的阶段。
- 引文："All four systems address the preliminary stage of design during which decisions on structural system type, material and location are made." (Maher, 1987, p.6)
- 源文件：第 11 行

### R5-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 明确写出的局限 ・ p.7

- 论断：作者明确指出 HI-RISE 目前局限于矩形周边和简单矩形结构网格的建筑。
- 引文："HI-RISE is currently restricted to buildings with a rectangular perimeter and a simple rectangular structural grid." (Maher, 1987, p.7)
- 源文件：第 31 行

### R5-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 一句话主张 ・ p.13

- 论断：作者主张四种描述子的感知分析中，Tangent Distance（TD）能更好地刻画平面图形状且离群更少。
- 引文："The perceptual analysis carried out on the four descriptors shows that Tangent Distance (TD) captures better ﬂoor plan shapes and presents fewer outliers." (Rodrigues et al., 2017, p.13)
- 源文件：第 7 行

### R5-06 ・ Rodrigues2017_Clustering_FloorPlans ・ 明确写出的局限 ・ p.13

- 论断：作者明确写出 TD 描述子的一个局限：同一形状类型的设计可能因对外墙每次转折处线段尺寸的敏感度而被判为不同。
- 引文："Another issue was found with this descriptor. In some cases, when designs have the same shape type, it may consider distinct due to the sensitivity over the size of the segments in every turn of the exterior wall (see groups F and G in Fig. 9 as an example)." (Rodrigues et al., 2017, p.13)
- 源文件：第 31 行

### R5-07 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 系统形态 ・ p.5

- 论断：作者实现了原型，使用户能把可视化构造的查询发送到 Coordinator 中间件，以交互式检索相似建筑平面图的描述。
- 引文："Our prototypes enable users to interactively retrieve descriptions of similar building floorplans by sending queries which are constructed visually to a Coordinator middleware." (Roith et al., 2017, p.5)
- 源文件：第 23 行

### R5-08 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 相似性或检索机制 ・ p.4

- 论断：系统实现了三种匹配与检索技术：MetisCBR、以 VF2 为代表的精确图匹配、以及以 index-based 指称的不精确图匹配。
- 引文："This section presents the three matching and retrieval techniques implemented in Archistant: MetisCBR, exact graph matching (referred as VF2), and inexact graph matching (referred as index-based)." (Sabri et al., 2017, p.4)
- 源文件：第 19 行

### R5-09 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 案例或数据的表示形式 ・ p.50

- 论断：采用图谱嵌入，把前一步生成的房间布局图表示到模式空间中。
- 引文："Graph Spectral Embedding [Luo et al., 2003] approach is adopted to represent the room layout graphs created in the previous stage in a pattern-space." (Sharma, 2018, p.50)
- 源文件：第 15 行

### R5-10 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 问题域 ・ p.1

- 论断：问题域是结构设计的概念阶段，涉及初选材料、选择建筑整体结构形式、生成粗略尺寸布置并考虑技术可能性。
- 引文："The conceptual phase of structural design involves selecting preliminary materials, selecting the overall structural form of the building, producing a rough dimensional layout, and considering technological possibilities." (Soibelman et al., 2000, p.1)
- 源文件：第 11 行

### R5-11 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 明确写出的局限 ・ p.4

- 论断：作者明确指出这些数据不足以归纳出好的泛化。
- 引文："We recognize the fact that these data are not sufﬁcient to induce a good generalization." (Soibelman et al., 2000, p.4)
- 源文件：第 31 行

### R5-12 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 案例或数据的表示形式 ・ p.8

- 论断：系统的过程性知识以产生式规则和 LISP 函数表示。
- 引文："The procedural knowledge is represented by production rules and LISP functions." (Sriram et al., 1985, p.8)
- 源文件：第 15 行

### R5-13 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 评价方式 ・ p.20

- 论断：常用评价指标包括 accuracy、F1 score、mAP 与 Matthews 相关系数 MCC。
- 引文："Commonly used evaluation metrics include accuracy, F1 score, mean average precision (mAP), and the Matthews correlation coefficient (MCC) [75]." (Ling et al., 2025, p.20)
- 源文件：第 27 行

### R5-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 相似性或检索机制 ・ p.8

- 论断：机制不是相似度检索，而是把布置设计转化为图上的边标签预测：输入特征经 GraphSAGE 层与 MLP 组合每条边及其两端节点的特征，再由分类算法输出预测值。
- 引文："The process of predicting edge labels using the GNN comprises passing the input features through GraphSAGE algorithm layers, followed by the application of an MLP to predict the edge features using the combined feature values of each edge and its two corresponding nodes as input. Finally, the feature information for each edge is processed using a classification algorithm to yield the corresponding predicted values." (Xia et al., 2025, p.8)
- 源文件：第 19 行

### R5-15 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 问题域 ・ p.2

- 论断：问题域是建筑平面图这类线绘图在检索场景下的图形识别与视觉美学。
- 引文："This paper is an early attempt to introduce visual aesthetics in graphics recognition, in particular in line drawings of architectural plans in a retrieval scenario." (de las Heras et al., 2014, p.2)
- 源文件：第 11 行

### R5-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 一句话主张 ・ p.8

- 论断：作者把 IoU 与 GED 合并成一个名为 SSIG 的度量，以此作为克服既有度量不足的方案。
- 引文："We overcome the shortcomings by combining IoU and GED into one metric, called SSIG." (van Engelenburg et al., 2023, p.8)
- 源文件：第 7 行

### R5-17 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 明确写出的局限 ・ p.8

- 论断：作者明确写出本文只考察 IoU 与 GED，未考虑其他常见的图像与图相似度度量。
- 引文："This work is however limited to investigating IoU and GED and does not consider other well-known image- and graph-based similarity metrics." (van Engelenburg et al., 2023, p.8)
- 源文件：第 31 行
