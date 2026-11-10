# round-09：判例集收口 → 契约 v1.2（自足轴三族边界）

> 触发：项目所有者回写 `CASES_SELF.md` 20 条（2026-11-10 16:09），4 处争议格子按预填保留。
> 结论：**自足轴口径定案并落契约 v1.2**；判定表改 4 条，两轴总量不变；工具修 2 个缺陷；9 项回归全绿。

## 一、回写结果

| 指标 | 值 |
|---|---|
| 填写 | 20/20（依据逐字命中引文，均 ≤15 字符） |
| 冻结基线一致率 | **16/20（80%）** |
| 表判 `DEP`、回写 `SELF` | 2 条：`C03→B2-05`、`C07→B3-11`（表偏严） |
| 表判 `SELF`、回写 `DEP` | 2 条：`C14→R3-12`、`C16→R4-13`（表偏松） |
| 表内 `DEPENDENT` 阳性确认 | 8/10 |
| 方向 | **2:2**，不是单向偏差 |

4 条差异全部落在同一处：`this/these` 后面跟的是**篇章名词**还是**内容名词**。表内对同一构造自身不一致
（`this section introduces` 判 `DEP`，`This section presents` 判 `SELF`；`This paper thoroughly examines` 判 `DEP`，
`This paper is` 判 `SELF`），这不是判读者马虎，是契约 v1.1 §二「引文以 this 开头即 `DEPENDENT`」与
§七.1「指示代词作限定词也算依赖」两条字面规则打架。

## 二、裁决与落表

| id | 引文首句 | 原判 | 现判 | 依据 |
|---|---|---|---|---|
| `B2-05` | `this section introduces the construction, training, and inference methods…` | `DEP` | `SELF` | 篇章自指，读者不必往回翻 |
| `B3-11` | `This paper thoroughly examines these feature retrieval methods…` | `DEP` | `SELF` | 同上；与 `R5-15` 同构造 |
| `R3-12` | `…, this approach enables effective retrieval of building floor plans.` | `SELF` | `DEP` | `this approach` 回指前文方法，先行词不在引文内 |
| `R4-13` | `These input graphs represented node features as…` | `SELF` | `DEP` | `These input graphs` 回指前文构造的图 |

**总量不变**（+2 −2）：

```
改判前：S80 / P50 / U1 · SELF118 / D13   非 SUPPORTED 51/131 = 38.9%
改判后：S80 / P50 / U1 · SELF118 / D13   非 SUPPORTED 51/131 = 38.9%
```

变的只有两个批次内部的 `DEPENDENT` 计数：`out_B2` 2→1、`out_B3` 4→3、`out_R3` 1→2、`out_R4` 0→1，
各自合计行已同步（`audit-count --check` 复算勾对）。所以此前所有引用汇总数字的报告**不需要重写**。

登记：`litrev/_probe/audit/DISPUTED.md` **D-02 = CLOSED**。

## 三、契约 v1.2：自足轴三族边界

新增 **§八**，并把 §二 轴 2 的 `DEPENDENT` 定义、§七.1 的「`this section` 也算依赖」加**修正声明**
（否则 agent 会按「契约自身矛盾 → `CONTRACT_CONFLICT` 停机」处理，整批卡住）：

| 族 | 形态 | 判 | 判据 |
|---|---|---|---|
| A 自指 | `this paper / study / work / article / section / chapter / the present study` + 谓语 | `SELF` | 指代对象就是本文本节 |
| B 形式主语 | `It is … that …` | `SELF` | 真主语在 `that` 从句内，且从句主语在引号内 |
| C 回指前文 | `this approach / these limitations / these input graphs / such approaches` + 谓语 | `DEPENDENT` | 先行词不在引文内，读者必须往回翻 |
| D 片段 | 名词/介词/`when` 从句/分词开头，主谓在引文外 | `DEPENDENT` | 主语缺失（§五.1 不变） |

判据一句话：**`this/these` 后跟篇章名词 = 自指 → `SELF`；后跟内容名词 = 回指 → 看先行词在不在引文内。**

## 四、影响面（实测，不是估计）

131 条按引文首句分族：

| 族 | 条数 | 原判 `DEPENDENT` | 需改 |
|---|---|---|---|
| A 自指 | 12 | 1（`B3-11`） | 1 |
| B 形式主语 | 1 | 0 | 0 |
| C 回指 / D 片段 | 118 | 12 | 3（`B2-05`、`R3-12`、`R4-13`） |

即 **v1.2 落盘只动 4 条**，其余 127 条与本节点状修正无关——这正是先补阳性样本、后改契约的收益：
若 round-06 时直接按「11:1 漂移」升 v1.2 整批重判自足轴，会白改约 120 条。

## 五、工具修复（本轮暴露的两个缺陷）

1. **`ROW_KEY_RE` 只认 `[SG]\d\d`**：冻结清单的还原函数对判例集答案键（`C01…`）**静默失效** →
   `cases --check` 在改判后必然变红，且 `drift` 永远为空（不会告警）。
   已放宽为 `[A-Z]\d\d`。修复后 `cases --check` 输出：
   `注：4 条在原判之后被裁决修改（B2-05, B3-11, R3-12, R4-13），仍按清单复现。`
2. **`verify-cases` 只报冻结基线**：改判落表后仍打印「16/20、表偏严/偏松」，会被读成「表还没改」。
   已加第二行 `按当前判定表复算：20/20（全部与回写一致；上行为冻结基线，不受改判影响）`。
   变异测试（把 `C14` 改回 `SELF`）→ 第二行变 `19/20`，复原后回 20/20。

## 六、交叉校验（全部实跑）

```
python tools/check.py                 → 9/9 ✓
python litrev/litrev.py verify 全库   → 131/131 PASS
audit-count --check                   → 每个批次合计行 ✓，汇总 S80/P50/U1 · SELF118/D13
audit-stale --check                   → 依据与卡片一致
gen_subagents --check                 → 42 个 agent 同步
sample --check                        → 10/80，戳 7d1a204d54
golden --check                        → 25 条，戳 d46f9e7c3f
cases --check                         → 20 条，戳 a4e66877dc（drift 4 条，按清单复现）
verify-sample                         → 10/10 与抽样时点原判一致，合计行自洽
verify-golden                         → 支撑 23/25、自足 25/25、双轴 23/25
verify-cases                          → 冻结基线 16/20；现表 20/20
```

## 七、剩余工作

| 项 | 状态 |
|---|---|
| 自足轴口径 | **已定案**（v1.2 §八），无需再补依据 |
| `REVIEW_NONSUPPORTED.md`（51 条支撑轴复核） | **未做**，唯一剩下的主线人活 |
| 支撑轴口径 | 未动；9.9% 配对漂移、`P≈13%` 不显著，金标准 2 条偏严（`G03`/`G18`）仍挂着，但不构成改契约的依据 |

## 八、复现

```bash
python tools/check.py                                  # 9 项结构自检
python tools/audit_prep.py verify-cases                # 冻结基线 + 现表复算
python litrev/litrev.py audit-count --check            # 汇总与合计行
git show <本轮 commit>:litrev/_probe/AUDIT_CONTRACT.md # 对照 v1.1 → v1.2 的 §二/§七.1/§八
```

## 九、边界声明

- v1.2 只裁**自足轴**。支撑轴的 `SUPPORTED/PARTIAL` 边界、截断引文（D-01 那条）**没有**因此改动。
- `17/20`、`19/20` 之类的数字只在本轮变异测试里出现，不是实测一致率；实测只有 16/20（冻结）与 20/20（现表）。
- 20/20 也不等于「判得对」：它是**回写与现表自洽**，可信度仍看 `verify-golden` 的支撑 23/25、自足 25/25。
