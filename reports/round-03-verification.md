# round-03 第三方核验（T1/T2/T3）

- 核验时间：2026-11-09 17:1x
- 核验对象：`0b72f7b` 之后的工作区改动（未提交）+ `reports/round-03-*.md`、`reports/perm-regress-02.md`
- 核验方式：不读报告结论，先从文件与 `opencode.db` 重算，再与报告比对。
- 结论：**流程真的跑起来了，权限隔离真的生效，抽检真的可复算；但 131 条汇总数字全线错，T1 的 15/15 PASS 不等于 15 条都能引用。**

## 一、原生执行证据（`opencode.db`，只读）

| 项 | 实测 |
|---|---|
| 本轮 `task` 调用 | 25 次，全部 `completed` |
| 子会话 | 22 个（16:21–17:04），全部 `parent_id` 指向主控 |
| 空 `<task_result>` | **1 次**（16:21:47，输出 98 字符 = 空壳模板） |
| 空结果恢复 | 16:25:30 用同一子会话 `ses_e4099cf14fferFFtcd70FLYICv` 重取，未新建任务 |
| 真并行 | T1 两条笔记 **同一毫秒** 16:46:35 双派发；T3 17:00:19–20 四路并发 |
| 权限拒绝 | **19 次**，全部带完整 ruleset |
| 其它工具错误 | 8 次，全为 `Could not find oldString`（探针造字符串，非权限） |
| 用量 | in 1,285,884 / out 47,953 tokens，cache read 29.7M，**$0.3956** |

19 次拒绝分布：`auditor-frag-b1` read 6、`ex-ahmed` read 4、`qx-borner` read 3、`checker` bash 2、`qx-ahmed` read 2 / edit 1、`ex-ahmed` edit 1。

**判读**：`RUNBOOK §四` 的空结果恢复规程第一次在真实运行中被动用到，且用对了（同 id 续派，未产生重复任务）。这是本轮最实的一项。

## 二、T3 权限回归：通过，且是我实测过的最严一版

报告里 14 条用例齐全，4 条新增（#2/#7/#9/#12）全部符合预期。文件级隔离在数据库里有 19 条拒绝作证：

- `ex-` 读别人 txt → 拒；`ex-` 写 notes → 拒
- `qx-` 改别人卡片 → 拒
- `auditor-frag-b1` 读 `FRAG_B2.md`、读 `out_B2.md`、读 `AGENT_ROLES.md` → 全拒
- `checker` 跑 `litrev.py text` → 拒（白名单只有 verify/matrix/locate）

报告 §三 关于「`oldString === newString` 会被幂等短路、测不出权限」的发现是对的，这是上一轮我漏掉的坑。

## 三、T2 抽检：机械可复核，全部对得上

- `out_S1.md`：16 行 + 合计行，S01–S16 与 `SAMPLE_S1.md` **id 完全对齐**。
- **依据逐字命中 16/16**（脚本复核：把 out 的「依据」列逐条在对应引文里查子串）。
- 支撑分布 SUPPORTED 12 / PARTIAL 4；自足 SELF 15 / DEPENDENT 1，与合计行一致。
- 触发项溯源正确：S16 与 `FRAG_B3.md` 的 `B3-15` 是同一文献、同一字段、同一引文（Zhao2023 评价方式 p.10）。**`HANDOFF-03` 写「对应的 auditor-rest-b*」是我写错了**，实际是 `frag_b3`，报告纠正得对。
- `out_B3.md` 重审：合计行自洽（S6/P10/U0/D7），与报告 §三 表一致。

## 四、T1 扩句：verify 全过，但 3 条仍是碎片

`verify`：Borner 8/8、Zhang 7/7，共 15/15 PASS（逻辑 14 条，#5 按用户选择 B 拆 p.8 + p.9）。
仅改 `- 引文：` 行，论断与字段结构未动 —— 符合角色边界。

但 `verify` 只验字符是否逐字存在，不验句子是否立得住。逐条读下来：

| 条目 | 新引文 | 判定 |
|---|---|---|
| Borner 1/2/3/4/6/7 | 完整句，主语谓语齐全 | 可用 |
| **Borner #5 p.8** | `...and SynGraph for Synthesis by using` | 结尾悬空，无宾语 |
| **Borner #5 p.9** | `Graph based representations` | **3 个词、无谓语**，全篇最短 |
| **Zhang #7** | `experimental conclusions concerning ascertainment of ... theory.` | **无主语** |
| Zhang 2/3/4/5 | 完整句（#3 公式区乱序但 verbatim） | 可用 |
| Zhang 1/6 | `this intelligent CRM...` / `This selection...` | 指示代词，指代待复核 |
| Borner 4/6/7 | 含 `The rst`、`ap proach o ers`、`struc tural` | Type3 连字缺口，按原样保留 |

即：**14 条逻辑条目里 12 条改成完整句，2 条没成（Borner #5、Zhang #7）**。`HANDOFF-03` 的完成条件只排除了「开头即代词/指示代词」，没排除「名词短语碎片」，所以按字面判据算过、按可引用性算没过。这是判据漏洞，下一轮要补「必须含限定动词」这一条。

### Zhang #7 本可修，卡在我的版面重建

原文完整句是 `There are only some experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory.`（标题 `2.2.1 ... BP Network for Case Retrieval,` 与正文同基线连排）。

但 `texts/Zhang2006...txt` 出来的是：

```
BP for Case There only
Network Retrieval, are some
experimental conclusions concerning ascertainment of
```

`There are only some` 被拆成两行交错，qx 只能从行首 `experimental` 起句，于是丢了主语。根因在 `_block_lines` / `_xy_cut`：PyMuPDF 把这一视觉行切成两个 block，`page_layout_text` 按 block 顺序输出，**没有「同基线、x 区间交叠的两个 block 合并」这一步**。真双栏的 x 区间不交叠，所以加这一步不会误合栏。

## 五、131 条汇总：三份文档全线错

以 `out_B1/B2/B3/R1..R5` 八个文件为准（`grep -c "^| B1-[0-9]* | SUPPORTED"` + 各行「合计」行交叉验证）：

| 集合 | 文件实际 | 文档写的 |
|---|---|---|
| T2 前（HEAD `0b72f7b`） | **S88 / P42 / U1；SELF114 / D17** | S84 / P45 / U2；SELF118 / D13 |
| T2 后（工作区） | **S84 / P46 / U1；SELF112 / D19** | S83 / P47 / U1；SELF115 / D16 |

- 分批次数字**全对**（B3 = S6/P10/D7，与它自己的合计行一致）。错的只有 131 汇总。
- 特征：不是随机错，是**拿上一轮已错的基线继续加减**。上一轮 `C4_REST_RESULT.md §七` 就写着「S88/P42/U1 变为 S84/P45/U2」，但 `out_*.md` 里从来没出现过 84/45/2 —— 那个「变成」只写在文档里。
- 影响面：`reports/round-03-sample.md §三`、`C4_REST_RESULT.md §八`、`C4_FRAG_RESULT.md §八` 三处已把这个错数字固化，下一轮会继续传。

**这是老毛病的复发**：汇总不 recount，接着上一个数字推。结构性修法是给 `litrev.py` 加一个 `audit-count` 子命令，让汇总只能由机器算出来。

## 六、其它

| 项 | 状态 |
|---|---|
| `tools/gen_subagents.py` 被主控改了 11 行 | 改动**正确**（`qx_target` = `full/` 若存在，否则 `notes/`）。但这暴露两件事：① 我上一轮生成的 qx 指向了不存在的 `notes/<文献>.md`，19 篇的 T1 本来会直接失败；② 主控有源码写权限，"生成器不被改"只是约定 |
| `ex-` 落点仍是 `notes/` | 与 qx 的 `full/` 不一致。对已有卡片的 19 篇再跑 `ex-` 会在 `notes/` 造一份没人读的副本，目前只靠「禁止用 ex- 返工」的提示词挡着 |
| 互判一致率 | 16 条抽检里 4 条与旧判不同（25%）；其中 3 条是旧 PARTIAL 被判 SUPPORTED。方向不一致，不能说「新判更严」 |
| 提交状态 | HEAD 仍是 `0b72f7b`；工作区 31 个改动 + 4 个未跟踪，未提交 |
| `litrev.py` / `AUDIT_CONTRACT.md` / 契约 | 未被改动 ✅ |

## 七、下一轮最小闭环（建议顺序）

1. `litrev.py`：`_block_lines` 之后加「同基线且 x 区间交叠 → 合并」；重跑 `text` + `index`，只复核 Zhang p.2 与 Borner p.8–9。
2. `litrev.py`：加 `audit-count` 子命令，把 131 汇总变成一条命令的输出；三份文档的错数字改为引用命令结果。
3. 修 `ex-` 落点（与 qx 同源）；`gen_subagents.py --check` 兜底。
4. 重派 `qx-zhang2006`（只补 #7 主语）与 `qx-borner1993`（#5 改为 p.8 截到 `...representations` 单词边界，撤掉 p.9 那条）。
5. T1 判据补一条：引文必须含限定动词，否则不算完成。

## 八、修复后复测（2026-11-09 17:2x）

### 1. 版面重建：两个缺陷都修了

| 缺陷 | 现象 | 修法 |
|---|---|---|
| 行分桶边界 | `round(y/2.5)` 在 66.25pt 处把一条视觉行切成两行：中心 66.2 与 66.3 落到桶 26/27，出现 `Graph` 单独成行 | 改为「按 y 排序后相邻差分 ≤ ytol/2 聚类」，不再用固定桶 |
| 同基线被切成两个 block | 标题与正文同基线连排时，PyMuPDF 给出两个 block，按 block 顺序输出 → 一行变两行、词序交错（`BP for Case There only` / `Network Retrieval, are some`） | 新增 `_merge_rows`：**同基线且 x 区间交叠**才合并。真双栏的 x 区间不交叠，不会误合；合并结果保留首次出现位置，不破坏 XY-cut 的栏序 |

证据：

- `Zhang2006` p.2 现在读作 `BP Network for Case Retrieval, There are only some experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory.` —— 原句连贯，主语回来了。
- `Borner1993` p.9 现在读作 `Graph based representations Both are integrated in a knowledge based system ...`。

健康度：`Borner1993` 7.73 → **7.87** 词/行（短行 31.6%），`Zhang2006` 6.33 → **6.83**（短行 19.9%）。

### 2. 回归：131 PASS + 1 PARAPHRASE

19 份笔记、132 条引文重跑 `verify`，与改动前逐篇对比：**18 份完全一致，1 份少 1 条 PASS**。

失败的是 `Zhang2006` #3（案例表示形式）：引文 `(k [l,m] m c is the upper limit of m. ) of the m, m, two case samples Xi and Y.` 在新 txt 里变成 `[l,m] m m, c m, is the upper limit of m.`。该处是上下标公式区，重排后与原文顺序不再逐字一致，而新顺序本身也是乱的（公式区无行结构）。**这不是回归错误，是语料换了之后这条引文必须重取**；`RUNBOOK §七.6` 已把它写成已知限制。

### 3. 汇总口径改成命令

新增 `python litrev/litrev.py audit-count`：

- 逐文件重算，并与每个 `out_*.md` 自报的「合计」行对照；8 个批次全部 ✓。
- 输出 `131 条 · SUPPORTED 84 / PARTIAL 46 / UNSUPPORTED 1 · SELF 112 / DEPENDENT 19 · 非 SUPPORTED 47/131 = 35.9%`。
- `--check` 在合计行与明细不一致时以退出码 1 结束，报告里的数字以后只能照抄这条命令。

`reports/round-03-sample.md`、`C4_REST_RESULT.md §八`、`C4_FRAG_RESULT.md §八` 三处错误汇总已按命令输出更正，并注明原数字是手算。

### 4. `ex-` 落点

生成器改为：卡片落点统一按「有 `full/` 用 `full/`，否则 `notes/`」，`ex-` 与 `qx-` 用同一处；**卡片已存在则不生成 `ex-`**（它只有创建权限，派它只会撞到已有文件）。

结果：22 篇都有卡片 → `ex-` 0 个，agent 总数 55 → 33（22 `qx-` + 9 `auditor-` + `checker` + `orchestrator`）。`RUNBOOK §六` 用例 1–4 已标注「需要有 `ex-` 实例时执行」。

### 5. 待办（第五步，必须在 OpenCode 里做）

重派 3 条，一条笔记一次：

| 文献 | 条目 | 要做的事 |
|---|---|---|
| `qx-zhang2006-...` | #7 明确写出的局限 | 引文起点前移到 `There are only some ...`，补齐主语 |
| `qx-zhang2006-...` | #3 案例或数据的表示形式 | 公式区已坏，改挑同段不含公式的句子 |
| `qx-borner1993-...` | #5 系统形态 | p.8 那条截到 `...Term based knowledge representations` 收尾，撤掉 p.9 的 `Graph based representations`（3 词无谓语） |

重派后 `verify` 应回到 132/132 PASS。
