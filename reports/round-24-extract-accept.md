# round-24 · 第 2 步第一段验收：开卷裁决 + 第二段备料

> 2026-11-11 · 承接 `3d33909`（HANDOFF-14 备料）与用户回报的抽取产物
> `ses_e36cd7689ffeDfVa9Vv0ovXiVX`（completed，权限拒绝 0 次）
> 本轮做两件事：接手 `HANDOFF-14 §五 第 5 项`（唯一需要人开卷的一关），以及 `§六` 第二段备料。

---

## 一、机械侧复核（我独立重跑，不采信回执）

| 项 | 结果 |
|---|---|
| 工作区 | 只多 `full/Ayzenshtadt2016_….md` 与它自己的 `_引文核验.md`（未跟踪），无其它污染 |
| `verify` | 全库 **138/138 PASS**（131 + 7）；新卡 `PASS 7 / 合计 7` |
| `card-check` | 全库 **20/20**；`--only` 1/1 |
| `card-coverage`（抽取后） | 按预期红：7 节未进任何批次输入 |
| `gen_subagents --check` | 按预期红：`ex-ayzenshtadt2016-…` 变陈旧残留（卡片已存在，生成器按设计不再给 `ex-`） |
| `audit-count` | 仍 `131 · S130/P1/U0` —— 抽取产物尚未进口径，正确 |

两项红都与回报一致，性质是「新卡已产出、尚未登记批次」，不是失败。

**一处语料观察**（不影响判定，登记备查）：§4 的 txt 原文是
`…every attribute of the meta\n•\ndata and additional data…`，PDF 项目符号 `•` 与换行插在
`meta` 和 `data` 中间；卡片抄成 `meta data`。字符级逐字查不到，但 `litrev.py norm_text`
会把版面符号与换行规范化掉，故 `verify` 判 PASS。这与 `Borner1993` 的 Type3 连字属同一类
版面噪声，只是方向相反（那边是丢字符、必须原样保留；这边是删版面符号）。
**逐字是 `norm_text` 后的等价，不是字符级 identical**，否则所有跨行 PDF 抽取的引文都会挂。
不改判、不改工具、不补字母。

---

## 二、§五 第 5 项：7 条论断开卷裁决

判据用 `AUDIT_CONTRACT.md` 轴 1 **原话**（论断的每个可检验成分——主体、动作、对象、范围、
限定强度——都能在引文里找到对应表述，且没有添加原文没有的内容），配合 §三.3「术语不得替换」
与 `CONTRACT.md` 三.7 第 ⑤ 类「术语替换与属性添加（专有名词的定义也算内容）」。
不自家枚举四类——round-16 的教训就是枚举会漏类。

| # | 节 | 裁决 | 复核要点 |
|---|---|---|---|
| 1 | 一句话主张 | 干净 | 提出 / 面向建筑设计领域 / 分布式检索系统 MetisCBR / agents work in groups (containers) / resolving of / user queries built with … Semantic Fingerprint，六个成分逐一在引文内 |
| 2 | 问题域 | 干净 | 「已无法充分」= `no longer able to adequately`，情态未升级；「日益增长的复杂性」= `increasing complexity of modern architectural projects` |
| 3 | 案例或数据的表示形式 | **干净** | 见下 |
| 4 | 相似性或检索机制 | **边界（严格读法可判 PARTIAL）** | 见下 |
| 5 | 系统形态 | 干净 | 括号内「用于实现所描述的智能体系统」= `(for the implementation of the described agent system)`，逐字对应；`JADE` / `myCBR` / `prototype` 都在引文内 |
| 6 | 评价方式 | 干净 | `5 rooms`、`6 connecting edges`、`with and without attribute weighting` 三个数值/范围全在引文内，无越界数值 |
| 7 | 明确写出的局限 | 干净 | `(manually, on this stage of development)` 最自然读法修饰 `was set`；论断「在这一开发阶段…是手工设定的」与之对应，未补缺席断言 |

### §3（用户观察点之一）：主谓重组 ≠ 越界

引文整句主语是 `CBR retrieval agents execute …`，论断重述为「待检索的案例位于…案例库中」。
契约轴 1 只禁**添加**，不禁重组，也不禁删成分：

- 「位于…案例库中」← `in the case base(s)`（修饰 `the most similar cases … in the case base(s)`）；
- 「底层基于属性-值的 CBR 域模型」← `the underlying attribute-value based CBR domain model`，逐词对应；
- 「待检索的」是把 `the most similar cases to the query or its parts` **弱化**成目的性描述，属于删成分，比原文更安全。

⇒ 判干净。用户说的「有主谓重组」成立，但不构成越界成分。

### §4（用户观察点之二）：命中，且比预判多两处

论断：`平面图检索的相似度计算会把元数据与附加数据的每一个属性都纳入考量。`
引文：`Floor plan agent works with following query types: Floorplan Query – every attribute of the meta data and additional data will be taken into account for the similarity measurement.`

有依据的成分：`every attribute` / `meta data and additional data` / `will be taken into account` / `for the similarity measurement` / `will`（会）——全部对得上。
问题出在**论断自己搭的那个框架**：

1. **「检索」← `Floorplan Query` / `query types`**：本篇里 `retrieval` 是有专指的词（同批 §3 引文的
   `CBR retrieval agents`、`retrieval process`），`query` 是查询输入。把 `query` 说成「检索」是术语替换，
   不是翻译选词。
2. **「计算」← `similarity measurement`**：`measurement` 是度量，本篇 p.6 另句确有
   `this similarity computation task`——但**那句不在这条引文里**。规则 9 要求「要写那些成分，就换一条覆盖它的引文」，
   不能从本篇别处借词。
3. **主体重组**：引文的框架是 `Floor plan agent works with … query types`（某智能体处理某查询类型），
   论断换成「平面图检索的相似度计算」这一抽象事件名词短语作主体，把「每个属性被纳入」归给了它。
   这与 §三.5「论断补主语不算越界」不同——那是引文缺主语时论断补上，这里是**换主语**。

同型先例：round-16 §5 把 `out of Neo4j` 写成「基于 Neo4j 图数据库的实现」，多出「图数据库」
与「实现」两个本条引文里没有的名词，判边界。本轮性质更轻（拿本篇别处存在的近义词替换本条引文里的词，
而非凭空造名词），但按契约严格读法仍是 `PARTIAL`；按宽松读法（中文综述里 measurement/computation、
query/retrieval 常被混译）可判 `SUPPORTED`。**这正是支撑轴 9.9% 漂移的典型形态。**

### round-16 复测结论

「约 1/7 节落在边界」本轮仍是 **1/7**，落点正是用户预判的 §4（§3 干净），且仍是第 ⑤ 类术语替换。
规则 9 补了第 ⑤ 类之后**边界率没有降到 0，但严重度降了一档**：round-16 是编造式属性添加，
本轮是近义术语替换。⇒ 抽取端「有效但未清零」的判定维持，不需要再改规则 9。

另外：`verify` 只看引文逐字、`card-check` 只看结构，两者都**不看论断内容**——这一条边界
只有人工关能拦住，这就是 §五.5 存在的理由。

---

## 三、处置决定：不改卡片，原样进批次

**决定**：不对 §4 做预改稿，`REST_B6.md` 逐字照抄子代理产物的 7 条论断与引文，让闭卷审计独立判。

理由：

1. 主控开卷裁决是**验收**，不是替审计员判。这一关的价值恰是人机互证：预先改掉，
   判定表看到的就是改后文本，无法验证抽取端规则 9 的真实效果。
2. 改的是子代理产物，会切断「产物 → 判定表」的可复现链；而 `R6` 是独立批次，
   不预改也不会污染既有 131 条。
3. 两个出口都明确，且都不增加额外派发：

| 审计员判 §4 | 与主控 | 口径 | 后续 |
|---|---|---|---|
| `SUPPORTED` | 分歧 | `S137/P1/U0`（138 条） | 登记 `DISPUTED.md`，`check.py` 11/11 绿 |
| `PARTIAL` | 一致 | `S136/P2/U0`（138 条） | 另起 `FIX_B6` 定点改稿（只删「检索」「计算」两个替换词），不动已封戳批次；`check.py` 仍 11/11 绿 |

两种情况下 `check.py` 都能到 11/11 绿（门禁不检查判定码取值，只检查戳与依据）。
若判 `PARTIAL`，改稿留到派发回收后再做，不在本轮预支。

---

## 四、第二段备料（已落盘）

| 项 | 值 |
|---|---|
| 批次输入 | `audit/REST_B6.md`：7 条（`R6-01…07`），格式照 `REST_B5.md`；`batch --only B6` 盖章 **戳 `7cb35452e0`** |
| 注册 | `BATCHES.json` 新增 `rest_b6`：`REST_B6.md → out_R6.md`（`out_R6.md` 进 131→138 口径） |
| 生成器 | 重跑 `gen_subagents.py`：新增 `auditor-rest-b6`，按设计移除已完成的 `ex-ayzenshtadt2016-…`；agent 仍 47 个，`gen --check` 47/47 绿 |
| 对账 | `card-coverage` **已销项**：20 张卡 / 138 条带引文的节 / 138 组覆盖 ✓ |
| `batch --check` | `0/138` 待刷新，`REST_B6.md` 显示「无变化」——输入与卡片逐字同源 |

`B3-04` 口径仍归用户，未动；`FIX_B5` 未落盘。

---

## 五、派发前修掉的一个工具缺陷（否则会白派一次）

备料后 `check.py` 的红项从 2 个变成 4 个，性质全变：`audit-stale --check` 报
「R6：7 条待重审 · 没有判定输出」，三个参考集 `--check` 报
「批次输入与判定表 id 不齐：只在输入 R6-01…07 / 只在输出 []」。**这 4 项是「批次已登记、
判定未产出」的必然结果**，`out_R6.md` 回来且首行戳一致即自愈。

但顺着这条线查出另一个**派完也不会自愈**的坑：`audit_prep.py` 的 `build_*` 头部写死
`f"判定表总条目 {len(recs)}"`，判定表 131 → 138 之后，三份已冻结的答案键
（`SAMPLE_S1.md` / `SAMPLE_S1_KEYS.md` / `GOLDEN_MAP.md` / `CASES_SELF_KEYS.md`）
复算出的这一行会变成 138，与磁盘上的 131 不一致 → `--check` 判「需重做抽检/金标准/判例集」，
等于逼人重填人开的卷。**判定表第一次真正扩容才暴露**，前面四轮改稿都在 131 条内打转，测不出来。

修法沿用项目既有口径「参考集冻结在清单 + 元信息层」：

- `tools/audit_prep.py` 新增 `frozen_total(recs, keys_path)`：从 `<!-- picks: … -->` 读 `total`，
  没有则退回 `len(recs)`（首次抽样时把当时的规模写进清单）；
- `build_sample` / `build_keys` / `build_golden_map` / `build_cases_map` 的「判定表总条目」改用它，
  三处 `picks_line(...)` 同步写 `total`；
- 三份答案键的冻结清单补 `total=131`，**人填的 `GOLDEN.md` / `CASES_SELF.md` 表格一字未动**。

**派发前只读模拟**（把 `audit_prep.load` 在内存里打桩成「判定表已含 7 条 R6 判定，共 138 条」）：

| 命令 | rc | 输出 |
|---|---|---|
| `sample --check` | 0 | `✓ 抽检批次可复现：10/80 条（12.5%），戳 7d1a204d54，答案键一致` |
| `golden --check` | 0 | `✓ 金标准可复现：25 条（S15/P9/U1），戳 d46f9e7c3f` |
| `cases --check` | 0 | `✓ 自足轴判例集可复现：20 条（表内 DEP 10），戳 a4e66877dc` |

三份戳全部不变，人填表格不必重开卷。`audit-stale` 的自愈条件由源码确认：
`out_R6.md` 存在 + `batch_stamp(out) == batch_stamp(REST_B6.md) == 7cb35452e0` 即不进 `stale_batches`。
规程已写进 `RUNBOOK §三附之三` 的「新增文献时的红项时序」。

---

## 六、当前状态与交接

- 工作区：`REST_B6.md`（新）、`BATCHES.json`、`audit_prep.py`、三份答案键、`RUNBOOK.md`、
  `AGENT_MAP.md`、`.generated_agents.json`、`auditor-rest-b6.md`（新）、`ex-ayzenshtadt2016-…`（删除）、
  新卡片 + 核验报告（未跟踪）。
- `check.py` 当前 **7 绿 / 4 红**，4 红全部是上表第二行「已登记未判定」的预期态；
  **别手工改戳、别补 `out_R6.md` 占位、别重抽参考集**。
- 下一步见 `HANDOFF-15.md`：用户重启 OpenCode 第二次 → 派 `auditor-rest-b6` → 我按四条验收 →
  `audit-count` 首次 `131 → 138`。
- `B3-04` 选 A 的合并窗口仍开着（第二次重启尚未发生）：现在定选 A，`fix_b5` 可与本轮同批生成，
  一次重启覆盖两个派发；派完再定就要另起一轮。
