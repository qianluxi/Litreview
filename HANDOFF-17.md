# HANDOFF-17：抽检补抽 S2（12 条，闭卷）

> 生产就绪第 ③ 步的机器侧一半。人开卷那一半是 `CASES_SELF_C2.md`（14 条），由你本人在确认后填，
> 不属于派发；判定完跑 `python tools/audit_prep.py verify-cases --name C2`。

## 一、这次派什么

| 项 | 值 |
|---|---|
| agent | `auditor-sample-s2` |
| 输入 | `litrev/_probe/audit/SAMPLE_S2.md`（戳 `8cf4be2cc9`，12 条） |
| 输出 | `litrev/_probe/audit/out_S2.md` |
| 性质 | 闭卷、只判论断层；抽检补抽第二批，测自洽/漂移 |
| 来源 | 排除 S1 已抽 10 条后的 128 条 `SUPPORTED` 池，`seed=71`、9.4% |

`auditor-sample-s2` 生成于 2026-11-11 round-28，**必须重启 OpenCode 之后**才能派，否则 `Unknown agent type`。
当前 agent 数 50。

## 二、派发前放行条件

```bash
python tools/check.py     # 期望 13/13 全绿
```

本轮备料后**没有预期红项**：判定表未动、批次戳未动、参考集按清单复现。若出现红项，先查 `git status` 有无未预期的改动，
不要为消红去改戳。

另外确认两件事：

1. `out_S2.md` **不存在**（`ls litrev/_probe/audit/out_S2.md` 应报 No such file）。
2. `SAMPLE_S2.md` 首行戳仍是 `8cf4be2cc9`。

## 三、派发词（逐字粘贴）

```
按 HANDOFF-17.md 做抽检，用 auditor-sample-s2 这个子代理。
```

回来只需回一行：`已写入 out_S2.md：N 行`，加 task id。

## 四、回来后的验收（主控做，四条）

1. **工作区**：`git status` 只多出 `out_S2.md`；`SAMPLE_S2.md`、答案键、既有 `out_*.md` 均未动。
2. **戳与表头**：`out_S2.md` 首行 = `> 快照 sha1: 8cf4be2cc9`；表头逐字照抄输入（不是契约 §四 示例行）；12 行 `S01→S12` 同序；合计行齐全。
3. **依据逐字**：每条依据在对应引文内连续命中、≤15 字，且**在源 txt 内也能命中**（`audit-stale` 只验前者，主控要补后者）。
4. **口径**：`python tools/audit_prep.py verify-sample --name S2`；`out_S2.md` **不进** `audit-count` 默认口径（前缀 `B,R`），
   判定表应保持 `S138/P0/U0`。`check.py` 仍 13/13 绿。

`verify-sample --name S2` 会输出本批与原判的一致率与方向；差异按 §五 登记 `DISPUTED.md`，
**不自动改表**（抽检差异 ≠ 错误，方向分治见 RUNBOOK §五）。
