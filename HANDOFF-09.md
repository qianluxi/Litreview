# HANDOFF-09：抽取通道第二次实测 —— 7 节卡片能不能真的进判定表

> 本轮只做 1 个 task。HANDOFF-08 证到了「抽取工读不到别人的文献」（权限成立），
> 但同时暴露两个更致命的问题：**抽出来的是「任意三句」**（与旧卡片引文交集 0），
> 且**落点回退到 `notes/`**（审计只读 `full/` 的 7 节卡片）——也就是说，
> 新文献抽出来的东西，按现状永远进不了判定表。
>
> 这两个问题本轮已改成机械可查的约束（见 §二）。本轮的任务是**用一次真实派发证明它通了**。
>
> **本轮不碰**：`out_*.md`、`BATCHES.json`、`AUDIT_CONTRACT.md`、任何 `full/*.md` 存量卡片、
> 判定表口径（`S87/P43/U1`）。

## 一、和第 08 次相比改了什么（都已落盘，不是计划）

| # | 问题 | 08 次的状态 | 本轮 |
|---|---|---|---|
| 1 | 抽取工不知道「抽哪些」 | 模板只写「怎么抄」，没写「抄哪些」→ 任意三句 | 模板改成**固定 7 节**，每节写明「要交代什么 / 常见写错」，见 `AGENT_ROLES.md` extractor 段 |
| 2 | 落点回退 `notes/`，审计不读 | `full/` 不存在就落 `notes/` | 新卡片**恒定落 `full/`**；`notes/` 下 3 篇早期基线原地不动、不另建副本 |
| 3 | 作者/年份靠模型猜 | 模板写 `(Author, Year, p.N)`，模型自己编 | 由生成器从 `aliases.json` + 文件名**算定并写进提示词**；算不出就**拒绝生成** `ex-` 并说明原因 |
| 4 | 结构没人查 | 只能靠人眼看 | 新增 `litrev.py card-check`：7 节齐全、节名逐字、每节 1 条引文、未涉及不带引文、标注能对上、无重复引文、引号数对齐 |

`card-check` 不是"建议"，已进 `tools/check.py`（现在是 **10 项**）；对存量 19 张卡片跑
`19/19 通过、131 条引文`——正好等于判定表条数，这个恒等式本身就是「7 节 × 每节 1 条」的直接证据。

## 二、演练对象与当前状态（已落盘，不要再改）

| 项 | 值 |
|---|---|
| 对象 | `Napps2021_BIM_VariantRetrieval_CBR` |
| 为什么还是它 | 它的卡片在 `notes/`（旧基线）、**不进 131 条判定表**（贡献 0 行）；移出后 `check.py` 仍 10/10 全绿，零波及 |
| 旧卡片 | 已备份 `$TEMP/litrev-drill-09/original_card.md`，1150 B，md5 `8aced5a8402184b41525a00f44c339ef` |
| 当前状态 | 旧卡片**已移出**（`git status` 显示 ` D notes/Napps2021_….md`，这是演练态） |
| 抽取工 | `.opencode/agents/ex-napps2021-bim-variantretrieval-cbr.md` 已生成，agent 文件 43 → **44** |
| 它的权限 | 读 = `CONTRACT.md` + 自己那篇 txt；写 = **只有 `litrev/_probe/full/Napps2021_….md`**；`bash`/`grep`/`glob` 整类不注册 |
| 提示词里的标注 | 已注入 `(Napps, 2021, p.N)`，模型不需要猜作者年份 |

## 三、派发前必须做的一件事：重启 OpenCode

`ex-` 定义是刚才才落盘的，**注册表只在启动时加载**。不重启会得到
`Unknown agent type`（round-11 踩过）。重启后先跑：

```bash
python tools/check.py
```

必须看到 `✓ 全部机械自检通过`（10 项）。红的先别派。

## 四、派发（1 个 task，逐字照发）

```
按 HANDOFF-09.md 做抽取，用 ex-napps2021-bim-variantretrieval-cbr 这个子代理。

它只能读 litrev/_probe/CONTRACT.md 和 litrev/_probe/texts/Napps2021_BIM_VariantRetrieval_CBR.txt，
只能新建 litrev/_probe/full/Napps2021_BIM_VariantRetrieval_CBR.md。

严格按 AGENT_ROLES.md / CONTRACT.md 的 7 节结构写：七个节标题的字、编号、顺序都不能改，
每节一行「- 论断：」+ 一行「- 引文："逐字原文" (Napps, 2021, p.N)」；
某节原文确实没有就写「- 论断：未涉及」，不留引文行。

引文要逐字、≥20 个英文字母、不跨页、页码取 <<<PAGE n>>> 的实际 n、
从句子开头起抄（不要图表标题或句中片段）、除引文外不出现英文双引号。
不要读 full/ 下别的卡片、不要读任何 out_*.md、不要读别的文献。

写完停下，报「已写入 full/Napps2021_BIM_VariantRetrieval_CBR.md：N 节，M 条引文」。
```

不要在同一句里追加权限反例——权限四条已在 `reports/perm-regress-03.md` 实测过，
本轮验的是**格式与路由**，不是权限。省下来的时间让它在 7 节上多花点。

## 五、验收（主控侧跑，逐条机械判定）

```bash
# 1. 结构门禁（这是本轮的核心验收）
python litrev/litrev.py card-check --only Napps2021_BIM_VariantRetrieval_CBR
#    必须：1/1 全部符合 7 节结构；且 [i] 片段提示为 0 条

# 2. 引文真假（逐字 / 页码 / 作者）
python litrev/litrev.py verify litrev/_probe/full/Napps2021_BIM_VariantRetrieval_CBR.md
#    必须：PASS=N 合计 N，退出码 0

# 3. 没污染别处
python tools/check.py            # 必须 10/10
git status --short               # 只应出现演练态的几行，不许有别的 out_*.md / full/*.md 变动
```

人工只判一件事：**7 条引文是否各自真的在回答那一节的问题**（前者是机械的，这一条只能是判断）。
逐条对照 table 里「要交代什么」一栏，不合格的单条记下来，不要整份推翻。

## 六、结论判定（三选一，别含糊）

| 档 | 条件 | 含义 |
|---|---|---|
| **通** | card-check 1/1、verify 全 PASS、片段 0 条、7 节都在回答本节问题 | 抽取通道可投产；新文献进场路径打通 |
| **格式通、内容偏** | 机械全绿，但若干节的论断与引文不咬合 | 通道可用，模板的"七节判断标准"要再加例子；不改权限、不改落点 |
| **不通** | card-check 或 verify 红 | 先看红在哪：结构红 = 模板表达不清；verify 红 = 抽取工在编引文（严重，要查它读了什么） |

**不要做的**：不要为了让 card-check 变绿而手改子代理产出的卡片。改了就分不清是
"模板教会了它"还是"你替它写对了"，这一轮的全部意义就是区分这两件事。

## 七、收尾（主控执行，可回滚）

```bash
# 还原旧卡片（md5 应回到 8aced5a8402184b41525a00f44c339ef）
cp "$TEMP/litrev-drill-09/original_card.md" litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md
md5sum litrev/_probe/notes/Napps2021_BIM_VariantRetrieval_CBR.md

# 生成物收进沙盘留档（非 out_*，不进 131 口径），再重生成 agent 定义（44 → 43）
mv litrev/_probe/full/Napps2021_BIM_VariantRetrieval_CBR.md litrev/_probe/audit/DRILL_09_card.md
mv litrev/_probe/full/Napps2021_BIM_VariantRetrieval_CBR_引文核验.md litrev/_probe/audit/DRILL_09_card_引文核验.md 2>/dev/null
python tools/gen_subagents.py && python tools/gen_subagents.py --check && python tools/check.py
```

## 八、演练成功后的一条岔路（要你定，不自动做）

如果结论是「通」，`full/Napps2021_….md` 就是一张合格的 7 节卡片。收下它意味着：

- 判定表从 131 条变 **138 条**（新增 7 条，全部未判）；
- 要追加一个审计批次（`BATCHES.json` 注册 + `out_*.md`），走一次闭卷判定；
- `notes/` 下那份 3 条目旧基线随之作废（`audit-count` 不读它，但两处并存会误导后来人）。

**代价是一次派发 + 7 条判定**，收益是"新文献能进表"从演示变成既成事实。**不做的代价也很低**：
`full/` 里没有它，判定表不动，演练产物留档在 `audit/DRILL_09_*` 里，
下次真要收新文献时，路径已经验过了。

我的建议：**先不收**。演练的目的是证明通道通，不是急着加 7 条待判条目；
真加的时候应该和下一篇新文献一起批量进，而不是为一条演练品单开一轮判定。

## 九、本轮**没有**解决的事（别当成已修）

1. **`WangHoward1991` 仍是扫描件**（文字层 0 词/行），要么 OCR、要么视觉抄录。生成器会跳过它并说明原因，但它的证据永远缺一块。
2. **`notes/` 下 3 篇早期基线仍是条目式**（`Ayzenshtadt2016`、`MaherGomez1997`、`Napps2021`），不在判定表内。要把它们纳入，得各自重抽一次 7 节卡片——不是本轮的事。
3. **43 条 PARTIAL 里 42 条一次都没动过**（`R2-15` 处置了一半，仍差一个括注）。那是稿件层工作，与抽取通道无关，仍挂着。
4. **`aliases.json` 是手工维护的**：新文献文件名不是 `AuthorYYYY_xxx` 时，生成器会拒绝派 `ex-` 并让你改文件名或补登记——这是设计，不是故障。
