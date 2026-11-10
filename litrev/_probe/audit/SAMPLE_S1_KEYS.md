# S1 答案键（主控侧留档）

> 由 `python tools/audit_prep.py sample` 生成，与 `SAMPLE_S1.md` 同源。
> 判定表总条目 131 · 当前 SUPPORTED 81 · 抽 10 条（12.3%）· seed=42 rate=12%。
> 输入快照戳：`0ff8391a63`
> **本文件是答案键：禁止贴给任何 `auditor-*`，也不要登记进 `BATCHES.json`。**
> 审计员的 read 白名单只有「契约 + 本批输入」，它读不到本文件；主控也不要在派发提示词里引用它。

## 抽样算法（可复现）

`pool = [判定表里 support == SUPPORTED 的条目，按 id 升序]`；`k = round(81 * 0.12) = 10`；`idx = sorted(random.Random(42).sample(range(81), 10))`；取 `pool[idx]`。

## 源批次输入戳（抽样时的口径）

| 批次输入 | 快照 sha1 |
|---|---|
| `FRAG_B1.md` | `9ff1753875` |
| `FRAG_B2.md` | `902e819463` |
| `FRAG_B3.md` | `a52c3ea485` |
| `REST_B1.md` | `c8ad398b0d` |
| `REST_B2.md` | `6e0fdbeb4f` |
| `REST_B3.md` | `2861fd7ff6` |
| `REST_B4.md` | `09168d9ad9` |
| `REST_B5.md` | `b8a12801bd` |

## 对照表（抽检 id → 原判定）

| 抽检 id | 原批次 id | 文献 | 节 | 原支撑 | 原自足 | 原依据 | 原缺什么 |
|---|---|---|---|---|---|---|---|
| S01 | B1-13 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 相似性或检索机制 | SUPPORTED | SELF | "weight distance" | — |
| S02 | B2-12 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 问题域 | SUPPORTED | SELF | "structural form" | — |
| S03 | B2-16 | delasHeras2014_RunlengthHistogram_FloorPlans | 相似性或检索机制 | SUPPORTED | SELF | "χ2 distance" | — |
| S04 | B3-02 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 明确写出的局限 | SUPPORTED | SELF | "only able to" | — |
| S05 | B3-10 | SriramMaherFenves1985_KBES_StructuralDesign | 问题域 | SUPPORTED | SELF | "not amenable to" | — |
| S06 | R1-12 | Survey2025_FloorPlanRetrieval_MDPI | 一句话主张 | SUPPORTED | SELF | "four primary features essential for the retrieval" | — |
| S07 | R2-03 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 案例或数据的表示形式 | SUPPORTED | SELF | "a graph G" | — |
| S08 | R2-08 | Roith2017_GraphBasedDesign_FederatedDB_VisEng | 明确写出的局限 | SUPPORTED | SELF | "input set" | — |
| S09 | R3-16 | delasHeras2014_RunlengthHistogram_FloorPlans | 评价方式 | SUPPORTED | SELF | "compared to gtA" | — |
| S10 | R5-05 | Rodrigues2017_Clustering_FloorPlans | 一句话主张 | SUPPORTED | SELF | "captures better" | — |

> 全部候选条目在抽样时点的支撑码都是 `SUPPORTED`；若 `verify-sample` 发现抽检回写里出现降档，按 RUNBOOK §五「整批重审」，不逐条修补。
