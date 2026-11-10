# G1 金标准映射（主控侧留档，不贴给任何人）

> 由 `python tools/audit_prep.py golden` 生成，与 `GOLDEN.md` 同源。
> 判定表总条目 131 · 分层抽 25 条 · seed=43。
> 输入快照戳：`d46f9e7c3f`
> **本文件是答案键**：记录每条 G id 对应的原批次 id 与原判定。判定者填 `GOLDEN.md` 时读不到本文件。
> 人填完后跑 `python tools/audit_prep.py verify-golden` 比对，输出一致率与方向分布。
> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`golden --check` 仍按抽样时点复现。

<!-- picks: B1-06,B1-07,B1-10,B1-11,B1-12,B1-14,B2-04,B2-06,B2-15,B3-12,B3-13,R1-04,R1-16,R2-01,R2-09,R3-07,R3-10,R4-01,R4-06,R4-07,R4-12,R4-14,R5-02,R5-06,R5-12 -->

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
