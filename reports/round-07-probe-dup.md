# round-07：B3-10 第三次判定 + frag 双跑（B1–B3）

- 执行对象：`HANDOFF-07.md` §二（4 个 task，顺序执行，做完停）
- 时间：2026-11-10
- 契约：v1.1 固定，未改契约、未改判定表、未补戳
- 本文件只记证据，**不裁决 B3-10 判得对不对**（HANDOFF-07 §五）。

## 一、前置核对（派活前实测）

| 项 | 实测 |
|---|---|
| `gen_subagents.py --check` | `✓ 同步：42 个文件与 AGENT_ROLES.md 一致`，EXIT=0 |
| 4 个新 agent 存在 | `auditor-frag-b3-probe.md`(2637 B)、`auditor-frag-b1-dup.md`、`auditor-frag-b2-dup.md`、`auditor-frag-b3-dup.md`（各 2627 B） |
| `FRAG_B3P.md` 第 6 行 | `> 快照 sha1: e894bb155c` |
| `FRAG_B3P.md` 条数 | 1（`^### B3-10`） |
| frag 输入条数 | B1=16、B2=16、B3=16 |
| 输出文件派活前 | `out_B3P.md` / `out_E1.md` / `out_E2.md` / `out_E3.md` **四个均不存在** |

## 二、派发（顺序执行，一次一个）

| # | agent | 子会话 / task id | 状态 | 权限拒绝 | 回执全文 |
|---|---|---|---|---|---|
| 1 | `auditor-frag-b3-probe` | `ses_e3bbe85e5ffeT5I4W8wJyVBpBu` | completed | 0 | `已写入 litrev/_probe/audit/out_B3P.md：1 条（SUPPORTED 0 / PARTIAL 1 / UNSUPPORTED 0；DEPENDENT 1）` |
| 2 | `auditor-frag-b1-dup` | `ses_e3bbdbe01ffefNPJtVeGRaRXPZ` | completed | 0 | `已写入 litrev/_probe/audit/out_E1.md：16 条（SUPPORTED 6 / PARTIAL 9 / UNSUPPORTED 1；DEPENDENT 3）` |
| 3 | `auditor-frag-b2-dup` | `ses_e3bba6d20ffeyBoaJB45dHFvb6` | completed | 0 | `已写入 litrev/_probe/audit/out_E2.md：16 条（SUPPORTED 7 / PARTIAL 9 / UNSUPPORTED 0；DEPENDENT 3）` |
| 4 | `auditor-frag-b3-dup` | `ses_e3bb81afdffe6FCs4WHPsUzoMq` | completed | 0 | `已写入 litrev/_probe/audit/out_E3.md：16 条（SUPPORTED 4 / PARTIAL 12 / UNSUPPORTED 0；DEPENDENT 3）` |

4 次全部 `completed`、回执非空、**权限拒绝 0 次**（没有任何 `ruleset` 拒绝原文返回）。没有并发：上一个返回并验收完才派下一个。

## 三、回执要求的 4 行

```
1. auditor-frag-b3-probe → out_B3P.md：1 条（SUPPORTED 0 / PARTIAL 1 / UNSUPPORTED 0；DEPENDENT 1）；权限拒绝 0 次
2. auditor-frag-b1-dup  → out_E1.md：16 条（SUPPORTED 6 / PARTIAL 9 / UNSUPPORTED 1；DEPENDENT 3）；权限拒绝 0 次
3. auditor-frag-b2-dup  → out_E2.md：16 条（SUPPORTED 7 / PARTIAL 9 / UNSUPPORTED 0；DEPENDENT 3）；权限拒绝 0 次
4. auditor-frag-b3-dup  → out_E3.md：16 条（SUPPORTED 4 / PARTIAL 12 / UNSUPPORTED 0；DEPENDENT 3）；权限拒绝 0 次
```

## 四、文件级验收（行数 / 戳 / 判定行 / 合计行）

| 文件 | 行数 | 首行戳 | = 输入第 6 行 | `^| Bn-\d\d |` 行数 | 末行合计 | 新文件 |
|---|---|---|---|---|---|---|
| `out_B3P.md` | **6** | `e894bb155c` | 是 | 1（B3-10） | 1 条（0/1/0；DEP 1） | 是 |
| `out_E1.md` | **21** | `9ff1753875` | 是 | 16 | 16 条（6/9/1；DEP 3） | 是 |
| `out_E2.md` | **22** | `902e819463` | 是 | 16 | 16 条（7/9/0；DEP 3） | 是 |
| `out_E3.md` | **22** | `a52c3ea485` | 是 | 16 | 16 条（4/12/0；DEP 3） | 是 |

行数构成：E1 = 戳 1 + 空行 1 + 表头 2 + 判定 16 + 合计 1（21）；E2/E3 同构但多一个空行（22）；B3P = 戳 1 + 空行 1 + 表头 2 + 判定 1 + 合计 1（6）。首行戳全部由 auditor 从输入原样抄回，**主控未补任何戳**。

已有判定输出一字未动（`git status --short --untracked-files=all`）：

```
?? litrev/_probe/audit/out_B3P.md
?? litrev/_probe/audit/out_E1.md
?? litrev/_probe/audit/out_E2.md
?? litrev/_probe/audit/out_E3.md
```

`out_B1..B3`、`out_R1..R5`、`out_D1..D5`、`out_S1`、卡片、契约、`litrev.py` 均未出现在变更里。

## 五、`check.py` 原始输出

```
  ✓ verify 全库: 131/131 PASS
  ✓ audit-count --check: 非 SUPPORTED：50/131 = 38.2%
  ✓ audit-count --prefixes S --check: 非 SUPPORTED：1/10 = 10.0%
  ✓ audit-stale --check: ✓ 全部判定的依据与卡片当前内容一致。
  ✓ batch --check: 合计待刷新 0/131 条（--check 不写盘）
  ✓ gen_subagents --check: ✓ 同步：42 个文件与 AGENT_ROLES.md 一致
  ✓ audit_prep sample --check: ✓ 抽检批次可复现：10/81 条（12.3%），戳 0ff8391a63，答案键一致，8 个源批次输入戳未变。
  ✓ audit_prep golden --check: ✓ 金标准可复现：25 条（S15/P9/U1），戳 d46f9e7c3f。（GOLDEN.md 表格为人填部分，不纳入比对）

✓ 全部机械自检通过。
EXIT=0
```

8/8 绿，退 0。round-06 那条 `golden --check` 失败已消失（该命令现在只比对模板、不比对人工填写的表格）。

## 六、`diff-dup --pair B:E` 原始输出

```
双跑配对：48 条（B* 原判 vs E* 重判）
  支撑轴漂移：6/48（12.5%）
  自足轴漂移：2/48（4.2%）
  任一轴漂移：8/48（16.7%）
  支撑轴差异：
    B1-05: PARTIAL → SUPPORTED
    B1-15: SUPPORTED → PARTIAL
    B2-08: SUPPORTED → PARTIAL
    B3-06: SUPPORTED → PARTIAL
    B3-10: SUPPORTED → PARTIAL
    B3-14: SUPPORTED → PARTIAL
  自足轴差异：
    B2-15: SELF → DEPENDENT
    B3-09: DEPENDENT → SELF
  [i] 双跑测的是同输入重复判定的随机漂移，不裁定谁判对；
      漂移率给「抽检 1/10 差异是噪声还是信号」一个基线（round-04 上界 14.3%）。
EXIT=0
```

## 七、`out_B3P.md` 单独检查（`audit-count` 不认该文件名）

```
戳行: e894bb155c （应 e894bb155c）
判定行: 1 （应 1）
合计行: 合计：1 条（SUPPORTED 0 / PARTIAL 1 / UNSUPPORTED 0；DEPENDENT 1）
EXIT=0
```

三项全部符合 HANDOFF-07 §三 的预期。

## 八、两条基线的并列（只列数字，不裁决）

### 8.1 漂移率：REST 双跑 vs frag 双跑

| 轴 | R:D（83 条，round-06） | B:E（48 条，本轮） | 方向分布（本轮） |
|---|---|---|---|
| 支撑 | 8.4%（7/83） | **12.5%（6/48）** | S→P 5 条、P→S 1 条 |
| 自足 | 12.0%（10/83） | **4.2%（2/48）** | SELF→DEP 1 条、DEP→SELF 1 条 |
| 任一轴 | 20.5%（17/83） | **16.7%（8/48）** | — |

两点可核的事实（不下结论）：

1. 支撑轴漂移在 frag 三批更高（12.5% vs 8.4%），且 6 条里 5 条是 **SUPPORTED→PARTIAL**（单向偏严）。
2. 自足轴漂移在 frag 三批低得多（2/48 vs 10/83），且两条方向相反——与 round-06 记录的 REST 侧「10 条全部单方向」形态不同。

按 131 条加权（83+48）粗算任一轴漂移 = (17+8)/131 ≈ **19.1%**，仅供对照，两组不是同一抽样框，不宜直接合并成一个数。

### 8.2 B3-10 目前已有的 4 次判定（按时间序，仅列事实）

| 来源 | 文件 | 支撑 | 自足 |
|---|---|---|---|
| round-04 重审 | `out_B3.md` | SUPPORTED | SELF |
| round-05 抽检（S05） | `out_S1.md` | PARTIAL | DEPENDENT |
| round-07 第三次独立判定 | `out_B3P.md` | PARTIAL | DEPENDENT |
| round-07 frag 双跑 | `out_E3.md` | PARTIAL | SELF |

计数：支撑 SUPPORTED 1 / PARTIAL 3；自足 SELF 2 / DEPENDENT 2。**如何裁定由你决定**，本轮未改 `out_B3.md`、未改任何既有判定。

## 九、仍未做的事

1. **B3-10 的裁定与（若需要的）`out_B3.md` 修正**——未做，按 HANDOFF-07 只取证不裁决。
2. 自足轴口径统一（升 v1.2 + 判例）——HANDOFF-07 §四 明确留到后续独立一轮；本轮证据显示 REST 与 frag 两侧漂移形态不同，这一条更有必要。
3. 131 条的全量双跑：现在只到 83+48=131 的**配对口径**（B:E 覆盖 B1–B3、R:D 覆盖 REST），但两轮不是同一批判读者配置（D 与 E 是不同 agent 实例），因此不能当作「131 条同一条件下的双跑」。若要后者，需要 B1–B3 与 REST 用同一套 dup 再跑一次。
4. 50 条非 SUPPORTED 人工复核（`REVIEW_NONSUPPORTED.md`）仍未开始。
5. 未提交 git：工作区为 4 个未跟踪新文件 + 本报告。
