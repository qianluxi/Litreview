# 交接给 OpenCode：第六轮（固定契约双跑 + 权限修复）

> 本轮要**重启 OpenCode 一次**：agent 定义改了（auditor 读回权限修复 + 5 个新 dup agent）。
> 重启后只做一件事：顺序派 5 个双跑 task，测「同一输入重复判定的漂移率」。
> 主控侧（人）有**并行的另一条路**：填 `GOLDEN.md` 25 条——这件事不需要 OpenCode，可以同时进行。

## 一、本轮为什么必须重启

| 改动 | 文件 | 生效条件 |
|---|---|---|
| auditor 读回权限修复 | 全部 9 个 `auditor-frag-b*`/`auditor-rest-b*` 的 read 白名单加了 `(out_*, allow)` | 重启 |
| 5 个双跑 agent | `auditor-rest-b{1-5}-dup`（新） | 重启 |
| 金标准工具 | `tools/audit_prep.py` 加 `golden`/`verify-golden`/`diff-dup` | 不用重启（主控侧） |
| 一键回归 | `tools/check.py` | 不用重启 |

读回权限修复解决了 round-04 发现的「auditor 写完不能读回自检、B2 因此把同一内容写两遍」。这是 round-04 核验留给你决定的 P1，本轮一并做掉。

## 二、任务：顺序派 5 个双跑 task（不要并发）

给主控的可粘指令（一次一个 `task`，跑完一个再派下一个——双跑测的是**一致性**，并发会引入资源竞争噪声）：

```
按 HANDOFF-06.md 执行本轮任务，不是摘要它。

重启后顺序派 5 个 task，每个调用对应的 dup agent，输入是原 REST_B*.md、输出是 out_D*.md：

| # | agent | 输入 | 输出 | 输入戳（首行要抄） |
|---|---|---|---|---|
| 1 | auditor-rest-b1-dup | litrev/_probe/audit/REST_B1.md | litrev/_probe/audit/out_D1.md | c8ad398b0d |
| 2 | auditor-rest-b2-dup | litrev/_probe/audit/REST_B2.md | litrev/_probe/audit/out_D2.md | 6e0fdbeb4f |
| 3 | auditor-rest-b3-dup | litrev/_probe/audit/REST_B3.md | litrev/_probe/audit/out_D3.md | 2861fd7ff6 |
| 4 | auditor-rest-b4-dup | litrev/_probe/audit/REST_B4.md | litrev/_probe/audit/out_D4.md | 09168d9ad9 |
| 5 | auditor-rest-b5-dup | litrev/_probe/audit/REST_B5.md | litrev/_probe/audit/out_D5.md | b8a12801bd |

每个 task 的要求：
- 闭卷：只读契约 + 本批输入（和原批次完全相同的输入），不读 out_R*.md、不读别的批次
- 输出第一行原样抄输入文件的 `> 快照 sha1: ...`，一个字符不能改
- 表头照 AUDIT_CONTRACT.md §四；83 条（R1=16/R2=17/R3=17/R4=16/R5=17）+ 末尾合计行
- 写完只回一行回执，不要重跑、不要顺手改别的文件
- 输出 out_D*.md 是**新文件**（不是覆盖 out_R*.md）；双跑的意义就是另存对照、不动旧表

派完 5 个就停，不要顺手做 B3 扩抽或别的批次。
```

## 三、验收（返回后，一条命令 + 两条专项）

```bash
python tools/check.py                                    # 结构性回归（8 项，退 0）
python litrev/litrev.py audit-count --prefixes D --check # 双跑 5 表自洽（D 不进 131 口径）
python tools/audit_prep.py diff-dup                      # R vs D 逐条比对，输出漂移率
```

`diff-dup` 输出：支撑轴/自足轴漂移率 + 逐条差异。这是 round-04 核验建议的「固定契约双跑测真一致性」，取代之前「跨版本重审当双跑」的上界 14.3%。

**预期内的现象**：漂移率不会是 0（round-04 同版本重判就有 1/16≈6.3%）。漂移率就是基线本身，不是失败。

## 四、主控侧并行路径：填 GOLDEN.md（不需要 OpenCode）

`litrev/_probe/audit/GOLDEN.md` 是一份 25 条的待填表（分层 S15/P9/U1，seed=43）。这是项目**唯一的「判得对」参照系**——抽检和判定表是同一个模型，只能测自洽；金标准是人开卷裁定，能测准确性。

填法：
- 打开 `GOLDEN.md`，每条 G01–G25 在表格里填 支撑/自足/依据/缺什么（照契约 §四）
- 可以读 `litrev/_probe/full/*.md` 卡片原文（开卷）
- **不要**读 `out_*.md`、`SAMPLE_S1_KEYS.md`、`GOLDEN_MAP.md`
- 填完跑：`python tools/audit_prep.py verify-golden`

`verify-golden` 输出：支撑轴一致率、自足轴一致率、方向分布（人判更严/更松）、差异按批次集中度。**这个一致率就是判定表的可信度估计**——做完才能说「131 条判定准确率 X%」。

GOLDEN.md 和双跑是两条独立证据，互不依赖，可以同时进行。

## 五、禁止事项

- 不跑 `batch` / `stamp-out`：8 个批次输入未变，跑了只制造无意义改动。
- 不改 `AUDIT_CONTRACT.md`、`litrev/litrev.py`、卡片 `full/*.md`。
- 不把 `GOLDEN_MAP.md` / `SAMPLE_S1_KEYS.md` 的内容贴给任何子代理。
- 不顺手做 B3 定向扩抽（等双跑漂移率出来再决定是否需要）。
- 不覆盖 `out_R*.md`（双跑的意义就是另存）。

## 六、做完写什么

`reports/round-06-dup.md`：

- 5 个 task id、子会话 id、各自 `<task_result>` 全文、是否被权限拒绝（本轮读回权限已修，应 0 次）；
- `check.py` 原始输出；
- `audit-count --prefixes D --check` 与 `diff-dup` 的**原始输出**（不是转述）；
- 一句话结论：双跑漂移率是多少，round-04 的 14.3% 上界是否被修正。

金标准那边另写 `reports/round-06-golden.md`（`verify-golden` 输出 + 一致率结论），两条分开记。

## 附：本轮离线已做（不要重做）

| 项 | 证据 |
|---|---|
| 读回权限修复 | `gen_subagents.py` auditor read 加 `(outp, allow)`，38 个 agent 已重生成 |
| 5 个 dup agent | `auditor-rest-b{1-5}-dup`，输入 REST_B*.md、输出 out_D{1-5}.md |
| 金标准工具 | `audit_prep.py golden` / `verify-golden` / `diff-dup` |
| 一键回归 | `tools/check.py`（8 项结构性检查，退 0） |
| 清理 | 删 round-03 遗留 `out_REWORK3.md` / `out_SAMPLE3.md` |
| 金标准已生成 | `GOLDEN.md`（25 条空表）+ `GOLDEN_MAP.md`（答案键），戳 `d46f9e7c3f` |
| 自检 | `check.py` 全绿：131/131 PASS、38 agent 同步、sample/golden --check 退 0 |
