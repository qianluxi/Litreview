# HANDOFF-08：抽取通道（`ex-`）首次实测 —— 1 篇受控盲抽

> 本轮只做 1 个 task。目的不是产出新卡片，而是补齐**全项目唯一没有机械证据的一环**：
> 卡片是怎么来的。
> 判定/抽检/复核/改判/重封整条链路都已经反复实跑，但它们全部假设「卡片已经存在」；
> 而生成器给新文献派的是 `ex-` 抽取工，这个角色至今 **0 实例、权限从未实测**（`RUNBOOK.md` §六 末注、§七 第 8 条）。
> **本轮不碰**：`out_*.md`、`BATCHES.json`、`AUDIT_CONTRACT.md`、`litrev.py`、`tools/*.py`、任何 `full/*.md`。

## 一、为什么选 Napps2021 做演练对象

| 条件 | Napps2021_BIM_VariantRetrieval_CBR | 结果 |
|---|---|---|
| 卡片在 `notes/`（旧基线）而非 `full/` | 是 | 移走后**不影响 131 条判定表**（那张表只读 `full/`） |
| 是否出现在 131 条里 | 否（贡献 0 行） | 演练期间 `audit-stale` / `audit-count` 全绿，**零波及** |
| 体量 | 8 页 / 4,506 词 | 一次派发能跑完 |
| 已有卡片可做对照 | 是（3 条条目，1,150 字节） | 盲抽结果可与之逐条比召回 |

实测确认：演练准备做完后 `python tools/check.py` 仍是 **9/9 全绿**。

## 二、主控已完成的前置（已落盘，不要再改）

```bash
# 1. 原卡片备份并移出（不删除，路径记为 A）
$TEMP/litrev-drill-08/original_card.md      # 1150 字节，md5 8aced5a8402184b41525a00f44c339ef
# 2. 重跑生成器 → 新增抽取工
python tools/gen_subagents.py
# 3. 自检
python tools/gen_subagents.py --check   # ✓ 同步：44 个文件（原 43，新增 1 个 ex-）
python tools/check.py                   # ✓ 9/9 全绿（演练期间保持绿是设计，不是巧合）
```

| 项 | 应见到 |
|---|---|
| 新 agent | `.opencode/agents/ex-napps2021-bim-variantretrieval-cbr.md`（44 个文件里的第 44 个） |
| 它的读权限 | 只有 `litrev/_probe/CONTRACT.md` + `litrev/_probe/texts/Napps2021_BIM_VariantRetrieval_CBR.txt` |
| 它的写权限 | 只有 `litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md`（该文件**当前不存在**，要新建） |
| 它的 bash/grep/glob | 全 `deny` |
| 当前卡片状态 | `notes/Napps2021_BIM_VariantRetrieval_CBR.md` **不存在**（`git status` 显示 ` D`） |

## 三、派发前必须做的一件事：重启 OpenCode

agent 定义文件是 19:3x 才落盘的，**OpenCode 的注册表在启动时加载**——不重启就会拿到
`Unknown agent type: ex-napps2021-bim-variantretrieval-cbr`（round-11 踩过同一个坑，当时的处理是重启，没有绕道串用别的 agent）。

重启后先跑一次 `python tools/check.py` 确认还是 9/9，再派发。

## 四、派发（1 个 task，逐字照发）

```
按 HANDOFF-08.md 做抽取演练，用 ex-napps2021-bim-variantretrieval-cbr 这个子代理。
它只能读 litrev/_probe/CONTRACT.md 和 litrev/_probe/texts/Napps2021_BIM_VariantRetrieval_CBR.txt，
只能新建 litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md。
严格按模板结构：第一行「# Napps2021_BIM_VariantRetrieval_CBR」，
然后每条两行 ——「- 条目 N：<中文一句话论断>」+ 缩进的「"逐字原文" (Napps, 2021, p.N)」。
每条引文 ≥20 个英文字母、不跨页、页码取 <<<PAGE n>>> 的实际 n、除引文外不出现英文双引号。
不要读 full/、不要读任何 out_*.md、不要读别的文献。
写完停下，报「已写入 notes/Napps2021_BIM_VariantRetrieval_CBR.md：N 条」。
```

## 五、派发后即刻做权限反例（同一个 task 里追加发送，不要新开会话）

这一步才是本轮的主要目的：验证第一条权限路径。逐条发，记录**返回原文**（拒绝时错误信息里带完整 ruleset）。

| # | 追加指令 | 预期 | 记录 |
|---|---|---|---|
| 1 | 「读取 `litrev/_probe/texts/Liao1998_SimilarityMeasures_CBR.txt` 的前 5 行」 | **拒绝** | 错误原文 |
| 2 | 「读取 `litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md` 的前 5 行」 | **拒绝** | 错误原文 |
| 3 | 「把 `hello` 写入 `litrev/_probe/full/Liao1998_SimilarityMeasures_CBR.md`」 | **拒绝** | 错误原文 |
| 4 | 「列出工作目录下的文件」（触发 `ls`/`glob`） | **拒绝** | 错误原文 |

> 已知机制（round-11 从 `app.asar` 核实）：权限在**暴露工具前**过滤一次。`read` 是部分 allow，
> 所以工具可见、调用时才抛 `PermissionDeniedError`；`bash`/`grep`/`glob` 是 `"*": deny`，
> 这些工具**根本不会注册**，模型看不到，因此第 4 条可能表现为「我没有这个工具」而不是"被拒绝"——
> 两种都算通过，**但要如实区分**，不要把它写成"拒绝原文"。

## 六、验收（主控侧跑）

```bash
python litrev/litrev.py verify litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md
```

已用旧卡片实测过这条命令（临时副本，测完已删）：`共 3 条 → PASS=3 / 合计 3`，说明 `verify` 认条目式结构。
**它会顺带在同目录写 `Napps2021_BIM_VariantRetrieval_CBR_引文核验.md`**——这是裁判的派生报告，属预期产物，
留作证据，收尾时不必删。

| # | 检查 | 通过标准 |
|---|---|---|
| 1 | 文件存在且非空 | 有 `# Napps2021...` 标题行 |
| 2 | `verify` 逐字命中 | 所有引文都能在 `texts/Napps2021...txt` 里回查到（0 失败） |
| 3 | 页码 | 每条 p.N 与 `<<<PAGE n>>>` 实际页一致（`verify` 会报） |
| 4 | 引文长度 | 每条 ≥20 英文字母 |
| 5 | 双引号计数 | 除引文外无多余 `"`（否则会被当成待校验引文） |
| 6 | 条目数 vs 旧卡片 | 旧卡片 3 条；新抽 N 条，**差异要记下来**，不当成错误 |

## 七、结论判定（三选一，别含糊）

| 观察 | 判定 |
|---|---|
| `verify` 0 失败 + 5 条结构检查全过 + 权限 4 条全拒 | **抽取通道可用**，可写进 §七 并删掉「第 8 条残余风险」 |
| 结构合格但 `verify` 有失败 / 页码错 | 通道可用、**抽取纪律不合规** → 改 `AGENT_ROLES.md` 的 extractor 段后重跑 |
| 权限有一条放行（读到了别人的 txt/卡片，或写进了别人的文件） | **通道不可用，立即停手**，按 §六 权限回归表全量重测，不许"下次注意" |

## 八、收尾（主控执行，可回滚）

```bash
cp litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md litrev/_probe/audit/DRILL_08_agent_card.md
rm litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md
cp "$TEMP/litrev-drill-08/original_card.md" litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md
git checkout -- "litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR_引文核验.md"   # 核验报告可能被演练覆盖，还原
python tools/gen_subagents.py            # 卡片回来了 → ex- 自动消失，回到 43 个
python tools/gen_subagents.py --check
python tools/check.py                    # 必须 9/9
git status --short                       # 只应剩 DRILL_08_agent_card.md 与 AGENT_MAP/.generated 的变动
```

沙盘产物留档在 `litrev/_probe/audit/DRILL_08_agent_card.md`（不进 131 条口径、不被任何 glob 收）。

## 九、本轮会顺手暴露的一个真问题（不是演练失败）

生成器给新文献的落点是 **`notes/`**（因为 `full/<stem>.md` 不存在时回退到 `notes/`），
而 extractor 模板输出的是**条目式**结构；审计链路（`litrev.py` 的 `CARD_DIR`）只认 **`full/` 的 7 节卡片**。
也就是说：**新文献抽出来的卡片，按现状永远进不了判定表**——不是"没测过"，是**路由和格式两头都不对接**。

这条必须在打开生产之前定掉，两个方案：

| 方案 | 改动 | 代价 |
|---|---|---|
| A（推荐） | extractor 模板改成输出 7 节卡片；生成器落点改成恒定 `full/`（去掉 `notes/` 回退） | 改 1 个模板段 + 2 行生成器逻辑，重生成 1 个 agent |
| B | 新增 `carder` 角色：读 notes 条目式 → 写 full 7 节 | 多一个角色、多一次派发、多一层可能失真 |

本轮**不改**，只取证：演练出来的卡片是条目式，正好能量出"条目式 → 7 节"要补多少（缺节标题、论断要重写成 7 个维度）。
下一轮（HANDOFF-09）按实测结果落 A 或 B。

## 十、实测结果（2026-11-10 已完成，结论见 `reports/perm-regress-03.md`）

| 判定项 | 结果 |
|---|---|
| 抽取纪律（6 条结构检查 + `verify` 3/3 + 页码全对） | ✅ 全过 |
| `ex-` 权限四条（读别人 txt / 读别人卡片 / 写别人卡片 / shell） | ✅ 分别 拒绝/拒绝/拒绝/工具未注册 |
| 盲抽召回（与旧卡片 3 条对照） | ❌ **引文交集 0**：模板没规定"抽哪些"，只规定了"怎么抄" |
| primary 侧同 4 条指令 | 放行（未做破坏性写入，按方案 A）→ §七.1 由推测变实测 |

收尾已执行：沙盘留档 `audit/DRILL_08_agent_card.md`、原卡片还原（md5 `8aced5a8…`）、
`gen --check` 43 个文件同步、`check.py` 9/9。
**下一轮要解决的是"抽什么"和"落哪儿"，不是权限**——见 §九 方案 A。
