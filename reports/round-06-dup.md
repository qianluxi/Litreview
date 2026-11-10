# round-06：固定契约双跑（REST_B1–B5 vs 重判）

- 执行对象：`HANDOFF-06.md` §二/§三（顺序派 5 个 dup task，做完停）
- 时间：2026-11-10
- 结论一句话：**双跑漂移率为「支撑轴 8.4%、自足轴 12.0%、任一轴 20.5%（17/83）」，round-04 的 14.3% 不是上界而是低估；自足轴 10 次漂移全部是 SELF→DEPENDENT（单方向），属系统性口径差而非随机噪声。**

## 一、前置核对（派活前，逐条实测）

| 项 | 实测 |
|---|---|
| 5 个 dup agent 存在 | `auditor-rest-b1-dup.md` … `auditor-rest-b5-dup.md`，各 2627 B |
| 输入戳（文件第 6 行） | B1 `c8ad398b0d` / B2 `6e0fdbeb4f` / B3 `2861fd7ff6` / B4 `09168d9ad9` / B5 `b8a12801bd`，与 HANDOFF-06 表逐字一致 |
| 输入条数（`^### R\d-\d\d`） | 16 / 17 / 17 / 16 / 17 = **83** |
| `out_D*.md` 派活前状态 | 5 个文件**均不存在**（不是覆盖，是新建） |
| dup agent 读白名单 | 契约 + 本批 `REST_B{n}.md` + 自己 `out_D{n}.md`；**不含** `out_R{n}.md`，闭卷成立 |

## 二、派发（顺序执行，无并发）

| # | agent | 子会话 / task id | 状态 | 权限拒绝 | 回执全文 |
|---|---|---|---|---|---|
| 1 | `auditor-rest-b1-dup` | `ses_e3bde2868ffeaTdr3NaHIk2dHK` | completed | 0 | `已写入 litrev/_probe/audit/out_D1.md：16 条（SUPPORTED 10 / PARTIAL 6 / UNSUPPORTED 0；DEPENDENT 1）` |
| 2 | `auditor-rest-b2-dup` | `ses_e3bd7f47dffe9C2Y2Fy2nkXIFu` | completed | 0 | `已写入 litrev/_probe/audit/out_D2.md：17 条（SUPPORTED 13 / PARTIAL 4 / UNSUPPORTED 0；DEPENDENT 2）` |
| 3 | `auditor-rest-b3-dup` | `ses_e3bd4e5beffemfaGZrYFQQiHZW` | completed | 0 | `已写入 litrev/_probe/audit/out_D3.md：17 条（SUPPORTED 11 / PARTIAL 6 / UNSUPPORTED 0；DEPENDENT 5）` |
| 4 | `auditor-rest-b4-dup` | `ses_e3bd302b6ffe8KZ4dtd4iYfOew` | completed | 0 | `已写入 litrev/_probe/audit/out_D4.md：16 条（SUPPORTED 11 / PARTIAL 5 / UNSUPPORTED 0；DEPENDENT 1）` |
| 5 | `auditor-rest-b5-dup` | `ses_e3bd1baa1ffe873g35SMH17q3F` | completed | 0 | `已写入 litrev/_probe/audit/out_D5.md：17 条（SUPPORTED 14 / PARTIAL 3 / UNSUPPORTED 0；DEPENDENT 5）` |

- 5 次全部 `completed`，`<task_result>` 全部非空，**权限拒绝 0 次**——与 HANDOFF-06 的预期一致（读回权限修复后，auditor 不再因读自己输出被拒）。
- 5 次都是单独一条消息、上一个返回后才派下一个，没有并发。
- 派发提示词里写明了：戳行逐字抄、表头照契约 §四、条数（16/17/17/16/17）、**id 用输入原 id（R1-01…）不改写成 D1-xx**（否则 `diff-dup` 按 id 交集比对会配不上）、闭卷且不读 `out_R*.md`、输出是新文件。

## 三、逐批判定验收（以文件为准）

| 批次 | 文件行数 | 首行戳 | = 输入第 6 行 | `^| Rn-\d\d |` 行数 | id 序列 | 末行合计 | 是否新文件 |
|---|---|---|---|---|---|---|---|
| D1 | 22 | `c8ad398b0d` | 是 | **16** | R1-01…R1-16 | 16 条（10/6/0；DEP 1） | 是 |
| D2 | 21 | `6e0fdbeb4f` | 是 | **17** | R2-01…R2-17 | 17 条（13/4/0；DEP 2） | 是 |
| D3 | 23 | `2861fd7ff6` | 是 | **17** | R3-01…R3-17 | 17 条（11/6/0；DEP 5） | 是 |
| D4 | 20 | `09168d9ad9` | 是 | **16** | R4-01…R4-16 | 16 条（11/5/0；DEP 1） | 是 |
| D5 | 22 | `b8a12801bd` | 是 | **17** | R5-01…R5-17 | 17 条（14/3/0；DEP 5） | 是 |

格式差异（不影响判定，记录备查）：`out_D2.md`、`out_D4.md` 的戳行与表头之间**没有空行**（D1/D3/D5 有）。契约 §四只要求「第一行是戳行，其后是表」，没有要求空行，`audit-count` 与 `diff-dup` 均能正常解析（见 §四原出）。未因此重派。

旧表未被触碰：`git status` 里没有 `out_R*.md` 的任何改动；`out_D1.md` 在我写它之后由并行的另一条路径提交入库，其余 4 个仍是未跟踪新文件。

## 四、三条验收命令的原始输出

### 1) `python tools/check.py`

```
  ✓ verify 全库: 131/131 PASS
  ✓ audit-count --check: 非 SUPPORTED：50/131 = 38.2%
  ✓ audit-count --prefixes S --check: 非 SUPPORTED：1/10 = 10.0%
  ✓ audit-stale --check: ✓ 全部判定的依据与卡片当前内容一致。
  ✓ batch --check: 合计待刷新 0/131 条（--check 不写盘）
  ✓ gen_subagents --check: ✓ 同步：38 个文件与 AGENT_ROLES.md 一致
  ✓ audit_prep sample --check: ✓ 抽检批次可复现：10/81 条（12.3%），戳 0ff8391a63，答案键一致，8 个源批次输入戳未变。
  ✗ audit_prep golden --check: rc=1   - 与当前判定表复算不一致：GOLDEN.md（判定表变了，需重做金标准）

✗ 回归未通过：audit_prep golden --check
EXIT=1
```

**7/8 绿，第 8 项失败，且与双跑无关。依据：**

- `audit_prep.py` 的 `parse_outputs()` 只收 `^out_[BR]\d+\.md$`，`out_D*.md` **不进入记录集**，所以双跑不可能改变 `golden --check` 的输入。
- `golden --check` 的实现是「按当前判定表重新生成 GOLDEN.md 全文，与磁盘文件逐字节比较」。而 `GOLDEN.md` 正处于**主控侧并行路径的填写中**（`git status` 显示 `M litrev/_probe/audit/GOLDEN.md`，其值是人手填的判定，不是空白模板），所以这项在「已填但未 `verify-golden`」的状态下必然不相等。
- 这一项要等金标准填完、按主控侧流程处理（`reports/round-06-golden.md` 记），不属于本轮 5 个 task 的验收范围。

### 2) `python litrev/litrev.py audit-count --prefixes D --check`

```
批次         条数  SUPP  PART  UNSU  SELF   DEP  合计行
--------------------------------------------------------------
D1         16    10     6     0    15     1  ✓
D2         17    13     4     0    15     2  ✓
D3         17    11     6     0    12     5  ✓
D4         16    11     5     0    15     1  ✓
D5         17    14     3     0    12     5  ✓
--------------------------------------------------------------
合计         83    59    24     0    69    14

口径：83 条 · SUPPORTED 59 / PARTIAL 24 / UNSUPPORTED 0 · SELF 69 / DEPENDENT 14
非 SUPPORTED：24/83 = 28.9%
EXIT=0
```

5 张表的合计行全部 ✓，D 前缀不进入 131 口径（`audit-count --check` 仍为 131 · 81/49/1 · 118/13，见 `check.py` 第 2 行）。

### 3) `python tools/audit_prep.py diff-dup`

```
双跑配对：83 条（R1-5 原判 vs D1-5 重判）
  支撑轴漂移：7/83（8.4%）
  自足轴漂移：10/83（12.0%）
  任一轴漂移：17/83（20.5%）
  支撑轴差异：
    R2-06: PARTIAL → SUPPORTED
    R2-07: SUPPORTED → PARTIAL
    R3-05: PARTIAL → SUPPORTED
    R3-06: SUPPORTED → PARTIAL
    R4-06: SUPPORTED → PARTIAL
    R4-08: SUPPORTED → PARTIAL
    R4-10: PARTIAL → SUPPORTED
  自足轴差异：
    R1-03: SELF → DEPENDENT
    R3-02: SELF → DEPENDENT
    R3-03: SELF → DEPENDENT
    R3-12: SELF → DEPENDENT
    R3-15: SELF → DEPENDENT
    R4-13: SELF → DEPENDENT
    R5-08: SELF → DEPENDENT
    R5-11: SELF → DEPENDENT
    R5-15: SELF → DEPENDENT
    R5-17: SELF → DEPENDENT
  [i] 双跑测的是同输入重复判定的随机漂移，不裁定谁判对；
      漂移率给「抽检 1/10 差异是噪声还是信号」一个基线（round-04 上界 14.3%）。
EXIT=0
```

配对 83/83，无「配不上 id」的告警——说明 5 个 dup agent 都按原 id 写、条数一处不差。

## 五、漂移率怎么读

### 5.1 分轴

| 轴 | 漂移条数 | 比例 | 方向分布 |
|---|---|---|---|
| 支撑 | 7/83 | **8.4%** | S→P 4 条、P→S 3 条（净 SUPPORTED −1：60→59） |
| 自足 | 10/83 | **12.0%** | **SELF→DEPENDENT 10 条，反向 0 条** |
| 任一轴 | 17/83 | **20.5%** | 无一条两轴同时变 |

### 5.2 R 与 D 的分批对照（R 数字取自 round-04 收尾的 `audit-count`）

| 批次 | 条数 | R 支撑 S/P/U | D 支撑 S/P/U | R 自足 S/D | D 自足 S/D |
|---|---|---|---|---|---|
| R1/D1 | 16 | 10/6/0 | 10/6/0 | 16/0 | 15/1 |
| R2/D2 | 17 | 13/4/0 | 13/4/0 | 15/2 | 15/2 |
| R3/D3 | 17 | 11/6/0 | 11/6/0 | 16/1 | 12/5 |
| R4/D4 | 16 | 12/4/0 | 11/5/0 | 16/0 | 15/1 |
| R5/D5 | 17 | 14/3/0 | 14/3/0 | 16/1 | 12/5 |
| 合计 | 83 | 60/23/0 | 59/24/0 | 79/4 | 69/14 |

注意：分批的支撑合计**恰好互相抵消**（R2/R3 各 1 升 1 降、R4 一升一降），所以只看分批汇总会误以为「只有 D4 变了 1 条」；真实漂移 7 条，必须看逐条。

### 5.3 两个结论

**(a) round-04 的 14.3% 不是上界，是低估。** 那个数字来自「跨版本重审」——输入文字变过的条目占大头，混入了「依据变了所以改判」的合理变动。本轮是**同一份输入、同一版契约、只换判读者**，得到任一轴 20.5%。真正的随机漂移基线应按本轮读：**支撑 8.4% / 自足 12.0% / 任一轴 20.5%**。

**(b) 自足轴 10/10 单向（SELF→DEPENDENT），这不是噪声，是口径差。** 随机漂移应当双向分布；单方向说明两批判读者对「主语是否落在引号外、指示代词算不算依赖」（契约 §二、§五.1、§七.1）的把握不一致，且 R 表一侧系统偏松。两条证据：
- R1–R5 的 DEPENDENT 只有 4/83（4.8%），D 侧为 14/83（16.9%），差 3.5 倍；
- round-04 记录的 B1–B3 内部漂移里也有 6 条是 DEPENDENT→SELF（反向），与 R 表同向偏松——两次独立观察指向同一个方向。

因此「131 条里 DEPENDENT 13 条」这个数字**不可当作定论**：按 D 侧口径它应是 20 条上下，合理区间 13–24。支撑轴同理，SUPPORTED 81 的区间约 76–86。

## 六、对 round-05 结论的修正（重要）

round-05 我写的是「S05 降档 → 原批次 B3 存在不该是 SUPPORTED 的条目 → 应整批重审 B3」。有了本轮的基线，这个推论**强度不够**：

- 支撑轴单项漂移率 8.4%/条 → 10 条抽检里「至少出现 1 条漂移」的概率 = `1-(1-0.084)^10 ≈ 58%`。
- 也就是说，**一次 10 条抽检出现 1 条支撑降档，属于最可能发生的情形之一**，单凭它不能判定 B3 的系统性偏松。

修正后的表述：S05 的降档是**信号候选，不是证据**。要把「B3 是系统性偏松」与「单条随机漂移」区分开，最小代价是**对 B3-10 做第三次独立判定**（同一输入、第三个 dup agent），而不是整批重审 B3：
- 若第三次仍判 PARTIAL → 2/2 一致，B3-10 应改判，B3 至少这一条确错；
- 若第三次判 SUPPORTED → 三种判定 1:2，属漂移，B3 不动。

HANDOFF-06 §五 明确「不顺手做 B3 定向扩抽（等双跑漂移率出来再决定）」，而漂移率现在已经出来了，**是否派第三次判定请你裁决**，本轮未做。

## 七、仍未做的事

1. **B3-10 第三次判定**（或 B3 定向扩抽）——等裁决，见 §六。在此之前「B3 有系统性偏松」不成立。
2. **自足轴口径统一**：R 侧与 D 侧对 §五.1/§七.1 的把握差 3.5 倍，需在契约里给出可操作的判定例子（例如「引文主语落在引号外」正/反各 3 例），否则每轮都会重演单向漂移。
3. `golden --check` 与「已填 GOLDEN.md」天然冲突（§四.1）：需要区分「模板未变」与「模板已填」，否则 `check.py` 在金标准填写期间永远退 1。
4. `check.py` 的金标准项不属于本轮 5 个 task 的验收；`reports/round-06-golden.md` 未写（主控侧并行路径）。
5. B1–B3（48 条）**没有做双跑**：本轮 dup agent 只覆盖 REST 五批。若要把 131 条全量基线补齐，还需 3 个 frag dup agent（要重启）。因此本文的 20.5% 是 83 条样本的估计，不是 131 条的实测。
