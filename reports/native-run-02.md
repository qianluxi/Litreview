# OpenCode 第二轮（C4 补齐）运行报告

- 日期：2026-11-09
- 范围：`HANDOFF-02.md` T1–T5；T5（permission 硬隔离）已通过第四次冒烟验收。
- 执行：主控 `orchestrator` 派发；`auditor` 判 C4，`extractor` 扩句，主控跑 `verify`。
- 结论：**48 条片段已审完（S28 / P19 / U1；D13），7 条 S+D 已扩句并通过 verify；剩余 83 条支撑轴已审完（S60 / P23 / U0；D4）。131 条全量口径：S88 / P42 / U1（非 SUPPORTED 43 条 = 32.8%），扩句前 D17。**（核验后最终值见 §0.4：S84 / P45 / U2；SELF118 / D13。）

## 0. 核验后修订（2026-11-09 14:55）

第三方核验报告 `native-run-02` 复核后，以下四处需要按修订后的口径读：

1. **空返回不是 1 次，是 3/8 次审计派发**：T1 B1、T4 B3、T4 B5 都返回 `state=completed` 但 `<task_result>` 为空；三次都带 `task_id` 恢复同一会话补交。**Runbook：任何 `task` 返回先检查 `<task_result>` 是否为空，空则带 `task_id` 重派**；不要把 `completed` 当成功。
2. **48 条片段里 14 条的根源在 PDF 文字层**：Borner1993 7 条 + Zhang2006 7 条；Borner 文字层 1.03 词/行、短行 99.6%，扩句只会把碎串变长。诊断见 `litrev/_probe/audit/CORPUS_TEXT_HEALTH.md`。这 14 条不能算“已处理”，需重新抽取或按页面视觉抄录。
3. **T3 返工结果**：B2-01、B2-05 已修到 `SUPPORTED / SELF`；B2-08 修到 `PARTIAL / SELF`（支撑变弱，需人决定改论断还是换引文）；B3-03 因 Borner 文字层问题阻塞。仅返工后的中间值是 S87 / P43 / U1、SELF120 / D11；并入下一条抽检复核后的最终值见第 4 条。详见 `C4_EXPAND_RESULT.md` §六、`C4_REST_RESULT.md` §七。
4. **88 条 SUPPORTED 不能当合格证**：第三方抽检 6 条，B3-10、B3-11、B3-13 被判偏宽。随后用 1 个 auditor 闭卷复核这 3 条：B3-10 → `PARTIAL / DEPENDENT`，B3-11 → `PARTIAL / DEPENDENT`，B3-13 → `UNSUPPORTED / SELF`。并入后 131 条为 **S84 / P45 / U2；SELF118 / D13**（非 SUPPORTED 47/131 = 35.9%）。原始表：`litrev/_probe/audit/out_SAMPLE3.md`。`AUDIT_CONTRACT.md` 已加 v1.1 补充（指示代词作限定词也算 DEPENDENT；SUPPORTED 只用于分诊，仍需 10%–15% 抽检）。

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
- 例外：MaherGomez1996 p.6（B2-08）原句跨 p.5–p.6，新引文以 p.6 页首 `and` 起首，但主语 `the primary object-based representation` 已入引号；`verify` PASS，建议人工复核是否接受该起首。**核验后已返工为完整句，判定 `PARTIAL / SELF`，见 §0.3。**

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

## 5. 131 条全量口径（T3 扩句前；最终值见 §0.4）

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
litrev/_probe/audit/CORPUS_TEXT_HEALTH.md                     Borner/Zhang 文字层诊断
litrev/_probe/audit/out_REWORK3.md                            3 条返工复核定表
litrev/_probe/audit/out_SAMPLE3.md                            3 条 SUPPORTED 抽检定表
reports/native-run-02.md                                     本报告
```

## 7. T5：read/edit/bash/grep/glob 全部受控，验收通过

### 7.1 已写入配置

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
  bash:
    "*": deny
  grep:
    "*": deny
  glob:
    "*": deny

# auditor.md
permission:
  read:
    "*": deny
    "litrev/_probe/AUDIT_CONTRACT.md": allow
    "litrev/_probe/audit/*": allow
  edit:
    "*": deny
  bash:
    "*": deny
  grep:
    "*": deny
  glob:
    "*": deny
```

- 比 HANDOFF 原建议多放行 `litrev/_probe/AUDIT_CONTRACT.md`，否则 auditor 连判定契约都读不到。
- `bash: "*": deny` 是第二次冒烟后补的：auditor 没有 `write/edit` 工具，但可以用 bash 写文件，绕过了 `edit` deny。

### 7.2 第二次冒烟：read/edit 已生效

| 测试 | 期望 | 实测 |
|---|---|---|
| extractor 读 `litrev/litrev.py` | 拒绝 | **拒绝**（`The user has specified a rule...`） |
| extractor 读 `_probe/notes/Napps2021...md` | 拒绝 | **拒绝** |
| extractor 读 `_probe/texts/Napps2021...txt` | 允许 | 允许 |
| extractor 写 `_probe/full/_permission_smoke_extractor.md` | 允许 | 允许（已清理） |
| auditor 读 `AUDIT_CONTRACT.md` | 允许 | 允许 |
| auditor 读 `_probe/audit/FRAG_B1.md` | 允许 | 允许 |
| auditor 读 `_probe/full/Ahmed2013...md` | 拒绝 | **拒绝** |
| auditor 写 `_probe/audit/_permission_smoke_auditor.md` | 拒绝 | **允许（bash 旁路）**，已清理 |

结论：`read` / `edit` 规则已生效，`auditor` 的 `read: "*": deny` 也没有导致 read 工具不注册；但 `bash` 未受管，auditor 用 `Set-Content` 成功写入了本应禁止的目录。extractor 的 bash 同样可能绕过 `read` deny，因此两边都加 `bash: "*": deny`。

### 7.3 第三次冒烟：read/edit/bash 已生效，grep/glob 是新的旁路

| 测试 | 期望 | 实测 |
|---|---|---|
| extractor 读 `litrev/litrev.py` | 拒绝 | **拒绝**（拒绝原文） |
| extractor 读 `_probe/notes/Napps2021...md` | 拒绝 | **拒绝** |
| extractor 读 `_probe/texts/Napps2021...txt` | 允许 | 允许 |
| extractor 写 `_probe/full/_permission_smoke_extractor.md` | 允许 | 允许（已清理） |
| extractor 用 bash 读 `litrev/litrev.py` | 拒绝/不可用 | **bash 工具不可用**（未读到内容） |
| auditor 读 `AUDIT_CONTRACT.md` | 允许 | 允许 |
| auditor 读 `_probe/audit/FRAG_B1.md` | 允许 | 允许 |
| auditor 读 `_probe/full/Ahmed2013...md` | 拒绝 | **拒绝** |
| auditor 用 bash 写 `_probe/audit/...` | 拒绝/不可用 | **bash 工具不可用**（未创建） |

追加测试发现 `grep` / `glob` 不受 `read` 规则约束：

| 测试 | 实测 |
|---|---|
| auditor `grep` `_probe/full/MaherGomez1996...md` | **允许**（命中 2 处） |
| auditor `glob` `_probe/full/*.md` | **允许**（返回 39 个文件名） |
| auditor `grep` `litrev/litrev.py` | **允许**（命中 `def norm_text`） |
| extractor `grep` `litrev/litrev.py` | **允许**（命中 `def norm_text`） |
| extractor `glob` `_probe/notes/*.md` | **允许**（返回 12 个文件名） |
| extractor `grep` `_probe/texts/Napps2021...txt` | **允许**（应允许） |

结论：`bash` 已经关闭，但 `grep` / `glob` 能直接绕过 `read` 隔离，读取 `litrev.py`、`full/*`、`notes/*`。已在两个 agent 加 `grep` / `glob` 规则：extractor 只放行 `_probe/texts/*`，auditor 全禁。

### 7.4 第四次冒烟：T5 通过

| 测试 | 期望 | 实测 |
|---|---|---|
| extractor 读 `litrev/litrev.py` | 拒绝 | **拒绝**（`The user has specified a rule...`） |
| extractor 读 `_probe/notes/Napps2021...md` | 拒绝 | **拒绝** |
| extractor 读 `_probe/texts/Napps2021...txt` | 允许 | 允许 |
| extractor 写 `_probe/full/_permission_smoke_extractor.md` | 允许 | 允许（已清理） |
| extractor `grep` `litrev/litrev.py` | 拒绝 | **拒绝** |
| extractor `glob` `_probe/notes/*.md` | 拒绝 | **拒绝** |
| auditor 读 `AUDIT_CONTRACT.md` | 允许 | 允许 |
| auditor 读 `_probe/audit/FRAG_B1.md` | 允许 | 允许 |
| auditor 读 `_probe/full/Ahmed2013...md` | 拒绝 | **拒绝** |
| auditor `grep` `_probe/full/*` | 拒绝/不可用 | **grep 工具不可用** |
| auditor `glob` `_probe/full/*.md` | 拒绝/不可用 | **glob 工具不可用** |
| auditor 用 bash 写 `_probe/audit/...` | 拒绝/不可用 | **bash 工具不可用**（未创建） |

结论：**T5 通过**。extractor 的越界 read/grep/glob 都被拒绝；auditor 只能读 `AUDIT_CONTRACT.md` 与 `_probe/audit/*`，没有 grep/glob/bash 写入通道。

已知功能代价：extractor 的 `grep` / `glob` 被全禁（连 `_probe/texts/*` 也被拒），因为 `grep: "*": deny` 与路径级 allow 的组合没有按预期放行。后续抽取若需要搜索长 txt，只能靠 `read` 分段读；或在路径级规则验证通过后单独放行 `texts/*`。不要为了省事重新放开未验证的 grep/glob。

通过标准：越界 call 必须拿到 `The user has specified a rule...` 的拒绝原文，或工具直接不可用；不是“看起来没报错”。

## 8. 下一步

1. 处理返工 + 抽检后的 47 条非 SUPPORTED（45 PARTIAL + 2 UNSUPPORTED）：只列不改，交人决定改论断还是换引文。
2. **优先修语料层**：Borner1993、Zhang2006 的 14 条片段不能用扩句解决；改用 `get_text("blocks")` 版面重建或按页面视觉抄录，重抽后重跑 `verify`。在处理前，这 14 条只记为“已知有问题”。
3. 人工复核 B2-08 的 `PARTIAL / SELF`：新引文自足但支撑变弱，需决定改论断还是换回/换句。
4. 对 84 条 SUPPORTED 按 10%–15% 抽检；第三方已点名 B3-10、B3-11、B3-13 三条偏宽，已复核为 PARTIAL/PARTIAL/UNSUPPORTED，仍需继续抽样。
5. **T5 已通过**（第四次冒烟）。已知功能代价：extractor 的 `grep` / `glob` 被全禁，连 `_probe/texts/*` 也不能用；后续抽取改靠 `read` 分段读。若要恢复 text 搜索，先验证路径级 allow 规则，再单独放行，不要直接放开全量 grep/glob。
6. 把“`task` 返回空 `<task_result>` 就带 `task_id` 重派”写进 runbook，不要把 `completed` 当成功。

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
