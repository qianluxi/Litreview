# C4 改稿后定点重判（31 条，闭卷，第二轮）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（v1.2，含 §八 自足轴三族边界）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。
> 这 31 条的**论断已按上一轮复核意见删改，引文一字未动**；请逐字读当前论断，不要凭对上一轮的印象下结论。
> 31 条原判全部是 `PARTIAL`（唯一的 `UNSUPPORTED` 条目 `B1-06` 不在本批，它要换引文，另走）。
> 本批改动只有两种：**删掉引文里没有的成分**，或**把被加强的情态降回原文强度**（`会`→`可能`、`被定义`→`可被定义`）。
> **依据列必须是从引文中逐字连续截取的一段（≤15 字），不得拼接、缩写、改写**；
> 例如引文写 `The attributes used to represent failure cases could be associated with`，
> 就只能填 `used to represent` 或 `could be associated`，不能填 `attributes-value`。
> 写 `SUPPORTED` 时依据列必须填；写 `PARTIAL`/`UNSUPPORTED` 时必须在末列写明缺哪个成分、该怎么补。
> 自足轴照常独立判，不要假设它和上一轮一样。
> 快照 sha1: 16c50d4085

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词，连续片段） | 缺什么/需补的一句 |
|----|------|------|----------------------------------------|--------------------|

### B1-02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 系统形态 ・ p.8

- 论断：系统形态是一个为 Touch & Write 实现的原型。
- 引文："the prototype is implemented for the Touch & Write" (Ahmed et al., 2013, p.8)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-04 ・ Borner1993_StructuralSimilarity_CBR ・ 相似性或检索机制 ・ p.6

- 论断：对新问题的初始分析可以通过基于属性描述的、成本不高的表面相似性评估来完成。
- 引文："The rst initial analysis of the new problem can be done by an inexpensive surface similarity assessment based on the attribute based descriptions" (Borner, 1993, p.6)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### B1-05 ・ Borner1993_StructuralSimilarity_CBR ・ 明确写出的局限 ・ p.10

- 论断：作者明确写出，修改规则条件或权重的学习在本实现中未被处理。
- 引文："Learning e g the storage of new cases new rules and the application of techniques like Knuth Bendix completion to guarantee completeness of struc tural knowledge or learning of modi cation rule conditions or weights are not addressed in this implementation" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 31 行）

### B1-07 ・ Liao1998_SimilarityMeasures_CBR ・ 系统形态 ・ p.13

- 论断：有一个 CBR 系统正在开发中，用于存储失效分析。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1

- 论断：问题域是结构设计项目，关注的是这类项目上的信息。
- 引文："information on structural design projects" (Maher and Gomez, 1996, p.1)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 11 行）

### B1-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 系统形态 ・ p.2

- 论断：CaseCAD 使用 Framekit。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### B1-11 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 系统形态 ・ p.7

- 论断：文中举例 HI-RISE 在 PSRL 中实现，PSRL 是框架式产生式系统。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-16 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11

- 论断：作者指出，由于剪力墙样本有限，过拟合更容易避免。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)
- 形式特征：首字母小写（源文件第 31 行）

### B2-04 ・ Borner1993_StructuralSimilarity_CBR ・ 系统形态 ・ p.9

- 论断：SynTerm 与 SynGraph 为系统提供专项设计问题的解法。
- 引文："SynTerm and SynGraph supply the system with solutions for special design problems" (Borner, 1993, p.9)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### B2-06 ・ Liao1998_SimilarityMeasures_CBR ・ 案例或数据的表示形式 ・ p.14

- 论断：失效案例用属性来表示。
- 引文："The attributes used to represent failure cases could be associated with" (Liao et al., 1998, p.14)
- 形式特征：未以句末标点结尾（源文件第 15 行）

### B2-07 ・ Liao1998_SimilarityMeasures_CBR ・ 评价方式 ・ p.19

- 论断：评价使用两个失效分析案例 X(case1) 与 Y(case2)。
- 引文："Two cases X(case1) and Y(case2) of failure analysis are used ; n1, n2, n3, and" (Liao et al., 1998, p.19)
- 形式特征：未以句末标点结尾（源文件第 27 行）

### B2-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 评价方式 ・ p.2

- 论断：作者从 14 个设计项目中回顾并收集了数据。
- 引文："Finally, we reviewed and collected data from 14 design projects." (Maher and Gomez, 1996, p.2)
- 形式特征：完整句（源文件第 27 行）

### B2-10 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 一句话主张 ・ p.3

- 论断：本文介绍 KBES 在 preliminary design、analysts 与 detailed design 的应用。
- 引文："In this paper applications of KBES to the preliminary design, analysts, and detailed design" (Sriram et al., 1985, p.3)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### B2-13 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 系统形态 ・ p.3

- 论断：作者构建了多输入单输出的三层 BP 网络。
- 引文："Thereupon we have built the multi-input-and- single-output, three-layer BP network." (Zhang, 2006, p.3)
- 形式特征：完整句（源文件第 23 行）

### B2-14 ・ Zhao2023_ShearWall_GNN ・ 问题域 ・ p.1

- 论断：问题域是剪力墙结构的结构方案设计，作者称其重要，因为它是引导整个项目的第一个阶段。
- 引文："Structural scheme design of shear wall structures is important because it is the first stage that guides the project along its entire" (Zhao et al., 2023, p.1)
- 形式特征：未以句末标点结尾（源文件第 11 行）

### B3-13 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 评价方式 ・ p.5

- 论断：选型结果与工程实践相同。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)
- 形式特征：完整句（源文件第 27 行）

### R1-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 问题域 ・ p.1

- 论断：问题域是建筑平面图——生成式设计方法能产出大量平面方案，这可能令决策者难以应对。
- 引文："Generative design methods are able to produce a large number of potential solutions of architectural ﬂoor plans, which may be overwhelming for the decision-maker to cope with." (Rodrigues et al., 2017, p.1)
- 源文件：第 11 行

### R1-10 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 案例或数据的表示形式 ・ p.6

- 论断：与案例描述中 19 个属性各自相关联的取值构成案例描述，并可被定义为案例表型。
- 引文："The values that are associated with each of the 19 attributes in the description of a case make up the case description and can be deﬁned as the case phenotype (Fig. 3)." (Soibelman et al., 2000, p.6)
- 源文件：第 15 行

### R2-02 ・ AamodtPlaza1994_CBR_Foundations ・ 明确写出的局限 ・ p.10

- 论断：作者指出，随着案例数量增加，这可能轻易导致索引的爆炸式增长。
- 引文："This may easily lead to an explosive growth of indices with increased number of cases." (Aamodt and Plaza, 1994, p.10)
- 源文件：第 31 行

### R2-15 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 评价方式 ・ p.13

- 论断：评价用 SIoU 与 BIoU 对比协同设计与顺序设计方法：协同设计方法 SIoU 0.625、BIoU 0.548，顺序设计方法 0.544、0.404。
- 引文："The SIoU and BIoU obtained using the proposed co-design method were 0.625 and 0.548, respectively, whereas those obtained using the successive design method were 0.544 and 0.404, respectively." (Xia et al., 2025, p.13)
- 源文件：第 27 行

### R3-01 ・ AamodtPlaza1994_CBR_Foundations ・ 案例或数据的表示形式 ・ p.9

- 论断：泛化情节（GE）包含 norms、cases 与 indices 三类对象，norms 是索引于该 GE 下的所有案例共有的特征。
- 引文："A generalized episode contains three different types of objects: Norms, cases and indices. Norms are features common to all cases indexed under a GE." (Aamodt and Plaza, 1994, p.9)
- 源文件：第 15 行

### R3-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 系统形态 ・ p.6

- 论断：HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文："HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language." (Maher, 1987, p.6)
- 源文件：第 23 行

### R3-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 系统形态 ・ p.2

- 论断：本文在同一设置下把四种形状表示作为平面图设计描述子加以研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)
- 源文件：第 23 行

### R3-12 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 案例或数据的表示形式 ・ p.3

- 论断：表示上识别独特的高层语义特征，并用特征向量计算图像相似度，以实现对建筑平面图的有效检索。
- 引文："By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans." (Ling et al., 2025, p.3)
- 源文件：第 15 行

### R3-13 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 问题域 ・ p.1

- 论断：既有方法对剪力墙与梁分别设计，未能充分处理这些构件之间的强相互依赖，因此需要针对剪力墙与梁结构的智能协同设计方法。
- 引文："However, as the separate design of shear walls and beams fails to adequately address the strong interdependence of these components, an intelligent co-design approach for shear wall and beam structures is required." (Xia et al., 2025, p.1)
- 源文件：第 11 行

### R3-17 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 系统形态 ・ p.1

- 论断：此外还开发了一个高效算法，用 SSIG 对大规模平面图库排序。
- 引文："In addition, an efﬁcient algorithm is developed that uses SSIG to rank a large-scale ﬂoor plan database." (van Engelenburg et al., 2023, p.1)
- 源文件：第 23 行

### R4-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 评价方式 ・ p.7

- 论断：评价方式是用线性评价函数评价备选方案。
- 引文："HI-RISE evaluates alternatives with a linear evaluation function." (Maher, 1987, p.7)
- 源文件：第 27 行

### R4-10 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 一句话主张 ・ p.1

- 论断：本文提出 M-RAM，通过分布式多推理机制向设计者提供经适应的既有设计方案，以辅助工程师完成高层建筑结构设计的概念阶段。
- 引文："This paper presents the M-RAM, which is intended to assist engineers in the conceptual phase of the structural design of tall buildings by providing designers with adapted past design solutions generated by a distributed multi-reasoning mechanism." (Soibelman et al., 2000, p.1)
- 源文件：第 7 行

### R5-01 ・ AamodtPlaza1994_CBR_Foundations ・ 系统形态 ・ p.6

- 论断：系统形态是两个互补的模型，分别代表对案例推理的两种视角。
- 引文："The two models are complementary and represent two views on case-based reasoning." (Aamodt and Plaza, 1994, p.6)
- 源文件：第 23 行

### R5-02 ・ Gu2024_ShearWall_Diffusion ・ 案例或数据的表示形式 ・ p.4

- 论断：不同构件与剪力墙可以用图像中的颜色编码。
- 引文："Different components and shear walls can be encoded using the colors in the image." (Gu et al., 2024, p.4)
- 源文件：第 15 行

### R5-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 相似性或检索机制 ・ p.8

- 论断：机制是用 GNN 预测边标签：输入特征先经 GraphSAGE 层，再由 MLP 以每条边及其两个对应节点的组合特征值为输入来预测边特征。
- 引文："The process of predicting edge labels using the GNN comprises passing the input features through GraphSAGE algorithm layers, followed by the application of an MLP to predict the edge features using the combined feature values of each edge and its two corresponding nodes as input. Finally, the feature information for each edge is processed using a classification algorithm to yield the corresponding predicted values." (Xia et al., 2025, p.8)
- 源文件：第 19 行

