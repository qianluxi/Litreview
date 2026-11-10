# 运行规约（RUNBOOK）

> 这份文件把"上一次是靠人现场补救"的几件事写成规程：**派发**、**验收**、**空结果恢复**、**抽检**、**权限回归**。
> 它和 `.opencode/agents/orchestrator.md` 的关系：orchestrator 里的规则是给模型看的摘要，这里是完整规程与可复现命令。两者不一致时以本文件为准，并修 orchestrator。
>
> 适用版本：OpenCode 1.18.25（桌面客户端，无 CLI）。

## 一、开工自检（六条命令，缺一条都别派活）

```bash
python tools/gen_subagents.py --check          # 子代理定义与角色模板是否同步
python litrev/litrev.py text --dry-run         # 语料文字层健康度（词/行 < 3 的文献不能派抽取工）
python litrev/litrev.py index                  # 重建索引（改过 PDF 或 vocab 时）
python litrev/litrev.py verify litrev/_probe/full/<文献>.md   # 引文层基线
python litrev/litrev.py audit-count --check    # 判定表自洽（汇总只能照抄它）
python litrev/litrev.py audit-stale --check    # 判定依据是否还成立（不为 0 就别说"已审 N 条"）
```

判定：

| 现象 | 含义 | 动作 |
|---|---|---|
| `--check` 报"与模板不一致" | 有人手改了 `.opencode/agents/` | 跑 `python tools/gen_subagents.py` 覆盖 |
| `--check` 报"陈旧残留" | 文献删了但 agent 还在 | 同上，生成器会清理 |
| `text --dry-run` 报 `← 仍碎片` | 文字层坏到按行取句必得碎片 | 该文献**不派** `ex-`，记入已知问题（需 OCR/视觉抄录） |
| `verify` 出现 PARAPHRASE / MISSING | 笔记里有非原文引文 | 先修笔记，别进入审计 |

## 二、派发协议

1. **先查表**：`litrev/_probe/AGENT_MAP.md`。agent 名由文件名派生，不是你想写什么就有什么。
2. **一篇文献一个 agent、一个文件**：`qx-<slug>` 只改自己那一张卡片（`_probe/full/<文献>.md`，没有则 `_probe/notes/<文献>.md`）。`ex-<slug>` 只在**卡片还不存在**时才生成——它只有创建权限，给已有卡片派它等于让它撞墙。权限是按路径写死的，越界会在调用时被拒——**被拒不是 bug，是隔离生效**。
3. **并行**：同一条消息里并列多个 `task` 调用。同一条消息里也不要给同一个 agent 派两个文件（它只认得自己那一个）。
4. **批次审计**：`auditor-<批次>` 的输入、输出在 `litrev/_probe/audit/BATCHES.json` 里登记。新增批次：改 JSON → 跑生成器 → 才会出现对应 agent。重跑一个已有批次会**覆盖**它的 `out_<批次>.md`——历史判定靠 git，不靠另存副本。
5. **核验归 checker**：只有 `checker` 的 bash 白名单放行 `python litrev/litrev.py verify|matrix|locate`。主控不要代跑（代跑会把"生成方"和"裁判"合并成一个人）。

## 三、验收协议（正式规程）

**`completed` ≠ 成功。** 每个 `task` 返回后依次过五条：

| # | 检查 | 判据 |
|---|---|---|
| 1 | 调用状态 | `completed` / `failed` / 权限拒绝（错误原文含 ruleset） |
| 2 | 交付文件存在 | 文件在，大小 > 0 |
| 3 | 格式合规 | 笔记：`- 论断：`/`- 引文：` 成对；审计表：表头 + 末行 `合计：` |
| 4 | 条数对得上 | 等于派发时要求的条数（不是"差不多") |
| 5 | 路径在授权内 | 文件名是本篇；没有写到 `_index/`、别人的笔记 |

分支：

| 情况 | 处理 | 禁止 |
|---|---|---|
| completed + 空 `task_result` + 文件合规 | 通过 | 不要重派（会产生第二份不一致结论） |
| completed + 空 `task_result` + 无文件 | 用原 `task_id` 恢复会话补写 | 不许新建任务 |
| completed + 文件不合规 | 原会话补交缺失部分 | 不许整篇重抽 |
| failed / 权限拒绝 | 记录原文，判断是派错 agent 还是授权缺口 | 不许静默跳过、不许换 agent 绕 |

> 为什么以文件为准：空 `<task_result>` 是 OpenCode 侧的已知现象（8 次派发 3 次）。把交付物做成文件之后，
> 空结果只是"没写回话"，不丢工作；而 `task_result` 里的文字本身从来不是证据。

### 三附：判定有效性（快照戳）

`audit-count` 只保证"判定表自己自洽"，**不保证"判定判的是卡片现在的文字"**。卡片一返工，旧判定就悄悄失效，
而汇总数字照样漂亮。所以三件事必须按顺序做：

```bash
python litrev/litrev.py audit-stale              # 1. 看哪些判定的依据已变（应为 0）
python litrev/litrev.py batch --check            # 2. 看批次输入落后卡片多少条（--check 不写盘）
python litrev/litrev.py batch                    # 3. 刷新批次输入，并写入「快照 sha1」戳
python litrev/litrev.py stamp-out                # 4. 已有输出：能按 git 历史证明"产出后输入未变"的，补戳；证不了的列为待重审
```

判定：

| 现象 | 含义 | 动作 |
|---|---|---|
| `audit-stale` 报"依据已过期" | 卡片改过，批次输入没跟上 | 先 `batch` 刷新，再**整批**重审，不要就地改 `out_*.md` |
| `audit-stale` 报"输出没回写戳" | 判定产出后输入被改过，或没人抄戳 | 该批判定不能进结论，整批重审 |
| `batch` 报"变动 N 条" | 这 N 条的判据已换 | N>0 的批次一律重审 |
| 三个命令全绿（stale 0 过期、batch 0 变动、戳齐全） | 判定与卡片文字对得上 | 才可以把汇总写进报告 |

审计员（`auditor-*`）的输出**第一行必须原样抄输入的 `> 快照 sha1: ...`**。抄错或漏抄 = 来源不明 = 整批重做。

## 四、空结果恢复规程（逐步照做）

1. 记录该 `task` 调用返回的 `task_id`（形如 `ses_...`），不要关掉会话。
2. 先看交付文件：`notes/<文献>.md` 或 `audit/out_<批次>.md` 是否存在且非空。
   - 存在 → 视为完成，补做第三节第 3–5 条检查。
   - 不存在 → 进入第 3 步。
3. 用原 `task_id` 恢复（resume），只发一句：「上次以 completed 返回但未写 `<路径>`，请现在把结果写入该文件，不要重新分析」。
4. 恢复后仍为空 → 视为失败，记录错误原文，改派同一 agent 一次（不是换 agent）。两次都空 → 停手，写进 `reports/` 并上报，不再重试。

**不许**：把空结果当成功继续下一步；不许用主控代写补上（证据链会断）。

## 五、抽检规程（2026-11-10 修订：候选集改为当前 SUPPORTED）

`SUPPORTED` 只是分诊结果，不是合格证（v1.1 契约 §七.2）。**抽样对象是当前判为 `SUPPORTED` 的条目，不是全库卡片**——
`litrev.py sample` 从 `_probe/full/*.md` 的全部 131 条里抽，会抽到本来就要人看的 PARTIAL/UNSUPPORTED，抽检失去意义。
改由主控侧 `tools/audit_prep.py` 从 8 张判定表取候选集（裁判 `litrev.py` 一字不改）：

```bash
python tools/audit_prep.py sample             # 写 SAMPLE_S1.md + SAMPLE_S1_KEYS.md（答案键）
python tools/audit_prep.py sample --check     # 复算比对；判定表或批次输入一变就报不一致
python tools/gen_subagents.py --check         # S1 已在 BATCHES.json 登记，正常无需重启
python tools/audit_prep.py review             # 非 SUPPORTED 人工复核清单（契约 §五.3）
```

- 比例 10–15%、种子固定（seed=42、rate=0.12）；**同一批数据重跑必须抽出同一组条目**（`--check` 验证）。
- 输入文件必须闭卷：**不写候选集的判定码、不写原依据、不写答案键路径**。答案键 `SAMPLE_S1_KEYS.md` 只在主控侧留档，
  `auditor-*` 的 read 白名单里没有它，派发提示词也不许引用它——否则等于把答案递给审计员。
- 输入第 6 行是 `> 快照 sha1: <10 位>`，输出首行必须原样抄；戳由所有 `- 论断：`/`- 引文：` 行算出（与 `batch` 同算法）。
- 派 `auditor-sample-s1` 写 `out_S1.md` 后，先跑 `python litrev/litrev.py audit-count --prefixes S --check`（表自洽），
  再跑 `python tools/audit_prep.py verify-sample`（戳/表头/10 行/合计行/依据逐字命中/命中率；退 0 才算过）。
- **差异 ≠ 错误**：`verify-sample` 只把回写与答案键（**抽样时点的原判**）逐条比对，它没有判定哪一侧判对的能力。
  退 1 只表示「两次判定不一致」，不构成「原表判错」或「抽检判错」的结论。
- 出现差异时**先登记、后裁决**，按方向分开处置（2026-11-10 修订，见 `reports/round-05-arbitration.md`）：

  | 方向 | 含义 | 第一步处置 |
  |---|---|---|
  | 原表 `SUPPORTED` → 抽检更严 | 疑似**原表偏松** | 登记争议项、冻结 131 条汇总，补证据后再定是否整批重审该条所属原批次 |
  | 原表非 `SUPPORTED` → 抽检 `SUPPORTED` | 疑似**抽检偏松** | 重审对象是抽检侧判读，不是原批次；同样先登记、后裁决 |

  补证据的两条正规路径：**① 对该条所属原批次的全部 `SUPPORTED` 定向扩抽**（判断是单条噪声还是系统性偏松）；
  **② 固定契约双跑**（另存对照文件、不覆盖旧表，测同一输入重复判定的漂移率）。两者都不改判定表。
- **禁止两种自动动作**：不因一次差异就自动「整批重审」（10 条抽检里某批次常只占 1–2 条，样本撑不起「系统性偏松」）；
  更不许「逐条改一条」把差异抹掉（逐条修会把系统性偏松掩盖成偶发，且 `S80/P50/U1` 这类数字只对应逐条修补）。
  是否整批重审、重审哪个批次，必须由**主控人工裁决**并写进 `reports/` 后才能派发。
- **答案键冻结**：判定表一旦变更，`SAMPLE_S1_KEYS.md` 即失效（`sample --check` 会报不一致）。
  重审前先留档当前答案键与 `out_S1.md`，不要在重审后拿新表复算旧答案键。
- **改判的级联代价（裁决前必算）**：候选池 = 当前 `SUPPORTED`，所以**任何一条改判都会移动池、换掉抽样**。
  实测：`B3-10` 从 `SUPPORTED` 改 `PARTIAL` 后池 81→80，`seed=42` 重抽的 10 条与现有只有 4 条重合（`S05` 直接消失）。
  后果链：`sample --check` 变红 → 需重生成输入与答案键 → 旧 `out_S1.md` 不再是磁盘上那 10 条 → `verify-sample` 变红 → 需再派一次
  `auditor-sample-s1`。**裁决一条 ≠ 改一个单元格**，派发前先按这个链路估工。
  根治办法（未实施）：把 `sample` 语义从「当前池」改为「池快照」（在答案键里记抽样时点的池），使已完成抽检对后续裁决免疫。
- 争议条目登记在 `litrev/_probe/audit/DISPUTED.md`（人工维护，不进 `BATCHES.json`、不贴给任何子代理）；
  `REVIEW_NONSUPPORTED.md` 是 `review` 自动生成的非 SUPPORTED 清单，两者不要混写。
- 抽检结论写进 `reports/`：命中率、方向、差异条目、是否补证据、裁决结果。`out_S1.md` 不进 131 条汇总（`audit-count` 默认前缀 B,R）。

### 金标准（判得对的参照系，2026-11-10 加入）

抽检只测**自洽**（同模型两次判定），不测**准确性**——抽的人和被抽的人是同一个判定者。要测准确性，必须有独立参照系：

```bash
python tools/audit_prep.py golden             # 分层抽 25 条（S15/P9/U1，seed=43）→ GOLDEN.md + GOLDEN_MAP.md
python tools/audit_prep.py golden --check     # 复算比对，判定表一变就报不一致
# 人填完 GOLDEN.md 的判定表（开卷，可读卡片原文，不读 out_*/答案键）
python tools/audit_prep.py verify-golden      # 比对人判 vs 判定表，输出一致率与方向分布
```

- `GOLDEN.md` 是给人填的表，**不进 `BATCHES.json`、不生成 agent、不被 `audit-count` 扫**（文件名不是 `out_*`）。
- `GOLDEN_MAP.md` 是答案键（G id → 原批次/原判定），主控留档，**不贴给任何人**；判定者填表时读不到它。
- `verify-golden` 的一致率是判定表可信度的**唯一估计**；差异不自动触发重审，按 §五「差异 ≠ 错误」登记 `DISPUTED.md` 后人工裁决。
- `golden --check` 只比对 `GOLDEN_MAP.md`（答案键）+ `GOLDEN.md` 的条目详情部分；**人填的判定表不纳入比对**（填后必然不等于空模板）。判定表一变，`GOLDEN_MAP` 即失效。

### 固定契约双跑（测漂移率，2026-11-10 加入）

round-04 用「跨版本重审」当双跑，得到 14.3% 漂移上界，但混入了契约版本变更。正规做法是**固定契约、同输入、另存对照**：

```bash
# REST 五批：派 auditor-rest-b{1-5}-dup（输入 REST_B*.md、输出 out_D{1-5}.md，不覆盖 out_R*.md）
python litrev/litrev.py audit-count --prefixes D --check   # 双跑 5 表自洽（D 不进 131 口径）
python tools/audit_prep.py diff-dup                        # 默认 R:D，输出漂移率

# frag 三批：派 auditor-frag-b{1-3}-dup（输入 FRAG_B*.md、输出 out_E{1-3}.md，不覆盖 out_B*.md）
python litrev/litrev.py audit-count --prefixes E --check
python tools/audit_prep.py diff-dup --pair B:E             # 前缀可配，默认 R:D
```

- 双跑测的是「同输入重复判定的随机漂移」，**不裁定谁判对**。
- 漂移率给「抽检 1/N 差异是噪声还是信号」一个基线；漂移率 ≠ 0 是预期，不是失败。
- 顺序派发（不并发），避免资源竞争噪声污染一致性测量。
- **已测基线（2026-11-10，v1.1 固定契约）**：

  | 配对框 | 条数 | 支撑 | 自足 | 任一 | 方向 |
  |---|---|---|---|---|---|
  | `R:D` | 83 | 8.4% | 12.0% | 20.5% | 自足 **10/10** SELF→DEP |
  | `B:E` | 48 | 12.5% | 4.2% | 16.7% | 支撑 S→P 5 / P→S 1；自足两向各 1 |
  | 合并 | 131 | 9.9%（9:4） | 9.2%（**11:1**） | 19.1% | — |

- **读数纪律**：自足轴 11:1 单向，二项检验 `P≈0.3%` → 属**系统性口径差**（重复判定更倾向判 `DEPENDENT`），
  且集中在长引文的 REST 批次（frag 侧几乎不漂）。支撑轴 9:4 单向，`P≈13%` → **不显著**，只能说方向提示偏松，
  不能据此断言判定表系统性偏松，更不能据此整批重审。
- 两组配对框不重叠（83+48=131），但 D 与 E 是不同 agent 实例、不同批次类型 → 合并值只作量级参考，
  **不得表述为「131 条在同一条件下的双跑」**。

## 六、权限回归测试（每次改权限必跑）

改完 `.opencode/agents/` 里的 permission，逐条实测下列用例，**记录返回原文**（拒绝时错误信息里带完整 ruleset，这是证据）：

> 用例 1–4 需要存在 `ex-` 实例。生成器现在只为「还没有卡片」的文献建 `ex-`，当前 22 篇都有卡片，所以 1–4 暂时没有对象；新增文献后跑一次生成器即可恢复。

| # | 角色 | 动作 | 预期 |
|---|---|---|---|
| 1 | `ex-<A>` | 读 `texts/<A>.txt` | 允许 |
| 2 | `ex-<A>` | 读 `texts/<B>.txt`（别的文献） | **拒绝** |
| 3 | `ex-<A>` | 读别人的卡片 | **拒绝** |
| 4 | `ex-<A>` | 写别人的卡片 | **拒绝** |
| 5 | `qx-<A>` | 改 `notes/<A>.md` | 允许 |
| 6 | `qx-<A>` | 改 `notes/<B>.md` | **拒绝** |
| 7 | `auditor-<批次1>` | 读 `FRAG_B2.md`（别的批次） | **拒绝** |
| 8 | `auditor-<批次1>` | 读 `out_B2.md`（别人的结果） | **拒绝** |
| 9 | `auditor-<批次1>` | 写 `out_B1.md` | 允许 |
| 10 | `auditor-<批次1>` | 用 bash 写文件 | **拒绝**（bash 全禁） |
| 11 | `checker` | `python litrev/litrev.py verify <稿>` | 允许 |
| 12 | `checker` | `python litrev/litrev.py text`（会写文件） | **拒绝** |
| 13 | `checker` | 直接 edit 稿件 | **拒绝**（edit 全禁） |
| 14 | 任意 subagent | 读 `litrev/_probe/AUDIT_CONTRACT.md` 以外的手写规则 | 按各自 allow 列表 |

注意两个机制的差别（上一轮踩过）：

- 若某类工具**只有** `"*": deny` 一条规则，OpenCode 在**暴露工具前**就把它过滤掉，模型看不到该工具，探针拿不到"拒绝"原文——这是设计，不是权限失效。要验"不能写"，得走它确实持有的工具（通常是 bash）。
- `read` 的禁读**不会**自动覆盖 `grep`/`glob`。三者要分别设。

## 七、已知残余风险（本轮未消除，别当成已解决）

1. **主控自身不受约束**：`orchestrator` 是 primary，bash/edit 没有 permission 限制。规程要求它不跑裁判、不代写，但这靠自律。要封死需给 primary 也加 permission 并实测（下一轮验证项）。
2. **`verify` 会写派生报告**：`checker` 的 edit 全禁，但 `verify` 自己会在稿件同目录生成 `<稿名>_引文核验.md`。这是裁判写的派生文件，不是改稿；证据是 `git diff` 里只有新增报告、没有原稿改动。
3. **静态权限 ≠ 任务级沙箱**：本次用「按文件生成 agent」逼近任务级隔离（每篇文献一对 `ex-`/`qx-`，每个批次一个 `auditor-`）。代价是 agent 数量随文献数线性增长，新增文献必须跑生成器。
4. **`subagent_depth = 1`**：仍是单层。不要在 Litreview 里为了"看起来更像多智能体"而打开二级调度——本项目的任务不需要。要做二级调度，在 `Opencode_Subagent` 项目里单独验证。另：新版本 OpenCode 文档把该键放进 `experimental`，升级时按实际 Schema 核对，不要照搬根级写法。
5. **工具与路径的匹配细节未完全查明**：复合 bash 命令（`;` 拼接）的匹配规则不直观，已实测出现过"部分放行"的怪现象。因此 `checker` 的命令一律写成**单条、不带 `cd`、不带 `&&`**。
6. **版面重建对公式/上下标区无效**：`text` 能把逐词断行修成正常行（Borner 1.03→7.87 词/行、Zhang 3.08→6.83），但含上下标的公式区仍会交错（`Zhang2006` p.2 的 `m m, c m, is the upper limit of m`）。这类区域不要从 txt 抄引文，改成挑同一段里不含公式的句子，或标注为已知问题。
7. **Borner1993 是 Type3 字体**：`fi`/`fl`/`ff` 连字没有 ToUnicode，被丢成空格（`The rst`、`ap proach o ers`、`modi cation`，约 0.9% 的 token）。`verify` 按 txt 比对放行，但引文里带这种缺口不能直接用在成稿；要么按原样保留并注明，要么避开该词。

## 八、变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-09 | 建立本规约；agents 改为模板生成（`AGENT_ROLES.md` + `gen_subagents.py`）；验收、空结果恢复、抽检、权限回归四条规程成文 |
| 2026-11-10 | §五 抽检候选集改为「当前 SUPPORTED」（`tools/audit_prep.py`），新增答案键闭卷纪律、`--check` 复现校验与 `verify-sample` 机械验收；`litrev.py` 未改 |
| 2026-11-10 | §五 补「差异 ≠ 错误」与方向分治：抽检降档**不自动**触发整批重审；新增争议项登记、答案键冻结、补证据两条正规路径，`verify-sample` 提示语同步按方向输出；判定表、`litrev.py`、`AUDIT_CONTRACT.md` 与 agent 定义均未改 |
| 2026-11-10 | §五 加金标准（`golden`/`verify-golden`）与固定契约双跑（`dup`/`diff-dup`）两条规程；新增 `tools/check.py` 一键回归（8 项结构性检查）；修 auditor 读回权限（read 加 `out_*` allow，需重启）；加 5 个 dup agent；删 round-03 遗留 `out_REWORK3`/`out_SAMPLE3` |
| 2026-11-10 | 双跑 5 批完成（漂移率：支撑 8.4% / 自足 12.0% / 任一轴 20.5%；自足轴 10/10 单向 SELF→DEPENDENT）；金标准 25 条填完（一致率 92%，2 条偏松 G03/G18）；修 `golden --check`（已填 GOLDEN.md 不再误报）；D-01 仍 OPEN，建议第三次独立判定 |
| 2026-11-10 | 双跑扩到 frag 三批（`--pair B:E`）：支撑 12.5% / 自足 4.2% / 任一 16.7%；**合并 131 条配对**任一轴 19.1%，自足轴 11:1 单向（`P≈0.3%`，系统性口径差）、支撑轴 9:4（`P≈13%`，不显著）。§五 增「改判的级联代价」（改判会移动抽检候选池、作废现有批次；实测重抽仅 4/10 重合）。D-01 证据到位（v1.1 下支撑 3:1），待裁决 |
