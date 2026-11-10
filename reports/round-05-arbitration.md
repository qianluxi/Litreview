# round-05 裁决记录：S1 抽检出现 1 条差异，先补证据再裁

- 日期：2026-11-10
- 输入：`reports/round-05-sample.md`（OpenCode 本轮报告）、`litrev/_probe/audit/out_S1.md`（本轮回写）
- 主控裁决：**「先补证据再裁」** —— 不采信本次降档为「原表判错」，不自动整批重审 B3，不逐条修补，
  冻结 131 条汇总；先修工具/规程的方向错误、登记争议项，补够证据后再决定是否整批重审。
- 本轮**没有派任何 task**、没有改判定表、没有改 `litrev.py` / 契约 / agent 定义，**无需重启 OpenCode**。

## 一、独立复跑（不采信报告转述）

```
$ python litrev/litrev.py audit-count --prefixes S --check
S1         10     9     1     0     9     1  ✓
合计         10     9     1     0     9     1
口径：10 条 · SUPPORTED 9 / PARTIAL 1 / UNSUPPORTED 0 · SELF 9 / DEPENDENT 1
EXIT=0

$ python litrev/litrev.py audit-count --check
合计        131    81    49     1   118    13
口径：131 条 · SUPPORTED 81 / PARTIAL 49 / UNSUPPORTED 1 · SELF 118 / DEPENDENT 13
EXIT=0

$ python tools/audit_prep.py verify-sample            （修改前）
  与答案键一致：9/10 · 降档 S05:SUPPORTED→PARTIAL
  [!] 按 RUNBOOK §五：抽检出现「该判 PARTIAL 却给了 SUPPORTED」→ 整批重审，不逐条修补。
EXIT=1
```

`sample --check` / `gen_subagents.py --check` / `audit-stale --check` / `batch --check` 均退 0。
工作区在裁决前只有 `M litrev/_probe/audit/out_S1.md` + `?? reports/round-05-sample.md`，与报告自述一致。

## 二、为什么不能把这次降档当成「抓到误判」

### 1. 输入逐字相同

`SAMPLE_S1.md` 的 S05 与 `FRAG_B3.md` 的 B3-10：论断、引文完全一致（抽检输入只少一行「形式特征」）。
不是「换了材料」，是同一份材料的重复判定不一致。

### 2. B3-10 已经判过四次，四个结果（git 取证）

| # | 来源 | 支撑 | 自足 | 依据 |
|---|---|---|---|---|
| 1 | `147f8e4` `out_B3.md` | SUPPORTED | SELF | `"not amenable"` |
| 2 | `e8c140b` `out_B3.md` | SUPPORTED | DEPENDENT | `"often ill-"` |
| 3 | `691939a` `out_B3.md`（当前表） | SUPPORTED | SELF | `"not amenable to"` |
| 4 | 本轮 `out_S1.md` S05 | PARTIAL | DEPENDENT | `"not amenable"` |

支撑轴 3:1、自足轴 2:2，四次依据都逐字命中引文（`audit-stale` 管不到判定码）。
`reports/round-04-verification.md` §三 已点名第 3 次「更像判错而非漂移」；第 4 次自足轴回到 `DEPENDENT`、
支撑轴首次出现 `PARTIAL`。**四次里没有一次可以自动充当标准答案**——`verify-sample` 只比对抽样时点的原判，
没有判定谁对的能力。

### 3. 第 4 次判据本身与契约有张力

| 抽检理由 | 契约 | 核对 |
|---|---|---|
| 「主语碎片起于句中，需补完整主语」→ DEPENDENT | §五.1 / §三.5 | 引文首句主语 `structural design` 自带、主谓齐全，不满足 DEPENDENT |
| `These problems` 代词主语 | §七.1 | 指代对象就在同一条引文的前句内 |
| 「"尤其" 系加强」 | §五.2 / §三.2 | 「尤其是其中…」是范围**收窄**，不是放大或情态升级 |
| 「"病构性" 无原词」 | §二 `PARTIAL` | **这一条支持降档**：引文截断在 `ill-`；但 §三.3 只管「术语替换」，未覆盖「截断」 |

四条理由一条明确支持降档、三条有张力。这是契约未覆盖的边界情形，**不是契约自相矛盾**，不写 `CONTRACT_CONFLICT` 停机。
`round-05-sample.md` §四「PARTIAL / DEPENDENT 判得成立」是单方面把抽检当金标准，本次裁决不采纳。

### 4. 「整批重审 B3」的样本支撑不足

10 条抽检里 B3 只占 2 条（S04、S05），其余 8 条散在 7 个批次——报告所谓「降档全部集中在 B3」是抽样结构决定的。
1/2 的差异推不出「B3 系统性偏松」；而 B3 是碎片批次（16 条里 12 条截断引文），round-04 重审已有 6 条码变化，
立刻再整批重判只会混入新一轮双跑漂移。

### 5. 报告里两处不严谨（留档，不改历史报告）

- §六「若 B3-10 最终为 PARTIAL，汇总由 S81/P49/U1 变 S80/P50/U1」——这个数字**只对应逐条改一条**，
  而那正是 RUNBOOK 明令禁止的动作；真整批重审 B3 不会只动 1 条。
- §五 已指出 `verify-sample` 提示语方向反了，§六 却仍按那句提示的措辞推出「应当整批重审 B3」。

## 三、本轮改了什么

| 文件 | 改动 |
|---|---|
| `tools/audit_prep.py` | `verify-sample` 差异按方向分治（原表偏松 / 抽检偏松 / 双向），明确「只报差异、不裁定谁对」，提示改为「登记争议项 → 冻结汇总 → 补证据 → 人工裁决」；`build_keys` 末尾注记同步改写。**退码逻辑不变，差异仍在就退 1** |
| `litrev/_probe/audit/SAMPLE_S1_KEYS.md` | 由改后的 `sample` 重新生成，只变末尾注记；抽样算法、10 条对照表、戳 `0ff8391a63` 全部未变 |
| `RUNBOOK.md` §五 | 新增「差异 ≠ 错误」、方向分治表、补证据两条正规路径、禁止两种自动动作、答案键冻结、争议项登记；§八 变更记录加一行 |
| `litrev/PIPELINE.md` 抽检段 | 同步方向表述，指向 `RUNBOOK.md` §五 |
| `HANDOFF-05.md` §四 | **只追加一条修订注**，说明旧措辞已被 §五 修订版覆盖；本轮指令原文未动（历史证据保持） |
| `litrev/_probe/audit/DISPUTED.md` | 新建，登记 D-01（B3-10）：四次判定、契约张力、裁决记录、冻结声明、补证据两条路径 |
| `reports/round-05-arbitration.md` | 本文件 |

**明确未动**：8 张判定表、`litrev/litrev.py`、`AUDIT_CONTRACT.md`、`BATCHES.json`、`.opencode/agents/`、`out_S1.md`、
`reports/round-05-sample.md`。裁决前工作区的 `out_S1.md` 与报告原文随 git 留档。

## 四、修完工具后 `verify-sample` 仍退 1（这是对的）

```
$ python tools/audit_prep.py verify-sample
  ✓ 首行戳一致：0ff8391a63
  ✓ 表头与契约 §四逐字一致
  ✓ 判定行 10 条，id 与顺序正确
  ✓ 依据逐字命中检查：10 条已比对引文原文
  ✓ 合计行自洽：(10, 9, 1, 0, 1)
  与答案键一致：9/10（答案键记录的是抽样时点的原判，不是标准答案） · 差异 S05:SUPPORTED→PARTIAL
  [i] 机械工具只报差异，不裁定哪一侧判对；格式项与一致项是两套独立判据。
  [!] 方向：原表 SUPPORTED → 抽检更严（疑似原表偏松）。按 RUNBOOK §五：
      登记争议项、冻结 131 条汇总，先补证据（定向扩抽 / 固定契约双跑），
      由主控人工裁决后才决定是否整批重审；不自动整批重审，也不逐条改判定表凑数。
EXIT=1
```

修的是**提示方向**，不是把差异抹掉。让工具退 0 需要改判定或改答案键，两者本轮都禁止。
临时目录变异测试（不写仓库）：全绿 → 0；原表偏松 → 1 且提示原表方向；抽检偏松 → 1 且提示抽检方向；
无戳/缺行 → 1 且列四条格式错误。四个分支全部符合预期。

## 五、冻结声明与准确表述

- 8 张判定表保持不动，汇总冻结 `131 条 · S81 / P49 / U1 · SELF118 / D13`；
- 在 D-01 `CLOSED` 之前，**不得**说「81 条有证据支撑」或「81 条已抽检通过」；
- 可以说：131 条引文逐字可溯（`verify`）、131 条判定依据未过期（`audit-stale`）、
  10 条 SUPPORTED 抽检中 9 条与抽样时点判定一致、1 条登记为争议项 `OPEN`。
- `依据未过期 ≠ 判定正确`，D-01 的四次摇摆就是实例。

## 六、下一步（未执行，需另行批准 + 重启 OpenCode）

1. **定向扩抽 B3 的 7 条 SUPPORTED**（`B3-02/03/06/10/12/14/16`）：回答「单条噪声还是系统性偏松」。
2. **固定契约双跑 REST 五批**（R1–R5 共 83 条，另存 `out_R*_dup.md`、不覆盖旧表）：给「1/10 差异是噪声还是信号」一个漂移率基线。
   这是 `reports/round-04-verification.md` §三 的正规建议；**双跑只测一致性，不能裁决谁判对**。

两条都要新增批次登记 → `gen_subagents.py` 生成新 agent → 重启 OpenCode；证据必须分开记，
不得拿跨版本重审冒充双跑。若最终要补「截断术语 / 多句引文第二句代词主语」的契约口径，须作为独立一轮升 v1.2，
并同步重做抽检基线（现有答案键会失效）。

其余三项仍挂账：② auditor 读回权限缺口（改了要重启）、④ 50 条非 SUPPORTED 人工复核（`REVIEW_NONSUPPORTED.md`）、
③ 即上面第 2 条。
