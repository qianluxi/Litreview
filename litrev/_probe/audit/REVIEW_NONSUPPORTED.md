# 非 SUPPORTED 人工复核清单

> 由 `python tools/audit_prep.py review` 从当前 8 张判定表生成；契约 §五.3：任何非 SUPPORTED 必须人看。
> 共 50 条：PARTIAL 49 / UNSUPPORTED 1 / 判定表总条目 131。
> 本清单只做待办登记，`复核结论` 与 `处理` 两栏由人填写；判定表一改就重新生成，不要手改条目。
> 引文与论断来自批次输入（已由 `audit-stale` 证明等于卡片当前文字），不要凭记忆改写。

## 按批次分布

| 批次输入 | 待复核 |
|---|---|
| `FRAG_B1.md` | 10 |
| `FRAG_B2.md` | 8 |
| `FRAG_B3.md` | 9 |
| `REST_B1.md` | 6 |
| `REST_B2.md` | 4 |
| `REST_B3.md` | 6 |
| `REST_B4.md` | 4 |
| `REST_B5.md` | 3 |

## 逐条

### 01 · B1-02 · Ahmed2013_Analysis_SketchRetrieval_FloorPlans · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："implemented for"
- 缺什么：删去"触控笔桌"（引文只说实现的平台名），或补原文对 Touch & Write 的说明
- 论断：系统形态是为 Touch & Write 触控笔桌实现的原型。
- 引文："the prototype is implemented for the Touch & Write" (Ahmed et al., 2013, p.8)
- 复核结论（人填）：
- 处理（人填）：

### 02 · B1-04 · Borner1993_StructuralSimilarity_CBR · 相似性或检索机制

- 当前判定：PARTIAL / SELF
- 引文里的依据："can be done"
- 缺什么：引文是 can be done（可能性），论断写成实然"先做"；改为"可以先通过…"
- 论断：检索流程先对新问题做低成本的表面相似性初始分析。
- 引文："The rst initial analysis of the new problem can be done by an inexpensive surface similarity assessment based on the attribute based descriptions" (Borner, 1993, p.6)
- 复核结论（人填）：
- 处理（人填）：

### 03 · B1-05 · Borner1993_StructuralSimilarity_CBR · 明确写出的局限

- 当前判定：PARTIAL / SELF
- 引文里的依据："not addressed"
- 缺什么：补回"在本实现中"：引文限定 in this implementation，论断放大为普遍未处理
- 论断：作者明确写出，修改规则条件或权重的学习未被处理。
- 引文："Learning e g the storage of new cases new rules and the application of techniques like Knuth Bendix completion to guarantee completeness of struc tural knowledge or learning of modi cation rule conditions or weights are not addressed in this implementation" (Borner, 1993, p.10)
- 复核结论（人填）：
- 处理（人填）：

### 04 · B1-06 · Liao1998_SimilarityMeasures_CBR · 问题域

- 当前判定：UNSUPPORTED / SELF
- 引文里的依据："to illustrate"
- 缺什么：引文只说某分析被用来举例，未触及"相似度度量"问题域；需换引文
- 论断：该文的问题域是 CBR 案例检索中的相似度度量（通用方法），并以失效分析为示例应用领域。
- 引文："analysis (Esaklul, 1990) is used to illustrate that applications with a mixture" (Liao et al., 1998, p.13)
- 复核结论（人填）：
- 处理（人填）：

### 05 · B1-07 · Liao1998_SimilarityMeasures_CBR · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："being developed"
- 缺什么：删"案例"（引文止于 failure analysis），或补原文 cases；"该文所依托"需补依据
- 论断：该文所依托的系统是一个正在开发、用于存储失效分析案例的 CBR 系统。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)
- 复核结论（人填）：
- 处理（人填）：

### 06 · B1-08 · MaherGomez1996_CBR_StructuralDesign · 问题域

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："design projects"
- 缺什么：删"建筑"（引文只作 structural design）；information≠"案例资料"，需补依据
- 论断：问题域是建筑结构设计，案例资料取自结构设计项目。
- 引文："information on structural design projects" (Maher and Gomez, 1996, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 07 · B1-09 · MaherGomez1996_CBR_StructuralDesign · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："using Framekit"
- 缺什么：引文止于"a frame-based"，"表示语言"无原文依据；"实现"对应 using 需核
- 论断：CaseCAD 以 Framekit 这一框架式表示语言实现。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)
- 复核结论（人填）：
- 处理（人填）：

### 08 · B1-11 · SriramMaherFenves1985_KBES_StructuralDesign · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："implemented in"
- 缺什么：引文只给 HI-RISE 一例且未称 prototype；"原型形态""文中系统"无依据
- 论断：文中系统以已实现的原型形态给出，例如 HI-RISE 在 PSRL 中实现。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)
- 复核结论（人填）：
- 处理（人填）：

### 09 · B1-12 · Zhang2006_BP_CaseRetrieval_HighriseStructureForm · 一句话主张

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："can overcome"
- 缺什么："现有案例检索方法"是 such 的指代，引文内无指代对象；需补原句或写明指代
- 论断：作者主张所提出的智能案例检索方法能够克服现有案例检索方法的若干不足。
- 引文："this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO." (Zhang, 2006, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 10 · B1-16 · Zhao2023_ShearWall_GNN · 明确写出的局限

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："limited shear"
- 缺什么：引文说样本有限使过拟合"更易避免"，非"需避免"；"用于训练"亦无原文
- 论断：作者明确写出用于训练的剪力墙样本有限，需避免过拟合。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)
- 复核结论（人填）：
- 处理（人填）：

### 11 · B2-04 · Borner1993_StructuralSimilarity_CBR · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："special design"
- 缺什么：原文只说 supply the system，未称二者为子系统/构成系统
- 论断：系统由 SynTerm 与 SynGraph 两个子系统构成，二者为同一系统提供专项设计问题的解法。
- 引文："SynTerm and SynGraph supply the system with solutions for special design problems" (Borner, 1993, p.9)
- 复核结论（人填）：
- 处理（人填）：

### 12 · B2-06 · Liao1998_SimilarityMeasures_CBR · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："could be"
- 缺什么："could be" 被写成"相关联"，"取值"原文无依据
- 论断：失效分析案例以属性（attribute）表示，属性再与相应的取值相关联。
- 引文："The attributes used to represent failure cases could be associated with" (Liao et al., 1998, p.14)
- 复核结论（人填）：
- 处理（人填）：

### 13 · B2-07 · Liao1998_SimilarityMeasures_CBR · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："Two cases"
- 缺什么："单个算例演示""说明计算过程"原文无
- 论断：评价以一对失效分析案例（case1 与 case2）做单个算例演示，用以说明所提混合度量的计算过程。
- 引文："Two cases X(case1) and Y(case2) of failure analysis are used ; n1, n2, n3, and" (Liao et al., 1998, p.19)
- 复核结论（人填）：
- 处理（人填）：

### 14 · B2-09 · MaherGomez1996_CBR_StructuralDesign · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："design projects"
- 缺什么：原文未称其为"评价所依据"的案例数据
- 论断：评价所依据的案例数据规模为 14 个设计项目。
- 引文："Finally, we reviewed and collected data from 14 design projects." (Maher and Gomez, 1996, p.2)
- 复核结论（人填）：
- 处理（人填）：

### 15 · B2-10 · SriramMaherFenves1985_KBES_StructuralDesign · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："In this paper"
- 缺什么：引文无"结构设计"；原文为 analysts，非 analysis
- 论断：作者把本文定位为介绍知识基专家系统（KBES）在结构设计的初步设计、分析与详细设计阶段的应用。
- 引文："In this paper applications of KBES to the preliminary design, analysts, and detailed design" (Sriram et al., 1985, p.3)
- 复核结论（人填）：
- 处理（人填）：

### 16 · B2-11 · SriramMaherFenves1985_KBES_StructuralDesign · 明确写出的局限

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："user interfaces"
- 缺什么：名词短语无主语；"实用实现需要"原文无
- 论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文："expert system development tools, notably in the areas of user interfaces, explanation capabilities" (Sriram et al., 1985, p.19)
- 复核结论（人填）：
- 处理（人填）：

### 17 · B2-13 · Zhang2006_BP_CaseRetrieval_HighriseStructureForm · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："single-output"
- 缺什么：原文只说 built，未称其为系统"核心"
- 论断：系统的核心是单输出的三层 BP 神经网络。
- 引文："Thereupon we have built the multi-input-and- single-output, three-layer BP network." (Zhang, 2006, p.3)
- 复核结论（人填）：
- 处理（人填）：

### 18 · B2-14 · Zhao2023_ShearWall_GNN · 问题域

- 当前判定：PARTIAL / SELF
- 引文里的依据："first stage"
- 缺什么：原文为 guides the project，非"结构设计过程"
- 论断：问题域是剪力墙结构的结构方案设计，作者称其为引导整个结构设计过程的第一阶段。
- 引文："Structural scheme design of shear wall structures is important because it is the first stage that guides the project along its entire" (Zhao et al., 2023, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 19 · B3-01 · Ahmed2013_Analysis_SketchRetrieval_FloorPlans · 相似性或检索机制

- 当前判定：PARTIAL / SELF
- 引文里的依据："subgraph"
- 缺什么：引文断在名词短语，"采用"无谓语依据，需补完整句
- 论断：检索算法采用子图匹配这一技术路线。
- 引文："As for the retrieval algorithm, subgraph matching approaches" (Ahmed et al., 2013, p.3)
- 复核结论（人填）：
- 处理（人填）：

### 20 · B3-04 · Borner1993_StructuralSimilarity_CBR · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："results support"
- 缺什么：缺"未给出数据集规模/指标数值"的缺席证据（需全库检索）
- 论断：评价方式是报告初期实验结果对上述主张的支持，未给出数据集规模或指标数值。
- 引文："The initial experimental results support the claims that the proposed ap proach o ers improved adaptation facilities in synthesis tasks together with a greater overall explanation performance" (Borner, 1993, p.10)
- 复核结论（人填）：
- 处理（人填）：

### 21 · B3-05 · Liao1998_SimilarityMeasures_CBR · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："for comparing"
- 缺什么：补"案例之间"依据（引文断在 comparing 后）
- 论断：该文在第二部分提出一种混合相似度度量，用于案例之间的比较。
- 引文："applications. In the second part, a hybrid similarity measure is proposed for comparing" (Liao et al., 1998, p.2)
- 复核结论（人填）：
- 处理（人填）：

### 22 · B3-07 · MaherGomez1996_CBR_StructuralDesign · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："presents four"
- 缺什么：补"四个案例""悉尼大学""设计系统"依据（引文断在 four）
- 论断：本文以四个案例的形式介绍作者在悉尼大学开发的基于案例设计系统。
- 引文："Toward that end, this article presents four" (Maher and Gomez, 1996, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 23 · B3-08 · MaherGomez1996_CBR_StructuralDesign · 相似性或检索机制

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："finding matches"
- 缺什么：补主语及"度量相关性""记忆项属性取值"依据
- 论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文："a given problem by finding matches between" (Maher and Gomez, 1996, p.4)
- 复核结论（人填）：
- 处理（人填）：

### 24 · B3-09 · MaherGomez1996_CBR_StructuralDesign · 明确写出的局限

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："a limited"
- 缺什么：引文仅 when 从句，缺主句及"只…适用"依据
- 论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文："when case memory contains a limited" (Maher and Gomez, 1996, p.10)
- 复核结论（人填）：
- 处理（人填）：

### 25 · B3-11 · Survey2025_FloorPlanRetrieval_MDPI · 系统形态

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："advanced fusion"
- 缺什么：补"综述/review"原词
- 论断：该文是综述，考察这些特征检索方法并提出面向未来研究的融合技术。
- 引文："This paper thoroughly examines these feature retrieval methods and introduces advanced fusion techniques to support future research" (Ling et al., 2025, p.23)
- 复核结论（人填）：
- 处理（人填）：

### 26 · B3-13 · Zhang2006_BP_CaseRetrieval_HighriseStructureForm · 评价方式

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："the same with"
- 缺什么：补"验证依据""工程实例"依据（原文为 practice engineering）
- 论断：以工程实例的检索结果与工程实际选型相同作为验证依据。
- 引文："This selection is the same with the practice engineering." (Zhang, 2006, p.5)
- 复核结论（人填）：
- 处理（人填）：

### 27 · B3-15 · Zhao2023_ShearWall_GNN · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："Ten-fold"
- 缺什么：引文断在 "standard"，补"标准差/评价指标"完整句
- 论断：每个模型在训练时执行十折交叉验证，并以验证集结果的平均值与标准差作为评价指标。
- 引文："Ten-fold cross-validation is performed for each model during training. Subsequently, the validation-set average and standard" (Zhao et al., 2023, p.10)
- 复核结论（人填）：
- 处理（人填）：

### 28 · R1-01 · AamodtPlaza1994_CBR_Foundations · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："a general framework is defined"
- 缺什么：引文没有提到“用于描述案例推理方法”；请删去这一目的，或补充原文依据
- 论断：本文提出一个通用的描述框架，用于描述案例推理方法，后续的描述与讨论都参照该框架。
- 引文："Initially, a general framework is defined, to which the subsequent descriptions and discussions will refer." (Aamodt and Plaza, 1994, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 29 · R1-02 · AamodtPlaza1994_CBR_Foundations · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："20.000 non-conformances were handled"
- 缺什么：引文只给出了处理的数值，没有提到“已部署应用”和“评价”；请删去这些说法，或补充部署应用的依据
- 论断：评价以已部署应用的实际运行数据呈现，例如在 1990 年 12 月至 1991 年 9 月间处理了 20,000 个 non-conformance。
- 引文："In the period December 90 - September 91 20.000 non-conformances were handled." (Aamodt and Plaza, 1994, p.17)
- 复核结论（人填）：
- 处理（人填）：

### 30 · R1-05 · Rodrigues2017_Clustering_FloorPlans · 问题域

- 当前判定：PARTIAL / SELF
- 引文里的依据："may be overwhelming"
- 缺什么：引文中的“may be overwhelming”被写成了“超出处理能力”，情态强度被提高；请补充“可能”
- 论断：问题域是建筑平面图——生成式设计方法会产出大量候选平面方案，超出决策者的处理能力。
- 引文："Generative design methods are able to produce a large number of potential solutions of architectural ﬂoor plans, which may be overwhelming for the decision-maker to cope with." (Rodrigues et al., 2017, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 31 · R1-10 · SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："can be deﬁned as the case phenotype"
- 缺什么：引文中的“can be defined”被改成了“被定义为”；请改成“可被定义为”
- 论断：案例以描述该案例的 19 个属性的取值来表示，这些取值构成案例描述，并被定义为案例表型。
- 引文："The values that are associated with each of the 19 attributes in the description of a case make up the case description and can be deﬁned as the case phenotype (Fig. 3)." (Soibelman et al., 2000, p.6)
- 复核结论（人填）：
- 处理（人填）：

### 32 · R1-14 · Xia2025_CoDesign_ShearWallBeam_GNN · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："rapid arrangement of floor slabs"
- 缺什么：引文用的是“rapid arrangement”，没有提到“原型”；请删去“原型”和“自动”这类说法，或补充依据
- 论断：系统形态为可运行的设计—分析流程原型：研究中调用 AIStructure 接口自动布置楼板并施加荷载，再用 PKPM API 完成自动建模与力学分析。
- 引文："This study utilized the AIStructure application programming interface (API) [30] to realize the rapid arrangement of floor slabs and application of loads to the beams and slabs. Subsequently, the PKPM API software development tool was employed to achieve automated structural modeling and mechanical analysis." (Xia et al., 2025, p.13)
- 复核结论（人填）：
- 处理（人填）：

### 33 · R1-16 · vanEngelenburg2023_SSIG_FloorPlan · 问题域

- 当前判定：PARTIAL / SELF
- 引文里的依据："a key factor in the architectural quality"
- 缺什么：引文没有提到“面向建筑设计中的平面图”；请删去这一说法，或补充依据
- 论断：论文面向建筑设计中的平面图，认为建筑的构图结构是建筑品质的关键因素。
- 引文："The compositional structure of a building is a key factor in the architectural quality." (van Engelenburg et al., 2023, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 34 · R2-01 · AamodtPlaza1994_CBR_Foundations · 问题域

- 当前判定：PARTIAL / SELF
- 引文里的依据："no universal"
- 缺什么：首句“本文讨论的是通用方法论”在引文里没有对应，应删去，或补上原文依据
- 论断：本文讨论的是案例推理的通用方法论，作者指出并不存在适用于每一个应用领域的通用案例推理方法。
- 引文："As for AI in general, there are no universal CBR methods suitable for every domain of application." (Aamodt and Plaza, 1994, p.7)
- 复核结论（人填）：
- 处理（人填）：

### 35 · R2-02 · AamodtPlaza1994_CBR_Foundations · 明确写出的局限

- 当前判定：PARTIAL / DEPENDENT
- 引文里的依据："may easily lead"
- 缺什么：“会”加强了 may，应改为“可能轻易导致”
- 论断：作者明确指出，这种索引方式会随案例数量的增加而轻易导致索引的爆炸式增长。
- 引文："This may easily lead to an explosive growth of indices with increased number of cases." (Aamodt and Plaza, 1994, p.10)
- 复核结论（人填）：
- 处理（人填）：

### 36 · R2-06 · Rodrigues2017_Clustering_FloorPlans · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："same length"
- 缺什么：引文只说“各聚类过程所用向量长度相同”，没有“每种描述子都表示成数值向量”这一内容，应删去或补上依据
- 论断：每种描述子都表示成长度相同的数值向量（100 个值），因此表示类型不影响算法性能。
- 引文："As the vector in every clustering process had the same length (100 values), the type of shape representation did not affect the performance of the algorithm." (Rodrigues et al., 2017, p.6)
- 复核结论（人填）：
- 处理（人填）：

### 37 · R2-15 · Xia2025_CoDesign_ShearWallBeam_GNN · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："0.625 and 0.548"
- 缺什么：原文作 successive design method，没有“工程师设计”，应删去或补上依据
- 论断：评价采用与工程师设计对比的交并比（SIoU、BIoU）：协同设计方法的 SIoU 为 0.625、BIoU 为 0.548，顺序设计方法分别为 0.544 与 0.404。
- 引文："The SIoU and BIoU obtained using the proposed co-design method were 0.625 and 0.548, respectively, whereas those obtained using the successive design method were 0.544 and 0.404, respectively." (Xia et al., 2025, p.13)
- 复核结论（人填）：
- 处理（人填）：

### 38 · R3-01 · AamodtPlaza1994_CBR_Foundations · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："features common"
- 缺什么：删去“案例记忆以泛化情节组织”，或补原文依据
- 论断：案例记忆以泛化情节组织，泛化情节包含 norms、cases 与 indices 三类对象，norms 是其下所有案例共有的特征。
- 引文："A generalized episode contains three different types of objects: Norms, cases and indices. Norms are features common to all cases indexed under a GE." (Aamodt and Plaza, 1994, p.9)
- 复核结论（人填）：
- 处理（人填）：

### 39 · R3-04 · Maher1987_ExpertSystems_StructuralDesign · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："implemented in"
- 缺什么：删去“专家系统原型”，或补原文依据
- 论断：系统形态是已实现的专家系统原型，例如 HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文："HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language." (Maher, 1987, p.6)
- 复核结论（人填）：
- 处理（人填）：

### 40 · R3-05 · Rodrigues2017_Clustering_FloorPlans · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："same settings"
- 缺什么：删去“对比/实验研究”，或补原文依据
- 论断：本文形态是在同一设置下把四种形状表示作为平面图设计描述子进行对比的实验研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)
- 复核结论（人填）：
- 处理（人填）：

### 41 · R3-12 · Survey2025_FloorPlanRetrieval_MDPI · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："feature vectors"
- 缺什么：删去“以…形式表示”，或补原文依据
- 论断：平面图以高层语义特征与特征向量的形式表示，并用特征向量计算图像相似度。
- 引文："By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans." (Ling et al., 2025, p.3)
- 复核结论（人填）：
- 处理（人填）：

### 42 · R3-13 · Xia2025_CoDesign_ShearWallBeam_GNN · 问题域

- 当前判定：PARTIAL / SELF
- 引文里的依据："separate design"
- 缺什么：将“生成”改为“分别设计”，或补原文依据
- 论断：问题域为剪力墙与梁的结构方案布置；既有方法分别生成剪力墙或梁，未处理二者的相互依赖，因此需要剪力墙与梁的协同设计方法。
- 引文："However, as the separate design of shear walls and beams fails to adequately address the strong interdependence of these components, an intelligent co-design approach for shear wall and beam structures is required." (Xia et al., 2025, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 43 · R3-17 · vanEngelenburg2023_SSIG_FloorPlan · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："SSIG to rank"
- 缺什么：删去“代码将公开”，引文无此内容
- 论断：产出形态是一个用 SSIG 对大规模平面图库排序的高效算法，作者称代码将公开。
- 引文："In addition, an efﬁcient algorithm is developed that uses SSIG to rank a large-scale ﬂoor plan database." (van Engelenburg et al., 2023, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 44 · R4-03 · Maher1987_ExpertSystems_StructuralDesign · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："The second part"
- 缺什么：引文主语为“第二部分”，删“论文定位为”或补全文依据
- 论断：作者将论文定位为介绍卡内基梅隆大学开发的四个专家系统，用以探索并界定初步设计阶段所做的决策。
- 引文："The second part presents four expert systems, developed at Carnegie Mellon University, that explore and define the decisions made during preliminary design." (Maher, 1987, p.3)
- 复核结论（人填）：
- 处理（人填）：

### 45 · R4-04 · Maher1987_ExpertSystems_StructuralDesign · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："alternatives"
- 缺什么：删“结构”（原文仅 alternatives），或补原文依据
- 论断：论文所述的评价方式是用线性评价函数评价备选结构方案。
- 引文："HI-RISE evaluates alternatives with a linear evaluation function." (Maher, 1987, p.7)
- 复核结论（人填）：
- 处理（人填）：

### 46 · R4-10 · SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign · 一句话主张

- 当前判定：PARTIAL / SELF
- 引文里的依据："multi-reasoning"
- 缺什么：删“（多推理模型）”，或补原文对该缩写的定义
- 论断：作者提出 M-RAM（多推理模型），通过分布式多推理机制向设计者提供经适应的既有设计方案，以辅助高层建筑结构设计的概念阶段。
- 引文："This paper presents the M-RAM, which is intended to assist engineers in the conceptual phase of the structural design of tall buildings by providing designers with adapted past design solutions generated by a distributed multi-reasoning mechanism." (Soibelman et al., 2000, p.1)
- 复核结论（人填）：
- 处理（人填）：

### 47 · R4-16 · vanEngelenburg2023_SSIG_FloorPlan · 评价方式

- 当前判定：PARTIAL / SELF
- 引文里的依据："large-scale"
- 缺什么：引文仅描述 RPLAN，需补“用于评价”的原文依据
- 论断：评价使用 RPLAN 这一大规模平面图数据集，其含逾 80k 套带语义分割区域的亚洲单户公寓。
- 引文："RPLAN is a large-scale dataset containing ﬂoor plan images with semantically segmented areas, consisting of >80k single-unit apartments across Asia." (van Engelenburg et al., 2023, p.5)
- 复核结论（人填）：
- 处理（人填）：

### 48 · R5-01 · AamodtPlaza1994_CBR_Foundations · 系统形态

- 当前判定：PARTIAL / SELF
- 引文里的依据："complementary"
- 缺什么：删去"理论性的描述框架"，或补原文依据
- 论断：系统形态是理论性的描述框架，用两个互补的模型来代表对案例推理的两种视角。
- 引文："The two models are complementary and represent two views on case-based reasoning." (Aamodt and Plaza, 1994, p.6)
- 复核结论（人填）：
- 处理（人填）：

### 49 · R5-02 · Gu2024_ShearWall_Diffusion · 案例或数据的表示形式

- 当前判定：PARTIAL / SELF
- 引文里的依据："can be encoded"
- 缺什么：can be encoded 为可能性，论断写成实际采用；改为"可用颜色编码"或补原文依据
- 论断：该文用图像中的颜色编码不同构件与剪力墙。
- 引文："Different components and shear walls can be encoded using the colors in the image." (Gu et al., 2024, p.4)
- 复核结论（人填）：
- 处理（人填）：

### 50 · R5-14 · Xia2025_CoDesign_ShearWallBeam_GNN · 相似性或检索机制

- 当前判定：PARTIAL / SELF
- 引文里的依据："edge labels"
- 缺什么：删去"不是相似度检索"（引文未作此否定），并补"布置设计"原文依据
- 论断：机制不是相似度检索，而是把布置设计转化为图上的边标签预测：输入特征经 GraphSAGE 层与 MLP 组合每条边及其两端节点的特征，再由分类算法输出预测值。
- 引文："The process of predicting edge labels using the GNN comprises passing the input features through GraphSAGE algorithm layers, followed by the application of an MLP to predict the edge features using the combined feature values of each edge and its two corresponding nodes as input. Finally, the feature information for each edge is processed using a classification algorithm to yield the corresponding predicted values." (Xia et al., 2025, p.8)
- 复核结论（人填）：
- 处理（人填）：
