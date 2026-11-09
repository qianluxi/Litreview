# C4 剩余 83 条支撑轴审计结果（REST_B1–B5）

- 审计对象：`litrev/_probe/audit/REST_B1.md`–`REST_B5.md`，共 83 条（16/17/17/16/17）。
- 审计范围：131 条全量引文中，排除 `FRAGMENTS_v1.md` 已审的 48 条片段后的剩余条目。
- 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节 v1 口径修订）。
- 执行：5 个 `auditor` 在同一条 assistant 消息内并列派发；B3、B5 首次返回为空，已恢复同一会话补交（见第五节）。

## 一、总判定分布

| 轴 | 码 | 条数 | 占比 |
|---|---|---:|---:|
| 支撑 | SUPPORTED | 60 | 72.3% |
| 支撑 | PARTIAL | 23 | 27.7% |
| 支撑 | UNSUPPORTED | 0 | 0.0% |
| 自足 | SELF | 79 | 95.2% |
| 自足 | DEPENDENT | 4 | 4.8% |
| **合计** | — | **83** | **100%** |

## 二、按文献分布

| 文献 | 条数 | SUPPORTED | PARTIAL | UNSUPPORTED | SELF | DEPENDENT |
|---|---:|---:|---:|---:|---:|---:|
| AamodtPlaza1994_CBR_Foundations | 7 | 1 | 6 | 0 | 6 | 1 |
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 1 | 1 | 0 | 0 | 1 | 0 |
| Gu2024_ShearWall_Diffusion | 6 | 5 | 1 | 0 | 6 | 0 |
| Maher1987_ExpertSystems_StructuralDesign | 7 | 4 | 3 | 0 | 7 | 0 |
| Rodrigues2017_Clustering_FloorPlans | 6 | 3 | 3 | 0 | 5 | 1 |
| Roith2017_GraphBasedDesign_FederatedDB_VisEng | 7 | 7 | 0 | 0 | 7 | 0 |
| Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 7 | 7 | 0 | 0 | 6 | 1 |
| SharmaThesis_ContentBasedFloorPlanRetrieval | 7 | 7 | 0 | 0 | 7 | 0 |
| SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 7 | 5 | 2 | 0 | 7 | 0 |
| SriramMaherFenves1985_KBES_StructuralDesign | 2 | 2 | 0 | 0 | 2 | 0 |
| Survey2025_FloorPlanRetrieval_MDPI | 6 | 5 | 1 | 0 | 6 | 0 |
| Xia2025_CoDesign_ShearWallBeam_GNN | 7 | 3 | 4 | 0 | 7 | 0 |
| Zhao2023_ShearWall_GNN | 1 | 1 | 0 | 0 | 1 | 0 |
| delasHeras2014_RunlengthHistogram_FloorPlans | 6 | 6 | 0 | 0 | 6 | 0 |
| vanEngelenburg2023_SSIG_FloorPlan | 6 | 3 | 3 | 0 | 5 | 1 |
| **合计** | **83** | **60** | **23** | **0** | **79** | **4** |

## 三、待改清单（支撑轴，只列不改，交人）

共 23 条。每条四件套：现文论断 / 引文原文 / 缺什么 / 位置。

**R1-01 ・ AamodtPlaza1994_CBR_Foundations ・ 一句话主张 ・ p.1 ・ 源文件第 7 行**
- 现文论断：本文提出一个通用的描述框架，用于描述案例推理方法，后续的描述与讨论都参照该框架。
- 引文原文：“Initially, a general framework is defined, to which the subsequent descriptions and discussions will refer.”
- 缺什么：引文没有提到“用于描述案例推理方法”；请删去这一目的，或补充原文依据
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 7 行（一句话主张，p.1）

**R1-02 ・ AamodtPlaza1994_CBR_Foundations ・ 评价方式 ・ p.17 ・ 源文件第 27 行**
- 现文论断：评价以已部署应用的实际运行数据呈现，例如在 1990 年 12 月至 1991 年 9 月间处理了 20,000 个 non-conformance。
- 引文原文：“In the period December 90 - September 91 20.000 non-conformances were handled.”
- 缺什么：引文只给出了处理的数值，没有提到“已部署应用”和“评价”；请删去这些说法，或补充部署应用的依据
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 27 行（评价方式，p.17）

**R1-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 问题域 ・ p.1 ・ 源文件第 11 行**
- 现文论断：问题域是建筑平面图——生成式设计方法会产出大量候选平面方案，超出决策者的处理能力。
- 引文原文：“Generative design methods are able to produce a large number of potential solutions of architectural ﬂoor plans, which may be overwhelming for the decision-maker to cope with.”
- 缺什么：引文中的“may be overwhelming”被写成了“超出处理能力”，情态强度被提高；请补充“可能”
- 位置：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md` 第 11 行（问题域，p.1）

**R1-10 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 案例或数据的表示形式 ・ p.6 ・ 源文件第 15 行**
- 现文论断：案例以描述该案例的 19 个属性的取值来表示，这些取值构成案例描述，并被定义为案例表型。
- 引文原文：“The values that are associated with each of the 19 attributes in the description of a case make up the case description and can be deﬁned as the case phenotype (Fig. 3).”
- 缺什么：引文中的“can be defined”被改成了“被定义为”；请改成“可被定义为”
- 位置：`litrev/_probe/full/SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign.md` 第 15 行（案例或数据的表示形式，p.6）

**R1-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 系统形态 ・ p.13 ・ 源文件第 23 行**
- 现文论断：系统形态为可运行的设计—分析流程原型：研究中调用 AIStructure 接口自动布置楼板并施加荷载，再用 PKPM API 完成自动建模与力学分析。
- 引文原文：“This study utilized the AIStructure application programming interface (API) [30] to realize the rapid arrangement of floor slabs and application of loads to the beams and slabs. Subsequently, the PKPM API software development tool was employed to achieve automated structural modeling and mechanical analysis.”
- 缺什么：引文用的是“rapid arrangement”，没有提到“原型”；请删去“原型”和“自动”这类说法，或补充依据
- 位置：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md` 第 23 行（系统形态，p.13）

**R1-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 问题域 ・ p.1 ・ 源文件第 11 行**
- 现文论断：论文面向建筑设计中的平面图，认为建筑的构图结构是建筑品质的关键因素。
- 引文原文：“The compositional structure of a building is a key factor in the architectural quality.”
- 缺什么：引文没有提到“面向建筑设计中的平面图”；请删去这一说法，或补充依据
- 位置：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md` 第 11 行（问题域，p.1）

**R2-01 ・ AamodtPlaza1994_CBR_Foundations ・ 问题域 ・ p.7 ・ 源文件第 11 行**
- 现文论断：本文讨论的是案例推理的通用方法论，作者指出并不存在适用于每一个应用领域的通用案例推理方法。
- 引文原文：“As for AI in general, there are no universal CBR methods suitable for every domain of application.”
- 缺什么：首句“本文讨论的是通用方法论”在引文里没有对应，应删去，或补上原文依据
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 11 行（问题域，p.7）

**R2-02 ・ AamodtPlaza1994_CBR_Foundations ・ 明确写出的局限 ・ p.10 ・ 源文件第 31 行**
- 现文论断：作者明确指出，这种索引方式会随案例数量的增加而轻易导致索引的爆炸式增长。
- 引文原文：“This may easily lead to an explosive growth of indices with increased number of cases.”
- 缺什么：“会”加强了 may，应改为“可能轻易导致”
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 31 行（明确写出的局限，p.10）

**R2-06 ・ Rodrigues2017_Clustering_FloorPlans ・ 案例或数据的表示形式 ・ p.6 ・ 源文件第 15 行**
- 现文论断：每种描述子都表示成长度相同的数值向量（100 个值），因此表示类型不影响算法性能。
- 引文原文：“As the vector in every clustering process had the same length (100 values), the type of shape representation did not affect the performance of the algorithm.”
- 缺什么：引文只说“各聚类过程所用向量长度相同”，没有“每种描述子都表示成数值向量”这一内容，应删去或补上依据
- 位置：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md` 第 15 行（案例或数据的表示形式，p.6）

**R2-15 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 评价方式 ・ p.13 ・ 源文件第 27 行**
- 现文论断：评价采用与工程师设计对比的交并比（SIoU、BIoU）：协同设计方法的 SIoU 为 0.625、BIoU 为 0.548，顺序设计方法分别为 0.544 与 0.404。
- 引文原文：“The SIoU and BIoU obtained using the proposed co-design method were 0.625 and 0.548, respectively, whereas those obtained using the successive design method were 0.544 and 0.404, respectively.”
- 缺什么：原文作 successive design method，没有“工程师设计”，应删去或补上依据
- 位置：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md` 第 27 行（评价方式，p.13）

**R3-01 ・ AamodtPlaza1994_CBR_Foundations ・ 案例或数据的表示形式 ・ p.9 ・ 源文件第 15 行**
- 现文论断：案例记忆以泛化情节组织，泛化情节包含 norms、cases 与 indices 三类对象，norms 是其下所有案例共有的特征。
- 引文原文：“A generalized episode contains three different types of objects: Norms, cases and indices. Norms are features common to all cases indexed under a GE.”
- 缺什么：删去“案例记忆以泛化情节组织”，或补原文依据
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 15 行（案例或数据的表示形式，p.9）

**R3-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 系统形态 ・ p.6 ・ 源文件第 23 行**
- 现文论断：系统形态是已实现的专家系统原型，例如 HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文原文：“HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language.”
- 缺什么：删去“专家系统原型”，或补原文依据
- 位置：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md` 第 23 行（系统形态，p.6）

**R3-05 ・ Rodrigues2017_Clustering_FloorPlans ・ 系统形态 ・ p.2 ・ 源文件第 23 行**
- 现文论断：本文形态是在同一设置下把四种形状表示作为平面图设计描述子进行对比的实验研究。
- 引文原文：“In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings.”
- 缺什么：删去“对比/实验研究”，或补原文依据
- 位置：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md` 第 23 行（系统形态，p.2）

**R3-12 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 案例或数据的表示形式 ・ p.3 ・ 源文件第 15 行**
- 现文论断：平面图以高层语义特征与特征向量的形式表示，并用特征向量计算图像相似度。
- 引文原文：“By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans.”
- 缺什么：删去“以…形式表示”，或补原文依据
- 位置：`litrev/_probe/full/Survey2025_FloorPlanRetrieval_MDPI.md` 第 15 行（案例或数据的表示形式，p.3）

**R3-13 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 问题域 ・ p.1 ・ 源文件第 11 行**
- 现文论断：问题域为剪力墙与梁的结构方案布置；既有方法分别生成剪力墙或梁，未处理二者的相互依赖，因此需要剪力墙与梁的协同设计方法。
- 引文原文：“However, as the separate design of shear walls and beams fails to adequately address the strong interdependence of these components, an intelligent co-design approach for shear wall and beam structures is required.”
- 缺什么：将“生成”改为“分别设计”，或补原文依据
- 位置：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md` 第 11 行（问题域，p.1）

**R3-17 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 系统形态 ・ p.1 ・ 源文件第 23 行**
- 现文论断：产出形态是一个用 SSIG 对大规模平面图库排序的高效算法，作者称代码将公开。
- 引文原文：“In addition, an efﬁcient algorithm is developed that uses SSIG to rank a large-scale ﬂoor plan database.”
- 缺什么：删去“代码将公开”，引文无此内容
- 位置：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md` 第 23 行（系统形态，p.1）

**R4-03 ・ Maher1987_ExpertSystems_StructuralDesign ・ 一句话主张 ・ p.3 ・ 源文件第 7 行**
- 现文论断：作者将论文定位为介绍卡内基梅隆大学开发的四个专家系统，用以探索并界定初步设计阶段所做的决策。
- 引文原文：“The second part presents four expert systems, developed at Carnegie Mellon University, that explore and define the decisions made during preliminary design.”
- 缺什么：引文主语为“第二部分”，删“论文定位为”或补全文依据
- 位置：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md` 第 7 行（一句话主张，p.3）

**R4-04 ・ Maher1987_ExpertSystems_StructuralDesign ・ 评价方式 ・ p.7 ・ 源文件第 27 行**
- 现文论断：论文所述的评价方式是用线性评价函数评价备选结构方案。
- 引文原文：“HI-RISE evaluates alternatives with a linear evaluation function.”
- 缺什么：删“结构”（原文仅 alternatives），或补原文依据
- 位置：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md` 第 27 行（评价方式，p.7）

**R4-10 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 一句话主张 ・ p.1 ・ 源文件第 7 行**
- 现文论断：作者提出 M-RAM（多推理模型），通过分布式多推理机制向设计者提供经适应的既有设计方案，以辅助高层建筑结构设计的概念阶段。
- 引文原文：“This paper presents the M-RAM, which is intended to assist engineers in the conceptual phase of the structural design of tall buildings by providing designers with adapted past design solutions generated by a distributed multi-reasoning mechanism.”
- 缺什么：删“（多推理模型）”，或补原文对该缩写的定义
- 位置：`litrev/_probe/full/SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign.md` 第 7 行（一句话主张，p.1）

**R4-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 评价方式 ・ p.5 ・ 源文件第 27 行**
- 现文论断：评价使用 RPLAN 这一大规模平面图数据集，其含逾 80k 套带语义分割区域的亚洲单户公寓。
- 引文原文：“RPLAN is a large-scale dataset containing ﬂoor plan images with semantically segmented areas, consisting of >80k single-unit apartments across Asia.”
- 缺什么：引文仅描述 RPLAN，需补“用于评价”的原文依据
- 位置：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md` 第 27 行（评价方式，p.5）

**R5-01 ・ AamodtPlaza1994_CBR_Foundations ・ 系统形态 ・ p.6 ・ 源文件第 23 行**
- 现文论断：系统形态是理论性的描述框架，用两个互补的模型来代表对案例推理的两种视角。
- 引文原文：“The two models are complementary and represent two views on case-based reasoning.”
- 缺什么：删去"理论性的描述框架"，或补原文依据
- 位置：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md` 第 23 行（系统形态，p.6）

**R5-02 ・ Gu2024_ShearWall_Diffusion ・ 案例或数据的表示形式 ・ p.4 ・ 源文件第 15 行**
- 现文论断：该文用图像中的颜色编码不同构件与剪力墙。
- 引文原文：“Different components and shear walls can be encoded using the colors in the image.”
- 缺什么：can be encoded 为可能性，论断写成实际采用；改为"可用颜色编码"或补原文依据
- 位置：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md` 第 15 行（案例或数据的表示形式，p.4）

**R5-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 相似性或检索机制 ・ p.8 ・ 源文件第 19 行**
- 现文论断：机制不是相似度检索，而是把布置设计转化为图上的边标签预测：输入特征经 GraphSAGE 层与 MLP 组合每条边及其两端节点的特征，再由分类算法输出预测值。
- 引文原文：“The process of predicting edge labels using the GNN comprises passing the input features through GraphSAGE algorithm layers, followed by the application of an MLP to predict the edge features using the combined feature values of each edge and its two corresponding nodes as input. Finally, the feature information for each edge is processed using a classification algorithm to yield the corresponding predicted values.”
- 缺什么：删去"不是相似度检索"（引文未作此否定），并补"布置设计"原文依据
- 位置：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md` 第 19 行（相似性或检索机制，p.8）

## 四、与 T1 片段审计合并：131 条全量口径

| 集合 | 条数 | SUPPORTED | PARTIAL | UNSUPPORTED | SELF | DEPENDENT |
|---|---:|---:|---:|---:|---:|---:|
| 48 条片段（T1 原始判定，T3 扩句前） | 48 | 28 | 19 | 1 | 35 | 13 |
| 83 条非片段（T4） | 83 | 60 | 23 | 0 | 79 | 4 |
| **131 条合计（T3 扩句前）** | **131** | **88** | **42** | **1** | **114** | **17** |

- 支撑轴：131 条中 `SUPPORTED` 88、`PARTIAL` 42、`UNSUPPORTED` 1；非 SUPPORTED 共 43 条 = 32.8%。
- 自足轴：131 条中 `DEPENDENT` 17 条 = 13.0%（T3 扩句前的状态）。
- **T3 影响**：48 条片段里有 7 条 `SUPPORTED+DEPENDENT` 已扩句并通过 `verify`；支撑轴判定不变（未改论断），自足轴应在扩句后重判。若 7 条全部转 `SELF`，则 DEPENDENT 从 17 降到 10；本报告未对扩句后的 7 条重跑 auditor，故不把 10 写死。
- 注意：48 条片段是按形式判据挑出的风险子集，不是随机样本；但它与 83 条非片段恰好互补，所以 131 条的合计数是全量口径，不是抽样外推。

## 五、机械复核记录

- **条数**：B1 16、B2 17、B3 17、B4 16、B5 17，合计 83；id 行序与批次文件 1:1。
- **依据列**：脚本逐条检查 `basis in quote`，83/83 命中，0 失败。其中 R4-05 首次写成 `72 floor plans`，与原文连字 `72 ﬂoor plans` 不逐字，已由同一 auditor 会话改为 `72 ﬂoor plans` 后复检通过。
- **合计行**：B1 `10/6/0；D0`、B2 `13/4/0；D2`、B3 `11/6/0；D1`、B4 `12/4/0；D0`、B5 `14/3/0；D1`，均与逐行统计一致。
- **总合计**：83 条（SUPPORTED 60 / PARTIAL 23 / UNSUPPORTED 0；DEPENDENT 4）。
- **空返回处置**：B3 `ses_e410043f0ffe9jZNHcSEWBUX2z` 与 B5 `ses_e41004245ffei11FdzVUZwDPzd` 首次 result 为空，均恢复同一会话补交 17 行；未新建第二个会话。B1 `ses_e4100460dffekawPp6sMmJWuIP`、B2 `ses_e410044deffeaNTH6EbC7l6Uze`、B4 `ses_e41004326ffefMjs8J0mrJ05gv` 首次即完整。

## 六、批次文件与原始输出

```
REST_B1.md / REST_B2.md / REST_B3.md / REST_B4.md / REST_B5.md   批次输入
out_R1.md  / out_R2.md  / out_R3.md  / out_R4.md  / out_R5.md   原始判定表
```