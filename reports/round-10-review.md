# round-10：非 SUPPORTED 51 条人工复核收口

> 触发：项目所有者填完 `REVIEW_NONSUPPORTED.md`（42 条 `维持` + 9 条 `待定`），2026-11-10 16:38。
> 9 条 `待定` 全是「需核全文」型——所有者已写明判断规则（「若全文无，删该成分；若有，补引文」），
> 本轮按该规则检索全文（`litrev/_probe/texts/*.txt`，带 `<<<PAGE n>>>` 页标）后补证。
> 结论：**51/51 `维持`，0 改判，0 待定**——非 SUPPORTED 复核收口，判定表一行未动（除 1 处理由措辞更正）。

## 一、汇总

```
python tools/audit_prep.py verify-review
非 SUPPORTED 复核：REVIEW_NONSUPPORTED.md · 条目 51 条
  维持 51
✓ 复核已收口：全部有结论、改判均带处理说明
```

| 项 | 值 |
|---|---|
| 待复核 | 51（PARTIAL 50 / UNSUPPORTED 1） |
| 维持 | **51** |
| 改判 `SUPPORTED` / `UNSUPPORTED` | 0 / 0 |
| 待定 | 0 |
| 判定表改动 | 无（仅 `out_R1.md` 的 `R1-14` 理由措辞更正） |

## 二、9 条 `待定` 的补证结果

全文检索后**全部落回 `维持`**：每条的缺失成分确实不在其引文内。区别只在于「原文别处有没有」——
有则建议补引文（稿件层动作），无则维持缺席。

| id | 所有者的核验问题 | 全文证据（页） | 结论 | 建议动作 |
|---|---|---|---|---|
| `B3-04` | 全文是否给出数据集规模/指标数值 | 11 页全文，评价段仅 “The initial experimental results support the claims”（p.10）；无百分比、无样本量，数字仅页码与参考文献 | 缺席成立 | 保留“未给出” |
| `R1-01` | 是否提「用于描述案例推理方法」 | p.1 只有 “a general framework is defined”；“framework for describing CBR methods” 首见 §3.2 **p.6** | 本页无 | 删该目的，或改引 p.6 |
| `R1-02` | 是否提「已部署应用/评价」 | p.17：General Dynamics、3 人年 “prototype and operational system”、成本降约 10%（$240,000） | 原文有 | 补该段引文 |
| `R1-14` | 是否提「原型/自动」 | **“自动” 就在引文内**（automated structural modeling and mechanical analysis）；全文无 prototype | 只缺“原型” | 删“原型”（原「缺什么」误把“自动”算缺失，已更正） |
| `R1-16` | 是否提「面向建筑设计中的平面图」 | p.1 引言 “Floor plans, as one of the most celebrated media for…” | 原文有 | 补该句 |
| `R2-01` | 是否提「通用方法论」 | p.6 “At the highest level of generality, a general CBR…” | 原文有 | 补该句 |
| `R2-06` | 是否提「每种描述子都是同长数值向量」 | p.2 “These descriptors have the same vector length and shape” | 原文有 | 补该句 |
| `R2-15` | 是否提「工程师设计」 | 引文数值的对比对象是 **successive design**；工程师设计另见 Fig.18(p.12) 与 p.13 “Compared with the engineer's design method” | 原文有，但不是这组数字 | **拆成两组对比**，否则数字归属错 |
| `R4-03` | 是否提「论文定位为」 | p.3 紧邻上句 “This paper considers the role the computer may play in other, less formalized, phases of the structural design” | 原文有 | 补该句 |

## 三、一处判定理由更正（码不变）

`out_R1.md` 的 `R1-14` 原写「没有提到“原型”；请删去“原型”和“自动”这类说法」——**“自动” 是错的**：
引文原文含 `automated structural modeling and mechanical analysis`。已改为只删“原型”，并注明“自动”不删。
判定码 `PARTIAL` 不变（“原型”仍是引文外成分）。

## 四、这个结果说明什么

三条独立证据现在指向同一个判断——**支撑轴判定表没有系统性判错**：

| 证据 | 数字 | 读法 |
|---|---|---|
| 固定契约双跑（131 条配对） | 9.9%（9:4），`P≈13%` | 不显著，方向提示偏松但不足以定性 |
| 人工金标准（25 条） | 23/25（92%） | 可信度高，2 条差异都是人判更严 |
| **逐条人工复核（51 条非 SUPPORTED）** | **51/51 维持** | 无人推翻任何一条判定码 |

对比自足轴：11:1 单向（`P≈0.3%`）+ 判例集 2:2 → 才够格改契约（v1.2 §八）。
支撑轴三条证据方向一致且都不显著 → **不改契约**，剩下的问题在稿件层不在判定层。

## 五、剩下的稿件层动作（不属于审计层）

51 条里 **43 条**无需改稿件（含 `B3-04` 的缺席成立）；**8 条**建议动手：

- 补引文 6 条：`R1-01`(p.6)、`R1-02`(p.17)、`R1-16`(p.1)、`R2-01`(p.6)、`R2-06`(p.2)、`R4-03`(p.3)
- 删/改论断 2 条：`R1-14`（删“原型”）、`R2-15`（拆成「vs 顺序设计」与「vs 工程师设计」两组）

这些是写作动作，改了要重跑 `litrev.py verify` + `audit-stale`，不改判定表。

## 六、复现

```bash
python tools/audit_prep.py verify-review     # 51 条维持，退 0
python tools/check.py                        # 9 项结构自检
grep -n "R1-14" litrev/_probe/audit/out_R1.md # 理由更正后的文本
```

## 七、边界声明

- 9 条 `待定` 的补证由主控执行（检索 `litrev/_probe/texts/*.txt` 全文），**判断规则是所有者预先写定的**
  （「若全文无 → 删该成分；若有 → 补引文」），主控只提供证据与建议动作，未新增判定码。
- `REVIEW_NONSUPPORTED.md` 是待办台账，不进 131 条汇总；它的「维持 51」不等于「51 条有证据支撑」，
  而是「51 条非 SUPPORTED 的判定理由经人核成立」。
- 本轮未改契约、未改判定码、未改 `litrev.py`、未重抽任何参考集。
