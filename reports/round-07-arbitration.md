# round-07 裁决执行：D-01 CLOSED + 参考集冻结改造

- 裁决：项目所有者 2026-11-10 授权「收口：支撑改 `PARTIAL`」（选项说明中已含「重做 S1 抽检基线、派一次 `auditor-sample-s1`、不用重启」）
- 执行人：主控（离线，未派任何 task）
- 影响面：`out_B3.md` 一条 + 合计行；`SAMPLE_S1.md` / `SAMPLE_S1_KEYS.md` 重抽；`tools/audit_prep.py` 两处改造；
  `GOLDEN_MAP.md` 加冻结清单；`REVIEW_NONSUPPORTED.md` 重生成；文档与登记表同步。
  **`litrev/litrev.py`（裁判）、`AUDIT_CONTRACT.md`（契约 v1.1）、`.opencode/agents/*`（agent 定义）均未改动 → 不需要重启 OpenCode。**

## 一、裁决内容

| 轴 | 裁决 | 依据 |
|---|---|---|
| 支撑 | `SUPPORTED → PARTIAL` | v1.1 固定契约下 4 次判定 1:3；三次 `PARTIAL` 收敛到同一可机械核验的缺陷：引文截断于 `often ill-`，论断的「病构性」（ill-structured）在引文内无完整词形 |
| 自足 | **不动**（保持 `SELF`） | 2:2 无法裁；自足轴存在 11:1 单向口径差（`P≈0.3%`），任何单条裁决都会被口径差污染；留待契约 v1.2 |

**未采纳的理由**：`out_B3P.md` 给出的另两条理由与事实不符（称 `structural design are` 主语在引号外、称 `problems` 未在引文内出现，
两者都在引文里）。裁决只采信「截断」一条，不背书错误理由；这一点已写进 `DISPUTED.md`，防止日后被当成判例援引。

## 二、落表动作与机械复算

```
$ python litrev/litrev.py audit-count --check
口径：131 条 · SUPPORTED 80 / PARTIAL 50 / UNSUPPORTED 1 · SELF 118 / DEPENDENT 13
非 SUPPORTED：51/131 = 38.9%
EXIT=0
```

`out_B3.md` 的 `B3-10` 行：`SUPPORTED | SELF | "not amenable to" | —` → `PARTIAL | SELF | "often ill-" | 引文在 often ill- 处截断…（D-01 裁决）`；
合计行 `S7/P9 → S6/P10`。依据 `"often ill-"` 逐字在卡片里，`audit-stale --check` 仍 131/131 一致。

## 三、发现的真实缺陷：一次裁决会把参考集全部打崩

改表后立刻复跑，两条检查变红——而且**不是预期内的**：

```
$ python tools/audit_prep.py golden --check
✗ 金标准自检未通过：
  - 与当前判定表复算不一致：GOLDEN_MAP.md（判定表变了，需重做金标准）
  - GOLDEN.md 条目详情与当前判定表复算不一致（判定表变了，需重做金标准）
```

原因：`pick_golden` 是**按支撑码分层抽样**（S15/P9/U1）。`B3-10` 从 `S` 变 `P` 后，两个层的池都变了，`seed=43` 重抽得到的是**另一批 25 条**。
后果是：**用户已填好的 25 条金标准（92% 一致率，项目唯一的准确性参照系）会因为一次单条裁决而作废，必须重填**。

抽检侧同理：`sample --check` 也按当前池重算，改判即红；且**新样本与旧 `out_S1.md` 不同源时，`verify-sample` 仍会算出一个
「9/10 一致」的假数字**（它只校验条目编号顺序，不校验首行戳是否同源——戳检查存在，但排在后面且不阻断比对）。

这两条都是设计缺陷：**参照集不能随被测对象漂移**。如果每裁一条就要重填 25 条金标准，这个系统的质量测量就永远做不完。

## 四、改造一：参考集冻结（`<!-- picks -->`）

`SAMPLE_*_KEYS.md` 与 `GOLDEN_MAP.md` 里新增一行机器可读的冻结清单：

```
<!-- picks: pool=80; k=10; seed=42; rate=0.12; B1-13,B2-12,B2-16,B3-02,B3-12,R1-13,R2-04,R2-09,R4-01,R5-06 -->
```

`--check` 改为**按清单复现**，不再按当前判定表重抽：

- 抽样条目事后被裁决修改 → 仍可逐字复现，只打印「N 条在原判之后被裁决修改（…）」；
- 判定表改动不再使已完成的金标准/抽检失效；
- 手改冻结清单会被抓出（`--check` 退 1）；
- 要抽新一批 → 另存旧文件后重跑 `sample`，旧样本按 commit 留档。

**变异测试（临时目录，未改仓库）**：

| 用例 | 期望 | 实测 |
|---|---|---|
| 冻结复现（判定表不动） | 样本 + 答案键逐字一致 | `True / True`，drift `[]` |
| **抽样中某条（B3-12）事后改判** | 仍逐字一致，drift 报出该条 | `True / True`，drift `['B3-12']` |
| 篡改冻结清单（删一个 id） | `sample --check` 退 1 | 退 1，报「与冻结清单复算不一致」 |
| 还原后 | 退 0 | 退 0 |

## 五、改造二：`verify-sample` 的同源门禁

原行为：戳不一致时只记一条 problem，但**继续算「与答案键一致 N/10」**——旧回写 + 新答案键会产出无意义的命中率。
现行为：戳不一致 → 立刻停机，不再算一致率：

```
$ python tools/audit_prep.py verify-sample
✗ 回写与本批输入不同源：
  - out_S1.md 首行 `> 快照 sha1: 0ff8391a63`
  - SAMPLE_S1.md 应为 `> 快照 sha1: 7d1a204d54`
  → 样本已重抽或回写是旧的，先按当前输入重派一次 auditor-sample-s1，再验收。
EXIT=1
```

**变异测试**（合成回写，临时目录）：

| 用例 | 实测 |
|---|---|
| 正确戳 + 10 条全 `SUPPORTED` | 退 0，`10/10` |
| 正确戳 + 1 条降档 | 退 1，`9/10 · 差异 S03:SUPPORTED→PARTIAL`，并要求登记争议项 |
| 戳不同源 | 退 1，且**不再输出一致率** |

## 六、S1 抽检基线重抽

候选池 80，`seed=42`、`rate=0.12` → 抽 10 条（12.5%），戳 **`7d1a204d54`**：

| S id | 原批次 id | 原判 |
|---|---|---|
| S01 | B1-13 | SUPPORTED |
| S02 | B2-12 | SUPPORTED |
| S03 | B2-16 | SUPPORTED |
| S04 | B3-02 | SUPPORTED |
| S05 | B3-12 | SUPPORTED |
| S06 | R1-13 | SUPPORTED |
| S07 | R2-04 | SUPPORTED |
| S08 | R2-09 | SUPPORTED |
| S09 | R4-01 | SUPPORTED |
| S10 | R5-06 | SUPPORTED / DEPENDENT |

与旧样本（戳 `0ff8391a63`，池 81）只有 4 条重合；旧 `S05 = B3-10` 已不在池内，符合预期。旧输入与答案键留档于 commit `7077b6f`。

## 七、当前状态

```
$ python tools/check.py
  ✓ verify 全库: 131/131 PASS
  ✓ audit-count --check: 非 SUPPORTED：51/131 = 38.9%
  ✓ audit-count --prefixes S --check: 非 SUPPORTED：1/10 = 10.0%
  ✓ audit-stale --check: 131/131 一致
  ✓ batch --check: 合计待刷新 0/131
  ✓ gen_subagents --check: 42 个文件同步
  ✓ audit_prep sample --check: 10/80（12.5%），戳 7d1a204d54
  ✓ audit_prep golden --check: 25 条（S15/P9/U1），戳 d46f9e7c3f
✓ 全部机械自检通过。   EXIT=0
```

`verify-sample` 单独跑仍是红的——因为 `out_S1.md` 还是旧回写（戳 `0ff8391a63`），这是**预期状态**：新样本尚未派发。
它不进 `check.py`（状态相关检查），不影响结构回归。

## 八、下一步（一步派发，不需要重启）

派 `auditor-sample-s1` 覆盖写 `out_S1.md`（read 白名单只有「契约 + `SAMPLE_S1.md`」，路径未变，agent 定义未改）。
回来后依次跑 `python litrev/litrev.py audit-count --prefixes S --check` → `python tools/audit_prep.py verify-sample`。
`verify-sample` 退 0，才能说「新一批 10 条抽检通过」。

同时仍未做：契约 v1.2（自足轴口径：截断术语 / 多句引文第二句代词主语 / 范围收窄）、51 条非 SUPPORTED 人工复核
（`REVIEW_NONSUPPORTED.md` 已按 51 条重生成）。
