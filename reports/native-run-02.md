# OpenCode 第二轮（C4 补齐）运行报告

- 日期：2026-11-09
- 范围：`HANDOFF-02.md` T1–T4；T5（permission 硬隔离）因需重启 OpenCode，本轮未改配置、未验收。
- 执行：主控 `orchestrator` 派发；`auditor` 判 C4，`extractor` 扩句，主控跑 `verify`。
- 结论：**48 条片段已审完（S28 / P19 / U1；D13），7 条 S+D 已扩句并通过 verify；剩余 83 条支撑轴已审完（S60 / P23 / U0；D4）。131 条全量口径：S88 / P42 / U1（非 SUPPORTED 43 条 = 32.8%），扩句前 D17。**

## 1. T1：48 条片段审计（同一条消息 3 个 task）

| 批次 | 文件 | 条数 | 支撑 | 自足 | 子会话 |
|---|---|---:|---|---|---|
| B1 | `FRAG_B1.md` | 16 | S8 / P7 / U1 | S15 / D1 | `ses_e410ab205ffeOCHyRo3WApZ0F5` |
| B2 | `FRAG_B2.md` | 16 | S10 / P6 / U0 | S9 / D7 | `ses_e410ab0eeffeXhoyPf8d0420wE` |
| B3 | `FRAG_B3.md` | 16 | S10 / P6 / U0 | S11 / D5 | `ses_e410aaff1ffeuOtxU3BirJFWLP` |
| **合计** | — | **48** | **S28 / P19 / U1** | **S35 / D13** | — |

- 三条 `task` 在同一条 assistant 消息内发出，起跑时间 14:18:29.766 / 14:18:30.044 / 14:18:30.313，极差 0.547s。
- B1 首次 `result` 为空；恢复同一会话后补交 16 行，未新建第二个会话。B2/B3 首次即完整。
- 机械复核：48/48 行序与批次文件一致；48/48「依据」列在该条引文中逐字命中；三份合计行与逐行统计一致。
- 原始表：`litrev/_probe/audit/out_B1.md`、`out_B2.md`、`out_B3.md`。
- 汇总：`litrev/_probe/audit/C4_FRAG_RESULT.md`。

## 2. T2：待改清单

- 总判定：48 条（S28 / P19 / U1；SELF35 / DEPENDENT13）。
- 支撑轴待改 20 条（19 PARTIAL + 1 UNSUPPORTED），只列不改，交人。
- 自足轴可自动处理 7 条（SUPPORTED + DEPENDENT），进入 T3。
- 与 v1 对照：上一轮 run1 12 条 = S7 / P5 / U0；`run_C_v1.md` 原始变异集 8 条 = S2 / P4 / U2，变异检出 5/5（无注入变异被放行为 SUPPORTED）。
- 注意：48 条是按形式判据挑出的片段，不是随机样本；41.7% 的非 SUPPORTED 不能直接外推到 131 条。

## 3. T3：7 条 S+D 扩句

对象：B2-01、B2-05、B2-08、B2-09、B3-02、B3-03、B3-16。

- 5 个 `extractor` 同一条消息并列，按篇分组（Ahmed、Gu、MaherGomez1996、Borner、vanEngelenburg），避免同一 md 被两个会话同时改；7 条全部覆盖。
- 输入走 `_probe/texts/*.txt`，不读 PDF（HANDOFF-02 §一.1 的纠正）。
- 只改指定「引文」行；论断、页码、其他条目未动。
- 主控重跑 `verify`：5 个文件各 7/7 PASS，退出码全 0；合计 35/35 PASS，无 PAGE / PARAPHRASE / MISSING。
- T3 后全量复核：19 篇 131/131 PASS，退出码全 0，确认没有误改其他 14 篇。
- 扩句前后对照：`litrev/_probe/audit/C4_EXPAND_RESULT.md`。
- 例外：MaherGomez1996 p.6（B2-08）原句跨 p.5–p.6，新引文以 p.6 页首 `and` 起首，但主语 `the primary object-based representation` 已入引号；未跨页拼接，未按「拆两条」处理。`verify` PASS，建议人工复核是否接受该起首。

## 4. T4：剩余 83 条支撑轴审计（5 批同一条消息）

| 批次 | 文件 | 条数 | 支撑 | 自足 | 子会话 |
|---|---|---:|---|---|---|
| B1 | `REST_B1.md` | 16 | S10 / P6 / U0 | S16 / D0 | `ses_e4100460dffekawPp6sMmJWuIP` |
| B2 | `REST_B2.md` | 17 | S13 / P4 / U0 | S15 / D2 | `ses_e410044deffeaNTH6EbC7l6Uze` |
| B3 | `REST_B3.md` | 17 | S11 / P6 / U0 | S16 / D1 | `ses_e410043f0ffe9jZNHcSEWBUX2z` |
| B4 | `REST_B4.md` | 16 | S12 / P4 / U0 | S16 / D0 | `ses_e41004326ffefMjs8J0mrJ05gv` |
| B5 | `REST_B5.md` | 17 | S14 / P3 / U0 | S16 / D1 | `ses_e41004245ffei11FdzVUZwDPzd` |
| **合计** | — | **83** | **S60 / P23 / U0** | **S79 / D4** | — |

- 5 条 `task` 同一条消息内发出，起跑时间 14:29:52.764–14:29:53.730，极差 0.966s。
- B3、B5 首次 `result` 为空；均恢复同一会话补交 17 行。B1/B2/B4 首次即完整。
- 机械复核：83/83 行序一致；83/83「依据」在该条引文中逐字命中；五份合计行与逐行统计一致。
- R4-05 首次依据写成 `72 floor plans`，与原文连字 `72 ﬂoor plans` 不逐字；已由同一会话改为 `72 ﬂoor plans` 后复检通过。
- 原始表：`out_R1.md`–`out_R5.md`；汇总：`C4_REST_RESULT.md`。

## 5. 131 条全量口径（T3 扩句前）

| 集合 | 条数 | S | P | U | SELF | DEPENDENT |
|---|---:|---:|---:|---:|---:|---:|
| 48 条片段（T1） | 48 | 28 | 19 | 1 | 35 | 13 |
| 83 条非片段（T4） | 83 | 60 | 23 | 0 | 79 | 4 |
| **合计** | **131** | **88** | **42** | **1** | **114** | **17** |

- 非 SUPPORTED：43/131 = 32.8%（42 PARTIAL + 1 UNSUPPORTED）。
- 自足：17/131 = 13.0%（T3 扩句前）。
- T3 已把其中 7 条 S+D 扩到含主语；支撑轴不变。若 7 条全部转 SELF，DEPENDENT 期望降到 10；本轮未对扩句后的 7 条重跑 auditor，故不把 10 写成实测值。

## 6. 产物清单

```
litrev/_probe/audit/FRAG_B1.md / FRAG_B2.md / FRAG_B3.md     T1 批次输入
litrev/_probe/audit/out_B1.md  / out_B2.md  / out_B3.md      T1 原始判定表
litrev/_probe/audit/C4_FRAG_RESULT.md                        T2 汇总与待改清单
litrev/_probe/audit/C4_EXPAND_RESULT.md                      T3 扩句对照与 verify
litrev/_probe/audit/REST_B1.md–REST_B5.md                    T4 批次输入
litrev/_probe/audit/out_R1.md–out_R5.md                      T4 原始判定表
litrev/_probe/audit/C4_REST_RESULT.md                        T4 汇总与 131 合并口径
reports/native-run-02.md                                     本报告
```

## 7. T5：未执行，等待重启

T5 需要改 `.opencode/agents/extractor.md` 与 `auditor.md` 的 `permission` 块并重启 OpenCode；当前会话内改了也不会生效，无法执行「主动越界拿到拒绝原文」的验收。因此本轮**没有改配置**，避免留下未验证的 permission 变更。

建议在重启后执行：

```yaml
# extractor.md
permission:
  read:
    "*": allow
    "litrev/litrev.py": deny
    "litrev/_index/*": deny
    "litrev/_probe/full/*": deny
    "litrev/_probe/notes/*": deny
  edit:
    "*": deny
    "litrev/_probe/full/*": allow

# auditor.md
permission:
  read:
    "*": deny
    "litrev/_probe/audit/*": allow
```

验收：让 extractor 主动读一次 `litrev/litrev.py`，必须拿到 `The user has specified a rule...` 的拒绝原文；再确认它仍能读 txt、仍能写自己的 md。

## 8. 下一步

1. 处理 T2/T4 的 43 条非 SUPPORTED（42 PARTIAL + 1 UNSUPPORTED）：只列不改，交人决定改论断还是换引文。
2. 对 T3 扩句后的 7 条补一次自足轴复判（预期转 SELF，但未实测）。
3. 人工复核 MaherGomez1996 p.6 的 `and` 起首是否接受。
4. 重启后做 T5，并保留拒绝原文作为验收证据。

## 9. 取证信息

- 本轮根会话：`ses_e41ee0cd9ffeLqhSEHBEqd6jnu`（directory `F:/project/PyProject/Litreview`）。
- T1 三条子会话见 §1；T3 五条见 `C4_EXPAND_RESULT.md` §五；T4 五条见 §4。
- 时间戳取自 `~/.local/share/opencode/opencode.db` 的 `part` 表（`mode=ro`），未改库。

---

> **第三方核验：`reports/native-run-02-verification.md`（2026-11-09 14:55）。**
> 机械指标全部复现（131/131 判定自洽、131/131 依据可回溯、批次切分无重复、7 条扩句逐字命中标注页、0 越界）。
> 三处需要修正的表述：① 3/8 次审计派发返回 `state=completed` 但 `<task_result>` 为空，补派带 `task_id` 才拿到结果，工具层不报错；
> ② 48 条片段里 14 条（Borner1993 7 + Zhang2006 7）的根源是 PDF 文字层逐词换行（1.03 / 2.93 词/行），扩句无效，须换抽取方式；
> ③ 88 条 SUPPORTED 抽检 6 条有 3 条偏宽，不能当「已通过」。
