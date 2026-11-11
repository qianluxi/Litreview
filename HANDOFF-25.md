# HANDOFF-25：P2 批次入库（6 篇英文围填海 → 收 5 拒 1）—— 待重启派抽取

> 日期：2026-11-11 · 上一轮：`HANDOFF-24`（P1 判定完成，`S179/P5/U0`）
> 本轮结论：6 篇新 PDF 验收**收 5 拒 1**；`index` **38 → 44**（已有条目 **0 变化**，第 5 次实证）；
> `gen_subagents` **61 → 71**（+5 对，拒收件被正确跳过）；`check.py` 仍 **12/13**（唯一红为已定案的 `sample S2`）。

## 一、逐篇验收

| 文献 | 页 | 词/行（raw→layout） | 短行 | 结论 |
|---|---|---|---|---|
| `Park2025_InSAR_Subsidence_Reclamation`（韩国西海岸 InSAR 沉降，IGARSS 2025） | 4 | 7.23 → 7.31 | 18.5% | **收** |
| `Elgaali2024_ANN_SoilProperties`（ANN 预测土性，ASET 2024） | 4 | 6.03 → 6.85 | 25.9% | **收** |
| `Zhu2022_Hydrodynamics_Zhoushan_Reclamation`（舟山围填海对水动力影响，ICGMRS 2022） | 4 | 7.53 → 7.23 | 27.7% | **收** |
| `Qu2011_CoastalTopography_SheyangEstuary`（射阳河口海岸地形，2011 IEEE） | 4 | 5.86 → 7.84 | 11.8% | **收** |
| `Lu2023_Settlement_Prediction_Reclamation`（吹填沉降预测，JCCME 2023） | 4 | 6.34 → 7.39 | 18.1% | **收** |
| `Structural_design_of_swimming_pools`（游泳池结构设计） | 12 | 1.11 → 8.80 | 100% → 21.4% | **拒**：全文乱码（`!" #$%&'`），字体缺 `ToUnicode`，layout 修复无效，工具无 OCR 通道 |

- 5 篇都是 4 页**短会议论文**，4 页是原文篇幅不是截断（正文、结论、参考文献齐全）。
- 拒收件**留盘未改名**（作证据），与 P1 的 `陆达仁`/`沈学明` 同处置。`gen_subagents` 对它报「取不到作者/年份」，不会为它生成 agent。
- **新入库判据的第二次确认**：这次拒收的原因不是「词/行低」（8.80 反而高于 5 篇里的三篇），而是**字符本身没有意义**。⇒ 「句子连续性」判据要再加一层：**前提是字符可读**。

## 二、入库动作

| 动作 | 结果 |
|---|---|
| 5 篇改名 `AuthorYYYY_xxx.pdf` | 全部完成 |
| `aliases.json` | 33 → **38**（新增 `Park`/`Elgaali`/`Zhu`/`Qu`/`Lu`） |
| `text` 抽取 | 5 篇按新名重抽，旧名 txt 已清理 |
| `index` | **38 → 44**，已有 38 条 `corpus`/`manifest` **0 变化** |
| `gen_subagents` | **61 → 71**，`--check` **71/71** |
| `check.py` | **12/13**，无新增红项 |

**姓氏冲突**：`Lu` 与已有的 `Lu2024_Clause_PrimitiveFunctions`（陆，基元函数库）**重姓**。年份不同（2023 vs 2024），引用标签 `(Lu, 2023)` 与 `(Lu, 2024)` 可区分，但派发词里必须强调**年份写准**——这是 `蒋灿/姜嘉伟` 那次撞标的同类陷阱。

## 三、这批的特殊价值（比 P1 更值得测）

P1 是**中文**围填海（18 条），这批是**英文同领域**围填海（预计 30 条左右）。这构成 **同领域、跨语言**的对照：

- 若本批英文 `DEP` 率仍落在英文基线附近（14/145 = 9.7%），则 `D-06` 的「中文 38% 是语言形态差异」得到**域控制**的加强——不是因为海岸工程文本更依赖上下文。
- 若本批英文 `DEP` 率明显抬高，则 `D-06` 的归因要改写：**领域**也在起作用。

⇒ 这是 `D-06` 定案（α 维持）后第一次能检验其归因的样本。**不要为了让它好看而干预判定**。

## 四、回来我跑的验收（抽取完成后）

1. `card-check` 5 张全过（7 节齐全、节名逐字、每节 1 论断 + 0/1 引文）。
2. `verify` 全库总数 = 184 + 本批引文数，逐条 PASS。
3. 5 个「未涉及」预判：`相似性或检索机制` 5 篇全未涉及（我已按 `retriev|similarit|case-based|query|nearest` 逐篇检索，仅 `Qu2011` 命中一处 `nearest beach line`，不是检索机制）。
4. `batch` 复算报「条目内容未变，仅更新戳」⇒ 证明我没手抄。
5. `gen --check` 71/71（本批不新增 agent）。
6. 预期 `check.py` 会红 **2 项**（`card-coverage` + `gen --check`）：5 张新卡带引文但尚未登记批次，`ex-` 变陈旧残留。**这是预期状态，不要修**。

## 五、5 条派发词（重启后并列发在同一条消息里）

> 重启是硬要求：`ex-park2025-...` 等 10 个 agent 只在启动时进注册表，不重启会报 `Unknown agent type`。

```
按 HANDOFF-25.md §五 的要求，用 ex-park2025-insar-subsidence-reclamation 抽取 Park2025_InSAR_Subsidence_Reclamation 这篇文献，产出 7 节卡片。
```

```
按 HANDOFF-25.md §五 的要求，用 ex-elgaali2024-ann-soilproperties 抽取 Elgaali2024_ANN_SoilProperties 这篇文献，产出 7 节卡片。
```

```
按 HANDOFF-25.md §五 的要求，用 ex-zhu2022-hydrodynamics-zhoushan-reclamation 抽取 Zhu2022_Hydrodynamics_Zhoushan_Reclamation 这篇文献，产出 7 节卡片。
```

```
按 HANDOFF-25.md §五 的要求，用 ex-qu2011-coastaltopography-sheyangestuary 抽取 Qu2011_CoastalTopography_SheyangEstuary 这篇文献，产出 7 节卡片。
```

```
按 HANDOFF-25.md §五 的要求，用 ex-lu2023-settlement-prediction-reclamation 抽取 Lu2023_Settlement_Prediction_Reclamation 这篇文献，产出 7 节卡片。
```

### 每篇的已知陷阱（贴进对应派发词，逐条不同）

- **`Park2025`**：p.1 顶部是 IEEE 版权块，**词序被倒置**（读成 `Symposium / Sensing / Remote / and / ...`）。不要从那里取句，正文从 `Abstract—` 起。
- **`Elgaali2024`**：p.1 版权块同样倒序；正文有大量 ANN 参数与 `R`/`RMS` 统计量，**符号照抄**（原文用 `RMS` 不是 `RMSE`）。
- **`Zhu2022`**：**p.1 是双栏交错**——`Abstract` 之后紧接右栏段落，且 `II.METHOD` 排在 `I.INTRODUCTION` **之前**。取句**必须以句末标点为界**，禁止跨栏拼接：拼出来的句子 `verify` 会 PASS（逐字都在），但它不是作者写的那句话。**这是本批唯一的高风险页**。
- **`Qu2011`**：单栏干净；节号写作 `II DATE AND METHODOLOGY`（缺句点，不是抽取错误）。正文含大量速率与距离（`4~6m/a`、`199.2m/a`、`0.94km`），**逐字保留波浪号与单位**。
- **`Lu2023`**：表格数字多，**表格行不要当句子抄**；负值写作 `-76.9 mm`，行末可能把负号与数字断在两行，抄写时确认是一个数。

### 全批共同要求

- 7 节固定（名/编号/顺序不可改）；某节原文没有就写 `- 论断：未涉及` 且**不留引文行**。
- 引文**从句子开头起抄**（首字母小写 = 片段 → `DEPENDENT`）。
- 页码用 **PDF 物理页**（`<<<PAGE n>>>`），不是会议论文集印张页码。
- **`系统形态`不许贴分类标签**：原文没有自述「已实现的系统/原型/框架/方法」措辞时，**只写它实际做了什么**，不要写「属纯方法研究」这类（`round-44` 已把这条写进 `AGENT_ROLES.md §5` 反例，P1 的 3 条就是这么被判 `PARTIAL` 的）。
- **情态不许升级**：「可以推测/能够确保/may」不许写成「表明/说明/目的是」（`AGENT_ROLES.md` 硬规则 9 ⑥）。
- **`Lu2023` 的引用年份必须写 2023**（库内已有 `Lu2024`，重姓）。

## 六、当前门禁状态

`check.py` **12/13**，唯一红项是 `audit_prep sample S2 --check`（`B2-08` 换引文导致的冻结参考集永久失效，已定案不修）。

判定表 **184 条 · `S179/P5/U0` · `SELF152/DEP32`**，本批尚未进表。

远程 **24 个 commit 未推**（`github.com/qianluxi/Litreview`），`D-05` 仍 OPEN（1 条，方向偏严，不拦投产）。
