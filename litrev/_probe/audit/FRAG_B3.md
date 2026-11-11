# C4 审计批次 B3（16 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节口径修订）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。
> 快照 sha1: b64ad5a18a

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词） | 缺什么/需补的一句 |
|----|------|------|--------------------------------|--------------------|

### B3-01 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 相似性或检索机制 ・ p.3

- 论断：作者认为子图匹配方法在检索算法上是有前景的路线。
- 引文："As for the retrieval algorithm, subgraph matching approaches seem to be promising." (Ahmed et al., 2013, p.3)
- 形式特征：完整句（源文件第 19 行）

### B3-02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 明确写出的局限 ・ p.9

- 论断：作者明确指出方法的弱点是只能找到实际存在的物理房间。
- 引文："Furthermore, a weak point of our approach is that it is only able to ﬁnd the physical existent rooms." (Ahmed et al., 2013, p.9)
- 形式特征：完整句（源文件第 31 行）

### B3-03 ・ Borner1993_StructuralSimilarity_CBR ・ 案例或数据的表示形式 ・ p.5

- 论断：案例中的对象由空间尺寸和另外九个属性表示。
- 引文："Following the work of Ludger Hovestadt Hov each object circle or ellipse will be represented by its spatial dimensions and nine further attributes like time at which this object was created aspect which assumes one of return air fresh air etc and morphology which refers to access connection etc" (Borner, 1993, p.5)
- 形式特征：未以句末标点结尾（源文件第 15 行）

### B3-04 ・ Borner1993_StructuralSimilarity_CBR ・ 评价方式 ・ p.10

- 论断：评价方式是报告初期实验结果对上述主张的支持，未给出数据集规模或指标数值。
- 引文："The initial experimental results support the claims that the proposed ap proach o ers improved adaptation facilities in synthesis tasks together with a greater overall explanation performance" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 27 行）

### B3-05 ・ Liao1998_SimilarityMeasures_CBR ・ 一句话主张 ・ p.3

- 论断：该文在第二部分提出一种混合相似度度量，用于案例之间的比较。
- 引文："In part 2, a hybrid similarity measure is proposed to compare cases having a mixture of crisp and fuzzy features." (Liao et al., 1998, p.3)
- 形式特征：完整句（源文件第 7 行）

### B3-06 ・ Liao1998_SimilarityMeasures_CBR ・ 相似性或检索机制 ・ p.17

- 论断：对模糊值采用「面积比方法」（area ratio method）计算两个模糊值之间的相似度。
- 引文："The area ratio method calculates the similarity between two fuzzy" (Liao et al., 1998, p.17)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### B3-07 ・ MaherGomez1996_CBR_StructuralDesign ・ 一句话主张 ・ p.1

- 论断：本文以四个案例的形式介绍作者在悉尼大学开发的基于案例设计系统。
- 引文："Toward that end, this article presents four “cases” of case-based building design sys- tems that we’ve developed at the University of Sydney: CaseCAD, CADsyn, Win, and Demex." (Maher and Gomez, 1996, p.1)
- 形式特征：完整句（源文件第 7 行）

### B3-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 相似性或检索机制 ・ p.4

- 论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文："The system measures a model's or a case's relevance to a given problem by finding matches between the attributes and values in the problem spec- ification and those in the object-based description of the memory item." (Maher and Gomez, 1996, p.4)
- 形式特征：完整句（源文件第 19 行）

### B3-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 明确写出的局限 ・ p.10

- 论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文："This approach is appropriate when case memory contains a limited num- ber of cases and inappropriate when case memory becomes very large." (Maher and Gomez, 1996, p.10)
- 形式特征：完整句（源文件第 31 行）

### B3-10 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 问题域 ・ p.4

- 论断：问题域是结构设计，尤其是其中不适合纯算法求解、常呈病构性的设计问题。
- 引文："However, a number of problems encountered in structural design are not amenable to purely algorithmic solutions. These problems are often ill- structured, and an experienced engineer deals with them using his judgment and experience." (Sriram et al., 1985, p.4)
- 形式特征：完整句（源文件第 11 行）

### B3-11 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 系统形态 ・ p.3

- 论断：该文旨在全面考察建筑平面图特征检索技术的关键方面，涵盖语义、空间、纹理与形状特征，并强调其意义与潜在应用。
- 引文："This paper aims to comprehensively investigate key aspects of building plan feature retrieval technology, including semantic, spatial, texture, and shape characteristics, while emphasizing their significance and potential applications." (Ling et al., 2025, p.3)
- 形式特征：完整句（源文件第 23 行）

### B3-12 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 案例或数据的表示形式 ・ p.1

- 论断：案例先按特征属性刻画、再转成目标案例。
- 引文："First, CBR needs to distinguish the characteristic attributes of the significant cases to form selection and then transforms them into target cases." (Zhang, 2006, p.1)
- 形式特征：完整句（源文件第 15 行）

### B3-13 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 评价方式 ・ p.5

- 论断：选型结果与工程实践相同。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)
- 形式特征：完整句（源文件第 27 行）

### B3-14 ・ Zhao2023_ShearWall_GNN ・ 案例或数据的表示形式 ・ p.2

- 论断：剪力墙结构以图数据表示，图由节点和边组成，结合节点位置特征后图是自然的向量化形式。
- 引文："data consist of graph nodes and edges. Combined with the location features of nodes, a graph is a natural vectorized form." (Zhao et al., 2023, p.2)
- 形式特征：首字母小写（源文件第 15 行）

### B3-15 ・ Zhao2023_ShearWall_GNN ・ 评价方式 ・ p.10

- 论断：每个模型在训练时执行十折交叉验证，并以验证集结果的平均值与标准差作为评价指标。
- 引文："Ten-fold cross-validation is performed for each model during training. Subsequently, the validation-set average and standard deviation of IoUpixel obtained from the ten-fold training sessions are used as specific evaluation indicators to evaluate the different graph representation methods and GNN models." (Zhao et al., 2023, p.10)
- 形式特征：完整句（源文件第 27 行）

### B3-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 案例或数据的表示形式 ・ p.2

- 论断：文献把平面图表示为显式建模形状、比例与位置的几何体，以及建模细分区域之间关系的图。
- 引文："Floor plans are digitally represented in various ways that each emphasize different components of interest e.g. as images allowing to model ﬁne-grained details such as materialization and furniture [21, 5], geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions [9, 13, 18, 12]." (van Engelenburg et al., 2023, p.2)
- 形式特征：完整句（源文件第 15 行）
