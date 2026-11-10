# 判定争议项登记（人工维护）

> 用途：登记「同一份输入出现两次及以上不一致判定」的条目。**这里不是判定表**，不进 131 条汇总，
> 不登记进 `BATCHES.json`，不贴给任何 `auditor-*`，也不由 `audit_prep.py review` 自动生成（那份是
> `REVIEW_NONSUPPORTED.md`，两者不要混写）。
> 规程依据：`RUNBOOK.md` §五（差异 ≠ 错误；先登记、后裁决）、契约 §七.2（`SUPPORTED` 只用于分诊）。
> 状态字段只允许 `OPEN` / `CLOSED`，`CLOSED` 必须写明裁决人、日期、依据与是否改判定表。

## 冻结声明（2026-11-10，D-01 CLOSED 后更新）

- D-01 已 `CLOSED`，`out_B3.md` 的 `B3-10` 已按裁决落表（`SUPPORTED → PARTIAL`，自足轴不动），
  131 条汇总随之更新为 **`S80 / P50 / U1 · SELF118 / D13`**，非 SUPPORTED 51 条。
- 该汇总仍只表示「判定表当前写了什么」，**不得表述为「80 条有证据支撑」或「80 条已抽检通过」**；
  它由 `python litrev/litrev.py audit-count --check` 唯一产生，不要手算。
- 旧 `SAMPLE_S1_KEYS.md`（戳 `0ff8391a63`、候选池 81）与对应 `out_S1.md` 是 round-05 的历史证据，
  已被 2026-11-10 的重抽覆盖；需要查阅时按 commit `7077b6f` 取（`git show 7077b6f:litrev/_probe/audit/SAMPLE_S1.md`）。
- 重抽后的 `SAMPLE_S1.md`（戳 `7d1a204d54`、候选池 80）等待 `auditor-sample-s1` 回写；在 `verify-sample` 退 0 之前，
  不得说「新一批抽检已通过」。
- **D-02 已 `CLOSED`（2026-11-10）**：自足轴判例集 20 条的回写有 4 条与判定表不一致（2:2），按裁决改判
  `B2-05`、`B3-11` → `SELF`，`R3-12`、`R4-13` → `DEPENDENT`，并落契约 v1.2 §八（自足轴三族边界）。
  两轴总量不变（`S80/P50/U1 · SELF118/D13`），因此**旧汇总数字仍有效，不要重算**；变的只是 2 个批次内部的 DEP 计数。
- `CASES_SELF_KEYS.md` 的冻结基线仍是改判**前**的 16/20，这是判例集的历史证据，不得改写；
  `verify-cases` 今后会继续打印 16/20 并把这 4 条列进 drift，属**预期**。

---

## D-01 · B3-10 / S05

- 状态：**CLOSED**（2026-11-10，裁决人=项目所有者；支撑改 `PARTIAL`、自足不动；已改 `out_B3.md` 与合计行）
- 文献 / 节：`SriramMaherFenves1985_KBES_StructuralDesign` · 问题域 · p.4
- 批次输入：`FRAG_B3.md` 的 `B3-10`；抽检输入：`SAMPLE_S1.md` 的 `S05`
- 输入逐字比对：**论断与引文完全相同**（抽检输入只少一行「形式特征」），不存在「换了材料」的解释。

论断：

```
问题域是结构设计，尤其是其中不适合纯算法求解、常呈病构性的设计问题。
```

引文：

```
"structural design are not amenable to purely algorithmic solutions. These problems are often ill-" (Sriram et al., 1985, p.4)
```

### 第 1–4 次判定（历史取证；第 5、6 次见文末）

| # | 来源 | 支撑 | 自足 | 依据 | 缺什么 / 说明 |
|---|---|---|---|---|---|
| 1 | `147f8e4` `out_B3.md` | SUPPORTED | SELF | `"not amenable"` | 无需补 |
| 2 | `e8c140b` `out_B3.md`（round-03） | SUPPORTED | DEPENDENT | `"often ill-"` | 支撑成分齐全；These problems 为代词主语，需补指代 |
| 3 | `691939a` `out_B3.md`（round-04，当前表） | SUPPORTED | SELF | `"not amenable to"` | — |
| 4 | `out_S1.md` `S05`（round-05 抽检） | **PARTIAL** | **DEPENDENT** | `"not amenable"` | 引文截断于 "ill-"、"病构性" 无原词；"尤其" 系加强；主语碎片起于句中，需补完整主语 |

前四次：支撑轴 3:1、自足轴 2:2，`audit-stale` 四次依据都逐字命中引文——**依据没过期，不等于判定正确**，本条即实例。
`reports/round-04-verification.md` §三 已点名第 3 次「更像判错而非漂移」；第 4 次在自足轴上回到 `DEPENDENT`，
在支撑轴上首次给出 `PARTIAL`。四个结果，没有一次可以自动充当标准答案。

> 注意口径：第 1、2 次在契约 v1.1 定型之前，**不能与后四次直接合并计数**。固定 v1.1 的只有第 3–6 次，见文末汇总。

### 第 4 次判据与契约的逐条对照（为什么不能直接采信）

| 抽检给的理由 | 契约 | 核对 |
|---|---|---|
| 「主语碎片起于句中，需补完整主语」→ DEPENDENT | §五.1「自足轴只管主语，只有主语缺失或代词作主语才判 DEPENDENT」；§三.5「论断补主语不算越界」 | 引文**首句**主语是 `structural design`，主谓齐全；不满足。§三.5 举例的 `it decomposes into...` 才是 DEPENDENT |
| `These problems are often ill-` 代词主语 | §七.1「指示代词作限定词，若指代对象未在引文内出现，判 DEPENDENT」 | 指代对象（前句的 `structural design are not amenable to...`）就在同一条引文内；§七.1 未必支持 |
| 「"尤其" 系加强」 | §五.2「加强限定词、放大范围」；§三.2「范围不得放大」 | 「尤其是其中…」是范围**收窄**，不是放大；也不是情态升级（§三.1） |
| 「"病构性" 无原词」 | §二 `PARTIAL` 定义「混入了引文无法证明的成分」 | **这一条支持降档**：引文截断在 `ill-`，`ill-structured` 未出现。但 §三.3「术语不得替换」管的是替换，并未覆盖「截断」 |

结论：四条理由里一条明确支持降档、三条与契约存在张力。**这是契约尚未覆盖的边界情形，不是契约自相矛盾**，
不要写 `CONTRACT_CONFLICT` 停机。`reports/round-05-sample.md` §四「PARTIAL / DEPENDENT 判得成立」是单方面把抽检
当成金标准，本登记不采纳。

### 裁决记录

| 日期 | 裁决 | 内容 |
|---|---|---|
| 2026-11-10 | 主控 | 选「**先补证据再裁**」：不采信本次降档为「原表判错」，不自动整批重审 B3，不逐条改 `out_B3.md`，冻结 131 条汇总；修工具/规程方向、登记本争议项，补够证据后再定。依据见 `reports/round-05-arbitration.md` |

### 补证据路径与结果

#### 路径 1：定向扩抽 B3 的 7 条 SUPPORTED —— **未执行**

仍需新增批次 + agent + 重启 OpenCode。B3 是碎片批次（16 条里 12 条截断引文），且 round-04 重审已有 6 条码变化。

#### 路径 2：固定契约双跑 REST 五批 —— **已执行（2026-11-10）**

5 个 `auditor-rest-b{n}-dup` 对原 `REST_B*.md` 重判，另存 `out_D{1-5}.md`（不覆盖旧表）。结果见 `reports/round-06-dup.md` 与 `reports/round-06.md`：

- **漂移率（83 条）**：支撑轴 8.4%（7/83）、自足轴 12.0%（10/83）、任一轴 20.5%（17/83）。
- **自足轴 10/10 单向 SELF→DEPENDENT**——系统性口径差，不是随机噪声。R 侧 DEPENDENT 4/83（4.8%），D 侧 14/83（16.9%），差 3.5 倍。
- round-04 的 14.3% 是**低估**（混入契约版本变更）；本轮 20.5% 是同输入同契约纯随机漂移的基线。

**对 D-01 的直接影响**：支撑轴单项漂移率 8.4%/条 → 10 条抽检出现 ≥1 条降档的概率 `1-(1-0.084)^10 ≈ 58%`。即 **S05 降档是信号候选，不是证据**——单凭它不能判定 B3 系统性偏松。

#### 路径 3：人工金标准（25 条）—— **已执行（2026-11-10）**

人开卷填 `GOLDEN.md` 25 条，`verify-golden` 比对判定表：

- **一致率**：支撑轴 23/25（92%）、自足轴 25/25（100%）、双轴 23/25（92%）。
- **差异 2 条**：G03（B1-10，引文止于"as"无"度量"）、G18（R4-01，PATDEX 不在引文内），均人判更严（原 S → 人 PARTIAL）。
- **D-01 不在金标准 25 条里**：金标准抽样 seed=43，B3-10 未被抽中。金标准证实判定表存在偏松，但与 D-01 无直接关联。

### round-06 时的状态（历史，已被 round-07 证据覆盖）

当时判 **OPEN**，理由：四次判定支撑 3:1、自足 2:2 无多数票；双跑基线显示 S05 降档有 58% 概率属随机漂移；
金标准 2 条偏松不涉及本条。收口路径定为「第三次独立判定」。该判定已于 round-07 执行，结果见下。

#### 路径 4：B3-10 第三次独立判定 —— **已执行（2026-11-10，round-07）**

`auditor-frag-b3-probe` 读 `FRAG_B3P.md`（与 `SAMPLE_S1.md` 的 `S05` 论断/引文逐字相同，只少一行「形式特征」，戳 `e894bb155c`），
写 `out_B3P.md`。`opencode.db` 取证：子会话 `ses_e3bbe85e5ffeT5I4W8wJyVBpBu`，只 read 契约 + 该输入、只 write 该输出，
`status=error` 计数 0（无权限拒绝）。

判定：**PARTIAL / DEPENDENT**，依据 `"not amenable to"`。

#### 路径 5：frag 双跑三批 —— **已执行（2026-11-10，round-07）**

`auditor-frag-b{1-3}-dup` 对原 `FRAG_B*.md` 重判，另存 `out_E{1-3}.md`（不覆盖 `out_B*.md`）。其中 `out_E3.md` 也含 `B3-10`，
判 **PARTIAL / SELF**，依据 `"often ill-"`。

双跑结果见 `reports/round-07-probe-dup.md` 与 `reports/round-07-verification.md`：frag 三批支撑轴漂移 12.5%（6/48）、
自足轴 4.2%（2/48）、任一轴 16.7%（8/48）；与 REST 五批合并后 131 条配对，任一轴 19.1%，支撑轴 9:4（`P≈13%`，不显著）、
**自足轴 11:1 单向（`P≈0.3%`）**。

### 第六次判定后的证据汇总（v1.1 固定契约下的 4 次）

| # | 来源 | 支撑 | 自足 | 依据 |
|---|---|---|---|---|
| 3 | `691939a`（当前表） | SUPPORTED | SELF | `"not amenable to"` |
| 4 | `out_S1.md` S05 | PARTIAL | DEPENDENT | `"not amenable"` |
| 5 | `out_B3P.md` | PARTIAL | DEPENDENT | `"not amenable to"` |
| 6 | `out_E3.md` | PARTIAL | SELF | `"often ill-"` |

**支撑轴 1:3、自足轴 2:2。**

**稳健交集**：#4/#5/#6 三条独立判定都指向同一个可机械核验的缺陷——引文在 `often ill-` 处截断，论断的「病构性」在引文内
没有完词依据（契约 §二「混入了引文无法证明的成分」）。这一条不依赖任何有争议口径（代词主语、范围收窄、加强词）。

**必须记录的反面证据**：#5 给出的另外两条理由与事实不符——「`structural design are` 主语在引号外」（实际在引号内）、
「`These problems` 的指代对象未在引文内出现」（`problems` 就在同一引文第二句）。#4 也有三条理由与契约有张力（见上文对照表）。
**因此采信的是「截断」这一条，不是那几条理由**；若日后有人引用本裁决，不得把那几条错误理由一并背书。

### 裁决执行记录（2026-11-10）

| 项 | 内容 |
|---|---|
| 裁决人 | 项目所有者（用户，2026-11-10 授权「收口：支撑改 PARTIAL」） |
| 支撑轴 | `SUPPORTED → PARTIAL`（依据：v1.1 下 3:1；三次 PARTIAL 收敛到同一可核验缺陷——引文截断于 `often ill-`，「病构性」无完整词形依据） |
| 自足轴 | **不动**（保持 `SELF`）。2:2 无法裁，且自足轴存在 11:1 单向口径差（`P≈0.3%`），单条裁决会被口径差污染；留待契约 v1.2 |
| 落表动作 | `out_B3.md` B3-10 行改判 + 依据改 `"often ill-"`、合计行 `S7/P9 → S6/P10`；`audit-count --check` 复算 `S80/P50/U1 · SELF118/D13` |
| 未采纳的理由 | `out_B3P.md` 那两条事实错误的理由（主语在引号外、`problems` 不在引文内）**不予背书**，只采信「截断」 |
| 级联处置 | 候选池 81→80，`SAMPLE_S1` 已按新池重抽（戳 `7d1a204d54`），旧样本/答案键留档于 commit `7077b6f`；待派一次 `auditor-sample-s1` |

### 为什么这次「改一条」不等于 RUNBOOK 禁止的「逐条修补凑数」

- 禁止的是**看着答案把数字改到与抽检一致**：没有独立证据、只为让 `verify-sample` 变绿。
- 本次是**先登记 → 冻结汇总 → 补两条证据（单条独立判定 + 固定契约双跑）→ 人工裁决 → 落表**的完整路径，
  且裁决依据可以脱离原始抽检独立复核（引文是否截断，任何人都能核对）。
- 落表后 `verify-sample` 的历史结论（9/10、降档 S05）**不作废、不改写**——它记录的是抽样时点的比对结果，
  现在有了裁决解释，而不是被抹平。

### 明确不做

- 不改 `AUDIT_CONTRACT.md`：补口径等于升 v1.2，会使 8 张已出表口径变更、答案键失效、抽检基线重做。
  若要补「截断术语 / 多句引文第二句代词主语」的口径，须作为独立一轮并同步重做抽检基线。
- 不改 `litrev/litrev.py`（裁判）、不改 `.opencode/agents/`（本轮无需重启）。
- 不跑 `batch` / `stamp-out`：8 个批次输入未变，跑了只制造无意义改动。

---

## D-02 · 自足轴判例集 C1 的 4 条差异（B2-05 / B3-11 / R3-12 / R4-13）

- 状态：**CLOSED**（2026-11-10，裁决人=项目所有者；按回写改判 4 条，已改 `out_B2/B3/R3/R4.md` 与各自合计行）
- 来源：`CASES_SELF.md`（自足轴判例集 C1，20 条，冻结清单 `CASES_SELF_IDS.txt`，戳 `a4e66877dc`）
- 性质：**判例裁定**，不是抽检差异——本集刻意选表内 `DEPENDENT` 10 条 + 双跑不一致 10 条，只为确认自足轴口径。

### 回写结果（20/20 全填，依据逐字命中引文）

| 指标 | 值 |
|---|---|
| 自足轴一致 | **16/20**（80%） |
| 表判 `DEP`、回写 `SELF` | 2 条：`C03→B2-05`、`C07→B3-11`（表偏严） |
| 表判 `SELF`、回写 `DEP` | 2 条：`C14→R3-12`、`C16→R4-13`（表偏松） |
| 表内 `DEPENDENT` 阳性确认 | 8/10 |
| 方向 | **2:2，不是单向偏差** |

### 4 条差异与裁决

| C | 原 id | 引文首句 | 表内 | 回写 | 裁决 | 理由 |
|---|---|---|---|---|---|---|
| C03 | `B2-05` | `this section introduces the construction, training, and inference methods…` | `DEP` | `SELF` | 改 `SELF` | `this section` 是篇章自指，不需往回翻（§八 A 族） |
| C07 | `B3-11` | `This paper thoroughly examines these feature retrieval methods…` | `DEP` | `SELF` | 改 `SELF` | `This paper` 同上；与 `R5-15`（`This paper is…` 判 `SELF`）同构造，原表自相矛盾 |
| C14 | `R3-12` | `…, this approach enables effective retrieval of building floor plans.` | `SELF` | `DEP` | 改 `DEP` | `this approach` 回指前文方法，先行词不在引文内（§八 C 族） |
| C16 | `R4-13` | `These input graphs represented node features as…` | `SELF` | `DEP` | 改 `DEP` | `These input graphs` 回指前文构造的图，同上 |

### 由此确定的口径（契约 v1.2 §八）

`this/these` 后跟**篇章名词**（paper / study / work / section / chapter）= 自指 → `SELF`；
后跟**内容名词**（approach / method / limitations / graphs）= 回指 → 看先行词在不在引文内；
`It is … that …` 形式主语 → `SELF`；片段（名词/介词/从句/分词开头，主谓在引号外）→ `DEPENDENT`。

### 为什么这不算「整批重审」

- **影响面实测**：131 条里 A 族 12 条（11 条本已 `SELF`）、B 族 1 条（已 `SELF`），落盘只动 4 条。
- **总量不变**：`SELF 118 / DEPENDENT 13` 与改判前完全相同（+2 −2），`S80/P50/U1` 不动 → 所有引用汇总数字的报告仍然有效。
- **答案键不失效**：`SAMPLE_S1_KEYS` / `GOLDEN_MAP` / `CASES_SELF_KEYS` 的冻结清单按 id 复现，改判只进 drift 报告，不重抽。

### 明确不做

- 不重判其余 125 条：它们与本节点状修正无关；「自指 11/12 已判 `SELF`」本身说明原表大体一致。
- 不改 `litrev/litrev.py`（裁判）；不改 `.opencode/agents/`（agent 只按路径读契约，v1.2 自动生效）。
- 不回写 `CASES_SELF.md` 的判定列：它记录的是**回写时点**的判断，改判后仍保留原值，与 `DISPUTED.md` 指向同一条裁决。
