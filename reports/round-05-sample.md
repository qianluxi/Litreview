# round-05：S1 抽检（SUPPORTED 10 条）

- 执行对象：`HANDOFF-05.md`（只派一次 `auditor-sample-s1`，做完停）
- 时间：2026-11-10
- 结论一句话：**抽检本身执行无误（戳、表头、10 行、合计、依据逐字全部通过），但命中 9/10 —— S05 由原判 SUPPORTED 降为 PARTIAL，原批次 B3 存在一条「不该是 SUPPORTED 的 SUPPORTED」。按 HANDOFF-05 §四「先别自己裁决」，本文只记录证据，不触发重审。**

## 一、派发（一次 task，无并发）

| 项 | 值 |
|---|---|
| agent | `auditor-sample-s1` |
| task / 子会话 id | `ses_e3ca76752ffeP1rMIcClZCPvcG` |
| 返回状态 | `completed` |
| 权限拒绝 | **0 次**（回执正常，`task_result` 非空，未出现 `ruleset` 拒绝原文） |
| 重派 | 无（只派一次） |

`<task_result>` 全文（不是长度阈值，逐字照抄）：

```
已写入 litrev/_probe/audit/out_S1.md：10 条（SUPPORTED 9 / PARTIAL 1 / UNSUPPORTED 0；DEPENDENT 1）
```

派发提示词没有透露候选集构成（81 条 SUPPORTED、seed、抽样池）、没有贴任何原判定、没有引用答案键路径；没有贴卡片内容。子代理只拿到 `SAMPLE_S1.md` + `AUDIT_CONTRACT.md`。

## 二、验收（HANDOFF-05 §三 六条，以文件为准）

| # | 检查 | 结果 | 证据 |
|---|---|---|---|
| 1 | 一次 task、`completed`、回执全文打印 | 通过 | 回执见 §一，非空 |
| 2 | 首行戳逐字一致 | 通过 | `out_S1.md` 第 1 行 = `> 快照 sha1: 0ff8391a63`，与 `SAMPLE_S1.md` 第 6 行逐字相同，无附加说明 |
| 3 | 表头 / 10 行 / id 顺序 / 合计 | 通过 | 文件 16 行 = 戳 1 + 空行 1 + 表头 2 + 判定 10 + 空行 1 + 合计 1；`^\| S\d\d \|` 计数 = 10；id 序列 `S01,…,S10` 与输入行序一致；合计 `10 条（9/1/0；DEP 1）` |
| 4 | `audit-count --prefixes S --check` 退 0 | 通过 | 原始输出见 §三 |
| 5 | `audit_prep.py verify-sample` 退 0 | **未通过** | 退 1：机械项全 ✓，但「与答案键一致：9/10 · 降档 S05」 |
| 6 | 改动范围 | 通过 | `git status --short` 只有 `M litrev/_probe/audit/out_S1.md`；卡片 / 契约 / `litrev.py` / `.opencode/agents/` 均未出现 |

> 第 5 条的「未通过」是**内容判定**，不是格式或落盘失败：戳/表头/条数/合计/依据逐字命中这四项全部 ✓。旧 `out_S1.md`（上一轮 16 条、无戳）已被覆盖为 10 条，`audit-count --prefixes S` 从 `S1 16 条` 变成 `S1 10 条`，与 HANDOFF-05 §三 的警示点一致。

## 三、两条命令的原始输出

### `python litrev/litrev.py audit-count --prefixes S --check`

```
批次         条数  SUPP  PART  UNSU  SELF   DEP  合计行
--------------------------------------------------------------
S1         10     9     1     0     9     1  ✓
--------------------------------------------------------------
合计         10     9     1     0     9     1

口径：10 条 · SUPPORTED 9 / PARTIAL 1 / UNSUPPORTED 0 · SELF 9 / DEPENDENT 1
非 SUPPORTED：1/10 = 10.0%
EXIT=0
```

### `python tools/audit_prep.py verify-sample`

```
抽检回写：litrev/_probe/audit/out_S1.md · 戳 0ff8391a63 · 10 条
  ✓ 首行戳一致：0ff8391a63
  ✓ 表头与契约 §四逐字一致
  ✓ 判定行 10 条，id 与顺序正确
  ✓ 依据逐字命中检查：10 条已比对引文原文
  ✓ 合计行自洽：(10, 9, 1, 0, 1)
  与答案键一致：9/10（答案键里候选条目原判均为 SUPPORTED） · 降档 S05:SUPPORTED→PARTIAL
  [!] 按 RUNBOOK §五：抽检出现「该判 PARTIAL 却给了 SUPPORTED」→ 整批重审，不逐条修补。
EXIT=1
```

### 附：131 条汇总未被抽检污染

`python litrev/litrev.py audit-count --check`（默认前缀 B,R，S1 不计入）：

```
合计        131    81    49     1   118    13

口径：131 条 · SUPPORTED 81 / PARTIAL 49 / UNSUPPORTED 1 · SELF 118 / DEPENDENT 13
非 SUPPORTED：50/131 = 38.2%
EXIT=0
```

与 round-04 收尾数字逐字相同：抽检回写没有进 131 条汇总。

## 四、10 条逐条对照（抽检 vs 答案键）

| 抽检 id | 原批次 id | 原判 | 抽检判 | 一致 | 差异 |
|---|---|---|---|---|---|
| S01 | B1-13 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S02 | B2-12 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S03 | B2-16 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S04 | B3-02 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| **S05** | **B3-10** | **SUPPORTED / SELF** | **PARTIAL / DEPENDENT** | **✗** | 支撑降档 + 自足降档 |
| S06 | R1-12 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S07 | R2-03 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S08 | R2-08 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S09 | R3-16 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |
| S10 | R5-05 | SUPPORTED / SELF | SUPPORTED / SELF | ✓ | — |

- **命中率：9/10 = 90%**（抽检比例为 12.3%，10 条）。
- **降档 1 条，全部集中在 1 个原批次**：`B3`（B3-10）。
- 降档方向：**原判偏松**（原表给 SUPPORTED，抽检判 PARTIAL），不是抽检偏松。

### S05 的具体判据（抽检表「缺什么」栏原文）

```
| S05 | PARTIAL | DEPENDENT | "not amenable" | 引文截断于 "ill-"，"病构性" 无原词；"尤其" 系加强；主语碎片起于句中，需补完整主语 |
```

输入引文为 `structural design are not amenable to purely algorithmic solutions. These problems are often ill-`：`ill-structured` 被截断在 `ill-`，论断里的「病构性」在引文中没有完整原词；`especially`（「尤其」）在引文中无对应；引文起于句中，主语落在引号外。按契约 §三.2（范围放大）与 §三.3（术语被截断即无原词）、§五.2（加强限定词 → PARTIAL）、§二自足轴（主语落在引号外 → DEPENDENT），PARTIAL / DEPENDENT 是更严的一档，判得成立。

### 与 round-04 的一条交叉证据

`B3-10` 正是 round-04 记录过的「依据未变但判定码漂移」4 条之一（旧 DEPENDENT → 重审 SELF）。本轮的抽检给出 PARTIAL / DEPENDENT，说明**那次漂移的方向是错的**：把一条本应降档的条目升成了 SUPPORTED。这是抽检机制第一次抓到具体误判，而不是抓到噪声。

## 五、`verify-sample` 提示语与本案方向不符（工具问题，未改）

`audit_prep.py` 打印的是：

```
[!] 按 RUNBOOK §五：抽检出现「该判 PARTIAL 却给了 SUPPORTED」→ 整批重审，不逐条修补。
```

而本案方向相反：**原判 SUPPORTED，抽检判 PARTIAL**。两者都落在「表里有一条 SUPPORTED 不该是 SUPPORTED」上，但含义不同：

- 提示语描述的是「抽检太松」——需要重审的是**抽检**这一侧的判读；
- 本案是「原表太松」——需要重审的是**原批次 B3**，抽检判定本身无错。

工具把两种方向合并成一句硬编码提示，容易让人去重审错的对象。这一条按 HANDOFF-05 §五「不改 `litrev.py`」的精神记在报告里（`audit_prep.py` 同属工具层，本轮未动），不在本轮修。

## 六、结论与下一步（未执行，等指示）

按 RUNBOOK §五「抽检条目出现『该判 PARTIAL 却给了 SUPPORTED』→ 整批重审，不逐条修补」的同一条原则，本案（原表 SUPPORTED 被抽检降为 PARTIAL）**应当整批重审 `B3`**，而不是逐条改 `out_S1.md` 或 `out_B3.md`。

但 HANDOFF-05 §四 明确写了「降档清单与命中率写进报告，**先别自己裁决**」，所以本轮到此为止，我没有：

- 重派 `auditor-frag-b3`；
- 修改 `out_B3.md` / `out_S1.md` 的任何判定；
- 跑 `batch` / `stamp-out`（8 个批次输入未变，跑只会制造无意义改动）。

**一句话结论**：SUPPORTED 81 条**不能**继续无条件只做分诊使用——90% 命中率、1/10 降档，且降档落在 `B3`；按规程应由你裁决是否整批重审 `B3`（连带影响：若 B3-10 最终为 PARTIAL，131 条汇总将由 S81/P49/U1 变为 S80/P50/U1）。

## 七、仍未做的事

1. **B3 整批重审（或只重审 B3-10）**——等你的裁决，见 §六。
2. 50 条非 SUPPORTED 人工复核（`REVIEW_NONSUPPORTED.md`）未开始。
3. `auditor-*` 读回自身输出的权限缺口未修（HANDOFF-05 决定本轮保持「无需重启」，本轮未触发：子代理没有尝试读回）。
4. 固定契约双跑 REST 五批未开始。
5. 未提交 git：工作区当前 `M litrev/_probe/audit/out_S1.md` + 本报告（未跟踪）。
