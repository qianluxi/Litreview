# 运行规约（RUNBOOK）

> 这份文件把"上一次是靠人现场补救"的几件事写成规程：**派发**、**验收**、**空结果恢复**、**抽检**、**权限回归**。
> 它和 `.opencode/agents/orchestrator.md` 的关系：orchestrator 里的规则是给模型看的摘要，这里是完整规程与可复现命令。两者不一致时以本文件为准，并修 orchestrator。
>
> 适用版本：OpenCode 1.18.25（桌面客户端，无 CLI）。

## 一、开工自检（四条命令，缺一条都别派活）

```bash
python tools/gen_subagents.py --check          # 子代理定义与角色模板是否同步
python litrev/litrev.py text --dry-run         # 语料文字层健康度（词/行 < 3 的文献不能派抽取工）
python litrev/litrev.py index                  # 重建索引（改过 PDF 或 vocab 时）
python litrev/litrev.py verify litrev/_probe/full/<文献>.md   # 引文层基线
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

## 四、空结果恢复规程（逐步照做）

1. 记录该 `task` 调用返回的 `task_id`（形如 `ses_...`），不要关掉会话。
2. 先看交付文件：`notes/<文献>.md` 或 `audit/out_<批次>.md` 是否存在且非空。
   - 存在 → 视为完成，补做第三节第 3–5 条检查。
   - 不存在 → 进入第 3 步。
3. 用原 `task_id` 恢复（resume），只发一句：「上次以 completed 返回但未写 `<路径>`，请现在把结果写入该文件，不要重新分析」。
4. 恢复后仍为空 → 视为失败，记录错误原文，改派同一 agent 一次（不是换 agent）。两次都空 → 停手，写进 `reports/` 并上报，不再重试。

**不许**：把空结果当成功继续下一步；不许用主控代写补上（证据链会断）。

## 五、抽检规程

`SUPPORTED` 只是分诊结果，不是合格证（v1.1 契约 §七.2）。每轮审计后：

```bash
python litrev/litrev.py sample litrev/_probe/full --rate 0.12 --seed 42 \
  --name "SUPPORTED 抽检 S1" --out litrev/_probe/audit/SAMPLE_S1.md
python tools/gen_subagents.py          # 新增批次 → 生成 auditor-sample-s1
```

- 比例 10–15%，种子固定，**同一批数据重跑必须抽出同一组条目**（可复核）。
- 抽检条目若出现"该判 PARTIAL 却给了 SUPPORTED" → **整批重审**，不逐条修补。
- 抽检结论要写成 `audit/out_S1.md` + 一条汇总结论（命中率、偏松方向、是否整批重审）。

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
