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
| `sample_s1` | `auditor-sample-s1` | `litrev/_probe/audit/SAMPLE_S1.md` | `litrev/_probe/audit/out_S1.md` | 抽检 S1（seed=42、10/81=12.3%；候选集构成不披露给审计员） |

## 固定角色

| Agent | 职责 |
|---|---|
| `orchestrator` | 主控（primary，手写，不生成） |
| `checker` | 核验（bash 白名单只放行 verify/matrix/locate/audit-count） |
