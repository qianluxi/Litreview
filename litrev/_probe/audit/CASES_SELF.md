# 自足轴判例集 C1（20 条，开卷裁定）

> 由 `python tools/audit_prep.py cases` 生成；条目清单见 `CASES_SELF_IDS.txt`（冻结，抽完不再重抽）。
> **这是给人填的表**：不进 `BATCHES.json`、不生成 agent、`auditor-*` 的 read 白名单不含本文件。
> 只判**自足轴**：论断脱离引文与上下文能不能独立读懂。可读卡片原文（开卷），但不要读 `out_*.md`、
> `SAMPLE_S1_KEYS.md`、`GOLDEN.md`、`CASES_SELF_KEYS.md`。
> 填法：每行填 自足（`SELF` / `DEPENDENT`）、引文里的依据（≤15 字，必须是引文原词）、
> 缺什么（`DEPENDENT` 必须写明缺的是哪个指代/专有名词；`SELF` 填 `—`）。
> 快照 sha1: a4e66877dc

## 预填说明（主控代填，待你审核修改）

> **判据**：自足轴看的是**引文**的主语在不在引号内（契约 §二 轴 2），不是看论断。
> **判 `DEPENDENT` 的两族**：① 引文是名词/介词/从句片段、主谓落在引号外（C01 C02 C04 C05 C06）；② 引文以 `this/these` + 谓语开头且指代前文具体对象（C08 C10 C14 C16），或主句主语被分词吞掉（C09）。
> **判 `SELF` 的自指族**：`this paper / this study / this work / this section / It is… that` 指的就是本文本节，不需要外部先行词（C03 C07 C11 C12 C13 C15 C17 C18 C19 C20）。
> **与表内现判有 4 处不同**：C03、C07（表判 `DEP`，此处判 `SELF`）、C14、C16（表判 `SELF`，此处判 `DEP`）。
> **这 4 条是同一个边界**：表内对自指句自己就不一致——C03「this section introduces」判 `DEP`，而 C17「This section presents」判 `SELF`；C07「This paper thoroughly examines」判 `DEP`，而 C19「This paper is」判 `SELF`。
> 若按契约字面「引文以 this 开头即 `DEPENDENT`」，则 C03/C07/C12/C15/C17/C19/C20 七条自指句都该改成 `DEPENDENT`——这批判例要定的就是这件事。

## 待填判定表（人填）

| id | 自足 | 引文里的依据（≤15 字，必须是引文原词） | 缺什么 / 需补的一句 |
|----|------|--------------------------------------|--------------------|
| C01 | DEPENDENT | "design projects" | 引文是名词短语（information on…），无主谓；缺"资料出自哪个项目/谁的研究" |
| C02 | DEPENDENT | "limited shear" | 引文是 easier to… 片段，主语在引号外；缺"是什么使过拟合更易避免" |
| C03 | SELF | "diffusion model" | —（主控预填 SELF：this section 是自指，非外部指代） |
| C04 | DEPENDENT | "user interfaces" | 引文是名词列举，无主谓；缺"谁需要、需要做到什么"（主谓都在引号外） |
| C05 | DEPENDENT | "finding matches" | finding matches between 的宾语缺失，主句在引号外 |
| C06 | DEPENDENT | "case memory" | 只有 when 从句，结论主句在引号外；limited 后还截断 |
| C07 | SELF | "advanced fusion" | —（主控预填 SELF：This paper 是自指） |
| C08 | DEPENDENT | "explosive" | This 指代前文的索引做法，先行词在引号外 |
| C09 | DEPENDENT | "weighted" | Coined as… 是分词开头，主句主语缺失（"7" 是脚注号） |
| C10 | DEPENDENT | "timeout errors" | These limitations 指代前文列出的局限，先行词在引号外 |
| C11 | SELF | "aforementioned" | — |
| C12 | SELF | "diffusion model" | — |
| C13 | SELF | "preliminary" | —（It 是形式主语，真主语在引号内） |
| C14 | DEPENDENT | "this approach" | this approach 指代前文介绍的方法，先行词在引号外 |
| C15 | SELF | "based on GNNs" | — |
| C16 | DEPENDENT | "input graphs" | these input graphs 指代前文构造的图，先行词在引号外 |
| C17 | SELF | "three matching" | — |
| C18 | SELF | "generalization" | —（主句主语 We 完整；these data 指代属边界，见注记） |
| C19 | SELF | "aesthetics" | — |
| C20 | SELF | "limited to" | — |

## 条目详情（判定时可读卡片原文，开卷）

### C01 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1

- 论断：问题域是建筑结构设计，案例资料取自结构设计项目。
- 引文："information on structural design projects" (Maher and Gomez, 1996, p.1)
- 卡片：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md`（可读原文上下文）

### C02 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11

- 论断：作者明确写出用于训练的剪力墙样本有限，需避免过拟合。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)
- 卡片：`litrev/_probe/full/Zhao2023_ShearWall_GNN.md`（可读原文上下文）

### C03 ・ Gu2024_ShearWall_Diffusion ・ 相似性或检索机制 ・ p.6

- 论断：该文采用的生成机制是带掩码张量的图像提示扩散模型。
- 引文："4 | THE CONSTRUCTION, TRAINING, AND INFERENCE OF NEURAL NETWORK MODELS To focus on the diffusion process features of the shear wall portion, this section introduces the construction, training, and inference methods for an image-prompt diffusion model with a mask tensor." (Gu et al., 2024, p.6)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### C04 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 明确写出的局限 ・ p.19

- 论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文："expert system development tools, notably in the areas of user interfaces, explanation capabilities" (Sriram et al., 1985, p.19)
- 卡片：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md`（可读原文上下文）

### C05 ・ MaherGomez1996_CBR_StructuralDesign ・ 相似性或检索机制 ・ p.4

- 论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文："a given problem by finding matches between" (Maher and Gomez, 1996, p.4)
- 卡片：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md`（可读原文上下文）

### C06 ・ MaherGomez1996_CBR_StructuralDesign ・ 明确写出的局限 ・ p.10

- 论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文："when case memory contains a limited" (Maher and Gomez, 1996, p.10)
- 卡片：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md`（可读原文上下文）

### C07 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 系统形态 ・ p.23

- 论断：该文是综述，考察这些特征检索方法并提出面向未来研究的融合技术。
- 引文："This paper thoroughly examines these feature retrieval methods and introduces advanced fusion techniques to support future research" (Ling et al., 2025, p.23)
- 卡片：`litrev/_probe/full/Survey2025_FloorPlanRetrieval_MDPI.md`（可读原文上下文）

### C08 ・ AamodtPlaza1994_CBR_Foundations ・ 明确写出的局限 ・ p.10

- 论断：作者明确指出，这种索引方式会随案例数量的增加而轻易导致索引的爆炸式增长。
- 引文："This may easily lead to an explosive growth of indices with increased number of cases." (Aamodt and Plaza, 1994, p.10)
- 卡片：`litrev/_probe/full/AamodtPlaza1994_CBR_Foundations.md`（可读原文上下文）

### C09 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 相似性或检索机制 ・ p.5

- 论断：SSIG 被表述为基于 IoU 的相似度与基于 nGED 的相似度之间的加权平均。
- 引文："Coined as SSIG (Structural Similarity by IoU and GED), 7 essentially computes a weighted average between a IoU-based and a nGED-based similarity metric." (van Engelenburg et al., 2023, p.5)
- 卡片：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md`（可读原文上下文）

### C10 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 明确写出的局限 ・ p.7

- 论断：作者明确写出，索引法的这些局限来自底层 Neo4j 数据库的内部超时错误。
- 引文："These limitations came from internal timeout errors of the underlying Neo4j database, most likely due to a congestion of the database system." (Sabri et al., 2017, p.7)
- 卡片：`litrev/_probe/full/Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM.md`（可读原文上下文）

### C11 ・ Gu2024_ShearWall_Diffusion ・ 系统形态 ・ p.2

- 论断：该文基于所提训练方法开发了剪力墙布置设计模型。
- 引文："A shear wall layout design model is developed based on the aforementioned training method." (Gu et al., 2024, p.2)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### C12 ・ Gu2024_ShearWall_Diffusion ・ 一句话主张 ・ p.15

- 论断：该文提出一种基于扩散模型的剪力墙结构智能设计方法。
- 引文："This study proposed an intelligent design method for shear wall structures based on a diffusion model." (Gu et al., 2024, p.15)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### C13 ・ Gu2024_ShearWall_Diffusion ・ 明确写出的局限 ・ p.15

- 论断：作者指出该研究中扩散模型的应用仍处于初步阶段。
- 引文："It is important to note that the use of the diffusion model in this study remains in its preliminary stage." (Gu et al., 2024, p.15)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### C14 ・ Survey2025_FloorPlanRetrieval_MDPI ・ 案例或数据的表示形式 ・ p.3

- 论断：平面图以高层语义特征与特征向量的形式表示，并用特征向量计算图像相似度。
- 引文："By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans." (Ling et al., 2025, p.3)
- 卡片：`litrev/_probe/full/Survey2025_FloorPlanRetrieval_MDPI.md`（可读原文上下文）

### C15 ・ Zhao2023_ShearWall_GNN ・ 一句话主张 ・ p.1

- 论断：作者提出一种基于图神经网络（GNN）的剪力墙布置智能设计方法。
- 引文："Therefore, this study develops an intelligent design method for shear wall layouts based on GNNs." (Zhao et al., 2023, p.1)
- 卡片：`litrev/_probe/full/Zhao2023_ShearWall_GNN.md`（可读原文上下文）

### C16 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 案例或数据的表示形式 ・ p.8

- 论断：数据以图表示，输入图的节点特征为二维或六维张量，边特征为九维张量。
- 引文："These input graphs represented node features as two- or six-dimensional tensors and represented edge features as nine-dimensional tensors as described in Section 3.2." (Xia et al., 2025, p.8)
- 卡片：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md`（可读原文上下文）

### C17 ・ Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM ・ 相似性或检索机制 ・ p.4

- 论断：系统实现了三种匹配与检索技术：MetisCBR、以 VF2 为代表的精确图匹配、以及以 index-based 指称的不精确图匹配。
- 引文："This section presents the three matching and retrieval techniques implemented in Archistant: MetisCBR, exact graph matching (referred as VF2), and inexact graph matching (referred as index-based)." (Sabri et al., 2017, p.4)
- 卡片：`litrev/_probe/full/Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM.md`（可读原文上下文）

### C18 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 明确写出的局限 ・ p.4

- 论断：作者明确指出这些数据不足以归纳出好的泛化。
- 引文："We recognize the fact that these data are not sufﬁcient to induce a good generalization." (Soibelman et al., 2000, p.4)
- 卡片：`litrev/_probe/full/SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign.md`（可读原文上下文）

### C19 ・ delasHeras2014_RunlengthHistogram_FloorPlans ・ 问题域 ・ p.2

- 论断：问题域是建筑平面图这类线绘图在检索场景下的图形识别与视觉美学。
- 引文："This paper is an early attempt to introduce visual aesthetics in graphics recognition, in particular in line drawings of architectural plans in a retrieval scenario." (de las Heras et al., 2014, p.2)
- 卡片：`litrev/_probe/full/delasHeras2014_RunlengthHistogram_FloorPlans.md`（可读原文上下文）

### C20 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 明确写出的局限 ・ p.8

- 论断：作者明确写出本文只考察 IoU 与 GED，未考虑其他常见的图像与图相似度度量。
- 引文："This work is however limited to investigating IoU and GED and does not consider other well-known image- and graph-based similarity metrics." (van Engelenburg et al., 2023, p.8)
- 卡片：`litrev/_probe/full/vanEngelenburg2023_SSIG_FloorPlan.md`（可读原文上下文）
