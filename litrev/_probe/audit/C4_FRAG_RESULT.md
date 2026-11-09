# C4 片段审计结果（FRAG_B1–B3，共 48 条）

- 审计对象：`litrev/_probe/audit/FRAG_B1.md` / `FRAG_B2.md` / `FRAG_B3.md`，各 16 条。
- 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节 v1 口径修订）。
- 执行：3 个 `auditor` 在同一条 assistant 消息内并列派发；B2、B3 首次即完整，B1 首次返回为空，已恢复同一会话补交 16 行（见第五节）。
- 机械复核：48/48 行序与批次文件一致；48/48「依据」列在该条引文中逐字命中；三份合计行与逐行统计一致。

## 一、总判定分布

| 轴 | 码 | 条数 | 占比 |
|---|---|---:|---:|
| 支撑 | SUPPORTED | 28 | 58.3% |
| 支撑 | PARTIAL | 19 | 39.6% |
| 支撑 | UNSUPPORTED | 1 | 2.1% |
| 自足 | SELF | 35 | 72.9% |
| 自足 | DEPENDENT | 13 | 27.1% |
| **合计** | — | **48** | **100%** |

## 二、按文献分布

| 文献 | 条数 | SUPPORTED | PARTIAL | UNSUPPORTED | SELF | DEPENDENT |
|---|---:|---:|---:|---:|---:|---:|
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 6 | 5 | 1 | 0 | 4 | 2 |
| Borner1993_StructuralSimilarity_CBR | 7 | 4 | 3 | 0 | 5 | 2 |
| Gu2024_ShearWall_Diffusion | 1 | 1 | 0 | 0 | 0 | 1 |
| Liao1998_SimilarityMeasures_CBR | 6 | 2 | 3 | 1 | 6 | 0 |
| MaherGomez1996_CBR_StructuralDesign | 7 | 2 | 5 | 0 | 3 | 4 |
| Rodrigues2017_Clustering_FloorPlans | 1 | 1 | 0 | 0 | 1 | 0 |
| SriramMaherFenves1985_KBES_StructuralDesign | 4 | 1 | 3 | 0 | 3 | 1 |
| Survey2025_FloorPlanRetrieval_MDPI | 1 | 1 | 0 | 0 | 1 | 0 |
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 7 | 4 | 3 | 0 | 6 | 1 |
| Zhao2023_ShearWall_GNN | 6 | 5 | 1 | 0 | 5 | 1 |
| delasHeras2014_RunlengthHistogram_FloorPlans | 1 | 1 | 0 | 0 | 1 | 0 |
| vanEngelenburg2023_SSIG_FloorPlan | 1 | 1 | 0 | 0 | 0 | 1 |
| **合计** | **48** | **28** | **19** | **1** | **35** | **13** |

## 三、待改清单

### 3.1 支撑轴待改（PARTIAL / UNSUPPORTED，只列不改，交人）

共 20 条。每条四件套：现文论断 / 引文原文 / 缺什么 / 位置。

**B1-02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 系统形态 ・ p.8 ・ 源文件第 23 行**
- 现文论断：系统形态是为 Touch & Write 触控笔桌实现的原型。
- 引文原文：“the prototype is implemented for the Touch & Write”
- 缺什么：删去"触控笔桌"，或补 Touch & Write 为触控笔桌的原文依据
- 位置：`litrev/_probe/full/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md` 第 23 行（系统形态，p.8）

**B1-05 ・ Borner1993_StructuralSimilarity_CBR ・ 明确写出的局限 ・ p.10 ・ 源文件第 31 行**
- 现文论断：作者明确写出，修改规则条件或权重的学习未被处理。
- 引文原文：“rule conditions or w eigh ts are not addressed”
- 缺什么：删去"修改……的学习"，引文只说不处理规则条件或权重本身
- 位置：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md` 第 31 行（明确写出的局限，p.10）

**B1-06 ・ Liao1998_SimilarityMeasures_CBR ・ 问题域 ・ p.13 ・ 源文件第 11 行**
- 现文论断：该文的问题域是 CBR 案例检索中的相似度度量（通用方法），并以失效分析为示例应用领域。
- 引文原文：“analysis (Esaklul, 1990) is used to illustrate that applications with a mixture”
- 缺什么：引文主体是"某分析被用作示例"，未涉及"相似度度量/CBR 案例检索"这一问题域，需换引文
- 位置：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md` 第 11 行（问题域，p.13）

**B1-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1 ・ 源文件第 11 行**
- 现文论断：问题域是建筑结构设计，案例资料取自结构设计项目。
- 引文原文：“information on structural design projects”
- 缺什么：删去"建筑"这一限定，或补其为建筑结构设计的依据
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 11 行（问题域，p.1）

**B1-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 系统形态 ・ p.2 ・ 源文件第 23 行**
- 现文论断：CaseCAD 以 Framekit 这一框架式表示语言实现。
- 引文原文：“CaseCAD using Framekit, a frame-based”
- 缺什么：引文止于"a frame-based"，"表示语言"需补全；"实现"宜改为"使用"
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 23 行（系统形态，p.2）

**B1-11 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 系统形态 ・ p.7 ・ 源文件第 23 行**
- 现文论断：文中系统以已实现的原型形态给出，例如 HI-RISE 在 PSRL 中实现。
- 引文原文：“buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system”
- 缺什么："文中系统以已实现的原型形态给出"系由 HI-RISE 一例放大，且"原型"无引文依据
- 位置：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md` 第 23 行（系统形态，p.7）

**B1-14 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 明确写出的局限 ・ p.2 ・ 源文件第 31 行**
- 现文论断：作者明确指出网络拓扑结构的确定缺乏成熟、系统的理论。
- 引文原文：“topological structure of networks instead of mature and”
- 缺什么："缺乏……理论"属缺席命题，需全库证据；"系统的"在引文止点外
- 位置：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md` 第 31 行（明确写出的局限，p.2）

**B1-16 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11 ・ 源文件第 31 行**
- 现文论断：作者明确写出用于训练的剪力墙样本有限，需避免过拟合。
- 引文原文：“easier to avoid overfitting owing to the limited shear wall samples.”
- 缺什么：引文为"easier to avoid overfitting"，非"需避免"；"用于训练"无依据
- 位置：`litrev/_probe/full/Zhao2023_ShearWall_GNN.md` 第 31 行（明确写出的局限，p.11）

**B2-03 ・ Borner1993_StructuralSimilarity_CBR ・ 问题域 ・ p.9 ・ 源文件第 11 行**
- 现文论断：系统面向工业建筑设计领域。
- 引文原文：“Both are in tegrated in a kno wledge based system whic h op erates in the domain of industrial building”
- 缺什么：删去“设计”，或补含 industrial building design 的依据；主语 Both 指代需还原
- 位置：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md` 第 11 行（问题域，p.9）

**B2-06 ・ Liao1998_SimilarityMeasures_CBR ・ 案例或数据的表示形式 ・ p.14 ・ 源文件第 15 行**
- 现文论断：失效分析案例以属性（attribute）表示，属性再与相应的取值相关联。
- 引文原文：“The attributes used to represent failure cases could be associated with”
- 缺什么："could be" 被写成断言，且 associated with 的对象（取值）在引文外，需补
- 位置：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md` 第 15 行（案例或数据的表示形式，p.14）

**B2-07 ・ Liao1998_SimilarityMeasures_CBR ・ 评价方式 ・ p.19 ・ 源文件第 27 行**
- 现文论断：评价以一对失效分析案例（case1 与 case2）做单个算例演示，用以说明所提混合度量的计算过程。
- 引文原文：“Two cases X(case1) and Y(case2) of failure analysis are used ; n1, n2, n3, and”
- 缺什么：“说明混合度量计算过程”引文未及，需补该句后续
- 位置：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md` 第 27 行（评价方式，p.19）

**B2-10 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 一句话主张 ・ p.3 ・ 源文件第 7 行**
- 现文论断：作者把本文定位为介绍知识基专家系统（KBES）在结构设计的初步设计、分析与详细设计阶段的应用。
- 引文原文：“In this paper applications of KBES to the preliminary design, analysts, and detailed design”
- 缺什么：删去“结构设计的”，或补含 structural design 的原句
- 位置：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md` 第 7 行（一句话主张，p.3）

**B2-11 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 明确写出的局限 ・ p.19 ・ 源文件第 30 行**
- 现文论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文原文：“expert system development tools, notably in the areas of user interfaces, explanation capabilities”
- 缺什么：“实用实现需要”无依据，需补含 require 的句子；引文无主语
- 位置：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md` 第 30 行（明确写出的局限，p.19）

**B2-13 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 系统形态 ・ p.3 ・ 源文件第 23 行**
- 现文论断：系统的核心是单输出的三层 BP 神经网络。
- 引文原文：“single-output, three-layer BP network.”
- 缺什么：“系统的核心”无依据需补；引文无主语
- 位置：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md` 第 23 行（系统形态，p.3）

**B3-04 ・ Borner1993_StructuralSimilarity_CBR ・ 评价方式 ・ p.10 ・ 源文件第 27 行**
- 现文论断：评价方式是报告初期实验结果对上述主张的支持，未给出数据集规模或指标数值。
- 引文原文：“The initial exp erimen tal results supp ort the claims”
- 缺什么：删去"未给出数据集规模或指标数值"，或补全库缺席证据
- 位置：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md` 第 27 行（评价方式，p.10）

**B3-05 ・ Liao1998_SimilarityMeasures_CBR ・ 一句话主张 ・ p.2 ・ 源文件第 7 行**
- 现文论断：该文在第二部分提出一种混合相似度度量，用于案例之间的比较。
- 引文原文：“applications. In the second part, a hybrid similarity measure is proposed for comparing”
- 缺什么：删去"案例之间的"，或补 comparing 的宾语依据
- 位置：`litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md` 第 7 行（一句话主张，p.2）

**B3-07 ・ MaherGomez1996_CBR_StructuralDesign ・ 一句话主张 ・ p.1 ・ 源文件第 7 行**
- 现文论断：本文以四个案例的形式介绍作者在悉尼大学开发的基于案例设计系统。
- 引文原文：“Toward that end, this article presents four”
- 缺什么：删去"悉尼大学""基于案例设计系统"及"四个案例"，或补原文依据
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 7 行（一句话主张，p.1）

**B3-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 相似性或检索机制 ・ p.4 ・ 源文件第 19 行**
- 现文论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文原文：“a given problem by finding matches between”
- 缺什么：删去"属性及取值""记忆项""度量相关性"，或补原文依据
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 19 行（相似性或检索机制，p.4）

**B3-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 明确写出的局限 ・ p.10 ・ 源文件第 31 行**
- 现文论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文原文：“when case memory contains a limited”
- 缺什么：删去"只在…时适用"的独占限定，或补主句
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 31 行（明确写出的局限，p.10）

**B3-12 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 案例或数据的表示形式 ・ p.2 ・ 源文件第 15 行**
- 现文论断：案例以向量形式送入网络的输入层。
- 引文原文：“the input layer is inputting vectors {xik4m and {Yk}m (k”
- 缺什么：删去"案例"，或补其原文依据
- 位置：`litrev/_probe/full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md` 第 15 行（案例或数据的表示形式，p.2）

### 3.2 自足轴待改（SUPPORTED + DEPENDENT，可进入 T3 扩句）

共 7 条。支撑轴已 SUPPORTED，问题只是引文被截断；只允许扩到完整句，不许改写或换句。

**B2-01 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 问题域 ・ p.1 ・ 源文件第 11 行**
- 现文论断：问题域是建筑设计中的相似建筑情境及对应的解决方案。
- 引文原文：“to guide solutions for similar architectural situations.”
- 缺什么：引文为不定式片段、无主语，需补主语（如“该文旨在…”）
- 位置：`litrev/_probe/full/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md` 第 11 行（问题域，p.1）

**B2-05 ・ Gu2024_ShearWall_Diffusion ・ 相似性或检索机制 ・ p.6 ・ 源文件第 19 行**
- 现文论断：该文采用的生成机制是带掩码张量的图像提示扩散模型。
- 引文原文：“methods for an image-prompt diffusion model with a mask tensor.”
- 缺什么：主语落在引号外，需补“该文采用/提出…”
- 位置：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md` 第 19 行（相似性或检索机制，p.6）

**B2-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 案例或数据的表示形式 ・ p.6 ・ 源文件第 15 行**
- 现文论断：案例以属性-值对（attribute-value pair）来描述。
- 引文原文：“uses attribute-value pairs to describe a case.”
- 缺什么：主语落在引号外（uses 前），需补主语
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 15 行（案例或数据的表示形式，p.6）

**B2-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 评价方式 ・ p.2 ・ 源文件第 27 行**
- 现文论断：评价所依据的案例数据规模为 14 个设计项目。
- 引文原文：“data from 14 design projects”
- 缺什么：名词片段无主语，需补主语
- 位置：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md` 第 27 行（评价方式，p.2）

**B3-02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 明确写出的局限 ・ p.9 ・ 源文件第 31 行**
- 现文论断：作者明确指出方法的弱点是只能找到实际存在的物理房间。
- 引文原文：“it is only able to ﬁnd the physical existent rooms.”
- 缺什么：补主语（该方法/系统）
- 位置：`litrev/_probe/full/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md` 第 31 行（明确写出的局限，p.9）

**B3-03 ・ Borner1993_StructuralSimilarity_CBR ・ 案例或数据的表示形式 ・ p.5 ・ 源文件第 15 行**
- 现文论断：案例中的对象由空间尺寸和另外九个属性表示。
- 引文原文：“represen ted b y its spatial dimensions and nine further attributes”
- 缺什么：补主语（被表示的对象）
- 位置：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md` 第 15 行（案例或数据的表示形式，p.5）

**B3-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 案例或数据的表示形式 ・ p.2 ・ 源文件第 15 行**
- 现文论断：文献把平面图表示为显式建模形状、比例与位置的几何体，以及建模细分区域之间关系的图。
- 引文原文：“geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions”
- 缺什么：补主语（文献/平面图）
- 位置：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md` 第 15 行（案例或数据的表示形式，p.2）

## 四、与 v1 标定对照

| 对象 | 条数 | SUPPORTED | PARTIAL | UNSUPPORTED | DEPENDENT | 非 SUPPORTED 占比 |
|---|---:|---:|---:|---:|---:|---:|
| 上一轮 run1（v1 基线） | 12 | 7 | 5 | 0 | 2 | 41.7% |
| 本轮片段集 | 48 | 28 | 19 | 1 | 13 | 41.7% |

- `_probe/audit/run_C_v1.md` 的变异集原始输出为 8 条（SUPPORTED 2 / PARTIAL 4 / UNSUPPORTED 2；DEPENDENT 2）。
- 按 `RESULT.md` 第八节记录，变异检出 **5/5**：没有一条注入变异被放行为 `SUPPORTED`。
- 注意：本轮的 48 条是按形式判据（首字母小写 / 未以句末标点结尾）挑出的片段，**不是全量随机样本**，所以 41.7% 的非 SUPPORTED 比例不能直接外推到 131 条；它只是片段集的风险结果，剩余 83 条由 T4 做支撑轴审计。
- 巧合但可核对：上一轮 12 条的非 SUPPORTED 为 5/12 = 41.7%，本轮片段集为 20/48 = 41.7%。

## 五、机械复核记录

- **行序**：B1/B2/B3 各 16 行，`B1-01→B1-16`、`B2-01→B2-16`、`B3-01→B3-16`，与批次文件 1:1，无合并、跳过、改序。
- **依据列**：脚本逐条检查 `basis in quote`，48/48 命中，0 失败。
- **合计行**：B1 `8/7/1；D1`、B2 `10/6/0；D7`、B3 `10/6/0；D5`，与逐行统计一致。
- **总合计**：48 条（SUPPORTED 28 / PARTIAL 19 / UNSUPPORTED 1；DEPENDENT 13）。
- **派发**：三条 `task` 在同一条消息内发出，起跑时间 14:18:29.766 / 14:18:30.044 / 14:18:30.313，极差 0.547s；B1 因首次空返回延到 14:22:11.743，B2/B3 分别于 14:19:28.620 / 14:20:23.385 结束。
- **B1 空返回处置**：首次 task `ses_e410ab205ffeOCHyRo3WApZ0F5` 的 result 为空；未新建第二个会话，而是恢复同一会话要求补交，补交内容为 16 行完整表。B2 `ses_e410ab0eeffeXhoyPf8d0420wE`、B3 `ses_e410aaff1ffeuOtxU3BirJFWLP` 首次即完整。

## 六、T3 输入清单（7 条，可直接派发）

| id | 文献 | 字段 | 页 | 源文件行 | 旧引文（需扩到完整句） |
|---|---|---|---:|---:|---|
| B2-01 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 问题域 | p.1 | 11 | “to guide solutions for similar architectural situations.” |
| B2-05 | Gu2024_ShearWall_Diffusion | 相似性或检索机制 | p.6 | 19 | “methods for an image-prompt diffusion model with a mask tensor.” |
| B2-08 | MaherGomez1996_CBR_StructuralDesign | 案例或数据的表示形式 | p.6 | 15 | “uses attribute-value pairs to describe a case.” |
| B2-09 | MaherGomez1996_CBR_StructuralDesign | 评价方式 | p.2 | 27 | “data from 14 design projects” |
| B3-02 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 明确写出的局限 | p.9 | 31 | “it is only able to ﬁnd the physical existent rooms.” |
| B3-03 | Borner1993_StructuralSimilarity_CBR | 案例或数据的表示形式 | p.5 | 15 | “represen ted b y its spatial dimensions and nine further attributes” |
| B3-16 | vanEngelenburg2023_SSIG_FloorPlan | 案例或数据的表示形式 | p.2 | 15 | “geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions” |
