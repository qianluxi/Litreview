# perm-regress-03：抽取通道（`ex-`）首测 + primary 不受约束实测

- 日期：2026-11-10
- 依据：`HANDOFF-08.md`（受控盲抽 Napps2021）+ `RUNBOOK.md` §六/§七
- 方法：把 `notes/Napps2021_BIM_VariantRetrieval_CBR.md` 临时移出（备份 1150 B，md5 `8aced5a8…`）→
  重跑生成器得到 `ex-napps2021-bim-variantretrieval-cbr`（43→**44** 个 agent）→ 派 1 个 task 盲抽 →
  同一批指令分别在 **subagent** 与 **orchestrator（primary）** 两个身份下各发一次。
- 演练期间 `check.py` 保持 **9/9 全绿**（`notes/` 不进 131 条口径，`audit-count`/`audit-stale` 零波及，这是选该对象的理由）。

## 一、抽取结果（结构 6 条全过）

`task` 新建了卡片，`python litrev/litrev.py verify` 结果：**`共 3 条 / PASS=3`**，页码标注与实际页逐一吻合。

| # | 检查项 | 标准 | 实测 |
|---|---|---|---|
| 1 | 文件存在、标题行 | `# Napps2021_BIM_VariantRetrieval_CBR` | ✓ 第 1 行 |
| 2 | `verify` 逐字命中 | 0 失败 | ✓ 3/3 PASS |
| 3 | 页码 | 与 `<<<PAGE n>>>` 一致 | ✓ p.1 / p.2 / p.7，核验报告「标注 vs 实际」全同 |
| 4 | ≥20 英文字母 | 每条 | ✓ 三条均远超 |
| 5 | 双引号计数 | 除引文外无多余 `"` | ✓ 只有 3 对 |
| 6 | 条目数 | 与旧卡片对照 | 3 条（旧卡也是 3 条） |

**结构、格式、纪律全对**。模板里那 6 条硬规则（逐字、≥20 字母、不跨页、页码取实际页、双引号、找不到报 NOT_FOUND）都被遵守了。

## 二、权限：同 4 条指令 × 2 个身份

| # | 指令 | `ex-napps2021-…`（subagent） | `orchestrator`（primary） |
|---|---|---|---|
| 1 | 读 `texts/Liao1998…txt` | **拒绝**（read ruleset：`*: deny` + 仅放行 CONTRACT 与本篇 txt） | **放行** |
| 2 | 读 `full/Liao1998…md` | **拒绝**（同上） | **放行** |
| 3 | 写 `full/Liao1998…md` | **拒绝**（edit ruleset：仅放行自己的 notes 目标） | **未执行**（见 §四，按 A 处理） |
| 4 | 列工作目录（`ls`/`glob`/`bash`） | **无此工具**——`bash`/`grep`/`glob` 是 `"*": deny`，在工具暴露前被过滤，模型根本看不到 | 放行（`bash`/`glob` 均可用） |

**第 4 条要写清口径**：subagent 侧不是"被拒绝"，是**工具没注册**。两种都算通过，但结论不同——
`read` 是部分 `allow`，所以工具可见、调用时才抛 `PermissionDeniedError`（拒绝原文带完整 ruleset）；
`bash`/`grep`/`glob` 是整类 `deny`，工具不存在。把前者写成"拒绝"、后者写成"不可用"，不要混。

> 证据强度说明：subagent 侧的拒绝原文由操作者按 ruleset 摘要回报（`{"permission":"read","pattern":"*","action":"deny"}` + 放行项），
> **未逐字留档**；round-11 的 3-B 探针（edit 越界、`task → general`）有逐字原文，本次没有。不影响结论，但归档强度不如前次。

## 三、结论一：抽取通道的文件级隔离成立

`ex-` 读不到别人的 txt、读不到别人的 `full/` 卡片、写不进别人的卡片、也没有 shell。
「闭卷判定」在 subagent 侧是**机制**，不是自律。`RUNBOOK.md` §七 第 8 条（"抽取通道从未实测"）可以销项。

## 四、结论二：primary 侧 0 拦截——§七.1 从「推测」变「实测」

两条只读指令在 `orchestrator` 身份下**全部放行**，无任何 ruleset 参与。

补充一条**静态证据**（比再跑一次破坏性操作更有力）：

```
opencode.json 的 permission 只有两条：webfetch: deny / websearch: deny
~/.config/opencode/opencode.jsonc 无 permission 键
```

即：主控在 `read`/`edit`/`bash` 三个面上**根本没有规则**，不存在"读放行、写另有拦截"的可能。
所以第 3 条（写 `hello` 进别人的卡片）**按方案 A 不执行**：它要证的东西已由"两次读放行 + 配置里只有两条 deny"证完，
而唯一新增的信息是"文件被破坏的那几秒"，收益为负。

顺带更正一处事实：`litrev.py`、若干卡片、`REST_B1/B2/B4` 的改动**已于 `4f8ce71` 提交**，
当前工作区在演练时只有演练态 4 个文件，不存在"并行未提交改动混进来分不清是谁改的"风险。
风险比原判断低，但结论不变——不做破坏性证据。

**因此 §七.1 现在的准确表述**：primary 不受权限约束，**已实测**（读两个受管路径均放行 + 配置层无规则），
不再是"靠自律的推测"。要封死必须给 primary 也写 permission 并重测 1–4，本项仍 OPEN。

## 五、结论三（本轮真正的坏消息）：抽取目标未定义，召回 0 重合

两次抽取都是 3 条，但**引文交集 = 0**：

| | 旧卡片（基线） | 演练新卡片 |
|---|---|---|
| 条目 1 | `outlines a solution for a BIM-based variant retrieval … using CBR and Pattern Matching (PM)` p.1 | `presents a solution for finding suitable variants … based on the IFC standard` p.1 |
| 条目 2 | `The method of graph pattern matching (GPM) …` p.3 | `The process of case-based reasoning can be represented as a cycle …` p.2 |
| 条目 3 | `the similarities are used for all entities stored in the IFC data structure …` p.3 | `a BIM-based solution for the retrieval process in the early design phase …` p.7 |

三条引文**没有一条重合**，主题也只是部分相交。原因不在审计员，在**模板没告诉抽取工"要抽什么"**：
`AGENT_ROLES.md` 的 extractor 段只规定了"怎么抄"（逐字、页码、长度），完全没规定"抄哪些"。
于是每次派发得到的是"这篇论文的任意三句"，而不是"综述需要的七个维度"。

这与 `RUNBOOK.md` §七 第 8 条原以为是"权限没测"完全不同：权限没问题，**信息目标缺失**才是拦路虎。
对生产的含义很直接——按现状派 10 篇会得到 10 份风格各异、互不可比的卡片，而且**不保证覆盖 7 节中的任何一节**。

## 六、两处必须在开生产前定掉（HANDOFF-09）

1. **抽取目标**：extractor 模板要按 7 节（一句话主张 / 问题域 / 表示形式 / 检索机制 / 系统形态 / 评价方式 / 明确局限）
   逐节要求"每节一至二条"，并允许"本节 NOT_FOUND"；否则召回随机。
2. **路由与格式**：生成器落点回退到 `notes/`（条目式），而审计 `CARD_DIR` 只认 `full/`（7 节）——
   新文献的卡片**按现状永远进不了判定表**。方案 A（extractor 直接产 7 节 + 落点恒定 `full/`）比方案 B（加 `carder` 转换角色）少一层失真。

本轮**只取证不改**（改模板要重生成全部 agent，且要重启才生效）。

## 七、留档与还原

| 项 | 位置 |
|---|---|
| 演练产出的卡片（沙盘） | `litrev/_probe/audit/DRILL_08_agent_card.md` |
| 其核验报告 | `litrev/_probe/audit/DRILL_08_agent_card_引文核验.md` |
| 原卡片备份 | `$TEMP/litrev-drill-08/original_card.md`（已还原到 `notes/`，md5 `8aced5a8…`） |

还原后：`gen_subagents --check` → 43 个文件同步（`ex-` 随卡片回归自动消失）；
`python tools/check.py` → **9/9 全绿**；工作区只剩上述两个沙盘文件未跟踪。
沙盘产物不进 131 条口径、不被任何 `glob("*.md")` 收（放在 `audit/` 下的非 `out_*` 名字）。
