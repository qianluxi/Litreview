# C4 剩余支撑轴审计批次 B3（17 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节口径修订）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词） | 缺什么/需补的一句 |
|----|------|------|--------------------------------|--------------------|

### R3-01 ・ AamodtPlaza1994_CBR_Foundations ・ 案例或数据的表示形式 ・ p.9

- 论断：案例记忆以泛化情节组织，泛化情节包含 norms、cases 与 indices 三类对象，norms 是其下所有案例共有的特征。
- 引文："A generalized episode contains three different types of objects: Norms, cases and indices. Norms are features common to all cases indexed under a GE." (Aamodt and Plaza, 1994, p.9)
- 源文件：第 15 行

### R3-02 ・ Gu2024_ShearWall_Diffusion ・ 一句话主张 ・ p.15

- 论断：该文提出一种基于扩散模型的剪力墙结构智能设计方法。
- 引文："This study proposed an intelligent design method for shear wall structures based on a diffusion model." (Gu et al., 2024, p.15)
- 源文件：第 7 行

### R3-03 ・ Gu2024_ShearWall_Diffusion ・ 明确写出的局限 ・ p.15

- 论断：作者指出该研究中扩散模型的应用仍处于初步阶段。
- 引文："It is important to note that the use of the diffusion model in this study remains in its preliminary stage." (Gu et al., 2024, p.15)
- 源文件：第 31 行

### R3-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 系统形态 ・ p.6

- 论断：系统形态是已实现的专家系统原型，例如 HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文："HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language." (Maher, 1987, p.6)
- 源文件：第 23 行

### R3-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 系统形态 ・ p.2

- 论断：本文形态是在同一设置下把四种形状表示作为平面图设计描述子进行对比的实验研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)
- 源文件：第 23 行

### R3-06 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 案例或数据的表示形式 ・ p.1

- 论断：建筑平面图指纹被形式化为图，并用一种公共 schema（AGraphML）编码，以表示空间构型。
- 引文："Our federated database system is queried using semantic building floorplan fingerprints, which are formalized as graphs and encoded in a common schema, like our AGraphML, to represent spatial configurations and perform graph matching." (Roith et al., 2017, p.1)
- 源文件：第 15 行

### R3-07 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 问题域 ・ p.1

- 论断：问题域是建筑平面图的概念设计，以及在该阶段检索相似的平面图。
- 引文："Until today, for the conceptual design of architectural ﬂoor plans, architects widely follow the traditional pen and paper based method to draw the conceptual ﬂoor plans, and retrieve the similar ﬂoor plans in the printed reference collections." (Sabri et al., 2017, p.1)
- 源文件：第 11 行

### R3-08 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 明确写出的局限 ・ p.7

- 论断：作者明确写出，索引法的这些局限来自底层 Neo4j 数据库的内部超时错误。
- 引文："These limitations came from internal timeout errors of the underlying Neo4j database, most likely due to a congestion of the database system." (Sabri et al., 2017, p.7)
- 源文件：第 31 行

### R3-09 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 一句话主张 ・ p.21

- 论断：论文提出面向建筑平面图的内容检索方法，从平面图中抽取不同特征以支持检索。
- 引文："In this thesis, techniques to analyse architectural floor plans and extraction of different features to aid in content based retrieval in floor plans is proposed." (Sharma, 2018, p.21)
- 源文件：第 7 行

### R3-10 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 评价方式 ・ p.143

- 论断：在 ROBIN 数据集上以 Mean Average Precision（MAP）评价；仅考虑房间布局时，检索得到的 MAP 值为 0.247。
- 引文："The Mean Average Precision (MAP) value obtained during retrieval on the ROBIN dataset was observed to be 0.247 in case only room layout was considered while retrieval, on the other hand incorporating both room layout and room decor features made retrieval quite specific." (Sharma, 2018, p.143)
- 源文件：第 27 行

### R3-11 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 系统形态 ・ p.7

- 论断：系统形态是实际实现的 M-RAM，由用 Java 编写的 WWW 界面接收输入并启动 manager 程序。
- 引文："In the actual M-RAM implementation, a WWW interface written in Java (e.g., ﬁrst tier) receives the expected data as input and launches the manager program (e.g., second tier)." (Soibelman et al., 2000, p.7)
- 源文件：第 23 行

### R3-12 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 案例或数据的表示形式 ・ p.3

- 论断：平面图以高层语义特征与特征向量的形式表示，并用特征向量计算图像相似度。
- 引文："By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans." (Ling et al., 2025, p.3)
- 源文件：第 15 行

### R3-13 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 问题域 ・ p.1

- 论断：问题域为剪力墙与梁的结构方案布置；既有方法分别生成剪力墙或梁，未处理二者的相互依赖，因此需要剪力墙与梁的协同设计方法。
- 引文："However, as the separate design of shear walls and beams fails to adequately address the strong interdependence of these components, an intelligent co-design approach for shear wall and beam structures is required." (Xia et al., 2025, p.1)
- 源文件：第 11 行

### R3-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 明确写出的局限 ・ p.15

- 论断：作者明确指出梁的生成依赖潜在梁的布置，因此仍需探索更好的潜在梁生成方法，例如引入更多工程经验规则与硬编码规则。
- 引文："Although case studies show that the algorithms of co-design have achieved good results, considering that the generation of beams depends on the arrangement of potential beams, it is still necessary to explore better methods for generating potential beams, such as introducing more engineering experience rules and hard-coding rules, to further optimize the generation of potential beams." (Xia et al., 2025, p.15)
- 源文件：第 31 行

### R3-15 ・ Zhao2023_ShearWall_GNN ・ 一句话主张 ・ p.1

- 论断：作者提出一种基于图神经网络（GNN）的剪力墙布置智能设计方法。
- 引文："Therefore, this study develops an intelligent design method for shear wall layouts based on GNNs." (Zhao et al., 2023, p.1)
- 源文件：第 7 行

### R3-16 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 评价方式 ・ p.8

- 论断：评价时将系统结果与三套 ground truth 模型对比并报告平均精度均值，对照 gtA、gtB、gtAB 的 mAP 分别为 0.67、0.63 和 0.66。
- 引文："In retrieval terms, the mean average precision (mAP) obtained also varies depending on the ground truth model. Thus, the mAP scores are 0.67 when compared to gtA, 0.63 to gtB, and 0.66 to gtAB." (de las Heras et al., 2014, p.8)
- 源文件：第 27 行

### R3-17 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 系统形态 ・ p.1

- 论断：产出形态是一个用 SSIG 对大规模平面图库排序的高效算法，作者称代码将公开。
- 引文："In addition, an efﬁcient algorithm is developed that uses SSIG to rank a large-scale ﬂoor plan database." (van Engelenburg et al., 2023, p.1)
- 源文件：第 23 行
