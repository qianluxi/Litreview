# round-05 主控侧准备报告（抽检 S1 重建）

- 时间：2026-11-10 10:0x，基线提交 `691939a`（工作区原本干净）
- 范围：**只做不依赖 OpenCode 的部分**。本轮没有派 `task`、没有重跑审计、没有改判定输出。
- 取证口径：以文件与命令退出码为准，不采信任何自述；`litrev/litrev.py` 一字未改。

## 一、做了什么

| # | 文件 | 改动 |
|---|---|---|
| 1 | `tools/audit_prep.py` | 新增主控侧准备工具，三个子命令：`sample` / `sample --check` / `review` / `verify-sample` |
| 2 | `litrev/_probe/audit/SAMPLE_S1.md` | **重建**：候选集从「全库 131 条」改为「当前 81 条 SUPPORTED」，抽 10 条（12.3%），头部加 `> 快照 sha1: 0ff8391a63`（第 6 行） |
| 3 | `litrev/_probe/audit/SAMPLE_S1_KEYS.md` | 新增答案键：抽样算法、8 个源批次输入戳、10 条「抽检 id → 原批次 id / 原判定」对照 |
| 4 | `litrev/_probe/audit/REVIEW_NONSUPPORTED.md` | 新增 50 条非 SUPPORTED 人工复核清单（PARTIAL 49 / UNSUPPORTED 1），留空「复核结论 / 处理」两栏 |
| 5 | `litrev/_probe/audit/BATCHES.json` | 只改 `sample_s1` 的 note（12.2% → 10/81=12.3%），路径未动 |
| 6 | `litrev/_probe/AGENT_MAP.md` | 由生成器同步上一条 note；**`.opencode/agents/` 下 33 个文件零改动** |
| 7 | `RUNBOOK.md` | §五 抽检规程重写：候选集口径、闭卷纪律、戳、`verify-sample` 验收；§八 加变更记录 |
| 8 | `litrev/PIPELINE.md` | 抽检段落改为新工具，写明「不要再直接用 `litrev.py sample` 生成 S1」 |
| 9 | `HANDOFF-05.md` | 新增：给 OpenCode 的可粘派发指令、六条验收、禁止事项、报告要求 |

**没有碰**：`litrev/litrev.py`、`AUDIT_CONTRACT.md`、卡片 `full/*.md`、8 张 `out_B*.md`/`out_R*.md`、
`out_S1.md`（旧 16 行无戳版保留作历史，等 OpenCode 覆盖）、`.opencode/agents/`、`opencode.json`。

## 二、三个设计决定（以及为什么）

1. **候选集必须是「当前 SUPPORTED」，不是全库。**
   契约 §七.2 要求 SUPPORTED 按 10–15% 抽检；原 `litrev.py sample` 从 `_probe/full/*.md` 的全部 131 条抽，
   会抽到本来就要人看的 PARTIAL/UNSUPPORTED，抽检等于稀释。新工具从 8 张判定表读候选集，
   `random.Random(42).sample(range(81), 10)`，按 id 升序固定。旧 `SAMPLE_S1.md` 抽的 16 条来自 131 条池，
   且在 `S84/P46/U1` 时代判定，早已失效。
2. **裁判不参与准备。** `tools/audit_prep.py` 只读批次输入与判定表，不写判定、不改 `litrev.py`。
   戳算法与 `litrev.py batch` 完全一致（对所有 `- 论断：`/`- 引文：` 行取 sha1 前 10 位），
   所以「输入戳 ↔ 输出首行」仍可用同样的机械方式核对。
3. **输入必须闭卷，答案键单独留档。** 第一版输入头写了「候选集是 81 条 SUPPORTED」，等于把答案递给审计员——
   已删。现在输入只说「81 条候选条目」，不出现任何判定码、原依据、答案键路径。答案键在
   `SAMPLE_S1_KEYS.md`，`auditor-*` 的 read 白名单只有「契约 + 本批输入」，读不到它；
   `BATCHES.json` 也没登记它。事后「命中率」由 `verify-sample` 拿答案键机械算，不靠人回忆。

`sample --check` 会复算整个批次与答案键并逐字比对，同时校验 8 个源批次输入戳未变——
判定表或卡片一改，抽检立刻报「需重做」，不会悄悄用旧样本。

## 三、机械自检（原始结果）

```
python tools/audit_prep.py sample
  判定表 131 条 · SUPPORTED 81 条 · 抽 10 条（12.3%，seed=42）
  输入：litrev/_probe/audit/SAMPLE_S1.md  > 快照 sha1: 0ff8391a63
  答案键：litrev/_probe/audit/SAMPLE_S1_KEYS.md（禁止贴给 auditor-*）

python tools/audit_prep.py sample --check
  ✓ 抽检批次可复现：10/81 条（12.3%），戳 0ff8391a63，答案键一致，8 个源批次输入戳未变。   EXIT=0

python tools/audit_prep.py review
  非 SUPPORTED 50 条 → litrev/_probe/audit/REVIEW_NONSUPPORTED.md（PARTIAL 49 / UNSUPPORTED 1）

python litrev/litrev.py verify  （逐篇跑 19 张卡片，按「汇总：PASS=n 合计 m」累加）
  卡片 19 篇 · 引文 131 条 · PASS 131 条 · 出现过的判定码 ['PASS'] · 异常 无

python litrev/litrev.py audit-count --check
  合计 131  81 / 49 / 1 · SELF 118 / DEPENDENT 13 · 非 SUPPORTED 50/131 = 38.2%   EXIT=0

python litrev/litrev.py audit-stale --check
  批次输入 131 条 · 卡片 19 篇 / 133 节 / 131 条引文
  判定依据与卡片一致：131/131   ✓ 全部判定的依据与卡片当前内容一致。   EXIT=0

python litrev/litrev.py batch --check
  8 个批次均「无变化」，合计待刷新 0/131 条（--check 不写盘）   EXIT=0

python tools/gen_subagents.py --check
  ✓ 同步：33 个文件与 AGENT_ROLES.md 一致   EXIT=0
```

`verify-sample` 在**临时目录**用合成回写做了三分支验证（没有往仓库写任何假的 `out_S1.md`）：

| 用例 | 结果 |
|---|---|
| 合规 10 行、戳/表头/合计全对、10/10 仍 SUPPORTED | `EXIT=0`，打印 6 条 ✓ |
| 一条降档 `S05: SUPPORTED→PARTIAL` | `EXIT=1`，打印降档清单 + 「整批重审」提示 |
| 无戳、缺判定行、缺合计行 | `EXIT=1`，逐条列出 4 个问题 |

## 四、抽出来的 10 条（答案键摘要）

| S | 原批次 id | 文献 | 节 |
|---|---|---|---|
| S01 | B1-13 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 相似性或检索机制 |
| S02 | B2-12 | Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 问题域 |
| S03 | B2-16 | delasHeras2014_RunlengthHistogram_FloorPlans | 相似性或检索机制 |
| S04 | B3-02 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 明确写出的局限 |
| **S05** | **B3-10** | **SriramMaherFenves1985_KBES_StructuralDesign** | 问题域 |
| S06 | R1-12 | Survey2025_FloorPlanRetrieval_MDPI | 一句话主张 |
| S07 | R2-03 | Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 案例或数据的表示形式 |
| S08 | R2-08 | Roith2017_GraphBasedDesign_FederatedDB_VisEng | 明确写出的局限 |
| S09 | R3-16 | delasHeras2014_RunlengthHistogram_FloorPlans | 评价方式 |
| S10 | R5-05 | Rodrigues2017_Clustering_FloorPlans | 一句话主张 |

**S05 = B3-10** 正是 `reports/round-04-verification.md` §三 单独点名可疑的那条
（上轮 `DEPENDENT → SELF`，引文 `These problems are often ill-` 按 §五.1 更像应判 DEPENDENT）。
这次由闭卷抽检独立重判，正好给一个不带旧结论的复核机会——但**不要在派发时提示这一点**，否则又污染闭卷。

## 五、这轮没做的（需要你决定 / 需要 OpenCode）

| 待办 | 为什么留着 |
|---|---|
| 派 `auditor-sample-s1` 写 `out_S1.md` | 只能在 OpenCode 里派一次 `task`；指令在 `HANDOFF-05.md`，**无需重启** |
| ② 修 auditor 读回权限 | 一行改动（`gen_subagents.py` 的 read 加 `(BATCH_OUT, "allow")`），但要重生成 9 个 agent 并重启；上轮核验明确「等你决定」，本轮不擅自引入 |
| ③ 固定契约双跑 REST 五批 | 需新增 5 个批次登记 + 5 个 agent（同样要重启），且应与本轮抽检分开记证据；不能用跨版本重审冒充双跑 |
| ④ 50 条非 SUPPORTED 逐条人看 | 清单已生成、栏位已留空；这是人工判断，不能由子代理代填 |

## 六、现在能说的准确话

131 条引文逐字可溯、131 条判定依据未过期，这两条仍然成立；`SUPPORTED` 仍只是分诊结果。
本轮把「SUPPORTED 必须抽检」从一句纪律变成了**可复现的批次 + 独立答案键 + 机械验收命令**，
但抽检本身还没跑完——**在 `out_S1.md` 回来并通过 `verify-sample` 之前，不能说「81 条 SUPPORTED 抽过了」**。
