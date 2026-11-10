# 判定争议项登记（人工维护）

> 用途：登记「同一份输入出现两次及以上不一致判定」的条目。**这里不是判定表**，不进 131 条汇总，
> 不登记进 `BATCHES.json`，不贴给任何 `auditor-*`，也不由 `audit_prep.py review` 自动生成（那份是
> `REVIEW_NONSUPPORTED.md`，两者不要混写）。
> 规程依据：`RUNBOOK.md` §五（差异 ≠ 错误；先登记、后裁决）、契约 §七.2（`SUPPORTED` 只用于分诊）。
> 状态字段只允许 `OPEN` / `CLOSED`，`CLOSED` 必须写明裁决人、日期、依据与是否改判定表。

## 冻结声明（2026-11-10）

在下列争议项 `CLOSED` 之前：

- 8 张判定表（`out_B1..B3.md`、`out_R1..R5.md`）**保持不动**，汇总冻结在
  `131 条 · S81 / P49 / U1 · SELF118 / D13`；
- 该汇总只表示「判定表当前写了什么」，**不得表述为「81 条有证据支撑」或「81 条已抽检通过」**；
- `SAMPLE_S1_KEYS.md`（抽样时点答案键）与 `out_S1.md`（本轮抽检回写，含 1 条差异）随 git 留档，
  不要在重审后拿新表复算旧答案键。

---

## D-01 · B3-10 / S05

- 状态：**OPEN**
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

### 同一输入的四次独立判定（git / 文件取证）

| # | 来源 | 支撑 | 自足 | 依据 | 缺什么 / 说明 |
|---|---|---|---|---|---|
| 1 | `147f8e4` `out_B3.md` | SUPPORTED | SELF | `"not amenable"` | 无需补 |
| 2 | `e8c140b` `out_B3.md`（round-03） | SUPPORTED | DEPENDENT | `"often ill-"` | 支撑成分齐全；These problems 为代词主语，需补指代 |
| 3 | `691939a` `out_B3.md`（round-04，当前表） | SUPPORTED | SELF | `"not amenable to"` | — |
| 4 | `out_S1.md` `S05`（round-05 抽检） | **PARTIAL** | **DEPENDENT** | `"not amenable"` | 引文截断于 "ill-"、"病构性" 无原词；"尤其" 系加强；主语碎片起于句中，需补完整主语 |

支撑轴 3:1、自足轴 2:2，`audit-stale` 四次依据都逐字命中引文——**依据没过期，不等于判定正确**，本条即实例。
`reports/round-04-verification.md` §三 已点名第 3 次「更像判错而非漂移」；第 4 次在自足轴上回到 `DEPENDENT`，
在支撑轴上首次给出 `PARTIAL`。四个结果，没有一次可以自动充当标准答案。

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

### 补证据的两条正规路径（未执行，需主控另行批准 + 重启 OpenCode）

两条都要新增批次登记 → `python tools/gen_subagents.py` 生成新 agent → **重启 OpenCode** 才生效；
本轮刻意未做，保持「无需重启」。

1. **定向扩抽 B3 的 7 条 SUPPORTED**（`B3-02/03/06/10/12/14/16`）：回答「B3 是系统性偏松还是单条噪声」。
   注意本轮 10 条抽检里 B3 只占 2 条（S04、S05），1/2 的差异撑不起「整批偏松」；B3 是碎片批次
   （16 条里 12 条截断引文），且 round-04 重审已有 6 条码变化，再整批重判会混入双跑漂移。
2. **固定契约双跑 REST 五批**：对 R1–R5 的 83 条另存 `out_R*_dup.md` 对照文件、**不覆盖旧表**，
   测「同一输入重复判定的漂移率」，给出「1/10 差异是噪声还是信号」的基线。这是
   `reports/round-04-verification.md` §三 建议的正规做法；**双跑只测一致性，不能用来裁决谁判对**。

两条路径的证据必须分开记，不得拿跨版本重审冒充双跑。

### 明确不做

- 不改 `AUDIT_CONTRACT.md`：补口径等于升 v1.2，会使 8 张已出表口径变更、答案键失效、抽检基线重做。
  若要补「截断术语 / 多句引文第二句代词主语」的口径，须作为独立一轮并同步重做抽检基线。
- 不改 `litrev/litrev.py`（裁判）、不改 `.opencode/agents/`（本轮无需重启）。
- 不跑 `batch` / `stamp-out`：8 个批次输入未变，跑了只制造无意义改动。
