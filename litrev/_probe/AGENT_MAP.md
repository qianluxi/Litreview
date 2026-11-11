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
| `Lin2022_BERT_DisasterTweet` | `ex-lin2022-bert-disastertweet` | `qx-lin2022-bert-disastertweet` |
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
| `fix_b2` | `auditor-fix-b2` | `litrev/_probe/audit/FIX_B2.md` | `litrev/_probe/audit/out_FIX_2.md` | 第二轮定点重判 31 条（A 情态加强 8 + B 术语属性添加 23）；不覆盖 out_*.md，输出名带下划线以避开 out_[A-Z]+<数字> 口径，不进 131 条汇总 |
| `fix_b3` | `auditor-fix-b3` | `litrev/_probe/audit/FIX_B3.md` | `litrev/_probe/audit/out_FIX_3.md` | 第三轮定点重判 13 条（C 引文截断 11 + E 方向不符 B1-06 + B1-08 改法错）：全部换成含主谓的完整引文，5 条论断同步最小改写；输出名带下划线，不进 131 条汇总 |
| `fix_b4` | `auditor-fix-b4` | `litrev/_probe/audit/FIX_B4.md` | `litrev/_probe/audit/out_FIX_4.md` | 第四轮定点重判 2 条（B3-01 情态升级、B3-05 对象限定被删）：引文一字未动，只改论断；输出名带下划线，不进 131 条汇总 |
| `rest_b6` | `auditor-rest-b6` | `litrev/_probe/audit/REST_B6.md` | `litrev/_probe/audit/out_R6.md` | 第 2 步新文献端到端：Ayzenshtadt2016 七节首次审计（7 条）；REST_B6 按新卡片生成，out_R6.md 首次把一篇新文献收进判定表（131→138） |
| `fix_b5` | `auditor-fix-b5` | `litrev/_probe/audit/FIX_B5.md` | `litrev/_probe/audit/out_FIX_5.md` | 第五轮定点重判 1 条（B3-04）：论断删掉「未给出数据集规模或指标数值」这个证明否定半句，引文一字未动；输出名带下划线，不进 138 条汇总 |
| `fix_b6` | `auditor-fix-b6` | `litrev/_probe/audit/FIX_B6.md` | `litrev/_probe/audit/out_FIX_6.md` | 第六轮定点重判 1 条（B2-08）：论断一字未动，引文换成同篇 p.10 的直接表述（原 p.6 那句讲的是「两系统差异」，不是「案例如何描述」）；输出名带下划线，不进 138 条汇总 |
| `probe_r6_04` | `auditor-probe-r6-04` | `litrev/_probe/audit/PROBE_R6-04.md` | `litrev/_probe/audit/out_P_6.md` | D-03 第三次独立判定（R6-04 单条，闭卷盲判）：前两次人开卷 PARTIAL / 机器闭卷 SUPPORTED 为 1:1；不改判定表，只补齐多数票 |
| `sample_s2` | `auditor-sample-s2` | `litrev/_probe/audit/SAMPLE_S2.md` | `litrev/_probe/audit/out_S2.md` | 抽检补抽第二批 12 条（seed=71，排除 S1 已抽 10 条）：从 128 条 SUPPORTED 池抽 9.4%，测自洽/漂移；out_S2 不进 audit-count 默认口径（前缀 B,R） |

## 固定角色

| Agent | 职责 |
|---|---|
| `orchestrator` | 主控（primary，手写，不生成） |
| `checker` | 核验（bash 白名单只放行 verify/matrix/locate/audit-count） |
