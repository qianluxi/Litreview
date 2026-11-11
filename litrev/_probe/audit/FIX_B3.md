# C4 改稿后定点重判（13 条，闭卷，第三轮 · 换引文）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（v1.2，含 §八 自足轴三族边界）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF、`texts/*.txt` 或 `full/*.md`。只依据下面给出的论断与引文判定。
> 这 13 条上一轮判为非 SUPPORTED，原因是**引文被截断/缺主语或方向不符**，本轮已在原文里找到
> 含主谓的完整句替换引文（引文按 OCR 原样抄录，断词连字、连字符换行均保留，不算错误）。
> 其中 5 条论断同步做了最小改写以贴齐新引文；请**逐字读当前论断**，不要凭上一轮印象下结论。
> 注意：引文变长会改变自足轴（原本靠上下文才能懂的片段可能变成完整句，反之亦然），
> **自足轴必须独立重判**，不许照抄上一轮。
> **依据列必须是从该条引文中逐字连续截取的一段（≤15 字），不得拼接、缩写、改写**；
> 例如引文写 `the attributes and values in the problem spec- ification`，
> 可填 `attributes and values`，不可填 `attributes-value`（跨词拼接）。
> 写 `SUPPORTED` 时依据列必须填；写 `PARTIAL`/`UNSUPPORTED` 时必须在末列写明缺哪个成分、该怎么补。
> 快照 sha1: a154464802

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词，连续片段） | 缺什么/需补的一句 |
|----|------|------|----------------------------------------|--------------------|

### B1-06 ・ Liao1998_SimilarityMeasures_CBR ・ 问题域 ・ p.2

- 论断：该文以 CBR 案例检索中的相似度度量为主题，并以失效分析为示例应用领域。
- 引文："This article focuses on the similarity measuring methods for CBR and comprises two parts. The rst part reviews the existing methods for measuring similarity in the literature based on more than 100 CBR project studies and some general similarity measures seen in other applications. In the second part, a hybrid similarity measure is proposed for comparing cases with a mixture of crisp and fuzzy features. Its application to the domain of failure analysis is illustrated." (Liao et al., 1998, p.2)
- 形式特征：完整句（源文件第 11 行）

### B1-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1

- 论断：作者从结构设计项目的资料中定位案例来源，资料来自悉尼一家工程咨询公司。
- 引文："We began our CBR projects by locating a source of information on structural design projects-a well-known engineering consulting firmthat has worked on many medium- to high-rise buildings in Sydney." (Maher and Gomez, 1996, p.1)
- 形式特征：完整句（源文件第 11 行）

### B1-12 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 一句话主张 ・ p.1

- 论断：作者主张该智能案例检索方法能克服学习能力差、检索效率低、智能水平不足等缺陷，并为高层结构 IFO 的案例检索提供更科学的方法。
- 引文："The result shows. this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO." (Zhang, 2006, p.1)
- 形式特征：完整句（源文件第 7 行）

### B2-11 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 明确写出的局限 ・ p.19

- 论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文："However, their full-scale practical implementation will require higher- level expert system development tools, notably in the areas of user interfaces, explanation capabilities and knowledge-acquisition capabilities." (Sriram et al., 1985, p.19)
- 形式特征：完整句（源文件第 30 行）

### B3-01 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 相似性或检索机制 ・ p.3

- 论断：作者认为子图匹配方法在检索算法上是有前景的路线。
- 引文："As for the retrieval algorithm, subgraph matching approaches seem to be promising." (Ahmed et al., 2013, p.3)
- 形式特征：完整句（源文件第 19 行）

### B3-05 ・ Liao1998_SimilarityMeasures_CBR ・ 一句话主张 ・ p.3

- 论断：该文在第二部分提出一种混合相似度度量，用于案例之间的比较。
- 引文："In part 2, a hybrid similarity measure is proposed to compare cases having a mixture of crisp and fuzzy features." (Liao et al., 1998, p.3)
- 形式特征：完整句（源文件第 7 行）

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

### B3-15 ・ Zhao2023_ShearWall_GNN ・ 评价方式 ・ p.10

- 论断：每个模型在训练时执行十折交叉验证，并以验证集结果的平均值与标准差作为评价指标。
- 引文："Ten-fold cross-validation is performed for each model during training. Subsequently, the validation-set average and standard deviation of IoUpixel obtained from the ten-fold training sessions are used as specific evaluation indicators to evaluate the different graph representation methods and GNN models." (Zhao et al., 2023, p.10)
- 形式特征：完整句（源文件第 27 行）

### R4-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 评价方式 ・ p.5

- 论断：评价使用 RPLAN 这一大规模平面图数据集，其含逾 80k 套带语义分割区域的亚洲单户公寓。
- 引文："In this paper, RPLAN [26] is used for analysis and eval- uation. RPLAN is a large-scale dataset containing ﬂoor plan images with semantically segmented areas, consisting of >80k single-unit apartments across Asia." (van Engelenburg et al., 2023, p.5)
- 源文件：第 27 行
