# 子代理映射表

> 由 `tools/gen_subagents.py` 生成，与 `.opencode/agents/` 同源。主控派活前先查这张表，不要凭记忆写 agent 名。

## 文献级（文件级隔离：每个 agent 只能读自己那篇 txt、只能写自己那条笔记）

| 文献 | 首次抽取 | 返工扩句 |
|---|---|---|
| `AamodtPlaza1994_CBR_Foundations` | —（卡片已存在） | `qx-aamodtplaza1994-cbr-foundations` |
| `Ahmed2013_Analysis_SketchRetrieval_FloorPlans` | —（卡片已存在） | `qx-ahmed2013-analysis-sketchretrieval-floorplans` |
| `Ayzenshtadt2016_ThinkingWithContainers_ICAART` | —（卡片已存在） | `qx-ayzenshtadt2016-thinkingwithcontainers-icaart` |
| `Borner1993_StructuralSimilarity_CBR` | —（卡片已存在） | `qx-borner1993-structuralsimilarity-cbr` |
| `delasHeras2014_RunlengthHistogram_FloorPlans` | —（卡片已存在） | `qx-delasheras2014-runlengthhistogram-floorplans` |
| `Gu2024_ShearWall_Diffusion` | —（卡片已存在） | `qx-gu2024-shearwall-diffusion` |
| `Liao1998_SimilarityMeasures_CBR` | —（卡片已存在） | `qx-liao1998-similaritymeasures-cbr` |
| `Maher1987_ExpertSystems_StructuralDesign` | —（卡片已存在） | `qx-maher1987-expertsystems-structuraldesign` |
| `MaherGomez1996_CBR_StructuralDesign` | —（卡片已存在） | `qx-mahergomez1996-cbr-structuraldesign` |
| `MaherGomez1997_CBR_in_Design` | —（卡片已存在） | `qx-mahergomez1997-cbr-in-design` |
| `Napps2021_BIM_VariantRetrieval_CBR` | —（卡片已存在） | `qx-napps2021-bim-variantretrieval-cbr` |
| `Rodrigues2017_Clustering_FloorPlans` | —（卡片已存在） | `qx-rodrigues2017-clustering-floorplans` |
| `Roith2017_GraphBasedDesign_FederatedDB_VisEng` | —（卡片已存在） | `qx-roith2017-graphbaseddesign-federateddb-viseng` |
| `Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM` | —（卡片已存在） | `qx-sabri2017-semanticpattern-floorplanretrieval-icpram` |
| `SharmaThesis_ContentBasedFloorPlanRetrieval` | —（卡片已存在） | `qx-sharmathesis-contentbasedfloorplanretrieval` |
| `SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign` | —（卡片已存在） | `qx-soibelmanpenamora2000-mram-conceptualstructuraldesign` |
| `SriramMaherFenves1985_KBES_StructuralDesign` | —（卡片已存在） | `qx-srirammaherfenves1985-kbes-structuraldesign` |
| `Survey2025_FloorPlanRetrieval_MDPI` | —（卡片已存在） | `qx-survey2025-floorplanretrieval-mdpi` |
| `vanEngelenburg2023_SSIG_FloorPlan` | —（卡片已存在） | `qx-vanengelenburg2023-ssig-floorplan` |
| `Xia2025_CoDesign_ShearWallBeam_GNN` | —（卡片已存在） | `qx-xia2025-codesign-shearwallbeam-gnn` |
| `Zhang2006_BP_CaseRetrieval_HighriseStructureForm` | —（卡片已存在） | `qx-zhang2006-bp-caseretrieval-highrisestructureform` |
| `Zhao2023_ShearWall_GNN` | —（卡片已存在） | `qx-zhao2023-shearwall-gnn` |

## 审计批次（批次级隔离：只能读本批输入、只能写本批输出）

| 批次 | Agent | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| `frag_b1` | `auditor-frag-b1` | `litrev/_probe/audit/FRAG_B1.md` | `litrev/_probe/audit/out_B1.md` | C4 句中片段 B1（16 条） |
| `frag_b2` | `auditor-frag-b2` | `litrev/_probe/audit/FRAG_B2.md` | `litrev/_probe/audit/out_B2.md` | C4 句中片段 B2（16 条） |
| `frag_b3` | `auditor-frag-b3` | `litrev/_probe/audit/FRAG_B3.md` | `litrev/_probe/audit/out_B3.md` | C4 句中片段 B3（16 条） |
| `rest_b1` | `auditor-rest-b1` | `litrev/_probe/audit/REST_B1.md` | `litrev/_probe/audit/out_R1.md` | 剩余 83 条复核 B1 |
| `rest_b2` | `auditor-rest-b2` | `litrev/_probe/audit/REST_B2.md` | `litrev/_probe/audit/out_R2.md` | 剩余 83 条复核 B2 |
| `rest_b3` | `auditor-rest-b3` | `litrev/_probe/audit/REST_B3.md` | `litrev/_probe/audit/out_R3.md` | 剩余 83 条复核 B3 |
| `rest_b4` | `auditor-rest-b4` | `litrev/_probe/audit/REST_B4.md` | `litrev/_probe/audit/out_R4.md` | 剩余 83 条复核 B4 |
| `rest_b5` | `auditor-rest-b5` | `litrev/_probe/audit/REST_B5.md` | `litrev/_probe/audit/out_R5.md` | 剩余 83 条复核 B5 |
| `sample_s1` | `auditor-sample-s1` | `litrev/_probe/audit/SAMPLE_S1.md` | `litrev/_probe/audit/out_S1.md` | 抽检 S1（seed=42、10/80=12.5%，2026-11-10 按 D-01 裁决后的新候选池重抽；候选集构成不披露给审计员） |
| `rest_b1_dup` | `auditor-rest-b1-dup` | `litrev/_probe/audit/REST_B1.md` | `litrev/_probe/audit/out_D1.md` | 固定契约双跑 R1（同输入另存对照，不覆盖 out_R1.md；前缀 D 不进 131 口径） |
| `rest_b2_dup` | `auditor-rest-b2-dup` | `litrev/_probe/audit/REST_B2.md` | `litrev/_probe/audit/out_D2.md` | 固定契约双跑 R2（同输入另存对照，不覆盖 out_R2.md；前缀 D 不进 131 口径） |
| `rest_b3_dup` | `auditor-rest-b3-dup` | `litrev/_probe/audit/REST_B3.md` | `litrev/_probe/audit/out_D3.md` | 固定契约双跑 R3（同输入另存对照，不覆盖 out_R3.md；前缀 D 不进 131 口径） |
| `rest_b4_dup` | `auditor-rest-b4-dup` | `litrev/_probe/audit/REST_B4.md` | `litrev/_probe/audit/out_D4.md` | 固定契约双跑 R4（同输入另存对照，不覆盖 out_R4.md；前缀 D 不进 131 口径） |
| `rest_b5_dup` | `auditor-rest-b5-dup` | `litrev/_probe/audit/REST_B5.md` | `litrev/_probe/audit/out_D5.md` | 固定契约双跑 R5（同输入另存对照，不覆盖 out_R5.md；前缀 D 不进 131 口径） |
| `frag_b3_probe` | `auditor-frag-b3-probe` | `litrev/_probe/audit/FRAG_B3P.md` | `litrev/_probe/audit/out_B3P.md` | B3-10 第三次独立判定（单条，与 S05 同输入；不覆盖 out_B3.md，前缀 B3P 不进 131 口径） |
| `frag_b1_dup` | `auditor-frag-b1-dup` | `litrev/_probe/audit/FRAG_B1.md` | `litrev/_probe/audit/out_E1.md` | 固定契约双跑 B1（口径统一后补 131 条全量基线的 frag 部分；前缀 E 不进 131 口径） |
| `frag_b2_dup` | `auditor-frag-b2-dup` | `litrev/_probe/audit/FRAG_B2.md` | `litrev/_probe/audit/out_E2.md` | 固定契约双跑 B2（补 131 条全量基线的 frag 部分；前缀 E 不进 131 口径） |
| `frag_b3_dup` | `auditor-frag-b3-dup` | `litrev/_probe/audit/FRAG_B3.md` | `litrev/_probe/audit/out_E3.md` | 固定契约双跑 B3（补 131 条全量基线的 frag 部分；前缀 E 不进 131 口径） |
| `fix_b1` | `auditor-fix-b1` | `litrev/_probe/audit/FIX_B1.md` | `litrev/_probe/audit/out_FIX.md` | 改稿后定点重判 8 条（R1-01/R1-02/R1-14/R1-16/R2-01/R2-06/R2-15/R4-03）；不覆盖 out_R*.md，文件名不匹配 out_[A-Z]+<数字> 口径，故不进 131 条汇总 |

## 固定角色

| Agent | 职责 |
|---|---|
| `orchestrator` | 主控（primary，手写，不生成） |
| `checker` | 核验（bash 白名单只放行 verify/matrix/locate/audit-count） |
