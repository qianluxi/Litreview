# C4 审计待判清单：48 条句中片段引文（v1）

> 生成方式：对 `litrev/_probe/full/*.md` 的 131 条引文按**形式判据**筛选——首字母小写，或未以句末标点结尾。
> 这是**风险上界**，不是判定结果：形式像片段不等于一定 `DEPENDENT`，必须由 `auditor` 按 `AUDIT_CONTRACT.md` 判。
> 生成时间 2026-11-09。全部 131 条已通过 `verify`（逐字存在、页码为 PDF 物理页）。

## 合计

| 项 | 数 |
|---|---|
| 待判条目 | 48 |
| 涉及文献 | 12 篇 |

| 文献 | 条数 |
|---|---:|
| `Borner1993_StructuralSimilarity_CBR` | 7 |
| `MaherGomez1996_CBR_StructuralDesign` | 7 |
| `Zhang2006_BP_CaseRetrieval_HighriseStructureForm` | 7 |
| `Ahmed2013_Analysis_SketchRetrieval_FloorPlans` | 6 |
| `Liao1998_SimilarityMeasures_CBR` | 6 |
| `Zhao2023_ShearWall_GNN` | 6 |
| `SriramMaherFenves1985_KBES_StructuralDesign` | 4 |
| `Gu2024_ShearWall_Diffusion` | 1 |
| `Rodrigues2017_Clustering_FloorPlans` | 1 |
| `Survey2025_FloorPlanRetrieval_MDPI` | 1 |
| `delasHeras2014_RunlengthHistogram_FloorPlans` | 1 |
| `vanEngelenburg2023_SSIG_FloorPlan` | 1 |

## 待判条目（闭卷：只给这五元组，不要读原文）

### F01 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 一句话主张 ・ p.1

- 论断：作者把本文贡献概括为两方面，其中第一项是提出名为 a.SCatch 的基于草图的系统。
- 引文："The contribution of this article is twofold. First, we propose a sketch-based system, namely the a.SCatch" (Ahmed et al., 2013, p.1)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### F02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 问题域 ・ p.1

- 论断：问题域是建筑设计中的相似建筑情境及对应的解决方案。
- 引文："to guide solutions for similar architectural situations." (Ahmed et al., 2013, p.1)
- 形式特征：首字母小写（源文件第 11 行）

### F03 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 相似性或检索机制 ・ p.3

- 论断：检索算法采用子图匹配这一技术路线。
- 引文："As for the retrieval algorithm, subgraph matching approaches" (Ahmed et al., 2013, p.3)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### F04 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 系统形态 ・ p.8

- 论断：系统形态是为 Touch & Write 触控笔桌实现的原型。
- 引文："the prototype is implemented for the Touch & Write" (Ahmed et al., 2013, p.8)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### F05 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 评价方式 ・ p.9

- 论断：评价在图像数据集上报告整体检测率，数值为 94.88%。
- 引文："images dataset. The overall detection rate is 94.88%" (Ahmed et al., 2013, p.9)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 27 行）

### F06 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 明确写出的局限 ・ p.9

- 论断：作者明确指出方法的弱点是只能找到实际存在的物理房间。
- 引文："it is only able to ﬁnd the physical existent rooms." (Ahmed et al., 2013, p.9)
- 形式特征：首字母小写（源文件第 31 行）

### F07 ・ Borner1993_StructuralSimilarity_CBR ・ 一句话主张 ・ p.10

- 论断：作者的核心主张是，只有在存在可据以把旧解正确改编到当前问题的知识时，才进行结构相似性评估。
- 引文："Structural similarit y is assessed if and only if there is kno wledge a v ailable to adapt old solutions correctly" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### F08 ・ Borner1993_StructuralSimilarity_CBR ・ 问题域 ・ p.9

- 论断：系统面向工业建筑设计领域。
- 引文："Both are in tegrated in a kno wledge based system whic h op erates in the domain of industrial building" (Borner, 1993, p.9)
- 形式特征：未以句末标点结尾（源文件第 11 行）

### F09 ・ Borner1993_StructuralSimilarity_CBR ・ 案例或数据的表示形式 ・ p.5

- 论断：案例中的对象由空间尺寸和另外九个属性表示。
- 引文："represen ted b y its spatial dimensions and nine further attributes" (Borner, 1993, p.5)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 15 行）

### F10 ・ Borner1993_StructuralSimilarity_CBR ・ 相似性或检索机制 ・ p.6

- 论断：检索流程先对新问题做低成本的表面相似性初始分析。
- 引文："initial analysis of the new problem can b e done b y an inexp ensiv e surfac e similarity" (Borner, 1993, p.6)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 19 行）

### F11 ・ Borner1993_StructuralSimilarity_CBR ・ 系统形态 ・ p.8

- 论断：该方法以原型形式实现于 SynTerm。
- 引文："Our approac h is protot ypically implemen ted in SynT erm" (Borner, 1993, p.8)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### F12 ・ Borner1993_StructuralSimilarity_CBR ・ 评价方式 ・ p.10

- 论断：评价方式是报告初期实验结果对上述主张的支持，未给出数据集规模或指标数值。
- 引文："The initial exp erimen tal results supp ort the claims" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 27 行）

### F13 ・ Borner1993_StructuralSimilarity_CBR ・ 明确写出的局限 ・ p.10

- 论断：作者明确写出，修改规则条件或权重的学习未被处理。
- 引文："rule conditions or w eigh ts are not addressed" (Borner, 1993, p.10)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 31 行）

### F14 ・ Gu2024_ShearWall_Diffusion ・ 相似性或检索机制 ・ p.6

- 论断：该文采用的生成机制是带掩码张量的图像提示扩散模型。
- 引文："methods for an image-prompt diffusion model with a mask tensor." (Gu et al., 2024, p.6)
- 形式特征：首字母小写（源文件第 19 行）

### F15 ・ Liao1998_SimilarityMeasures_CBR ・ 一句话主张 ・ p.2

- 论断：该文在第二部分提出一种混合相似度度量，用于案例之间的比较。
- 引文："applications. In the second part, a hybrid similarity measure is proposed for comparing" (Liao et al., 1998, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 7 行）

### F16 ・ Liao1998_SimilarityMeasures_CBR ・ 问题域 ・ p.13

- 论断：该文的问题域是 CBR 案例检索中的相似度度量（通用方法），并以失效分析为示例应用领域。
- 引文："analysis (Esaklul, 1990) is used to illustrate that applications with a mixture" (Liao et al., 1998, p.13)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 11 行）

### F17 ・ Liao1998_SimilarityMeasures_CBR ・ 案例或数据的表示形式 ・ p.14

- 论断：失效分析案例以属性（attribute）表示，属性再与相应的取值相关联。
- 引文："The attributes used to represent failure cases could be associated with" (Liao et al., 1998, p.14)
- 形式特征：未以句末标点结尾（源文件第 15 行）

### F18 ・ Liao1998_SimilarityMeasures_CBR ・ 相似性或检索机制 ・ p.17

- 论断：对模糊值采用「面积比方法」（area ratio method）计算两个模糊值之间的相似度。
- 引文："The area ratio method calculates the similarity between two fuzzy" (Liao et al., 1998, p.17)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### F19 ・ Liao1998_SimilarityMeasures_CBR ・ 系统形态 ・ p.13

- 论断：该文所依托的系统是一个正在开发、用于存储失效分析案例的 CBR 系统。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### F20 ・ Liao1998_SimilarityMeasures_CBR ・ 评价方式 ・ p.19

- 论断：评价以一对失效分析案例（case1 与 case2）做单个算例演示，用以说明所提混合度量的计算过程。
- 引文："Two cases X(case1) and Y(case2) of failure analysis are used ; n1, n2, n3, and" (Liao et al., 1998, p.19)
- 形式特征：未以句末标点结尾（源文件第 27 行）

### F21 ・ MaherGomez1996_CBR_StructuralDesign ・ 一句话主张 ・ p.1

- 论断：本文以四个案例的形式介绍作者在悉尼大学开发的基于案例设计系统。
- 引文："Toward that end, this article presents four" (Maher and Gomez, 1996, p.1)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### F22 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1

- 论断：问题域是建筑结构设计，案例资料取自结构设计项目。
- 引文："information on structural design projects" (Maher and Gomez, 1996, p.1)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 11 行）

### F23 ・ MaherGomez1996_CBR_StructuralDesign ・ 案例或数据的表示形式 ・ p.6

- 论断：案例以属性-值对（attribute-value pair）来描述。
- 引文："uses attribute-value pairs to describe a case." (Maher and Gomez, 1996, p.6)
- 形式特征：首字母小写（源文件第 15 行）

### F24 ・ MaherGomez1996_CBR_StructuralDesign ・ 相似性或检索机制 ・ p.4

- 论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文："a given problem by finding matches between" (Maher and Gomez, 1996, p.4)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 19 行）

### F25 ・ MaherGomez1996_CBR_StructuralDesign ・ 系统形态 ・ p.2

- 论断：CaseCAD 以 Framekit 这一框架式表示语言实现。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### F26 ・ MaherGomez1996_CBR_StructuralDesign ・ 评价方式 ・ p.2

- 论断：评价所依据的案例数据规模为 14 个设计项目。
- 引文："data from 14 design projects" (Maher and Gomez, 1996, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 27 行）

### F27 ・ MaherGomez1996_CBR_StructuralDesign ・ 明确写出的局限 ・ p.10

- 论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文："when case memory contains a limited" (Maher and Gomez, 1996, p.10)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 31 行）

### F28 ・ Rodrigues2017_Clustering_FloorPlans ・ 相似性或检索机制 ・ p.4

- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as" (Rodrigues et al., 2017, p.4)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### F29 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 一句话主张 ・ p.3

- 论断：作者把本文定位为介绍知识基专家系统（KBES）在结构设计的初步设计、分析与详细设计阶段的应用。
- 引文："In this paper applications of KBES to the preliminary design, analysts, and detailed design" (Sriram et al., 1985, p.3)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### F30 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 问题域 ・ p.4

- 论断：问题域是结构设计，尤其是其中不适合纯算法求解、常呈病构性的设计问题。
- 引文："structural design are not amenable to purely algorithmic solutions. These problems are often ill-" (Sriram et al., 1985, p.4)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 11 行）

### F31 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 系统形态 ・ p.7

- 论断：文中系统以已实现的原型形态给出，例如 HI-RISE 在 PSRL 中实现。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### F32 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 明确写出的局限 ・ p.19

- 论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文："expert system development tools, notably in the areas of user interfaces, explanation capabilities" (Sriram et al., 1985, p.19)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 30 行）

### F33 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 系统形态 ・ p.23

- 论断：该文是综述，考察这些特征检索方法并提出面向未来研究的融合技术。
- 引文："This paper thoroughly examines these feature retrieval methods and introduces advanced fusion techniques to support future research" (Ling et al., 2025, p.23)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### F34 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 一句话主张 ・ p.1

- 论断：作者主张所提出的智能案例检索方法能够克服现有案例检索方法的若干不足。
- 引文："this intelligent CRM can overcome such shortcomings" (Zhang, 2006, p.1)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 7 行）

### F35 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 问题域 ・ p.1

- 论断：研究问题为高层建筑结构形式选型优化。
- 引文："High-rise structural form selection optimization is" (Zhang, 2006, p.1)
- 形式特征：未以句末标点结尾（源文件第 11 行）

### F36 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 案例或数据的表示形式 ・ p.2

- 论断：案例以向量形式送入网络的输入层。
- 引文："the input layer is inputting vectors {xik4m and {Yk}m (k" (Zhang, 2006, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 15 行）

### F37 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 相似性或检索机制 ・ p.2

- 论断：相似度度量采用以属性相对欧氏加权距离为基础的方法。
- 引文："the relative Euclidean weight distance of attributes (see" (Zhang, 2006, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 19 行）

### F38 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 系统形态 ・ p.3

- 论断：系统的核心是单输出的三层 BP 神经网络。
- 引文："single-output, three-layer BP network." (Zhang, 2006, p.3)
- 形式特征：首字母小写（源文件第 23 行）

### F39 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 评价方式 ・ p.5

- 论断：以工程实例的检索结果与工程实际选型相同作为验证依据。
- 引文："selection is the same with the practice engineering." (Zhang, 2006, p.5)
- 形式特征：首字母小写（源文件第 27 行）

### F40 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 明确写出的局限 ・ p.2

- 论断：作者明确指出网络拓扑结构的确定缺乏成熟、系统的理论。
- 引文："topological structure of networks instead of mature and" (Zhang, 2006, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 31 行）

### F41 ・ Zhao2023_ShearWall_GNN ・ 问题域 ・ p.1

- 论断：问题域是剪力墙结构的结构方案设计，作者称其为引导整个结构设计过程的第一阶段。
- 引文："Structural scheme design of shear wall structures is important because it is the first stage that guides the project along its entire" (Zhao et al., 2023, p.1)
- 形式特征：未以句末标点结尾（源文件第 11 行）

### F42 ・ Zhao2023_ShearWall_GNN ・ 案例或数据的表示形式 ・ p.2

- 论断：剪力墙结构以图数据表示，图由节点和边组成，结合节点位置特征后图是自然的向量化形式。
- 引文："data consist of graph nodes and edges. Combined with the location features of nodes, a graph is a natural vectorized form." (Zhao et al., 2023, p.2)
- 形式特征：首字母小写（源文件第 15 行）

### F43 ・ Zhao2023_ShearWall_GNN ・ 相似性或检索机制 ・ p.9

- 论断：相似性以 IoUpixel 衡量，比较对象是 GNN 生成结果与真值结果在像素图像上的重合。
- 引文："shear wall design results generated by the GNN model and the ground-truth shear wall design results in pixel images, i.e., IoUpixel, is" (Zhao et al., 2023, p.9)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 19 行）

### F44 ・ Zhao2023_ShearWall_GNN ・ 系统形态 ・ p.3

- 论断：系统形态是作者建立的一套基于 GNN 的剪力墙布置设计方法，并以图 1 给出其方法流程。
- 引文："This study establishes a GNN-based shear wall layout design method, as shown in Figure 1. The developed method consists of three" (Zhao et al., 2023, p.3)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### F45 ・ Zhao2023_ShearWall_GNN ・ 评价方式 ・ p.10

- 论断：每个模型在训练时执行十折交叉验证，并以验证集结果的平均值与标准差作为评价指标。
- 引文："Ten-fold cross-validation is performed for each model during training. Subsequently, the validation-set average and standard" (Zhao et al., 2023, p.10)
- 形式特征：未以句末标点结尾（源文件第 27 行）

### F46 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11

- 论断：作者明确写出用于训练的剪力墙样本有限，需避免过拟合。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)
- 形式特征：首字母小写（源文件第 31 行）

### F47 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 相似性或检索机制 ・ p.5

- 论断：两幅平面图签名之间的相似度用 χ2 距离计算。
- 引文："Let P and Q be the signatures of two diﬀerent ﬂoor plan images. Their similarity is calculated by means of the χ2 distance:" (de las Heras et al., 2014, p.5)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### F48 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 案例或数据的表示形式 ・ p.2

- 论断：文献把平面图表示为显式建模形状、比例与位置的几何体，以及建模细分区域之间关系的图。
- 引文："geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions" (van Engelenburg et al., 2023, p.2)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 15 行）
