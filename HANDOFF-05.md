# 交接给 OpenCode：第五轮（S1 抽检）

> 本文件只列**一件事**：派一次 `auditor-sample-s1`，把 SUPPORTED 抽检做完。
> **不要重启 OpenCode**（agent 定义一字未改），不要改任何配置，不要顺手做别的批次。
> 主控侧已经把能离线做完的部分全做完了，见下节；这些不要重做。

## 一、主控侧已完成（已机械自检，不要重算）

| 项 | 值 | 证据 |
|---|---|---|
| 引文层 | 19 篇 / **131 条全部 PASS**，其它判定码 0 | 逐篇重跑 `litrev.py verify`，汇总行合计 |
| 判定表自洽 | 131 条 · S81 / P49 / U1 · SELF118 / D13 | `audit-count --check` 退 0 |
| 判定依据未过期 | 131/131 与卡片一致 | `audit-stale --check` 退 0 |
| 批次输入 | 0/131 待刷新，8 个戳齐全 | `batch --check` 退 0 |
| 子代理 | 33 个，与模板同步；**`.opencode/agents/` 无任何改动** | `gen_subagents.py --check` 退 0 |
| 抽检批次 | 从当前 **81 条 SUPPORTED** 按 seed=42 抽 **10 条（12.3%）** | `audit_prep.py sample --check` 退 0 |
| 输入快照戳 | `> 快照 sha1: 0ff8391a63`（在 `SAMPLE_S1.md` **第 6 行**） | 文件原文 |
| 答案键 | `SAMPLE_S1_KEYS.md`，主控侧留档 | 文件原文 |
| 人工复核清单 | `REVIEW_NONSUPPORTED.md`，50 条（P49 / U1） | 文件原文 |

抽检输入是**闭卷**的：文件里没有候选集的判定码、没有原依据、没有答案键路径。
`SAMPLE_S1_KEYS.md` 是答案键，`auditor-*` 的 read 白名单里没有它——**不要把它贴进派发提示词，也不要让子代理去读**。

## 二、任务：派一次 `auditor-sample-s1`

给主控的可粘指令（一次一个 `task`，不要并发）：

```
按 HANDOFF-05.md 执行本轮任务，不是摘要它。

只派一次 task，调用 agent `auditor-sample-s1`：
- 输入：litrev/_probe/audit/SAMPLE_S1.md（10 条）
- 输出：覆盖写 litrev/_probe/audit/out_S1.md（旧文件是上一轮 16 条、无戳，已作废，不要读它、不要参考它）
- 输出第一行原样抄输入第 6 行的 `> 快照 sha1: 0ff8391a63`，一个字符都不能改
- 表头照 `AUDIT_CONTRACT.md` §四 逐字抄；10 行判定（S01–S10，行序与输入一致）+ 末尾一行「合计：10 条（...）」
- 闭卷：不读卡片、别的批次、答案键；不在提示词里透露候选集构成或任何原判定
- 写完只回一行回执，不要重跑、不要顺手改别的文件
```

## 三、验收（返回后逐条过，以文件为准）

| # | 检查 | 判据 |
|---|---|---|
| 1 | 调用状态 | 一次 `task`、`completed`；若 `<task_result>` 为空但文件合规，按 `RUNBOOK.md` §三 视为通过。打印回执全文，别用长度阈值判空 |
| 2 | 首行戳 | `out_S1.md` 第一行 == `> 快照 sha1: 0ff8391a63`，与输入第 6 行逐字相同、不带附加说明 |
| 3 | 格式 | 契约 §四 表头；`^\| S\d\d \|` 判定行**恰好 10 条**、id 为 S01–S10；末尾合计行与明细自洽 |
| 4 | 表自洽 | `python litrev/litrev.py audit-count --prefixes S --check` 退 0（S1 不计入 131 条汇总，默认前缀是 B,R） |
| 5 | 机械验收 | `python tools/audit_prep.py verify-sample` 退 0：戳/表头/10 行/合计/依据逐字命中/**仍判 SUPPORTED 10/10** 全过 |
| 6 | 改动范围 | `git status --short` 里除 `out_S1.md` 与本轮报告外没有别的文件；卡片、契约、`litrev.py`、`.opencode/agents/` 均未动 |

**已知且预期内的现象**：`auditor-sample-s1` 的 `read` 白名单只有「契约 + 本批输入」，没有 `out_S1.md`。
如果它写完想读回自己的输出，会被拒（错误原文带完整 ruleset）。这是 `reports/round-04-verification.md` §二 记录的
生成器缺口，**本轮决定不改**（改了要重生成 9 个 agent 并重启）。按文件为准验收即可，**不要因此重派、不要换 agent、不要当成失败**。

## 四、抽检没过怎么办

`verify-sample` 若报「降档」（某条被判成 PARTIAL / UNSUPPORTED），按 `RUNBOOK.md` §五：**整批重审**
（答案键里记着该条对应的原批次 id），不要逐条改 `out_S1.md` 去凑数字。降档清单与命中率写进报告，先别自己裁决。

## 五、禁止事项

- 不跑 `batch` / `stamp-out`：8 个批次输入未变，跑了只会制造无意义改动；`batch --check` 可以跑，不写盘。
- 不改 `AUDIT_CONTRACT.md`、`litrev/litrev.py`、`.opencode/agents/` 下带 `AUTO-GENERATED` 的文件、卡片 `full/*.md`。
- 不把 `SAMPLE_S1_KEYS.md` / `REVIEW_NONSUPPORTED.md` 的内容贴给任何子代理。
- 不顺手做下一步（固定契约双跑、50 条人工复核、权限修复）；本轮做完就停。

## 六、做完写什么

`reports/round-05-sample.md`：

- `task id`、子会话 id、`<task_result>` 全文、是否被权限拒绝过及次数；
- `audit-count --prefixes S --check` 与 `audit_prep.py verify-sample` 的**原始输出**（不是转述）；
- 10 条判定与答案键的逐条对照（命中率、有无降档、降档集中在哪个原批次）；
- 一句话结论：SUPPORTED 81 条能否继续只做分诊使用，还是触发整批重审。

## 附：主控侧这轮为什么没动其它三项

| 待办 | 状态 | 为什么没在这轮做 |
|---|---|---|
| ② 修 auditor 读回权限 | 留给你决定 | 改 `gen_subagents.py` 要重生成 9 个 agent 并重启 OpenCode；本轮刻意保持「无需重启」 |
| ③ 固定契约双跑 REST 五批 | 未开始 | 需要新增 5 个批次登记 + 5 个 agent（同样要重启），且要与本轮抽检分开记证据 |
| ④ 50 条非 SUPPORTED 人看 | 清单已生成 | `REVIEW_NONSUPPORTED.md` 已按当前判定表列好待填栏位；这是人工判断，不能由子代理代填 |
