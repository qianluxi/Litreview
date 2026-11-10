# round-12：8 条改稿的定点重判回写（`reseal` 首次实际使用）

> 触发：round-10 复核结论给出的稿件层动作（6 条补引文 + 2 条删改论断）已由主控代改完成，
> 定点批次 `FIX_B1.md`（8 条，戳 `3961e704f7`）派出 `auditor-fix-b1`，
> 2026-11-10 17:5x 会话 `ses_e3b217740ffeEBpwrIAIq3WRdG` 返回 completed，`out_FIX.md` 整份写入。
> 结论：`reseal` 三条门槛全过并落表，`check.py` **9/9 全绿**，口径 `S80/P50/U1 → S87/P43/U1`。

## 一、派发与输出核验

| 项 | 值 |
|---|---|
| task id | `ses_e3b217740ffeEBpwrIAIq3WRdG`（completed） |
| 输出 | `litrev/_probe/audit/out_FIX.md`，14 行，整份重写（旧戳 `2300ca676f` 残留 0 处） |
| 首行戳 | `> 快照 sha1: 3961e704f7`，与 `FIX_B1.md` 第 10 行逐字一致 |
| 判定行 | 8 条，顺序 `R1-01 R1-02 R1-14 R1-16 R2-01 R2-06 R2-15 R4-03` |
| 合计行 | 8 条（SUPPORTED 7 / PARTIAL 1 / UNSUPPORTED 0；DEPENDENT 0） |
| 权限拒绝 | 0 次 |
| 改动范围 | 只有未跟踪新文件 `out_FIX.md`，无其它文件变更 |

「依据列是否为连续截取」由派发方另做子串比对（只核格式，不判支撑）：

```
R1-01 "general framework"  R1-02 "were handled"   R1-14 "AIStructure"
R1-16 "one of the most"    R2-01 "no universal CBR"  R2-06 "did not affect"
R2-15 "0.625 and 0.548"    R4-03 "four expert systems"      → 全部连续命中
```

上一轮被 `reseal` 拒掉的 `AIStructure API`（跨词拼接）已改为连续片段 `AIStructure`。

**关于「≤15 字」**：3 条依据按字符数超 15（17/16/19），但 `FIX_B1.md` 自己给的示例
`application programming interface` 是 33 字符 —— 可见该上限不是按字符计的。
机械门禁（`reseal` 门槛 3）只查"逐字连续命中"，从不数字符；措辞已在 `RUNBOOK.md` §三附之二注明为软约束，
按"短到能一眼定位、不跨词拼接"执行，判据不留歧义但也不假装有硬阈值。

## 二、`reseal` 执行

```bash
python litrev/litrev.py reseal --check     # 先干跑
R1   可重封 4 条（R1-01, R1-02, R1-14, R1-16）→ 4b2ce8c0a4
R2   可重封 3 条（R2-01, R2-06, R2-15）→ 1c518a453b
R4   可重封 1 条（R4-03）→ 3740f34619

python litrev/litrev.py reseal             # 落盘
R1   重封 4 行 → 戳 4b2ce8c0a4（原 4dff615）
R2   重封 3 行 → 戳 1c518a453b（原 6877968）
R4   重封 1 行 → 戳 3740f34619（原 531e480）
台账已追加：litrev/_probe/audit/RESEAL.md
```

三条门槛全部满足：①定点输出戳与输入戳同源；②原批次变动条目全部有新判定（8/8，无漏判）；
③依据逐字连续命中新引文（8/8）。

`stamp-out` 在改稿后拒绝补戳是本项目的**护栏**，本次没有绕它，走的是 `reseal` 正路。

## 三、口径变化

| | SUPPORTED | PARTIAL | UNSUPPORTED | 非 SUPPORTED |
|---|---|---|---|---|
| before（round-10） | 80 | 50 | 1 | 51 / 131 = 38.9% |
| after（round-12） | **87** | **43** | 1 | **44 / 131 = 33.6%** |
| Δ | +7 | −7 | 0 | −7 |

自足轴未动：`SELF 118 / DEPENDENT 13`。

`python litrev/litrev.py audit-count`：

```
合计        131    87    43     1   118    13
口径：131 条 · SUPPORTED 87 / PARTIAL 43 / UNSUPPORTED 1 · SELF 118 / DEPENDENT 13
非 SUPPORTED：44/131 = 33.6%
```

`audit-stale`：131/131 依据与卡片当前内容一致。

## 四、参考集受影响情况（机械核对）

| 参考集 | 与 8 条重叠 | 处理 |
|---|---|---|
| `SAMPLE_S1_KEYS.md`（10 条） | 无 | 不变；`verify-sample` 10/10、戳 `7d1a204d54` 仍自洽 |
| `GOLDEN_MAP.md`（25 条） | **`R1-16`、`R2-01`** | 人判基于旧文 → 判后返工，从分母剔除（25→**23**） |
| `CASES_SELF_KEYS.md`（20 条） | 无 | 不变；`verify-cases` 16/20、复算 20/20 |
| `REVIEW_NONSUPPORTED.md`（51 条） | 8 条中 7 条转 SUPPORTED | 台账**不改**（历史记录）；覆盖门禁证明当前 44 条全部登记 |

`python tools/audit_prep.py verify-golden`：

```
[!] 判后返工失效 2 条（人判基于旧文，已从分母剔除）：G13(R1-16), G14(R2-01)
支撑轴一致：21/23（91%）   自足轴一致：23/23（100%）   双轴都一致：21/23（91%）
[!] 人判更严（原 S → 人非 S）2 条：G03, G18 → 疑似原表偏松
```

即：剔除的两条原本是**一致**的，所以 23/25（92%）→ 21/23（91%），一致率几乎不动。
这是"判后返工"条款第一次真实生效，不是新差异。

## 五、本轮新增的机械门禁

`verify-review` 之前只统计台账内部（填写率 / 维持 / 改判），**不证明"该登记的都没漏"**——
新出现一个 PARTIAL 而没重新生成台账时，统计照样全绿。本轮加了覆盖门禁：

```
覆盖：当前非 SUPPORTED 44 条，台账已登记 44 条
[i] 台账另有 7 条已转为 SUPPORTED（历史记录，保留不改）：R1-01, R1-02, R1-14, R1-16, R2-01, R2-06, R4-03
✓ 复核已收口
```

变异验证（把台账截到前 10 条）：报「台账漏登 34 条」并退 1 —— 门禁确实会红，不是死代码。

## 六、残留（1 条，未收口，已知且不掩盖）

`R2-15` 仍为 `PARTIAL`。改稿已按复核建议拆成两组数值对比，但论断里的**「交并比」括注**在引文里没有对应表述
（引文只给 `SIoU` / `BIoU` 两个缩写与数值，未展开定义）。判定 `PARTIAL` 是诚实的，不是失败。

两条出口：

1. 删掉「交并比」括注 → 论断与引文完全对齐，可转 `SUPPORTED`（+1）；
2. 在全文别处补 SIoU/BIoU 的定义引文 → 也可转 `SUPPORTED`。

本轮**没有做**，理由是：删一个词就要再走一轮派发 + `reseal` + 重新封戳，收益 1 条，
且当前卡片已如实标注、不存在失真。留作下一轮的 P2，与其它稿件层动作合并处理，不为凑数单独开一轮。

## 七、回归

```
python tools/check.py
  ✓ verify 全库: 131/131 PASS
  ✓ audit-count --check: 非 SUPPORTED：44/131 = 33.6%
  ✓ audit-count --prefixes S --check: 非 SUPPORTED：0/10 = 0.0%
  ✓ audit-stale --check: ✓ 全部判定的依据与卡片当前内容一致。
  ✓ batch --check: 合计待刷新 0/131 条（--check 不写盘）
  ✓ gen_subagents --check: ✓ 同步：43 个文件与 AGENT_ROLES.md 一致
  ✓ audit_prep sample --check: ✓ 10/80 条，戳 7d1a204d54；3 个批次在抽样后重封（按抽样时点口径复现）
  ✓ audit_prep golden --check: ✓ 25 条（S15/P9/U1），戳 d46f9e7c3f
  ✓ audit_prep cases --check: 4 条在原判之后被裁决修改，仍按清单复现
✓ 全部机械自检通过。
```

`sample --check` 报告「3 个批次在抽样后重封」是**预期输出**：`reseal` 改了 `REST_B1/B2/B4` 的戳，
而抽检答案键冻结的是抽样时点口径（`key_stamps`），所以按历史戳复现、不误判为不一致。
这正是把冻结做到"元信息层"的收益——若只冻条目清单，这里会直接变红。
