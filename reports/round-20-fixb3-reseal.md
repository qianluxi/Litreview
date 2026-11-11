# round-20 · FIX_B3 派发回收与 reseal 收口（2026-11-11）

## 一、结论

派发 `auditor-fix-b3` 一次完成（真 task，权限拒绝 0），13 条定点重判中 11 条转 `SUPPORTED`、2 条仍 `PARTIAL`；
`reseal` 三门槛全过、重封 4 个批次，`check.py` **11/11 绿**。

```
131 条 · SUPPORTED 128 / PARTIAL 3 / UNSUPPORTED 0 · SELF 118 / DEPENDENT 13
非 SUPPORTED：14/131 = 10.7%  →  3/131 = 2.3%
```

派发单给的上限是 `S130/P1/U0`，**没到，差 2 条**：`B3-01`、`B3-05`。两条都不是引文问题，是论断问题
（情态升级 / 范围放大），下一轮只改论断即可，不必再动语料。

## 二、输出验收（主控重算，四条全过）

| # | 要求 | 结果 |
|---|---|---|
| 1 | 首行戳与输入同源 | `FIX_B3.md` = `out_FIX_3.md` = `a154464802`，首行整行 `> 快照 sha1: a154464802` |
| 2 | 表头 / 行数 / id 行序 | 表头与输入第 19 行逐字相等；13 行、列数恒 5、id 序列与输入**逐位相同** |
| 3 | 依据逐字命中 | 13/13 为本条引文子串，10–15 字符，0 拼接；11 条 SUPPORTED 依据非空；2 条 PARTIAL 末列均有具体成分与改法 |
| 4 | 工作区污染 | 派发后 `git status` 仅 `?? out_FIX_3.md` |

末行合计 `13 条（SUPPORTED 11 / PARTIAL 2 / UNSUPPORTED 0；DEPENDENT 3）` 与表内分布自洽。

> 表头是同会话内做过一次最小修正后的结果：agent 首版按契约 §四 示例表头输出，与派发单「列头与输入一致」冲突。
> 这不是判错，是指令打架，已在 §五.1 根治。

## 三、13 条改判明细

| id | 原判（69b676a） | 新判 | 自足变化 |
|---|---|---|---|
| B1-06 | UNSUPPORTED / SELF | **SUPPORTED** / SELF | — |
| B1-08 | PARTIAL / DEPENDENT | **SUPPORTED** / **SELF** | DEP → SELF |
| B1-12 | PARTIAL / DEPENDENT | **SUPPORTED** / DEPENDENT | — |
| B2-11 | PARTIAL / DEPENDENT | **SUPPORTED** / DEPENDENT | — |
| B3-01 | PARTIAL / SELF | PARTIAL / SELF | — |
| B3-05 | PARTIAL / SELF | PARTIAL / SELF | — |
| B3-07 | PARTIAL / SELF | **SUPPORTED** / SELF | — |
| B3-08 | PARTIAL / DEPENDENT | **SUPPORTED** / **SELF** | DEP → SELF |
| B3-09 | PARTIAL / DEPENDENT | **SUPPORTED** / DEPENDENT | — |
| B3-10 | PARTIAL / SELF | **SUPPORTED** / SELF | — |
| B3-11 | PARTIAL / SELF | **SUPPORTED** / SELF | — |
| B3-15 | PARTIAL / SELF | **SUPPORTED** / SELF | — |
| R4-16 | PARTIAL / SELF | **SUPPORTED** / SELF | — |

`B1-06` 是全局唯一一条 `UNSUPPORTED`，至此归零。重封批次：`B1 3 / B2 1 / B3 8 / R4 1`（戳
`81c78be532` / `05632596fd` / `b64ad5a18a` / `3231c9e097`），台账追加 `RESEAL.md`。

## 四、自足轴又动了一次，方向相反

`SELF 116 / DEP 15` → `SELF 118 / DEP 13`，净 **−2 DEPENDENT**（`B1-08`、`B3-08`）。
两条都是引文从名词短语/截断片段换成含主谓的完整句后，原先落在引号外的先行词进了引文内，
论断不再依赖上下文 → `SELF`。

round-18 改**论断**时净 +2 DEPENDENT，本轮改**引文**时净 −2。合起来说明一件事：
自足判的是「论断能否脱离上下文读懂」，而论断与引文**两边都能改变答案**；
派发单里任何「这轴应该不变」的预演都不要写成断言。

## 五、两个非数据问题（均已修）

### 1. 契约 §四 与派发单的表头冲突（用户回报中发现）

历史上三套表头并存：

| 出处 | 依据列措辞 |
|---|---|
| `AUDIT_CONTRACT.md §四` 示例 | `引文里的依据（≤15 字，必须是引文原词）` + `缺什么 / 需补的一句` |
| `FRAG_B* / REST_B*` 批次输入 | `（≤15字，引文原词）` |
| `FIX_B2 / FIX_B3` 定点输入 | `（≤15字，引文原词，连续片段）` |

契约原话「表头以本节为准，不要用批次输入里那份简化表头」与派发单「列头与输入文件给的一致」直接冲突，
agent 照契约执行反而被判不合规，同会话返工一次。**按契约执行不算判错，是主控给的两份指令打架。**

修法（选「以输入为准」，不动任何输入文件）：
- 契约 §四 增「**表头以本次派发的输入文件为准**，逐字照抄输入里那一行；示例行只作缺表头时的兜底」，
  并写明三套措辞只是历史模板差别、不构成格式差异、不改变判定口径；记录 2026-11-11 定案缘由。
- `AGENT_ROLES.md` 对应一句同步改成「表头逐字照抄本次输入文件 `{{BATCH_IN}}`」，重生成后 21 个
  `auditor-*` 定义同步，`gen --check` 45/45 绿。
- **保留 §四 第 57 行示例表头原样**：`audit_prep.contract_header()` 靠 `| id | 支撑 | 自足 |` 这一行取表头，
  改它会影响抽检答案键。`_payload_stamp` / `stamp_text` 只算 `- 论断：`/`- 引文：` 行，
  契约、表头、页码变化都**不参与戳**——本轮全部封印未受修复影响（`FIX_B3` 仍 `a154464802`）。

### 2. 参考集详情节的元信息没跟着冻结

`reseal` 后 `check.py` 9 绿 2 红，`golden --check` / `cases --check` 报「条目详情与当前判定表复算不一致（需重做）」。
diff 出来只有两行、都只是**页码**：金标准 `G01 p.13→p.2`、判例集 `C07 p.23→p.3`。
原因是原文存档只冻结了论断/引文两行，详情标题里的 `doc / sec / page` 仍取当前判定表；
本轮换引文改了页码，于是「同一份人判材料」被误报成不一致。这违反「参考集冻结在清单 + 元信息层」的既定原则。

修法：`audit_prep.py` 新增 `detail_heads(path, prefix)`，从人填表 `## 条目详情` 节抓抽样时点的标题行；
`build_golden` / `build_cases` 在 `--check` 时按它复现标题，非 `--check`（重抽）仍用当前元信息。
`arch` 的二元组结构、`verify-*` 的返工比对逻辑一律不动。标题不参与 `stamp_text`，戳不变。
顺手跑 `golden-migrate` 给 `GOLDEN_MAP.md` 补齐 25 条原文存档节，消掉长期那条「旧版、建议迁移」提示；
**人填表 `GOLDEN.md` / `CASES_SELF.md` 一个字未改**（`git status` 为空）。

## 六、参考集读数（判后返工剔除后）

| 参考集 | 有效分母 | 读数 |
|---|---|---|
| 抽检 S1 | 10（0 重叠） | 与答案键一致 10/10，依据逐字命中 10/10 |
| 金标准 | 25 → **15**（10 条返工失效） | 支撑 13/15（87%）、自足 15/15（100%）、双轴 13/15 |
| 判例集 C1 | 20 → **12**（8 条返工） | 冻结基线 16/20；剔除后自足 10/12（83%）、表内 DEP 阳性确认 **2/3** |

金标准 2 条差异（`G03`→`B1-10`、`G18`→`R4-01`，均人判更严）已于 2026-11-10 登记在
`DISPUTED.md`，不自动触发重审。判例集阳性样本只剩 3 条、确认 2 条。
**补抽 + 人开卷重判已是硬需求**：15 条与 12 条的一致率只能当粗估，不是精确可信度。

## 七、剩余 3 条（下一步 `FIX_B4`，都只改论断）

| id | 现判 | 问题 | 建议改法 |
|---|---|---|---|
| `B3-01` | PARTIAL | 论断「**是**有前景的路线」把引文 `seem to be promising` 升格成断言 | 改为「作者认为子图匹配方法在检索算法上**似乎是**有前景的路线」 |
| `B3-05` | PARTIAL | 论断「用于案例之间的比较」把引文 `having a mixture of crisp and fuzzy features` 的对象限定删没了 | 改为「用于**含清晰与模糊混合特征的**案例之间的比较」 |
| `B3-04` | PARTIAL | 「未给出数据集规模或指标数值」是缺席命题，单条引文证不完 | **待用户定口径**：A 删半句 / B 长期留账，两案见 `HANDOFF-12 §八` |

`B3-01` 是我 round-19 改稿时把 `seem to be` 译丢了，属本轮自伤，认账；`B3-05` 是上轮遗留。
两条都无需再碰语料与引文，改 2 行论断 + 重判 2 条即可。`B3-04` 定案后可一并处理。

⚠️ 现在**不要**直接改这 3 行：`FIX_B3.md` / `out_FIX_3.md` 的戳 `a154464802` 绑定当前文字，
一改就作废，必须按 `reseal` 规程另起 `FIX_B4` 定点批次重判。

## 八、复现命令

```bash
python tools/check.py                                  # 11/11 绿
python litrev/litrev.py audit-count                     # S128/P3/U0 · SELF118/DEP13
python tools/audit_prep.py verify-golden                # 15 条有效，13/15
python tools/audit_prep.py verify-cases                 # 12 条有效，10/12
python tools/gen_subagents.py --check                   # 45/45 同步
python litrev/litrev.py reseal --check \
  --fix-input FIX_B3.md --fix-out out_FIX_3.md          # 已并入，此处仅作历史复算
```
