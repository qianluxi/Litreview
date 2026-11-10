# round-08：新一批抽检（S1）验收 + 自足轴判例集

- 时间：2026-11-10 15:28–15:45
- 契约：v1.1 固定，**未改契约、未改判定表、未改 `litrev.py`**
- 输入：`SAMPLE_S1.md`（10 条，戳 `7d1a204d54`，按新池 80 重抽）
- 产出：`out_S1.md`（auditor-sample-s1 回写）+ 本报告 + `CASES_SELF_IDS.txt` / `CASES_SELF.md` / `CASES_SELF_KEYS.md`

## 一、派发与取证（不靠截图）

子会话 `ses_e3ba49979ffe1PpcDYISA5A8ga`（agent `auditor-sample-s1`，15:28:06 → 15:29:05，59 秒）：

| 项 | 实测 |
|---|---|
| 工具调用 | 3 次：`read` 契约、`read` `SAMPLE_S1.md`、`write` `out_S1.md` |
| 闭卷 | 只读了「契约 + 本批输入」两个文件，**未读卡片、未读其它批次、未读任何 `out_*.md`、未读答案键** |
| 权限拒绝 | 0 次（无 `ruleset` 拒绝原文） |
| 只写自己的输出 | 是，唯一写操作是 `out_S1.md` |

这是本项目第一次用 `opencode.db` 的 `part` 表把「闭卷」验成机械事实，而不是靠回执自述。

## 二、文件级验收

```
python tools/audit_prep.py verify-sample
  抽检回写：out_S1.md · 戳 7d1a204d54 · 10 条
  ✓ 首行戳一致：7d1a204d54
  ✓ 表头与契约 §四逐字一致
  ✓ 判定行 10 条，id 与顺序正确
  ✓ 依据逐字命中检查：10 条已比对引文原文
  ✓ 合计行自洽：(10, 10, 0, 0, 1)
  与答案键一致：10/10
EXIT=0
```

- 合计：`SUPPORTED 10 / PARTIAL 0 / UNSUPPORTED 0；DEPENDENT 1`，与判定行自洽。
- 依据栏 10 条全部逐字出现在引文里（连字归一后），包括 `χ2 distance`（U+03C7）、`target cases`、`in one system` 这类原词。
- 与抽样时点原判 **10/10 一致**，无方向差异。

**这个 10/10 不能读成「判得对」**：它是自洽（同模型两次判定），支撑轴漂移基线 9.9% 下，10 条全中的概率约 `0.9^10 ≈ 35%`——属正常范围，不构成证据。

## 三、一次意外的强证据：金标准自足轴 25/25

跑金标准比对时顺带看到分轴数字：

```
python tools/audit_prep.py verify-golden
  支撑轴一致：23/25（92%）
  自足轴一致：25/25（100%）
  [!] 人判更严（原 S → 人非 S）2 条：G03, G18
```

对上轮「自足轴 11:1 单向漂移、`P≈0.3%` 系统性口径差」这个结论，这是一次重要修正：

- 漂移是**模型对模型**的重复判定差异，只说明边界**不稳**；
- 金标准是**人对表**，自足轴 25/25，说明已判的 `SELF/DEPENDENT` 与人的读法一致；
- 但 25 条里 `DEPENDENT` 只有 3 条（G05/G11/G24），**阳性样本太少**，还撑不起「DEPENDENT 判得准」的结论。

所以结论要改口径：**自足轴不是「判错」，是「边界不稳 + 阳性样本不足」**。原计划的「升 v1.2 统一口径」因此暂缓——先把阳性样本补足，再决定要不要改契约。

## 四、新增：自足轴判例集 C1（20 条）

`CASES_SELF_IDS.txt` 显式冻结条目（一行 `id | 理由`），选取口径两条并集：

| 口径 | 条数 | 说明 |
|---|---|---|
| A 表内 `DEPENDENT` | 13 | 阳性是否成立，逐条要人确认 |
| B 双跑自足轴不一致 | 12 | 边界情形：10 条 REST `SELF→DEP`、`B2-15`、`B3-09` |
| 两口径重复（`B3-09`） | −1 | 既在表内 `DEP`、双跑又判 `SELF`，最有信息量的一条 |
| 去重（金标准已人判） | −4 | `B1-12`(G05)、`B3-13`(G11)、`R5-06`(G24) 人判 `DEP`；`B2-15`(G09) 表判 `SELF`、人判 `SELF`、双跑判 `DEP` |
| **合计** | **20** | 表内 `DEPENDENT` 10 + 边界 10 |

`B2-15` 那一条已经很有价值：双跑把它判成 `DEPENDENT`，人和表都判 `SELF` → **双跑那一侧偏松**，不是表偏严。这削弱了「11:1 说明表偏严」的解读。

新增两条命令（已进一键回归）：

```bash
python tools/audit_prep.py cases           # → CASES_SELF.md（20 条，戳 a4e66877dc）+ CASES_SELF_KEYS.md
python tools/audit_prep.py cases --check   # 复算比对，人填表不纳入 → ✓ 可复现
python tools/audit_prep.py verify-cases    # 人填完再跑：自足轴一致率 + 方向 + DEPENDENT 阳性确认率
```

变异测试（临时填 20 行、故意把 C01 从 `DEP` 改成 `SELF`，跑完复原）：

```
自足轴一致：19/20（95%）
[!] 表判 DEPENDENT、人判 SELF 1 条：C01(B1-08) → 表偏严
表内 DEPENDENT 阳性确认：9/10；未确认：C01→B1-08
EXIT=0
```

方向与阳性确认都对；`cases --check` 在复原后回到 `✓ 可复现`。

## 五、当前状态

```
python tools/check.py        # 9 项（新增 cases --check）
  ✓ verify 全库: 131/131 PASS
  ✓ audit-count --check: 非 SUPPORTED：51/131 = 38.9%
  ✓ audit-count --prefixes S --check: 非 SUPPORTED：0/10 = 0.0%
  ✓ audit-stale --check    ✓ batch --check    ✓ gen_subagents --check（42 个）
  ✓ sample --check（10/80，戳 7d1a204d54）
  ✓ golden --check（25 条，戳 d46f9e7c3f）
  ✓ cases --check（20 条，戳 a4e66877dc）
EXIT=0
```

`verify-sample` 从「预期红」转为**绿**：新样本已被回写、同源、10/10。

## 六、剩余与下一步

| # | 事项 | 谁做 | 状态 |
|---|---|---|---|
| 1 | 131 条判定的结构完整性 | 机械 | ✅ 9/9 绿，131/131 PASS |
| 2 | 80 条 SUPPORTED 的抽检（12.5%） | 子代理 | ✅ 10/10 一致 |
| 3 | 判定表可信度（人开卷 25 条） | 人 | ✅ 支撑 23/25、自足 25/25 |
| 4 | **自足轴阳性确认（20 条）** | 人 | ⬜ 待填 `CASES_SELF.md` |
| 5 | **51 条非 SUPPORTED 人工复核** | 人 | ⬜ 待填 `REVIEW_NONSUPPORTED.md` |
| 6 | 契约 v1.2（自足轴口径） | 主控 | ⏸ 要等 4 的数，避免凭猜测改契约 |

第 4、5 两项是同一张桌子上的活，可以一次坐下做完：20 条判例（只填自足轴）+ 51 条复核（支撑轴）。
做完第 4 项，v1.2 才有依据：若 10 条 `DEPENDENT` 全被确认 → 表没错、双跑偏松，v1.2 只需写「判 `DEPENDENT` 必须写出缺的哪个指代」；若多条被推翻 → 表偏严，需整批重判自足轴。
