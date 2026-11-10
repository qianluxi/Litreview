> **已收口（2026-11-10 16:2x）**：项目所有者回写 20 条，4 处争议按预填保留 → 见 `reports/round-09-v12.md`
> 与 `DISPUTED.md` D-02（CLOSED）。本文保留为预填过程的记录，其中的 16/20 是**冻结基线**，不是最终口径。

# round-08b：自足轴判例集预填 + 口径诊断

- 时间：2026-11-10 15:46–16:05
- 性质：**主控代填**，供用户审核修改；不是人判结论，也不改判定表
- 产物：`CASES_SELF.md`（20 条已填）、`reports/round-08-cases-prefill.md`（本文件）

## 一、判据先对齐：自足轴看的是**引文**，不是论断

契约 §二 轴 2 原文：

> `SELF`：引文自带主语与指代，单看这一句就知道在说谁、说什么
> `DEPENDENT`：引文以 `it / this / these / such` 开头，**或主语落在引号外**

所以判的是「**这条引文**能不能脱离上下文读」，不是「论断写得清不清楚」。论断补主语不算越界（§三.5）。预填按此执行。

## 二、20 条预填结果

| C | 原批次 | 引文形态 | 预填 | 表内 | 差 |
|---|---|---|---|---|---|
| C01 | B1-08 | 名词短语 `information on…` | DEPENDENT | DEPENDENT | |
| C02 | B1-16 | 形容词短语 `easier to…` | DEPENDENT | DEPENDENT | |
| C03 | B2-05 | 标题 + `this section introduces…` | SELF | DEPENDENT | **差** |
| C04 | B2-11 | 名词列举 `expert system development tools, notably…` | DEPENDENT | DEPENDENT | |
| C05 | B3-08 | 介词短语 `a given problem by finding matches between` | DEPENDENT | DEPENDENT | |
| C06 | B3-09 | `when` 从句 + 截断 | DEPENDENT | DEPENDENT | |
| C07 | B3-11 | `This paper thoroughly examines…` | SELF | DEPENDENT | **差** |
| C08 | R2-02 | `This may easily lead to…` | DEPENDENT | DEPENDENT | |
| C09 | R2-17 | 分词开头 `Coined as SSIG…, 7 essentially computes…` | DEPENDENT | DEPENDENT | |
| C10 | R3-08 | `These limitations came from…` | DEPENDENT | DEPENDENT | |
| C11 | R1-03 | 主谓齐全 + `aforementioned` 作状语 | SELF | SELF | |
| C12 | R3-02 | `This study proposed…` | SELF | SELF | |
| C13 | R3-03 | `It is important to note that…`（形式主语） | SELF | SELF | |
| C14 | R3-12 | 状语 + `this approach enables…` | DEPENDENT | SELF | **差** |
| C15 | R3-15 | `Therefore, this study develops…` | SELF | SELF | |
| C16 | R4-13 | `These input graphs represented…` | DEPENDENT | SELF | **差** |
| C17 | R5-08 | `This section presents…` | SELF | SELF | |
| C18 | R5-11 | `We recognize the fact that these data…` | SELF | SELF | |
| C19 | R5-15 | `This paper is an early attempt…` | SELF | SELF | |
| C20 | R5-17 | `This work is however limited to…` | SELF | SELF | |

`verify-cases` 复算：**16/20（80%）**，2 条表偏严（C03、C07）、2 条表偏松（C14、C16），表内 10 条 `DEPENDENT` 阳性确认 **8/10**。

**方向是 2:2，不是单向。** 所以这批判例证不出「表偏严」或「表偏松」——证出的是**有 4 个格子契约没写**。

## 三、真正的发现：表内对同一构造自己就不一致

把这 4 条差异摊开看，全是两个族的边界：

**族 A：自指句**（`this paper / this study / this work / this section` + 谓语）——指的就是本文本节，不需要外部先行词。

- C07 `This paper thoroughly examines…` → 表判 `DEPENDENT`
- C17 `This section presents…` → 表判 `SELF`
- C19 `This paper is an early attempt…` → 表判 `SELF`
- C12 `This study proposed…`、C15 `Therefore, this study develops…`、C20 `This work is however limited to…` → 表判 `SELF`

同一种句法，**两个码都出现过**。这不是判读者马虎，是契约字面「引文以 `it / this / these / such` 开头即 `DEPENDENT`」与语用直觉（`this paper` 谁都知道指本文）直接冲突，两条路都合法。

**族 B：`this/these` 指代前文具体对象**

- C10 `These limitations…` → 表判 `DEPENDENT` ✔
- C16 `These input graphs…` → 表判 `SELF` ✘（同为指代前文对象）
- C14 `this approach enables…` → 表判 `SELF` ✘
- C08 `This may easily lead to…` → 表判 `DEPENDENT` ✔

## 四、131 条的分族实测（解释掉「11:1 单向漂移」）

按引文开头把 131 条分类，再看当前自足码：

| 引文形态 | 条数 | 其中判 `DEPENDENT` | 比例 |
|---|---|---|---|
| 自指句（`This paper/study/work/section…`） | 12 | **1**（`B3-11`） | 8.3% |
| `it/this/these/such` 指代前文非自指对象 | 6 | 4（`B1-12` `B3-13` `R2-02` `R3-08`） | 66.7% |
| 纯片段（截断/名词短语，主谓在引号外） | 36 | 6 | 16.7% |
| 完整句、非指代 | 77 | 2（`R2-17` `R5-06`） | 2.6% |
| 合计 | 131 | 13 | 9.9% |

关键一点：**表内对自指句其实 11/12 都判 `SELF`**。也就是说，那 11 次 `SELF→DEPENDENT` 双跑翻转里，有 5 次翻的是自指句（`B2-15` `R3-02` `R5-08` `R5-15` `R5-17`）——**双跑那一侧按字面读、表这一侧按语用读**。

所以「11:1 单向漂移」的机理不是「表偏松/偏严」，而是：**约 13 条落在契约没定义的格子里，谁抽到谁翻**。这也是为什么漂移率 9.9% 看着随机，方向却一边倒。

## 五、建议的 v1.2 条文（等你确认第 2 节的 4 个格子后落盘）

在契约 §五.1 后追加一条，只补定义、不改四元组、不改输出格式：

> **6. 自足轴的三条边界（v1.2）**
> a. 自指主语不算依赖：`this paper / this study / this work / this section / this article` + 谓语 → `SELF`（指的就是本文本节，无需外部先行词）。
> b. 形式主语不算依赖：`It is important/notable that…`、`It can be seen that…` 的真主语在 `that` 从句内 → `SELF`。
> c. 只有 `it / this / these / such` **指代前文具体对象**（`this approach` / `these limitations` / `these data` / `this method`）且先行词在引号外，或主句主语被分词/从句吞掉 → `DEPENDENT`；纯名词短语、截断片段一律 `DEPENDENT`（主谓在引号外）。

**影响面（已算）**：131 条里最多 13 条需要确认（12 条自指句 + 1 条形式主语），其中当前判了 `DEPENDENT` 的只有 `B3-11` 一条。也就是说 v1.2 落盘后判定表的改动量是 **0–1 条**，不会引发整批重审——这正是上轮「先补阳性样本再改契约」想要的结果。

## 六、需要你做的事（只 4 个格子）

打开 `CASES_SELF.md`，只需确认这 4 行；其余 16 行如无异议就保持：

| C | 引文 | 我填 | 表内 | 你要定的 |
|---|---|---|---|---|
| C03 | `this section introduces … image-prompt diffusion model` | SELF | DEPENDENT | 自指算不算依赖 |
| C07 | `This paper thoroughly examines these feature retrieval methods` | SELF | DEPENDENT | 同上（且与 C17/C19 必须同码） |
| C14 | `this approach enables effective retrieval` | DEPENDENT | SELF | `this approach` 指前文方法算不算依赖 |
| C16 | `These input graphs represented node features…` | DEPENDENT | SELF | `these + 名词` 指前文构造算不算依赖 |

改完跑 `python tools/audit_prep.py verify-cases`；一致率与方向会重算，我再据此落 v1.2 条文并登记 `DISPUTED.md`（若与表有差异）。

## 七、口径提醒

这次是**主控代填**，`verify-cases` 输出里的「回写」指本预填，不是人判。它的 16/20 不能当「判定表可信度」读——可信度仍看 `verify-golden`（支撑 23/25、自足 25/25，人开卷）。本集的作用只有一个：把自足轴那 13 条边界情形固定成人判，供 v1.2 引用。
