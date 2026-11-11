# HANDOFF-16 · 合并派发：`FIX_B5`（B3-04 收口）+ `PROBE_R6-04`（D-03 第三次判定）

> 2026-11-11 · 承接 `HANDOFF-15` / `reports/round-25-rest-b6.md` / `DISPUTED.md` D-03
> 你选了「都做」：① `B3-04` 按选 A 删半句 → 定点重判 → 口径清零；② `R6-04` 做第三次独立判定，
> 把 1:1 变成多数票。两件事各需一个新 agent，**合并到一次重启**。
> 本轮**只派发**，验收与 `reseal` 由我做完后再报你。

---

## 一、已落盘（不要再改）

| 项 | 值 |
|---|---|
| 卡片改动 | `full/Borner1993_StructuralSimilarity_CBR.md` §6 论断：删「，未给出数据集规模或指标数值」，**引文一字未动**。改后：`评价方式是报告初期实验结果对上述主张的支持。` |
| 批次输入 | `litrev/_probe/audit/FRAG_B3.md` 已 `batch --only B3` 刷新，**戳 `18c979470b → e58bc1a19f`**（与 round-23 预演值逐字相同），变动 **1/16** 条（`REST_B3.md` 无变化） |
| 定点批次 | `FIX_B5.md`（1 条 `B3-04`，改后论断 + 原引文），戳 **`3106b1c52a`**（`_payload_stamp` 自算，头部与内容已互验） |
| 单条复核 | `PROBE_R6-04.md`（1 条 `R6-04`，论断/引文与 `REST_B6.md` 逐字同源），戳 **`03897de76d`** |
| 注册 | `BATCHES.json` 新增 `fix_b5`（→ `out_FIX_5.md`）、`probe_r6_04`（→ `out_P_6.md`），批次 23 → 25 |
| 新审计员 | `.opencode/agents/auditor-fix-b5.md`、`.opencode/agents/auditor-probe-r6-04.md`（生成于 **14:49**；各只读「契约 + 本批输入 + 本批输出」、只写本批输出、`bash` 全 deny） |
| 生成器 | 已重跑：agent **47 → 49**，`gen --check` 49/49 绿 |
| 第二道门槛 | **已提前证完**：`reseal` 变更集 = `['B3-04']`，`FIX_B5` 恰好覆盖，无新增无删除 |

**文件命名的两个坑（已避开，别改）**：`out_P6.md` 会被 `audit-count` 的 `^out_[A-Z]+\d+\.md$` 命中、污染 138 口径，
所以写 `out_P_6.md`；`out_FIX_5.md` 带下划线，同理不进汇总。

**没有动**：`AUDIT_CONTRACT.md`、`AGENT_ROLES.md`、`out_B3.md`、`out_R6.md`、任何既有卡片、
三个参考集、判定表口径（仍 `S137/P1/U0`）。

---

## 二、派发前：重启 OpenCode

新 agent 只在客户端启动时进注册表。**重启时间必须晚于 14:49**（两个 agent 的生成时间），否则 `Unknown agent type`。

重启后跑 `python tools/check.py`，预期 **7 绿 / 4 红**：

| 红项 | 实际输出 | 为什么 |
|---|---|---|
| `audit-stale --check` | `B3：16 条待重审 · 口径已变 18c979470b→e58bc1a19f（未重审）` | 卡片改了、批次已刷新，`out_B3.md` 还是旧戳 |
| `sample --check` | `这些条目的输入戳与判定戳不一致…['B3-01'…]` | `audit_prep.load()` 的戳一致性门禁（**不是** HANDOFF-15 那种「id 不齐」） |
| `golden --check` | 同上 | 同上 |
| `cases --check` | 同上 | 同上 |

**放行条件**：除这 4 项外其余 7 项全绿，且红项文字与上表一致。
注意与上一轮的差别——上轮红因是「id 不齐」，本轮是「**戳不一致**」，因为 `B3` 的 16 条 id 都还在，只是输入文字变了。
任何别的红项、或 `audit-count` 不再是 `137/1/0` → 先别派，告诉我。

**绝对不要**为消红去手工改 `out_B3.md` 的戳、补建 `out_FIX_5.md` / `out_P_6.md` 占位、重抽参考集。
这 4 项会在 `reseal` 后**自动**变绿。

---

## 三、派发词（两个都派，顺序不限）

第一次（定点重判）：

```
按 HANDOFF-16.md 做定点重判，用 auditor-fix-b5 这个子代理。
```

第二次（单条复核）：

```
按 HANDOFF-16.md 做单条复核，用 auditor-probe-r6-04 这个子代理。
```

两个互不依赖，可以连着派，也可以先派一个看回报再派另一个。

---

## 四、回报只要两行

```
已写入 out_FIX_5.md：N 行 ｜ task id ｜ 拒绝次数
已写入 out_P_6.md：N 行 ｜ task id ｜ 拒绝次数
```

预期各 1 行判定（不是 7 行）。

---

## 五、我回来的验收路径

**`fix_b5`（走 reseal，改判定表）**
1. 戳 = `3106b1c52a`（与 `FIX_B5.md` 同源）、表头与 `FIX_B5.md` 逐字一致、行序 `B3-04`、合计齐。
2. 依据词逐字连续命中该条引文且 ≤15 字。
3. `reseal --fix-input FIX_B5.md --fix-out out_FIX_5.md` → 重封 `out_B3.md` 为 `e58bc1a19f`，`RESEAL.md` 追加台账。
4. `audit-count` → `B3` 变 `S16/P0/U0`，总口径 **`S138/P0/U0`**（非 SUPPORTED 从 1 降到 0）。
5. `check.py` 回到 **11/11 绿**（三参考集随戳自愈，分母仍 `15/12/10`）。

**`probe_r6_04`（只裁决 D-03，不动判定表）**
1. 戳 = `03897de76d`、1 行、依据逐字命中。
2. 与 `out_R6.md` 的 `R6-04`（`SUPPORTED`）、我的开卷裁决（`PARTIAL`）三方比对，形成 2:1。
3. **重要偏差要写进裁决**：`auditor` 角色模板末尾有一句「拿不准时给更严的那一档」，
   这对本次盲判是**偏向 `PARTIAL`** 的指令偏差。因此即便第 3 次判 `PARTIAL` 构成 2:1，
   也不能把它当成「契约判据支持 `PARTIAL`」的纯证据——要在 `D-03` 里标明这一层。
4. `out_P_6.md` 不进 `audit-count`、不进 `BATCHES` 汇总，`check.py` 不受影响。

---

## 六、不要做

- 不要因为 `B3` 16 条都报「戳不一致」就去整批重审：`reseal` 才是出口，且只改 1 条。
- 不要动 `out_R6.md`（已封戳 `7cb35452e0`，`D-03` 的证据就是它）。
- 不要重抽三个参考集，也不要手改人开的卷。
- 不要把 `out_FIX_5.md` 改名成 `out_FIX5.md`，也不要把 `out_P_6.md` 改成 `out_P6.md`。
