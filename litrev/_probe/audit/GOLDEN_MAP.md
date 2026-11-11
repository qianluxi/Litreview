# G1 金标准映射（主控侧留档，不贴给任何人）

> 由 `python tools/audit_prep.py golden` 生成，与 `GOLDEN.md` 同源。
> 判定表总条目 131 · 分层抽 25 条 · seed=43。
> 输入快照戳：`d46f9e7c3f`
> **本文件是答案键**：记录每条 G id 对应的原批次 id 与原判定。判定者填 `GOLDEN.md` 时读不到本文件。
> 人填完后跑 `python tools/audit_prep.py verify-golden` 比对，输出一致率与方向分布。
> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`golden --check` 仍按抽样时点复现。

<!-- picks: total=131,B1-06,B1-07,B1-10,B1-11,B1-12,B1-14,B2-04,B2-06,B2-15,B3-12,B3-13,R1-04,R1-16,R2-01,R2-09,R3-07,R3-10,R4-01,R4-06,R4-07,R4-12,R4-14,R5-02,R5-06,R5-12 -->

## 对照表（G id → 原判定）

| G id | 原批次 id | 文献 | 节 | 原支撑 | 原自足 | 原依据 | 原缺什么 |
|---|---|---|---|---|---|---|---|
| G01 | B1-06 | Liao1998_SimilarityMeasures_CBR | 问题域 | UNSUPPORTED | SELF | "to illustrate" | 引文只说某分析被用来举例，未触及"相似度度量"问题域；需换引文 |
| G02 | B1-07 | Liao1998_SimilarityMeasures_CBR | 系统形态 | PARTIAL | SELF | "being developed" | 删"案例"（引文止于 failure analysis），或补原文 cases；"该文所依托"需补依据 |
| G03 | B1-10 | Rodrigues2017_Clustering_FloorPlans | 相似性或检索机制 | SUPPORTED | SELF | "Ward linkage" | — |
| G04 | B1-11 | SriramMaherFenves1985_KBES_StructuralDesign | 系统形态 | PARTIAL | SELF | "implemented in" | 引文只给 HI-RISE 一例且未称 prototype；"原型形态""文中系统"无依据 |
| G05 | B1-12 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 一句话主张 | PARTIAL | DEPENDENT | "can overcome" | "现有案例检索方法"是 such 的指代，引文内无指代对象；需补原句或写明指代 |
| G06 | B1-14 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 明确写出的局限 | SUPPORTED | SELF | "mature and" | — |
| G07 | B2-04 | Borner1993_StructuralSimilarity_CBR | 系统形态 | PARTIAL | SELF | "special design" | 原文只说 supply the system，未称二者为子系统/构成系统 |
| G08 | B2-06 | Liao1998_SimilarityMeasures_CBR | 案例或数据的表示形式 | PARTIAL | SELF | "could be" | "could be" 被写成"相关联"，"取值"原文无依据 |
| G09 | B2-15 | Zhao2023_ShearWall_GNN | 系统形态 | SUPPORTED | SELF | "Figure 1" | — |
| G10 | B3-12 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 案例或数据的表示形式 | SUPPORTED | SELF | "characteristic" | — |
| G11 | B3-13 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 评价方式 | PARTIAL | DEPENDENT | "the same with" | 补"验证依据""工程实例"依据（原文为 practice engineering） |
| G12 | R1-04 | Maher1987_ExpertSystems_StructuralDesign | 案例或数据的表示形式 | SUPPORTED | SELF | "in the form of frames and rules" | — |
| G13 | R1-16 | vanEngelenburg2023_SSIG_FloorPlan | 问题域 | PARTIAL | SELF | "a key factor in the architectural quality" | 引文没有提到“面向建筑设计中的平面图”；请删去这一说法，或补充依据 |
| G14 | R2-01 | AamodtPlaza1994_CBR_Foundations | 问题域 | PARTIAL | SELF | "no universal" | 首句“本文讨论的是通用方法论”在引文里没有对应，应删去，或补上原文依据 |
| G15 | R2-09 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 一句话主张 | SUPPORTED | SELF | "combines CBR" | — |
| G16 | R3-07 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 问题域 | SUPPORTED | SELF | "the conceptual" | — |
| G17 | R3-10 | SharmaThesis_ContentBasedFloorPlanRetrieval | 评价方式 | SUPPORTED | SELF | "0.247 in case" | — |
| G18 | R4-01 | AamodtPlaza1994_CBR_Foundations | 相似性或检索机制 | SUPPORTED | SELF | "surface match" | — |
| G19 | R4-06 | Roith2017_GraphBasedDesign_FederatedDB_VisEng | 相似性或检索机制 | SUPPORTED | SELF | "12 fingerprints" | — |
| G20 | R4-07 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 案例或数据的表示形式 | SUPPORTED | SELF | "XML-based" | — |
| G21 | R4-12 | Survey2025_FloorPlanRetrieval_MDPI | 相似性或检索机制 | SUPPORTED | SELF | "tree editing" | — |
| G22 | R4-14 | delasHeras2014_RunlengthHistogram_FloorPlans | 一句话主张 | SUPPORTED | SELF | "drawing style" | — |
| G23 | R5-02 | Gu2024_ShearWall_Diffusion | 案例或数据的表示形式 | PARTIAL | SELF | "can be encoded" | can be encoded 为可能性，论断写成实际采用；改为"可用颜色编码"或补原文依据 |
| G24 | R5-06 | Rodrigues2017_Clustering_FloorPlans | 明确写出的局限 | SUPPORTED | DEPENDENT | "same shape type" | 引文 it 需补主语 |
| G25 | R5-12 | SriramMaherFenves1985_KBES_StructuralDesign | 案例或数据的表示形式 | SUPPORTED | SELF | "LISP functions" | — |

> 共 25 条。

## 原文存档（抽样时点，返工后按此复现）

> 判定时点给出的论断与引文原文。稿件返工后**本节不改写**：`GOLDEN.md` 的条目详情按本节复现，
> `verify-golden` 用本节 vs 当前批次输入比对，把判后被返工的条目列为「失效」并从分母剔除。

### G01 ・ B1-06

- 论断：该文的问题域是 CBR 案例检索中的相似度度量（通用方法），并以失效分析为示例应用领域。
- 引文："analysis (Esaklul, 1990) is used to illustrate that applications with a mixture" (Liao et al., 1998, p.13)

### G02 ・ B1-07

- 论断：该文所依托的系统是一个正在开发、用于存储失效分析案例的 CBR 系统。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)

### G03 ・ B1-10

- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as" (Rodrigues et al., 2017, p.4)

### G04 ・ B1-11

- 论断：文中系统以已实现的原型形态给出，例如 HI-RISE 在 PSRL 中实现。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)

### G05 ・ B1-12

- 论断：作者主张所提出的智能案例检索方法能够克服现有案例检索方法的若干不足。
- 引文："this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO." (Zhang, 2006, p.1)

### G06 ・ B1-14

- 论断：作者明确指出网络拓扑结构的确定缺乏成熟、系统的理论。
- 引文："There are only some experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory." (Zhang, 2006, p.2)

### G07 ・ B2-04

- 论断：系统由 SynTerm 与 SynGraph 两个子系统构成，二者为同一系统提供专项设计问题的解法。
- 引文："SynTerm and SynGraph supply the system with solutions for special design problems" (Borner, 1993, p.9)

### G08 ・ B2-06

- 论断：失效分析案例以属性（attribute）表示，属性再与相应的取值相关联。
- 引文："The attributes used to represent failure cases could be associated with" (Liao et al., 1998, p.14)

### G09 ・ B2-15

- 论断：系统形态是作者建立的一套基于 GNN 的剪力墙布置设计方法，并以图 1 给出其方法流程。
- 引文："This study establishes a GNN-based shear wall layout design method, as shown in Figure 1. The developed method consists of three" (Zhao et al., 2023, p.3)

### G10 ・ B3-12

- 论断：案例先按特征属性刻画、再转成目标案例。
- 引文："First, CBR needs to distinguish the characteristic attributes of the significant cases to form selection and then transforms them into target cases." (Zhang, 2006, p.1)

### G11 ・ B3-13

- 论断：以工程实例的检索结果与工程实际选型相同作为验证依据。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)

### G12 ・ R1-04

- 论断：论文所述的知识表示形式是框架与规则，过程性知识则以 Lisp 函数表示。
- 引文："The declarative knowledge is represented in the form of frames and rules and the procedural knowledge in the form of Lisp functions." (Maher, 1987, p.6)

### G13 ・ R1-16

- 论断：论文面向建筑设计中的平面图，认为建筑的构图结构是建筑品质的关键因素。
- 引文："The compositional structure of a building is a key factor in the architectural quality." (van Engelenburg et al., 2023, p.1)

### G14 ・ R2-01

- 论断：本文讨论的是案例推理的通用方法论，作者指出并不存在适用于每一个应用领域的通用案例推理方法。
- 引文："As for AI in general, there are no universal CBR methods suitable for every domain of application." (Aamodt and Plaza, 1994, p.7)

### G15 ・ R2-09

- 论断：作者主张其新颖性在于把 CBR、精确图匹配与不精确图匹配组合在同一个系统中，用于建筑平面图检索。
- 引文："The novelty of our approach is that it combines CBR, exact, and inexact graph matching in one system in the domain of retrieval of architectural ﬂoor plans." (Sabri et al., 2017, p.1)

### G16 ・ R3-07

- 论断：问题域是建筑平面图的概念设计，以及在该阶段检索相似的平面图。
- 引文："Until today, for the conceptual design of architectural ﬂoor plans, architects widely follow the traditional pen and paper based method to draw the conceptual ﬂoor plans, and retrieve the similar ﬂoor plans in the printed reference collections." (Sabri et al., 2017, p.1)

### G17 ・ R3-10

- 论断：在 ROBIN 数据集上以 Mean Average Precision（MAP）评价；仅考虑房间布局时，检索得到的 MAP 值为 0.247。
- 引文："The Mean Average Precision (MAP) value obtained during retrieval on the ROBIN dataset was observed to be 0.247 in case only room layout was considered while retrieval, on the other hand incorporating both room layout and room decor features made retrieval quite specific." (Sharma, 2018, p.143)

### G18 ・ R4-01

- 论断：PATDEX 使用一个依赖领域但全局的相似性度量，基于表层匹配来评估相似性。
- 引文："A domain-dependent, but global similarity metric is used to assess similarity based on surface match." (Aamodt and Plaza, 1994, p.12)

### G19 ・ R4-06

- 论断：作者目前定义了 12 个指纹，用于检查节点属性、边属性或完全图同构。
- 引文："We have currently defined 12 fingerprints that check, for example, properties of nodes, edges or full graph isomorphism (Weber et al. 2011)." (Roith et al., 2017, p.7)

### G20 ・ R4-07

- 论断：平面图数据用 AGraphML 这种基于 XML 的表示形式来描述。
- 引文："AGraphML is the XML-based representation for ﬂoor plans. The speciﬁcation (Langenhan, 2015) of AGraphML deﬁnes attributes for this representation." (Sabri et al., 2017, p.4)

### G21 ・ R4-12

- 论断：检索以树编辑距离作为衡量查询相似度的度量。
- 引文："Floor plan retrieval is then executed using tree editing distance as a metric for query similarity." (Ling et al., 2025, p.14)

### G22 ・ R4-14

- 论断：作者主张本文提出了一个用于描述建筑平面图绘图风格的感知模型。
- 引文："In this paper we have proposed a perceptual model to describe the drawing style in architectural plans." (de las Heras et al., 2014, p.10)

### G23 ・ R5-02

- 论断：该文用图像中的颜色编码不同构件与剪力墙。
- 引文："Different components and shear walls can be encoded using the colors in the image." (Gu et al., 2024, p.4)

### G24 ・ R5-06

- 论断：作者明确写出 TD 描述子的一个局限：同一形状类型的设计可能因对外墙每次转折处线段尺寸的敏感度而被判为不同。
- 引文："Another issue was found with this descriptor. In some cases, when designs have the same shape type, it may consider distinct due to the sensitivity over the size of the segments in every turn of the exterior wall (see groups F and G in Fig. 9 as an example)." (Rodrigues et al., 2017, p.13)

### G25 ・ R5-12

- 论断：系统的过程性知识以产生式规则和 LISP 函数表示。
- 引文："The procedural knowledge is represented by production rules and LISP functions." (Sriram et al., 1985, p.8)
