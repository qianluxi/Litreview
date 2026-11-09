# round-03 抽检 S1 结果

- 任务：HANDOFF-03 T2（P0）SUPPORTED 抽检 S1。
- 输入：`litrev/_probe/audit/SAMPLE_S1.md`（16 条，seed=42，12.2%，未换种子）。
- 判定：`litrev/_probe/audit/out_S1.md`（16 行 + 合计行）。
- 执行：`auditor-sample-s1`，子会话 `ses_e4099cf14fferFFtcd70FLYICv`。
  - 首次返回 `completed` 但 `<task_result>` 为空、且未写文件；按 RUNBOOK §四用原 `task_id` 恢复，补交成功。
- 输出合计：16 条（SUPPORTED 12 / PARTIAL 4 / UNSUPPORTED 0；DEPENDENT 1）。
- 机械检查：16/16「依据」列都在该条引文中逐字命中；行序 S01–S16；合计行与逐行统计一致。

## 一、抽检结果

| id | 文献 | 字段 | 新判定 | 旧判定 | 一致性 |
|---|---|---|---|---|---|
| S01 | AamodtPlaza1994 | 7. 明确写出的局限 | PARTIAL / DEPENDENT | R2-02 PARTIAL / DEPENDENT | 一致 |
| S02 | Ahmed2013 | 1. 一句话主张 | SUPPORTED / SELF | B1-01 SUPPORTED / SELF | 一致 |
| S03 | Ahmed2013 | 2. 问题域 | SUPPORTED / SELF | B2-01 SUPPORTED / SELF | 一致 |
| S04 | delasHeras2014 | 2. 问题域 | SUPPORTED / SELF | R5-15 SUPPORTED / SELF | 一致 |
| S05 | delasHeras2014 | 3. 表示形式 | SUPPORTED / SELF | R1-15 SUPPORTED / SELF | 一致 |
| S06 | delasHeras2014 | 6. 评价方式 | SUPPORTED / SELF | R3-16 SUPPORTED / SELF | 一致 |
| S07 | Gu2024 | 1. 一句话主张 | SUPPORTED / SELF | R3-02 SUPPORTED / SELF | 一致 |
| S08 | Liao1998 | 1. 一句话主张 | PARTIAL / SELF | B3-05 PARTIAL / SELF | 一致 |
| S09 | MaherGomez1996 | 3. 表示形式 | PARTIAL / SELF | B2-08 PARTIAL / SELF | 一致 |
| S10 | Rodrigues2017 | 1. 一句话主张 | SUPPORTED / SELF | R5-05 SUPPORTED / SELF | 一致 |
| S11 | Rodrigues2017 | 3. 表示形式 | SUPPORTED / SELF | R2-06 PARTIAL / SELF | **不一致** |
| S12 | Rodrigues2017 | 5. 系统形态 | SUPPORTED / SELF | R3-05 PARTIAL / SELF | **不一致** |
| S13 | Roith2017 | 1. 一句话主张 | SUPPORTED / SELF | R1-06 SUPPORTED / SELF | 一致 |
| S14 | Sabri2017 | 2. 问题域 | SUPPORTED / SELF | R3-07 SUPPORTED / SELF | 一致 |
| S15 | vanEngelenburg2023 | 6. 评价方式 | SUPPORTED / SELF | R4-16 PARTIAL / SELF | **不一致** |
| S16 | Zhao2023 | 6. 评价方式 | PARTIAL / SELF | B3-15 SUPPORTED / SELF | **不一致（触发）** |

## 二、命中率与方向

- 严格同判：**12/16 = 75%**。
- 按旧 SUPPORTED 计：旧 SUPPORTED 10 条，新判仍 SUPPORTED 9 条，**命中 9/10 = 90%**。
- **旧 SUPPORTED → 新 PARTIAL：1 条**（S16 / B3-15），即“该判 PARTIAL 却给了 SUPPORTED”的抽检命中，触发整批重审。
- 反向不一致：3 条旧 PARTIAL → 新 SUPPORTED（S11 / R2-06、S12 / R3-05、S15 / R4-16）。这不是触发条件，但说明这批旧 PARTIAL 里至少有 3 条被新审计判得更松，需记录，不能当成“新判更严”一概而论。

## 三、整批重审：frag_b3

- 触发条目 S16 对应 `B3-15`，实际所属批次是 **`frag_b3`**（输入 `FRAG_B3.md`、输出 `out_B3.md`），不是 `rest_b3`。HANDOFF-03 写“对应的 auditor-rest-b*”，与实际批次号不符；按实际条目所属批次重审。
- 执行：`auditor-frag-b3`，子会话 `ses_e409522c5ffepY4tCkvSbQu7H5`。
- `out_B3.md` 已覆盖（RUNBOOK §2.4：重跑批次会覆盖输出，历史靠 git）。

| 项 | 旧 out_B3 | 新 out_B3 |
|---|---:|---:|
| SUPPORTED | 10 | 6 |
| PARTIAL | 6 | 10 |
| UNSUPPORTED | 0 | 0 |
| DEPENDENT | 5 | 7 |

具体变化 5 条：

| id | 旧 | 新 | 说明 |
|---|---|---|---|
| B3-01 | SUPPORTED / SELF | PARTIAL / SELF | 引文止于名词短语，无谓语 |
| B3-10 | SUPPORTED / SELF | SUPPORTED / DEPENDENT | 支撑不变，`These problems` 指代需补 |
| B3-11 | SUPPORTED / SELF | PARTIAL / DEPENDENT | “该文是综述”无引文依据；`these feature` 指代在外 |
| B3-13 | SUPPORTED / SELF | PARTIAL / SELF | “作为验证依据”无依据，`selection` 与“检索结果”需补对应 |
| B3-15 | SUPPORTED / SELF | PARTIAL / SELF | 引文止于 `standard`，`deviation` 与“作为评价指标”系补全；**S16 触发项已确认** |

重审后 131 条最新口径（**数字由 `python litrev/litrev.py audit-count` 重算，不是手加分项**）：

| 集合 | 条数 | SUPPORTED | PARTIAL | UNSUPPORTED | SELF | DEPENDENT |
|---|---:|---:|---:|---:|---:|---:|
| 全量 | 131 | 84 | 46 | 1 | 112 | 19 |

- 非 SUPPORTED：47/131 = 35.9%。
- 与 T2 前（S88 / P42 / U1；SELF114 / D17）相比：`frag_b3` 重审把 4 条旧 SUPPORTED 降为 PARTIAL，新增 2 条 DEPENDENT（B3-10、B3-11）。
- **更正（2026-11-09）**：本节原先写的「83/47/1、SELF115/D16、T2 前 84/45/2」是手算错误。逐文件核对后，`out_*.md` 的实际数字是本表这两行；`audit-count` 已核对每个批次文件自报的「合计」行，8 个全部一致，错的是跨批汇总这一步。

## 四、结论

1. S1 抽检**触发一次整批重审**：`frag_b3`，不是逐条修补。
2. `SUPPORTED` 的抽检命中率为 **9/10 = 90%**；严格同判 12/16 = 75%。这不是“SUPPORTED 全部可信”的证据，只说明这批 SUPPORTED 里至少 1 条已被抽检推翻。
3. 旧 PARTIAL 中有 3 条被新审计判成 SUPPORTED（S11、S12、S15），方向是“新判更松”，不触发重审，但应作为下一轮审计口径复核样本。
4. `out_B3.md` 已覆盖；旧版在 git 历史里。`C4_FRAG_RESULT.md` / `C4_REST_RESULT.md` 的旧汇总不再是最新口径，最新以本报告第三节为准。
