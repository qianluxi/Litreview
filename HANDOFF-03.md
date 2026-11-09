# HANDOFF-03：下一轮（P0/P1 收口）

> 上游依据：外部审阅意见（P0/P1/P2 清单）+ 本轮代码修复。
> **角色定义、权限、验收规程已经在代码里改完了**，本轮只剩四件必须在 OpenCode 里跑的事。
> 规程见 `RUNBOOK.md`；角色规则见 `litrev/_probe/AGENT_ROLES.md`；派活先查 `litrev/_probe/AGENT_MAP.md`。

## 已完成，勿重跑

| 项 | 落点 | 证据 |
|---|---|---|
| Extractor 拆成「首次抽取 / 返工扩句」两个角色，输出目录矛盾消除 | `AGENT_ROLES.md` + `.opencode/agents/ex-*` / `qx-*` | `gen_subagents.py --check` 55 个文件同步 |
| Auditor 提示词不再复述判定规则，唯一来源 = `AUDIT_CONTRACT.md`（含 §五、§七） | `AGENT_ROLES.md` ROLE: auditor | 生成物里搜不到"自足轴只看主语"旧句 |
| Auditor 按批次隔离（只读本批、只写本批输出） | `audit/BATCHES.json` + `auditor-<批次>` 9 个 | 每份 frontmatter 只 allow 自己那两行路径 |
| Checker 加权限：edit 全禁、bash 只放行 verify/matrix/locate | `.opencode/agents/checker.md`（生成） | frontmatter 可见白名单 |
| Extractor 文件级隔离（只读自己那篇 txt、只写自己那条笔记） | `ex-*` / `qx-*` 44 个 | 同上 |
| 任务验收协议 + 空结果恢复规程 | `orchestrator.md` + `RUNBOOK.md` §三/§四 | — |
| 14 条片段的根因修复（版面重建） | `litrev.py text`；Borner 1.03→7.60 词/行，Zhang 3.08→6.33 | 131 条引文重跑 verify 仍 131/131 PASS |
| SUPPORTED 抽检机械化 | `litrev.py sample` | `audit/SAMPLE_S1.md` 已生成（16/131，seed=42） |

## T0 开工自检（必须先跑）

```bash
python tools/gen_subagents.py --check
python litrev/litrev.py text --dry-run
python litrev/litrev.py index
python litrev/litrev.py verify litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md
```

四条全绿再动手。`--check` 报不一致 → 先 `python tools/gen_subagents.py` 覆盖，不要在生成文件上手工修补。

## T1（P2 → 现在可做）14 条片段引文扩句

- **派给**：`qx-borner1993-structuralsimilarity-cbr`、`qx-zhang2006-bp-caseretrieval-highrisestructureform`（**一次一条笔记**，不要合并派发）
- **输入**：各自 `litrev/_probe/texts/<文献>.txt`（已换成版面重建版）+ 自己那条 `notes/<文献>.md`
- **要改哪些**：`litrev/_probe/audit/C4_FRAG_RESULT.md` §三 里这两篇的条目（Borner 7 条：一句话主张/问题域/表示形式/检索机制/系统形态/评价方式/局限；Zhang 7 条同构）。**主控把这个清单写进 task 提示词**——`qx` 没有读审计结果的权限。
- **约束（已写进角色）**：只向前后扩；不跨页；含连字缺口的词按原样保留（`modi cation`、`speci c`），**不许补字母**；扩不动写 `- 无法扩句: 原因`。
- **完成条件**：两个 agent 都写出更新后的笔记 → `checker` 跑 `python litrev/litrev.py verify litrev/_probe/full/<文献>.md`，两篇合计 14 条仍全部 PASS，且 `C4_FRAG_RESULT.md` 里标 DEPENDENT 的条目在新引文中不再出现"开头即代词/指示代词无指代对象"。
- **产出报告**：`reports/round-03-expand.md`，逐条列「旧引文 / 新引文 / 页 / 判定变化」。

> 这条以前做不成，是因为文字层本身碎了（扩句只会把碎片拉长）。现在 txt 的句子是完整的，可以做；但 Borner 的 Type3 连字缺口仍在（0.9% 的 token），见 `CORPUS_TEXT_HEALTH.md` 末节。

## T2（P0）SUPPORTED 抽检 S1

- **派给**：`auditor-sample-s1`
- **输入**：`litrev/_probe/audit/SAMPLE_S1.md`（16 条，seed=42、12.2%，**不要换种子**）
- **输出**：写 `litrev/_probe/audit/out_S1.md`
- **完成条件**：16 行 + 合计行；16/16「依据」列的词能在该条引文里逐字命中。
- **判据**：拿 `out_S1.md` 与 `out_B*/out_R*` 的既有判定逐条对照。
  - 抽检里出现"该判 PARTIAL 却给了 SUPPORTED" → **整批重审**（对应的 `auditor-rest-b*`），不逐条修补；
  - 0 命中 → 在报告里写明抽检比例与命中率，作为"SUPPORTED 可信度"的唯一证据。
- **产出**：`reports/round-03-sample.md`（命中率、偏松方向、是否触发整批重审）。

## T3（P1）权限回归（14 条用例）

按 `RUNBOOK.md` §六 的表逐条实测。重点新增的四条（上一轮没测过）：

| # | 角色 | 动作 | 预期 |
|---|---|---|---|
| 2 | `ex-<A>` | 读 `texts/<B>.txt` | 拒绝 |
| 7 | `auditor-frag-b1` | 读 `FRAG_B2.md` | 拒绝 |
| 9 | `auditor-frag-b1` | 写 `out_B1.md` | 允许 |
| 12 | `checker` | `python litrev/litrev.py text`（会写文件） | 拒绝 |

- **记录**：被拒时错误原文里带完整 ruleset，原样贴进报告，不要转述。
- **注意**：若某工具只有 `"*": deny` 一条规则，模型看不到该工具（暴露前就被过滤），拿不到拒绝原文——这是设计，改用它确实持有的 `bash` 验证。
- **产出**：`reports/perm-regress-02.md`，逐条「角色/动作/结果/原文摘要」。

## T4（P1）不做的事，写清理由

- **不加二级调度**：`subagent_depth` 保持 1。Litreview 的任务是"两三个人干同一层的活"，加层级只会增加空结果与权限传递的复杂度。要在 `Opencode_Subagent` 项目里单独验证。
- **不给 primary 加权限限制**：本轮未做（`orchestrator` 的 bash 仍不受约束）。这是已知残余风险第 1 条，下一轮如果要封，先设计"主控只读 + checker 独占执行"的规则再改，不要边跑边调。

## T5（P2）WangHoward1991 去留

`王氏 1991` 是 130 页扫描件，文字层 0 字符，生成器已**不为它生成抽取工**。

- 决策一：不引用 → 在 `_probe/RESULT.md` 里标注"无文字层，未纳入"。
- 决策二：要引用 → 先 OCR 出 txt，再跑 `gen_subagents.py` 生成 `ex-`/`qx-`，然后照常派活。

**不要**在没 OCR 的情况下给它派 `ex-`：agent 会被生成器拒绝，硬派只会得到一次失败调用。

## 全局验收

| 项 | 通过标准 |
|---|---|
| T1 | 两篇 14 条扩句后 `verify` 全 PASS；报告列出每条新旧对照 |
| T2 | `out_S1.md` 存在且 16 行；报告写明命中率与是否整批重审 |
| T3 | 14 条用例结果齐全；4 条新增用例全部符合预期 |
| 总 | `reports/round-03-*.md` 三份齐；`git status` 里没有意外改动（尤其 `litrev/litrev.py`、`tests`、契约文件） |

## 禁止

- 不用 `ex-` 做返工（它只会报"文件已存在"）、不用 `qx-` 做首次抽取（文件不存在它无从改）。
- 不让主控代跑 `verify` 出判定；不让主控代写笔记。
- 不改 `AUDIT_CONTRACT.md` 的判定规则来"迁就"结果；要改先停下来说明理由。
- 不用新种子重抽 S1（会失去可比性）。
- 不手工编辑 `.opencode/agents/` 下带 `AUTO-GENERATED` 的文件。
