# S1 答案键（主控侧留档）

> 由 `python tools/audit_prep.py sample` 生成，与 `SAMPLE_S1.md` 同源。
> 判定表总条目 131 · 抽样时点 SUPPORTED 80 · 抽 10 条（12.5%）· seed=42 rate=12%。
> 输入快照戳：`7d1a204d54`
> **本文件是答案键：禁止贴给任何 `auditor-*`，也不要登记进 `BATCHES.json`。**
> 审计员的 read 白名单只有「契约 + 本批输入」，它读不到本文件；主控也不要在派发提示词里引用它。
<!-- picks: pool=80,k=10,seed=42,rate=0.12,total=131,B1-13,B2-12,B2-16,B3-02,B3-12,R1-13,R2-04,R2-09,R4-01,R5-06 -->

## 抽样算法（可复现）

`pool = [判定表里 support == SUPPORTED 的条目，按 id 升序]`；`k = round(80 * 0.12) = 10`；`idx = sorted(random.Random(42).sample(range(80), 10))`；取 `pool[idx]`。

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
| S05 | B3-12 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 案例或数据的表示形式 | SUPPORTED | SELF | "characteristic" | — |
| S06 | R1-13 | Survey2025_FloorPlanRetrieval_MDPI | 明确写出的局限 | SUPPORTED | SELF | "may not adequately represent" | — |
| S07 | R2-04 | Gu2024_ShearWall_Diffusion | 评价方式 | SUPPORTED | SELF | "primarily" | — |
| S08 | R2-09 | Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 一句话主张 | SUPPORTED | SELF | "combines CBR" | — |
| S09 | R4-01 | AamodtPlaza1994_CBR_Foundations | 相似性或检索机制 | SUPPORTED | SELF | "surface match" | — |
| S10 | R5-06 | Rodrigues2017_Clustering_FloorPlans | 明确写出的局限 | SUPPORTED | DEPENDENT | "same shape type" | 引文 it 需补主语 |

> 全部候选条目在抽样时点的支撑码都是 `SUPPORTED`；本文件记录的是**抽样时点的原判**，不是标准答案。
> `verify-sample` 只报差异、不裁定谁对。若报差异，按 RUNBOOK §五：登记争议项、冻结 131 条汇总、
> 先补证据（定向扩抽 / 固定契约双跑），由主控人工裁决后才决定是否整批重审；不自动重审、不逐条修补。
> 上方 `<!-- picks -->` 是**冻结清单**：判定表事后被裁决修改，本文件不失效，`sample --check` 仍按抽样时点原判复现；
> 若要抽新一批，先另存旧文件再重跑 `sample`，不要在旧文件上手改。
