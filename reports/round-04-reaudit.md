# round-04：B1–B3 整批重审

- 执行对象：`HANDOFF-04.md`（只做 B1–B3 三批重审，做完停）
- 时间：2026-11-10
- 判定标准：`litrev/_probe/AUDIT_CONTRACT.md` §四 / §五 / §七（B1–B3 重审适用 §七，见契约 §七 首段）
- 结论一句话：**三批各 16 条重审完成，戳行齐全，`audit-count --check` 退 0、`audit-stale --check` 退 0，131 条判定有效**；同时测出一个旧表未覆盖的事实——闭卷整批重跑在同一份输入上会产生约 4/28 的判定码漂移（见 §六）。

## 一、开工自检（原始输出）

### 1) `python tools/gen_subagents.py --check`

第一次直接跑，控制台死在**成功提示的 print 语句**上（GBK 不能编码 `✓`），退出码 1：

```
Traceback (most recent call last):
  File "F:\project\PyProject\Litreview\tools\gen_subagents.py", line 302, in <module>
    sys.exit(main())
             ~~~~^^
  File "F:\project\PyProject\Litreview\tools\gen_subagents.py", line 264, in main
    print(f"\u2713 ͬ����{len(files)} ���ļ��� AGENT_ROLES.md һ��")
    ~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeEncodeError: 'gbk' codec can't encode character '\u2713' in position 0: illegal multibyte sequence
EXIT=1
```

traceback 落在第 264 行的编解码，不在比对逻辑里。设 `PYTHONIOENCODING=utf-8` 重跑：

```
✓ 同步：33 个文件与 AGENT_ROLES.md 一致
EXIT=0
```

判定：**同步一致，退 0**。附带记一条环境问题：本机 PowerShell 默认 GBK 控制台会让这个脚本在「已经比对成功之后」崩掉，属于可复现的显示层缺陷（不是同步失败，也不该据此判 agent 文件被手改）。本轮全程用 `PYTHONIOENCODING=utf-8` 取输出。

### 2) `python litrev/litrev.py batch --check`

```
FRAG_B1.md        16 条  无变化
FRAG_B2.md        16 条  无变化
FRAG_B3.md        16 条  无变化
REST_B1.md        16 条  无变化
REST_B2.md        17 条  无变化
REST_B3.md        17 条  无变化
REST_B4.md        16 条  无变化
REST_B5.md        17 条  无变化

合计待刷新 0/131 条（--check 不写盘）
EXIT=0
```

### 3) `python litrev/litrev.py audit-count --check`

```
批次         条数  SUPP  PART  UNSU  SELF   DEP  合计行
--------------------------------------------------------------
B1         16     8     7     1    15     1  ✓
B2         16    10     6     0     9     7  ✓
B3         16     6    10     0     9     7  ✓
R1         16    10     6     0    16     0  ✓
R2         17    13     4     0    15     2  ✓
R3         17    11     6     0    16     1  ✓
R4         16    12     4     0    16     0  ✓
R5         17    14     3     0    16     1  ✓
--------------------------------------------------------------
合计        131    84    46     1   112    19

口径：131 条 · SUPPORTED 84 / PARTIAL 46 / UNSUPPORTED 1 · SELF 112 / DEPENDENT 19
非 SUPPORTED：47/131 = 35.9%
EXIT=0
```

### 4) `python litrev/litrev.py audit-stale --check`（预期退 1，本轮要修的就是它）

```
批次输入 131 条 · 卡片 19 篇 / 133 节 / 131 条引文
判定依据与卡片一致：131/131

[!] 下列批次的判定不能用于结论（输入与判定输出的快照戳不一致）：
  - B1：16 条待重审 · 输出没回写戳（未按规程）
  - B2：16 条待重审 · 输出没回写戳（未按规程）
  - B3：16 条待重审 · 输出没回写戳（未按规程）

[!] 0 条判定的依据已过期，0 条对不上卡片，3 个批次待重审。
    重审请按批次整体重跑（不要在旧 out_*.md 上就地改判）。
EXIT=1
```

与预期一致：退 1、只列 B1/B2/B3、原因是「输出没回写戳」。注意这里同时显示「判定依据与卡片一致：131/131」——即**卡片的文字没再变过，这 48 条作废的原因仅仅是旧输出没戳**，所以整批重跑时输入与旧输出引用的是同一份文字。

### 5) `python litrev/litrev.py verify litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md`

```
引文核验：Borner1993_StructuralSimilarity_CBR.md  共 7 条
==============================================================================
OK  1. L7    PASS        Structural similarity is assessed if and only if there is know
OK  2. L11   PASS        Although our approach is more theoretical in nature and not re
OK  3. L15   PASS        Following the work of Ludger Hovestadt Hov each object circle 
OK  4. L19   PASS        The rst initial analysis of the new problem can be done by an
OK  5. L23   PASS        SynTerm and SynGraph supply the system with solutions for spec
OK  6. L27   PASS        The initial experimental results support the claims that the p
OK  7. L31   PASS        Learning e g the storage of new cases new rules and the applic
==============================================================================
汇总：PASS=7   合计 7
报告：F:\project\PyProject\Litreview\litrev\_probe\full\Borner1993_StructuralSimilarity_CBR_引文核验.md
EXIT=0
```

7/7 PASS。**五条自检与预期一致，进入派发。**

## 二、派发记录（一次一个 task，B1 → B2 → B3）

| 批次 | agent | 子会话 / task id | 返回状态 | `task_result` | 首行戳 |
|---|---|---|---|---|---|
| B1 | `auditor-frag-b1` | `ses_e3ce38f48ffegBmyb4A9KWoV4B` | `completed` | 非空（「已写入 …out_B1.md：16 条（SUPPORTED 6 / PARTIAL 9 / UNSUPPORTED 1；DEPENDENT 3）」） | `> 快照 sha1: 9ff1753875` |
| B2 | `auditor-frag-b2` | `ses_e3ce07a4dffee1DwrCQxXVQUQE` | `completed` | 非空（「已写入 …out_B2.md：16 条（SUPPORTED 8 / PARTIAL 8 / UNSUPPORTED 0；DEPENDENT 2）」） | `> 快照 sha1: 902e819463` |
| B3 | `auditor-frag-b3` | `ses_e3cdcd3dcffeaFbavFzG22f7OM` | `completed` | 非空（「已写入 …out_B3.md：16 条（SUPPORTED 7 / PARTIAL 9 / UNSUPPORTED 0；DEPENDENT 4）」） | `> 快照 sha1: a52c3ea485` |

- 三次派发**都是单独一条消息**，没有并发，所以不存在「空结果定位不到是哪条」的情形。
- **空 `task_result` 发生次数：0/3**，未触发 RUNBOOK §四 恢复流程。
- 三次都没有 `CONTRACT_CONFLICT` 停机，也没有权限拒绝（每个 auditor 只读本批 `FRAG_B{n}.md` + 契约、只写 `out_B{n}.md`）。
- 派发提示词三条硬要求都写进了：抄第 6 行戳、忽略输入第 8 行的旧模板句、表头照抄契约 §四（不用输入第 10 行的简化表头）。没有贴任何卡片内容，没有让它读别的批次。

## 三、验收（按 HANDOFF-04 §验收 五条，以文件为准）

### 机械检查的原始输出

| 批次 | 文件总行数 | 首行 | 输入第 6 行 | 匹配 `^\| Bn-\d\d \|` 的判定行 | 末行合计 |
|---|---|---|---|---|---|
| B1 | 21 | `> 快照 sha1: 9ff1753875` | `> 快照 sha1: 9ff1753875` | **16** | 16 条（6/9/1；DEP 3） |
| B2 | 21 | `> 快照 sha1: 902e819463` | `> 快照 sha1: 902e819463` | **16** | 16 条（8/8/0；DEP 2） |
| B3 | 21 | `> 快照 sha1: a52c3ea485` | `> 快照 sha1: a52c3ea485` | **16** | 16 条（7/9/0；DEP 4） |

> 每条判定行都是独立正则计数（`^\| B1-\d\d \|` 等），不是数文件总行数；21 行 = 戳 1 + 空行 1 + 表头 2 + 判定 16 + 合计 1，与 HANDOFF 给的「加戳后 21 行」一致。

### 逐条结论

| # | 检查 | B1 | B2 | B3 |
|---|---|---|---|---|
| 1 | 调用状态 | completed | completed | completed |
| 2 | 输出被覆盖、首行是戳、16 条判定、末行有合计 | 是 | 是 | 是 |
| 3 | 戳与输入第 6 行逐字相同、无附加说明 | 是 | 是 | 是 |
| 4 | 合计与表内条数自洽、`audit-count` 可解析 | 是（表内 ✓） | 是（✓） | 是（✓） |
| 5 | 只写本批输出 | 是 | 是 | 是 |

第 5 条的机械证据（三次派发后 `git status --porcelain`，逐次递增，没有第四类文件）：

```
 M litrev/_probe/audit/out_B1.md
----
 M litrev/_probe/audit/out_B1.md
 M litrev/_probe/audit/out_B2.md
----
 M litrev/_probe/audit/out_B1.md
 M litrev/_probe/audit/out_B2.md
 M litrev/_probe/audit/out_B3.md
```

卡片（`_probe/full/*.md`）、`AUDIT_CONTRACT.md`、`litrev.py`、`.opencode/agents/*` 均未出现在变更列表里；本轮也**没有**跑不带参数的 `batch`，**没有**跑 `stamp-out`。

## 四、新旧判定差异（18 条）

「依据是否变过」一列取自 HANDOFF-04 的 20 条清单（`B1-03/04/05/12/13/14`、`B2-01/03/04/05/08/09/12/13`、`B3-02/03/04/12/13/16`）；不在清单里的条目，输入文字与旧判定所依据的文字**完全相同**，差异只能来自重判本身。

| id | 旧判定（支撑/自足） | 新判定（支撑/自足） | 变化 | 依据是否变过 | 改判理由（新表「缺什么」栏原文节选） |
|---|---|---|---|---|---|
| B1-04 | SUPPORTED / SELF | PARTIAL / SELF | 支撑降级 | 是 | 引文是 `can be done`（可能性），论断写成实然「先做」 |
| B1-07 | SUPPORTED / SELF | PARTIAL / SELF | 支撑降级 | **否** | 删「案例」（引文止于 failure analysis）；「该文所依托」需补依据 |
| B1-08 | PARTIAL / SELF | PARTIAL / DEPENDENT | 自足降级 | **否** | `information on design projects` 无主语 |
| B1-12 | SUPPORTED / SELF | PARTIAL / DEPENDENT | 支撑+自足降级 | 是 | 「现有案例检索方法」是 `such` 的指代，引文内无指代对象 |
| B1-14 | PARTIAL / SELF | SUPPORTED / SELF | 支撑升级 | 是 | —— |
| B2-01 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | 是 | —— |
| B2-03 | PARTIAL / DEPENDENT | SUPPORTED / SELF | 支撑+自足升级 | 是 | —— |
| B2-04 | SUPPORTED / SELF | PARTIAL / SELF | 支撑降级 | 是 | 原文只说 supply the system，未称二者为子系统/构成系统 |
| B2-08 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | 是 | —— |
| B2-09 | SUPPORTED / DEPENDENT | PARTIAL / SELF | 支撑降级 | 是 | 原文未称其为「评价所依据」的案例数据 |
| B2-13 | PARTIAL / DEPENDENT | PARTIAL / SELF | 自足升级 | 是 | —— |
| B2-14 | SUPPORTED / SELF | PARTIAL / SELF | 支撑降级 | **否** | 原文为 `guides the project`，非「结构设计过程」 |
| B3-02 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | 是 | —— |
| B3-03 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | 是 | —— |
| B3-10 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | **否** | —— |
| B3-12 | PARTIAL / SELF | SUPPORTED / SELF | 支撑升级 | 是 | —— |
| B3-13 | PARTIAL / SELF | PARTIAL / DEPENDENT | 自足降级 | 是 | 引文无主语 |
| B3-16 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 自足升级 | 是 | —— |

20 条「依据变过」的条目里：**14 条改了判定码，6 条判定码不变**（B1-03、B1-05、B1-13、B2-05、B2-12、B3-04）。28 条「依据未变」的条目里：**4 条改了判定码**（B1-07、B1-08、B2-14、B3-10）。

### 汇总变化（照抄 `audit-count`，非手算）

| 口径 | 旧 | 新 | Δ |
|---|---|---|---|
| SUPPORTED | 84 | 81 | −3 |
| PARTIAL | 46 | 49 | +3 |
| UNSUPPORTED | 1 | 1 | 0 |
| SELF | 112 | 118 | +6 |
| DEPENDENT | 19 | 13 | −6 |
| 非 SUPPORTED | 47/131 = 35.9% | 50/131 = 38.2% | +2.3 pt |

分批评定码变化方向不统一，说明这不是「整体变松」或「整体变严」，而是逐条重判：

- B1：SUPPORTED 8→6（−2），PARTIAL 7→9（+2）。
- B2：SUPPORTED 10→8（−2），PARTIAL 6→8（+2），且 DEPENDENT 7→2（§五.1 口径下的自足升级集中在这一批）。
- B3：SUPPORTED 6→7（+1），PARTIAL 10→9（−1），DEPENDENT 7→4。

## 五、收尾两条命令（原始输出）

### `python litrev/litrev.py audit-count --check`

```
批次         条数  SUPP  PART  UNSU  SELF   DEP  合计行
--------------------------------------------------------------
B1         16     6     9     1    13     3  ✓
B2         16     8     8     0    14     2  ✓
B3         16     7     9     0    12     4  ✓
R1         16    10     6     0    16     0  ✓
R2         17    13     4     0    15     2  ✓
R3         17    11     6     0    16     1  ✓
R4         16    12     4     0    16     0  ✓
R5         17    14     3     0    16     1  ✓
--------------------------------------------------------------
合计        131    81    49     1   118    13

口径：131 条 · SUPPORTED 81 / PARTIAL 49 / UNSUPPORTED 1 · SELF 118 / DEPENDENT 13
非 SUPPORTED：50/131 = 38.2%
EXIT=0
```

### `python litrev/litrev.py audit-stale --check`

```
批次输入 131 条 · 卡片 19 篇 / 133 节 / 131 条引文
判定依据与卡片一致：131/131

✓ 全部判定的依据与卡片当前内容一致。
EXIT=0
```

两条都退 0 → **131 条判定有效**（8 个批次：B1–B3 本日重审 + R1–R5 沿用旧表，依据仍与卡片逐字一致）。

## 六、本轮测出的一件事：闭卷整批重跑不是确定性的

28 条「输入文字一字未变」的条目重新判了一遍，有 4 条判定码变了：

| id | 旧 | 新 | 方向 |
|---|---|---|---|
| B1-07 | SUPPORTED / SELF | PARTIAL / SELF | 变严 |
| B1-08 | PARTIAL / SELF | PARTIAL / DEPENDENT | 变严 |
| B2-14 | SUPPORTED / SELF | PARTIAL / SELF | 变严 |
| B3-10 | SUPPORTED / DEPENDENT | SUPPORTED / SELF | 变松 |

也就是同一份输入两次闭卷判定，判定码不一致率 **4/28 ≈ 14.3%**（支撑轴 3/28，自足轴 2/28）。这一条比数字本身重要：

- 它说明「R1–R5 的 83 条仍然有效」这句话的准确含义是**「`audit-stale` 认为依据没变，所以不需要重审」**，而不是「这 83 条判定被复核为对」。旧表从未在同一输入上重判过，其自身漂移率未知，量级按本轮估计可能与之同阶。
- 三次 SUPPORTED→PARTIAL 的降级说明**旧表偏松**的方向；另一条 DEPENDENT→SELF 是反向，属噪声，不是统一趋势。
- 因此：任何把 SUPPORTED 数当质量指标的表述（例如"84/131 条有证据支撑"）都应在脚注里写清这是一次性判定的结果，重复判定会漂 ±3～4 条。

这条不需要立刻返工（`audit-stale` 退 0，规程层面已到位），但应写进下一轮的改进项：闭卷判定的双人/双跑一致性检验，比继续加抽检比例更能暴露问题。

## 七、仍然没做的事

1. **SUPPORTED 抽检未重做，`SAMPLE_S1` 已失效。** 证据：`SAMPLE_S1.md` 最后一次改动是 commit `e9ff551`（11-09 16:04），其后卡片在 `e8c140b`（17:24）、`f7afb87`（21:10）、`6877968`（21:26）三次被改写；`audit-stale` 的批次注册表只覆盖 8 个 `frag_/rest_` 批次，**不覆盖 `sample_s1`**，所以它无法机械证明自己的 16 条仍与卡片一致；而且本轮 SUPPORTED 集合从 84 变成 81，按 `sample` 的抽取逻辑，候选集合本身就变了。要重跑：

   ```bash
   python litrev/litrev.py sample litrev/_probe/full --rate 0.12 --seed 42 --out litrev/_probe/audit/SAMPLE_S1.md
   python tools/gen_subagents.py
   ```

   然后派 `auditor-sample-s1` 写 `out_S1.md`。本轮按 HANDOFF-04「做完停下」没有执行。
2. **`gen_subagents.py` 在 GBK 控制台下崩溃**（§一.1），需给脚本加 `sys.stdout.reconfigure(encoding='utf-8')` 或统一运行时设 `PYTHONIOENCODING`。属工具缺陷，不在本轮授权范围，未改。
3. **非 SUPPORTED 的 50 条没有人看过**：契约 §五.3 要求任何非 SUPPORTED 必须人看，本轮只产判定，没有逐条处理「缺什么」。
4. **主控仍不受权限约束**（RUNBOOK §七.1 的已知残余风险），而且本文档暴露了规程自身的一处张力：RUNBOOK §一 的开工自检**要求主控**跑 `verify`，§二.5 又规定「核验归 checker，主控不要代跑」。本轮按 HANDOFF-04 直接跑了那 5 条（含 `verify` 单篇基线），所以「生成方 + 裁判」在这一步仍是同一只手。要么把 §一 的自检收窄到不碰裁判命令，要么明确「自检用的 verify 不构成结论」并留痕——目前是后者，靠文字约定而非权限。
5. 未提交 git（按惯例由用户决定提交时机）；工作区当前只有 3 个 `out_B*.md` 的修改 + 本报告。
