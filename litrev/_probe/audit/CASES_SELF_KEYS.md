# C1 自足轴判例集映射（主控侧留档，不贴给任何人）

> 由 `python tools/audit_prep.py cases` 生成，与 `CASES_SELF.md` 同源；条目清单来自 `CASES_SELF_IDS.txt`。
> 判定表总条目 131 · 本集 20 条（表内 DEPENDENT 10 + 双跑边界 10）。
> 输入快照戳：`a4e66877dc`
> **本文件是答案键**：记录每条 C id 对应的原批次 id 与表内现判；判定者填表时读不到本文件。
> 人填完后跑 `python tools/audit_prep.py verify-cases`，输出自足轴一致率与方向。
> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`cases --check` 仍按清单复现。

<!-- picks: total=131,B1-08,B1-16,B2-05,B2-11,B3-08,B3-09,B3-11,R2-02,R2-17,R3-08,R1-03,R3-02,R3-03,R3-12,R3-15,R4-13,R5-08,R5-11,R5-15,R5-17 -->

## 对照表（C id → 表内现判）

| C id | 原批次 id | 文献 | 节 | 表内支撑 | 表内自足 | 表内依据 | 表内缺什么 |
|---|---|---|---|---|---|---|---|
| C01 | B1-08 | MaherGomez1996_CBR_StructuralDesign | 问题域 | PARTIAL | DEPENDENT | "design projects" | 删"建筑"（引文只作 structural design）；information≠"案例资料"，需补依据 |
| C02 | B1-16 | Zhao2023_ShearWall_GNN | 明确写出的局限 | PARTIAL | DEPENDENT | "limited shear" | 引文说样本有限使过拟合"更易避免"，非"需避免"；"用于训练"亦无原文 |
| C03 | B2-05 | Gu2024_ShearWall_Diffusion | 相似性或检索机制 | SUPPORTED | DEPENDENT | "diffusion model" | 引文以 this section 作主语，需补指代（如本研究） |
| C04 | B2-11 | SriramMaherFenves1985_KBES_StructuralDesign | 明确写出的局限 | PARTIAL | DEPENDENT | "user interfaces" | 名词短语无主语；"实用实现需要"原文无 |
| C05 | B3-08 | MaherGomez1996_CBR_StructuralDesign | 相似性或检索机制 | PARTIAL | DEPENDENT | "finding matches" | 补主语及"度量相关性""记忆项属性取值"依据 |
| C06 | B3-09 | MaherGomez1996_CBR_StructuralDesign | 明确写出的局限 | PARTIAL | DEPENDENT | "a limited" | 引文仅 when 从句，缺主句及"只…适用"依据 |
| C07 | B3-11 | Survey2025_FloorPlanRetrieval_MDPI | 系统形态 | PARTIAL | DEPENDENT | "advanced fusion" | 补"综述/review"原词 |
| C08 | R2-02 | AamodtPlaza1994_CBR_Foundations | 明确写出的局限 | PARTIAL | DEPENDENT | "may easily lead" | “会”加强了 may，应改为“可能轻易导致” |
| C09 | R2-17 | vanEngelenburg2023_SSIG_FloorPlan | 相似性或检索机制 | SUPPORTED | DEPENDENT | "Coined as SSIG" | —（主句缺主语，引用时需补 SSIG） |
| C10 | R3-08 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 明确写出的局限 | SUPPORTED | DEPENDENT | "timeout errors" | 自足性方面需补充说明“These limitations”指代什么 |
| C11 | R1-03 | Gu2024_ShearWall_Diffusion | 系统形态 | SUPPORTED | SELF | "aforementioned training method" | — |
| C12 | R3-02 | Gu2024_ShearWall_Diffusion | 一句话主张 | SUPPORTED | SELF | "diffusion model" | — |
| C13 | R3-03 | Gu2024_ShearWall_Diffusion | 明确写出的局限 | SUPPORTED | SELF | "preliminary" | — |
| C14 | R3-12 | Survey2025_FloorPlanRetrieval_MDPI | 案例或数据的表示形式 | PARTIAL | SELF | "feature vectors" | 删去“以…形式表示”，或补原文依据 |
| C15 | R3-15 | Zhao2023_ShearWall_GNN | 一句话主张 | SUPPORTED | SELF | "based on GNNs" | — |
| C16 | R4-13 | Xia2025_CoDesign_ShearWallBeam_GNN | 案例或数据的表示形式 | SUPPORTED | SELF | "node features" | — |
| C17 | R5-08 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 相似性或检索机制 | SUPPORTED | SELF | "three matching" | — |
| C18 | R5-11 | SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 明确写出的局限 | SUPPORTED | SELF | "not sufﬁcient" | — |
| C19 | R5-15 | delasHeras2014_RunlengthHistogram_FloorPlans | 问题域 | SUPPORTED | SELF | "line drawings" | — |
| C20 | R5-17 | vanEngelenburg2023_SSIG_FloorPlan | 明确写出的局限 | SUPPORTED | SELF | "limited to" | — |

> 共 20 条。

## 原文存档（抽样时点，返工后按此复现）

> 判定时点给出的论断与引文原文。稿件返工后**本节不改写**：`CASES_SELF.md` 的条目详情按本节复现，
> `verify-cases` 用本节 vs 当前批次输入比对，把判后被返工的条目列为「失效」并从分母剔除。

### C01 ・ B1-08

- 论断：问题域是建筑结构设计，案例资料取自结构设计项目。
- 引文："information on structural design projects" (Maher and Gomez, 1996, p.1)

### C02 ・ B1-16

- 论断：作者明确写出用于训练的剪力墙样本有限，需避免过拟合。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)

### C03 ・ B2-05

- 论断：该文采用的生成机制是带掩码张量的图像提示扩散模型。
- 引文："4 | THE CONSTRUCTION, TRAINING, AND INFERENCE OF NEURAL NETWORK MODELS To focus on the diffusion process features of the shear wall portion, this section introduces the construction, training, and inference methods for an image-prompt diffusion model with a mask tensor." (Gu et al., 2024, p.6)

### C04 ・ B2-11

- 论断：作者指出实用实现需要专家系统开发工具，尤其在人机界面与解释能力方面。
- 引文："expert system development tools, notably in the areas of user interfaces, explanation capabilities" (Sriram et al., 1985, p.19)

### C05 ・ B3-08

- 论断：系统通过查找问题描述与记忆项中属性及取值的匹配来度量相关性。
- 引文："a given problem by finding matches between" (Maher and Gomez, 1996, p.4)

### C06 ・ B3-09

- 论断：作者指出这种检索方式只在案例记忆中的案例数量有限时适用。
- 引文："when case memory contains a limited" (Maher and Gomez, 1996, p.10)

### C07 ・ B3-11

- 论断：该文是综述，考察这些特征检索方法并提出面向未来研究的融合技术。
- 引文："This paper thoroughly examines these feature retrieval methods and introduces advanced fusion techniques to support future research" (Ling et al., 2025, p.23)

### C08 ・ R2-02

- 论断：作者明确指出，这种索引方式会随案例数量的增加而轻易导致索引的爆炸式增长。
- 引文："This may easily lead to an explosive growth of indices with increased number of cases." (Aamodt and Plaza, 1994, p.10)

### C09 ・ R2-17

- 论断：SSIG 被表述为基于 IoU 的相似度与基于 nGED 的相似度之间的加权平均。
- 引文："Coined as SSIG (Structural Similarity by IoU and GED), 7 essentially computes a weighted average between a IoU-based and a nGED-based similarity metric." (van Engelenburg et al., 2023, p.5)

### C10 ・ R3-08

- 论断：作者明确写出，索引法的这些局限来自底层 Neo4j 数据库的内部超时错误。
- 引文："These limitations came from internal timeout errors of the underlying Neo4j database, most likely due to a congestion of the database system." (Sabri et al., 2017, p.7)

### C11 ・ R1-03

- 论断：该文基于所提训练方法开发了剪力墙布置设计模型。
- 引文："A shear wall layout design model is developed based on the aforementioned training method." (Gu et al., 2024, p.2)

### C12 ・ R3-02

- 论断：该文提出一种基于扩散模型的剪力墙结构智能设计方法。
- 引文："This study proposed an intelligent design method for shear wall structures based on a diffusion model." (Gu et al., 2024, p.15)

### C13 ・ R3-03

- 论断：作者指出该研究中扩散模型的应用仍处于初步阶段。
- 引文："It is important to note that the use of the diffusion model in this study remains in its preliminary stage." (Gu et al., 2024, p.15)

### C14 ・ R3-12

- 论断：平面图以高层语义特征与特征向量的形式表示，并用特征向量计算图像相似度。
- 引文："By identifying unique high-level semantic features and employing feature vectors to calculate image similarity, this approach enables effective retrieval of building floor plans." (Ling et al., 2025, p.3)

### C15 ・ R3-15

- 论断：作者提出一种基于图神经网络（GNN）的剪力墙布置智能设计方法。
- 引文："Therefore, this study develops an intelligent design method for shear wall layouts based on GNNs." (Zhao et al., 2023, p.1)

### C16 ・ R4-13

- 论断：数据以图表示，输入图的节点特征为二维或六维张量，边特征为九维张量。
- 引文："These input graphs represented node features as two- or six-dimensional tensors and represented edge features as nine-dimensional tensors as described in Section 3.2." (Xia et al., 2025, p.8)

### C17 ・ R5-08

- 论断：系统实现了三种匹配与检索技术：MetisCBR、以 VF2 为代表的精确图匹配、以及以 index-based 指称的不精确图匹配。
- 引文："This section presents the three matching and retrieval techniques implemented in Archistant: MetisCBR, exact graph matching (referred as VF2), and inexact graph matching (referred as index-based)." (Sabri et al., 2017, p.4)

### C18 ・ R5-11

- 论断：作者明确指出这些数据不足以归纳出好的泛化。
- 引文："We recognize the fact that these data are not sufﬁcient to induce a good generalization." (Soibelman et al., 2000, p.4)

### C19 ・ R5-15

- 论断：问题域是建筑平面图这类线绘图在检索场景下的图形识别与视觉美学。
- 引文："This paper is an early attempt to introduce visual aesthetics in graphics recognition, in particular in line drawings of architectural plans in a retrieval scenario." (de las Heras et al., 2014, p.2)

### C20 ・ R5-17

- 论断：作者明确写出本文只考察 IoU 与 GED，未考虑其他常见的图像与图相似度度量。
- 引文："This work is however limited to investigating IoU and GED and does not consider other well-known image- and graph-based similarity metrics." (van Engelenburg et al., 2023, p.8)
