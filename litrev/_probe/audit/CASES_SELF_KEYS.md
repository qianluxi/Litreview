# C1 自足轴判例集映射（主控侧留档，不贴给任何人）

> 由 `python tools/audit_prep.py cases` 生成，与 `CASES_SELF.md` 同源；条目清单来自 `CASES_SELF_IDS.txt`。
> 判定表总条目 131 · 本集 20 条（表内 DEPENDENT 10 + 双跑边界 10）。
> 输入快照戳：`a4e66877dc`
> **本文件是答案键**：记录每条 C id 对应的原批次 id 与表内现判；判定者填表时读不到本文件。
> 人填完后跑 `python tools/audit_prep.py verify-cases`，输出自足轴一致率与方向。
> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`cases --check` 仍按清单复现。

<!-- picks: B1-08,B1-16,B2-05,B2-11,B3-08,B3-09,B3-11,R2-02,R2-17,R3-08,R1-03,R3-02,R3-03,R3-12,R3-15,R4-13,R5-08,R5-11,R5-15,R5-17 -->

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
