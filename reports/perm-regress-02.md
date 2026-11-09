# perm-regress-02：T3 权限回归（14 条）

- 日期：2026-11-09
- 依据：`HANDOFF-03.md` T3 + `RUNBOOK.md` §六。
- 方法：每个角色单独会话实测；写权限用**存在且不同**的 oldString/newString 真正触发权限检查。允许写入的测试文件（`out_B1.md`、`full/Ahmed2013...md`）在测试后已用 `git checkout --` 还原，未留下内容改动。
- 被拒时保留工具返回的完整 ruleset；只有工具本身未挂载时记“不可用”。

## 一、14 条结果

| # | 角色 | 动作 | 预期 | 结果 | 原文摘要 |
|---|---|---|---|---|---|
| 1 | `ex-ahmed2013-...` | 读 `texts/Ahmed2013...txt` | 允许 | **允许** | 读到 `# SOURCE: Ahmed2013_Analysis_SketchRetri...` |
| 2 | `ex-ahmed2013-...` | 读 `texts/Borner1993...txt`（别的文献） | 拒绝 | **拒绝** | 完整 ruleset 见 §二.1 |
| 3 | `ex-ahmed2013-...` | 读 `notes/Napps2021...md` | 拒绝 | **拒绝** | 同 §二.1 的 read ruleset |
| 4 | `ex-ahmed2013-...` | 写 `notes/Napps2021...md` | 拒绝 | **拒绝** | 完整 edit ruleset 见 §二.2 |
| 5 | `qx-ahmed2013-...` | 改自己的 `full/Ahmed2013...md` | 允许 | **允许** | `Edit applied successfully.`（已还原） |
| 6 | `qx-ahmed2013-...` | 改 `full/Gu2024...md`（别人的卡片） | 拒绝 | **拒绝** | 完整 edit ruleset 见 §二.3 |
| 7 | `auditor-frag-b1` | 读 `FRAG_B2.md`（别的批次） | 拒绝 | **拒绝** | 完整 ruleset 见 §二.4 |
| 8 | `auditor-frag-b1` | 读 `out_B2.md`（别人的结果） | 拒绝 | **拒绝** | 同 §二.4 的 read ruleset |
| 9 | `auditor-frag-b1` | 写 `out_B1.md`（本批输出） | 允许 | **允许** | edit 成功（已还原） |
| 10 | `auditor-frag-b1` | 用 bash 写文件 | 拒绝 | **不可用** | 本会话未挂载 `bash` 工具，未执行 |
| 11 | `checker` | `verify` 一篇稿件 | 允许 | **允许** | 退出码 0，`PASS=8 合计 8` |
| 12 | `checker` | `python litrev/litrev.py text`（会写文件） | 拒绝 | **拒绝** | 完整 ruleset 见 §二.5 |
| 13 | `checker` | 直接 edit 稿件 | 拒绝 | **不可用** | 本会话未挂载 `edit` 工具，等同拒绝 |
| 14 | 任意 subagent 读手写规则 | `auditor-frag-b1` 读 `AGENT_ROLES.md` | 按 allow 列表 | **拒绝** | 同 §二.4 的 read ruleset |
| 14b | 任意 subagent 读手写规则 | `ex-ahmed2013-...` 读 `AGENT_ROLES.md` | 按 allow 列表 | **拒绝** | 同 §二.1 的 read ruleset（只放行 CONTRACT + 本篇 txt） |

**四条新增用例全部符合预期**：2 拒绝、7 拒绝、9 允许、12 拒绝。

## 二、完整 ruleset（拒绝原文）

### 1. ex-ahmed 读别的文献 / notes（#2、#3、#14b）

```
The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"read","pattern":"*","action":"allow"},{"permission":"read","pattern":"*.env","action":"ask"},{"permission":"read","pattern":"*.env.*","action":"ask"},{"permission":"read","pattern":"*.env.example","action":"allow"},{"permission":"read","pattern":"*","action":"deny"},{"permission":"read","pattern":"litrev/_probe/CONTRACT.md","action":"allow"},{"permission":"read","pattern":"litrev/_probe/texts/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.txt","action":"allow"}]
```

### 2. ex-ahmed 写 notes/Napps（#4）

```
The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"edit","pattern":"*","action":"deny"},{"permission":"edit","pattern":"litrev/_probe/notes/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md","action":"allow"}]
```

### 3. qx-ahmed 写别人的卡片（#6）

```
The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"edit","pattern":"*","action":"deny"},{"permission":"edit","pattern":"litrev/_probe/full/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md","action":"allow"}]
```

### 4. auditor-frag-b1 读别的批次/别人的结果/手写规则（#7、#8、#14）

```
The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"read","pattern":"*","action":"allow"},{"permission":"read","pattern":"*.env","action":"ask"},{"permission":"read","pattern":"*.env.*","action":"ask"},{"permission":"read","pattern":"*.env.example","action":"allow"},{"permission":"read","pattern":"*","action":"deny"},{"permission":"read","pattern":"litrev/_probe/AUDIT_CONTRACT.md","action":"allow"},{"permission":"read","pattern":"litrev/_probe/audit/FRAG_B1.md","action":"allow"}]
```

### 5. checker 运行 text（#12）

```
The user has specified a rule which prevents you from using this specific tool call. Here are some of the relevant rules [{"permission":"*","action":"allow","pattern":"*"},{"permission":"bash","pattern":"*","action":"deny"},{"permission":"bash","pattern":"python litrev/litrev.py verify*","action":"allow"},{"permission":"bash","pattern":"python litrev/litrev.py matrix*","action":"allow"},{"permission":"bash","pattern":"python litrev/litrev.py locate*","action":"allow"}]
```

## 三、写权限测试的方法说明

第一次探针用 `oldString === newString`，edit 工具在权限检查前做了幂等短路，返回 `No changes`，无法区分“允许”和“拒绝”。因此对 #4、#6 改用**存在且不同**的 oldString/newString：

- #4 ex-ahmed 写 notes/Napps：被 edit ruleset 拒绝，文件未改。
- #6 qx-ahmed 写 Gu 卡片：被 edit ruleset 拒绝，文件未改。
- #5 qx-ahmed 写自己的 Ahmed 卡片：`Edit applied successfully.`，随后 `git checkout --` 还原。
- #9 auditor-frag-b1 写 out_B1：edit 成功，随后 `git checkout --` 还原。

测试后已确认：

- `notes/Napps2021...md`、`full/Gu2024...md`、`full/Ahmed2013...md`、`audit/out_B1.md` 均无残留改动。
- 未创建 `litrev/_probe/audit/_perm_probe.md`。

## 四、结论

- 14 条用例齐全；四条新增用例 2/7/9/12 全部符合预期。
- `ex-` 只能读自己的 txt + CONTRACT；`qx-` 只能写自己的卡片；`auditor-<批次>` 只能读本批输入 + 契约、只能写本批输出；`checker` 只能跑 verify/matrix/locate，不能 text，也没有 edit 工具。
- 权限层与 RUNBOOK §六 的预期一致；没有发现新的越界缺口。
