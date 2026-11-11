# S2 答案键（主控侧留档）

> 由 `python tools/audit_prep.py sample` 生成，与 `SAMPLE_S2.md` 同源。
> 判定表总条目 138 · 抽样时点 SUPPORTED 128 · 抽 12 条（9.4%）· seed=71 rate=9%。
> 输入快照戳：`8cf4be2cc9`
> **本文件是答案键：禁止贴给任何 `auditor-*`，也不要登记进 `BATCHES.json`。**
> 审计员的 read 白名单只有「契约 + 本批输入」，它读不到本文件；主控也不要在派发提示词里引用它。
<!-- picks: pool=128,k=12,seed=71,rate=0.09375,total=138,B1-03,B1-07,B1-16,B2-08,B3-06,B3-13,R1-07,R1-09,R2-12,R3-10,R4-05,R5-14 -->

## 抽样算法（可复现）

`pool = [判定表里 support == SUPPORTED 的条目，按 id 升序]`；`k = round(128 * 0.09375) = 12`；`idx = sorted(random.Random(71).sample(range(128), 12))`；取 `pool[idx]`。

## 源批次输入戳（抽样时的口径）

| 批次输入 | 快照 sha1 |
|---|---|
| `FRAG_B1.md` | `81c78be532` |
| `FRAG_B2.md` | `05632596fd` |
| `FRAG_B3.md` | `e58bc1a19f` |
| `REST_B1.md` | `84be957ff5` |
| `REST_B2.md` | `7695094c1c` |
| `REST_B3.md` | `d8ca4201bf` |
| `REST_B4.md` | `3231c9e097` |
| `REST_B5.md` | `6cad652fa1` |
| `REST_B6.md` | `7cb35452e0` |

## 对照表（抽检 id → 原判定）

| 抽检 id | 原批次 id | 文献 | 节 | 原支撑 | 原自足 | 原依据 | 原缺什么 |
|---|---|---|---|---|---|---|---|
| S01 | B1-03 | Borner1993_StructuralSimilarity_CBR | 一句话主张 | SUPPORTED | SELF | "if and only if" | — |
| S02 | B1-07 | Liao1998_SimilarityMeasures_CBR | 系统形态 | SUPPORTED | SELF | "being developed" | — |
| S03 | B1-16 | Zhao2023_ShearWall_GNN | 明确写出的局限 | SUPPORTED | DEPENDENT | "easier to avoid" | 自足缺主语：引文是谓语片段，需补主语（如 overfitting is easier to avoid …） |
| S04 | B2-08 | MaherGomez1996_CBR_StructuralDesign | 案例或数据的表示形式 | SUPPORTED | SELF | "attribute-value" | — |
| S05 | B3-06 | Liao1998_SimilarityMeasures_CBR | 相似性或检索机制 | SUPPORTED | SELF | "area ratio" | — |
| S06 | B3-13 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 评价方式 | SUPPORTED | DEPENDENT | "the same with" | 自足缺先行词：this selection 的所指不在引文内，需补明"哪一项选型" |
| S07 | R1-07 | Roith2017_GraphBasedDesign_FederatedDB_VisEng | 评价方式 | SUPPORTED | SELF | "Seven architects were asked" | — |
| S08 | R1-09 | SharmaThesis_ContentBasedFloorPlanRetrieval | 相似性或检索机制 | SUPPORTED | SELF | "two phase matching and retrieval" | — |
| S09 | R2-12 | SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 相似性或检索机制 | SUPPORTED | SELF | "subset of cases" | — |
| S10 | R3-10 | SharmaThesis_ContentBasedFloorPlanRetrieval | 评价方式 | SUPPORTED | SELF | "0.247 in case" | — |
| S11 | R4-05 | Rodrigues2017_Clustering_FloorPlans | 评价方式 | SUPPORTED | SELF | "72 ﬂoor plans" | — |
| S12 | R5-14 | Xia2025_CoDesign_ShearWallBeam_GNN | 相似性或检索机制 | SUPPORTED | SELF | "predicting edge" | — |

> 全部候选条目在抽样时点的支撑码都是 `SUPPORTED`；本文件记录的是**抽样时点的原判**，不是标准答案。
> `verify-sample` 只报差异、不裁定谁对。若报差异，按 RUNBOOK §五：登记争议项、冻结 131 条汇总、
> 先补证据（定向扩抽 / 固定契约双跑），由主控人工裁决后才决定是否整批重审；不自动重审、不逐条修补。
> 上方 `<!-- picks -->` 是**冻结清单**：判定表事后被裁决修改，本文件不失效，`sample --check` 仍按抽样时点原判复现；
> 若要抽新一批，先另存旧文件再重跑 `sample`，不要在旧文件上手改。
