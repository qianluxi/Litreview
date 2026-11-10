# 人工金标准 G1（25 条，开卷裁定）

> 由 `python tools/audit_prep.py golden` 生成，seed=43，分层（SUPPORTED 15 / PARTIAL 9 / UNSUPPORTED 1）。
> **这是给人填的表，不是给子代理的**：不进 `BATCHES.json`、不生成 agent、`auditor-*` 的 read 白名单不含本文件。
> 判定者可读卡片原文（开卷），独立于判定表给出判定——这是项目唯一的「判得对」参照系。
> 填法：在下表每行填 支撑/自足/依据/缺什么，照契约 §四 表头与判定码；首行原样抄本文件的 `> 快照 sha1:`。
> 不要读 `out_*.md`、`SAMPLE_S1_KEYS.md`、`GOLDEN_MAP.md`；可以读 `litrev/_probe/full/*.md` 卡片原文。
> 快照 sha1: d46f9e7c3f

## 待填判定表（照契约 §四，人填）

| id  | 支撑          | 自足        | 引文里的依据（≤15 字，必须是引文原词）          | 缺什么 / 需补的一句                            |
| --- | ----------- | --------- | ------------------------------ | -------------------------------------- |
| G01 | UNSUPPORTED | SELF      | "to illustrate"                | 引文未触及 CBR/相似度度量问题域，论断主体无依据             |
| G02 | PARTIAL     | SELF      | "being developed"              | "案例"超出引文（止于 failure analysis），需补 cases |
| G03 | PARTIAL     | SELF      | "Ward linkage"                 | 引文止于 distance as，"度量"一词不在引文内           |
| G04 | PARTIAL     | SELF      | "implemented in"               | "原型形态"无依据（引文无 prototype），范围放大          |
| G05 | PARTIAL     | DEPENDENT | "can overcome"                 | such 指代对象不在引文内，"现有案例检索方法"需补            |
| G06 | SUPPORTED   | SELF      | "mature and systematic theory" | —                                      |
| G07 | PARTIAL     | SELF      | "supply the system"            | "子系统""构成"无依据，引文只说 supply               |
| G08 | PARTIAL     | SELF      | "could be"                     | "取值"超出引文，could be 升级为实际                |
| G09 | SUPPORTED   | SELF      | "GNN-based shear wall"         | —                                      |
| G10 | SUPPORTED   | SELF      | "characteristic attributes"    | —                                      |
| G11 | PARTIAL     | DEPENDENT | "the same with"                | This 指代不在引文内，"验证依据"超出引文                |
| G12 | SUPPORTED   | SELF      | "frames and rules"             | —                                      |
| G13 | PARTIAL     | SELF      | "key factor"                   | "面向建筑设计中的平面图"引文无依据                     |
| G14 | PARTIAL     | SELF      | "no universal"                 | "本文讨论通用方法论"引文无对应                       |
| G15 | SUPPORTED   | SELF      | "combines CBR"                 | —                                      |
| G16 | SUPPORTED   | SELF      | "conceptual design"            | —                                      |
| G17 | SUPPORTED   | SELF      | "0.247"                        | —                                      |
| G18 | PARTIAL     | SELF      | "surface match"                | PATDEX 不在引文内，论断主体为引文外专有名词              |
| G19 | SUPPORTED   | SELF      | "12 fingerprints"              | —                                      |
| G20 | SUPPORTED   | SELF      | "XML-based"                    | —                                      |
| G21 | SUPPORTED   | SELF      | "tree editing distance"        | —                                      |
| G22 | SUPPORTED   | SELF      | "perceptual model"             | —                                      |
| G23 | PARTIAL     | SELF      | "can be encoded"               | can be 可能性写成实际采用，情态升级                  |
| G24 | SUPPORTED   | DEPENDENT | "same shape type"              | it 指代 this descriptor，需补主语             |
| G25 | SUPPORTED   | SELF      | "production rules"             | —                                      |
合计：25 条（SUPPORTED 13 / PARTIAL 11 / UNSUPPORTED 1；DEPENDENT 3）

## 条目详情（判定时可读卡片原文，开卷）

### G01 ・ Liao1998_SimilarityMeasures_CBR ・ 问题域 ・ p.13

- 论断：该文的问题域是 CBR 案例检索中的相似度度量（通用方法），并以失效分析为示例应用领域。
- 引文："analysis (Esaklul, 1990) is used to illustrate that applications with a mixture" (Liao et al., 1998, p.13)
- 卡片：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md`（可读原文上下文）

### G02 ・ Liao1998_SimilarityMeasures_CBR ・ 系统形态 ・ p.13

- 论断：该文所依托的系统是一个正在开发、用于存储失效分析案例的 CBR 系统。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)
- 卡片：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md`（可读原文上下文）

### G03 ・ Rodrigues2017_Clustering_FloorPlans ・ 相似性或检索机制 ・ p.4

- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as" (Rodrigues et al., 2017, p.4)
- 卡片：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md`（可读原文上下文）

### G04 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 系统形态 ・ p.7

- 论断：文中系统以已实现的原型形态给出，例如 HI-RISE 在 PSRL 中实现。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)
- 卡片：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md`（可读原文上下文）

### G05 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 一句话主张 ・ p.1

- 论断：作者主张所提出的智能案例检索方法能够克服现有案例检索方法的若干不足。
- 引文："this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO." (Zhang, 2006, p.1)
- 卡片：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`（可读原文上下文）

### G06 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 明确写出的局限 ・ p.2

- 论断：作者明确指出网络拓扑结构的确定缺乏成熟、系统的理论。
- 引文："There are only some experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory." (Zhang, 2006, p.2)
- 卡片：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`（可读原文上下文）

### G07 ・ Borner1993_StructuralSimilarity_CBR ・ 系统形态 ・ p.9

- 论断：系统由 SynTerm 与 SynGraph 两个子系统构成，二者为同一系统提供专项设计问题的解法。
- 引文："SynTerm and SynGraph supply the system with solutions for special design problems" (Borner, 1993, p.9)
- 卡片：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md`（可读原文上下文）

### G08 ・ Liao1998_SimilarityMeasures_CBR ・ 案例或数据的表示形式 ・ p.14

- 论断：失效分析案例以属性（attribute）表示，属性再与相应的取值相关联。
- 引文："The attributes used to represent failure cases could be associated with" (Liao et al., 1998, p.14)
- 卡片：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md`（可读原文上下文）

### G09 ・ Zhao2023_ShearWall_GNN ・ 系统形态 ・ p.3

- 论断：系统形态是作者建立的一套基于 GNN 的剪力墙布置设计方法，并以图 1 给出其方法流程。
- 引文："This study establishes a GNN-based shear wall layout design method, as shown in Figure 1. The developed method consists of three" (Zhao et al., 2023, p.3)
- 卡片：`litrev/_probe/full/Zhao2023_ShearWall_GNN.md`（可读原文上下文）

### G10 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 案例或数据的表示形式 ・ p.1

- 论断：案例先按特征属性刻画、再转成目标案例。
- 引文："First, CBR needs to distinguish the characteristic attributes of the significant cases to form selection and then transforms them into target cases." (Zhang, 2006, p.1)
- 卡片：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`（可读原文上下文）

### G11 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 评价方式 ・ p.5

- 论断：以工程实例的检索结果与工程实际选型相同作为验证依据。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)
- 卡片：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`（可读原文上下文）

### G12 ・ Maher1987_ExpertSystems_StructuralDesign ・ 案例或数据的表示形式 ・ p.6

- 论断：论文所述的知识表示形式是框架与规则，过程性知识则以 Lisp 函数表示。
- 引文："The declarative knowledge is represented in the form of frames and rules and the procedural knowledge in the form of Lisp functions." (Maher, 1987, p.6)
- 卡片：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md`（可读原文上下文）

### G13 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 问题域 ・ p.1

- 论断：论文面向建筑设计中的平面图，认为建筑的构图结构是建筑品质的关键因素。
- 引文："The compositional structure of a building is a key factor in the architectural quality." (van Engelenburg et al., 2023, p.1)
- 卡片：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md`（可读原文上下文）

### G14 ・ AamodtPlaza1994_CBR_Foundations ・ 问题域 ・ p.7

- 论断：本文讨论的是案例推理的通用方法论，作者指出并不存在适用于每一个应用领域的通用案例推理方法。
- 引文："As for AI in general, there are no universal CBR methods suitable for every domain of application." (Aamodt and Plaza, 1994, p.7)
- 卡片：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md`（可读原文上下文）

### G15 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 一句话主张 ・ p.1

- 论断：作者主张其新颖性在于把 CBR、精确图匹配与不精确图匹配组合在同一个系统中，用于建筑平面图检索。
- 引文："The novelty of our approach is that it combines CBR, exact, and inexact graph matching in one system in the domain of retrieval of architectural ﬂoor plans." (Sabri et al., 2017, p.1)
- 卡片：`litrev/_probe/full/Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM.md`（可读原文上下文）

### G16 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 问题域 ・ p.1

- 论断：问题域是建筑平面图的概念设计，以及在该阶段检索相似的平面图。
- 引文："Until today, for the conceptual design of architectural ﬂoor plans, architects widely follow the traditional pen and paper based method to draw the conceptual ﬂoor plans, and retrieve the similar ﬂoor plans in the printed reference collections." (Sabri et al., 2017, p.1)
- 卡片：`litrev/_probe/full/Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM.md`（可读原文上下文）

### G17 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 评价方式 ・ p.143

- 论断：在 ROBIN 数据集上以 Mean Average Precision（MAP）评价；仅考虑房间布局时，检索得到的 MAP 值为 0.247。
- 引文："The Mean Average Precision (MAP) value obtained during retrieval on the ROBIN dataset was observed to be 0.247 in case only room layout was considered while retrieval, on the other hand incorporating both room layout and room decor features made retrieval quite specific." (Sharma, 2018, p.143)
- 卡片：`litrev/_probe/full/SharmaThesis_ContentBasedFloorPlanRetrieval.md`（可读原文上下文）

### G18 ・ AamodtPlaza1994_CBR_Foundations ・ 相似性或检索机制 ・ p.12

- 论断：PATDEX 使用一个依赖领域但全局的相似性度量，基于表层匹配来评估相似性。
- 引文："A domain-dependent, but global similarity metric is used to assess similarity based on surface match." (Aamodt and Plaza, 1994, p.12)
- 卡片：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md`（可读原文上下文）

### G19 ・ Roith2017_GraphBasedDesign_FederatedDB_VisEng ・ 相似性或检索机制 ・ p.7

- 论断：作者目前定义了 12 个指纹，用于检查节点属性、边属性或完全图同构。
- 引文："We have currently defined 12 fingerprints that check, for example, properties of nodes, edges or full graph isomorphism (Weber et al. 2011)." (Roith et al., 2017, p.7)
- 卡片：`litrev/_probe/full/Roith2017_GraphBasedDesign_FederatedDB_VisEng.md`（可读原文上下文）

### G20 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 案例或数据的表示形式 ・ p.4

- 论断：平面图数据用 AGraphML 这种基于 XML 的表示形式来描述。
- 引文："AGraphML is the XML-based representation for ﬂoor plans. The speciﬁcation (Langenhan, 2015) of AGraphML deﬁnes attributes for this representation." (Sabri et al., 2017, p.4)
- 卡片：`litrev/_probe/full/Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM.md`（可读原文上下文）

### G21 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 相似性或检索机制 ・ p.14

- 论断：检索以树编辑距离作为衡量查询相似度的度量。
- 引文："Floor plan retrieval is then executed using tree editing distance as a metric for query similarity." (Ling et al., 2025, p.14)
- 卡片：`litrev/_probe/full/Survey2025_FloorPlanRetrieval_MDPI.md`（可读原文上下文）

### G22 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 一句话主张 ・ p.10

- 论断：作者主张本文提出了一个用于描述建筑平面图绘图风格的感知模型。
- 引文："In this paper we have proposed a perceptual model to describe the drawing style in architectural plans." (de las Heras et al., 2014, p.10)
- 卡片：`litrev/_probe/full/delasHeras2014_RunlengthHistogram_FloorPlans.md`（可读原文上下文）

### G23 ・ Gu2024_ShearWall_Diffusion ・ 案例或数据的表示形式 ・ p.4

- 论断：该文用图像中的颜色编码不同构件与剪力墙。
- 引文："Different components and shear walls can be encoded using the colors in the image." (Gu et al., 2024, p.4)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### G24 ・ Rodrigues2017_Clustering_FloorPlans ・ 明确写出的局限 ・ p.13

- 论断：作者明确写出 TD 描述子的一个局限：同一形状类型的设计可能因对外墙每次转折处线段尺寸的敏感度而被判为不同。
- 引文："Another issue was found with this descriptor. In some cases, when designs have the same shape type, it may consider distinct due to the sensitivity over the size of the segments in every turn of the exterior wall (see groups F and G in Fig. 9 as an example)." (Rodrigues et al., 2017, p.13)
- 卡片：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md`（可读原文上下文）

### G25 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 案例或数据的表示形式 ・ p.8

- 论断：系统的过程性知识以产生式规则和 LISP 函数表示。
- 引文："The procedural knowledge is represented by production rules and LISP functions." (Sriram et al., 1985, p.8)
- 卡片：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md`（可读原文上下文）
