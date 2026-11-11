# HANDOFF-14 · 第 2 步：新文献端到端（第一段：抽取）

> 2026-11-11 · 承接 `e2afe25`（FIX_B4 收口）与 `round-22` 的「4 步」结论
> **本轮只做第 2 步的第一段：真实派发一次抽取工，让一篇从未进过判定表的文献产出 7 节卡片。**
> 第二段（登记批次 → 派审计 → 进 131 口径）依赖抽取产物，必须等回报后做，见 §六。

---

## 一、为什么是这篇，以及为什么要先「转正」

查 `tools/gen_subagents.py` 对 26 篇 txt 的实际判定：

| 状态 | 篇数 | 能否当新文献 |
|---|---|---|
| 已入库 `full/` | 19 | 否（首次抽取已完成，不生成 `ex-`） |
| `notes/` 下有旧条目式卡片 | 3 | **原本否**：生成器按设计不给它们 `ex-`，落点指 `notes/`，永远进不了判定表 |
| `duplicate_of` 重复下载副本 | 3 | 否（内容与已入库文献重复） |
| 文字层 0.0 词/行 | 1（`WangHoward1991`，130 页空文本） | 否（需 OCR/视觉抄录） |

**结论：库里现成没有一篇「生成器眼里」的新文献。** 要跑通全链路，得先把一篇旧基线「转正」——这恰好是生产里最常见的场景（已有条目式草笔记，要正式纳入判定表），比另外找一篇新 PDF 更贴近现实，也不需要你提供素材。

选 **`Ayzenshtadt2016_ThinkingWithContainers_ICAART`**：

- 版面最干净：`wpl=7.2` 词/行、8 页 / 5779 词，远高于生成器 3 词/行的拒派线；
- **没演练过**（`Napps2021` 已做过 3 次 `DRILL_08/09/10`，再用它测不出泛化）；
- `aliases.json` 已登记 `Ayzenshtadt`，生成器算得出 `(Ayzenshtadt, 2016, p.N)`，不会拒派；
- 旧条目式卡片有 3 条引文，可作**事后对照**（不给子代理读，也不作标准答案）。

做法沿用 `HANDOFF-09` 的先例：把旧笔记 `git mv` 到 `audit/DRILL_11_baseline/` **留档而非删除**，生成器即把它当新文献、落点自动变成 `full/`。可逆：`git mv` 保留历史，随时能还原。

> `verify` / `card-check` / `card-coverage` 三者都只扫 `full/`（`check.py:34`、`litrev.py:1049`），
> 所以移走 `notes/` 不影响 131 口径 —— 已实测 `check.py` 仍是 **11/11 绿**。

## 二、已落盘（不要再改）

| 项 | 值 |
|---|---|
| 旧笔记留档 | `audit/DRILL_11_baseline/Ayzenshtadt2016_legacy_card.md` + `_引文核验.md`（`git status` 显示 `R`，不是 `D`） |
| 新抽取工 | `.opencode/agents/ex-ayzenshtadt2016-thinkingwithcontainers-icaart.md`（46 → **47**） |
| 它的读权限 | 只有 `litrev/_probe/CONTRACT.md` + `litrev/_probe/texts/Ayzenshtadt2016_ThinkingWithContainers_ICAART.txt` |
| 它的写权限 | 只有 `litrev/_probe/full/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md`（**只创建、不修改**） |
| 不注册的工具 | `bash` / `grep` / `glob` 整类 deny（工具不注册，不是调用时抛错） |
| 注入的标注 | `(Ayzenshtadt, 2016, p.N)`，模型不需要猜作者年份 |
| 机械状态 | `gen --check` 47/47 同步 · `check.py` **11/11 绿** · `verify` 131/131 · `card-check` 19/19 |

**没有动**：`BATCHES.json`、任何 `out_*.md`、`AUDIT_CONTRACT.md`、`AGENT_ROLES.md`、19 张存量卡片、判定表口径 `S130/P1/U0`。

## 三、派发前：重启 OpenCode

`ex-ayzenshtadt2016-…` 是新生成的，**注册表只在客户端启动时加载**，不重启会 `Unknown agent type`（round-11 踩过）。重启后先跑：

```bash
python tools/check.py
```

必须看到 `✓ 全部机械自检通过`（11 项）。红项先别派。

## 四、第一段派发词（1 个 task，逐字粘贴）

```
按 HANDOFF-14.md 做抽取，用 ex-ayzenshtadt2016-thinkingwithcontainers-icaart 这个子代理。

它只能读 litrev/_probe/CONTRACT.md 和
litrev/_probe/texts/Ayzenshtadt2016_ThinkingWithContainers_ICAART.txt，
只能新建 litrev/_probe/full/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md。

严格按 AGENT_ROLES.md / CONTRACT.md 的 7 节结构写：七个节标题的字、编号、顺序都不能改，
每节一行「- 论断：」+ 一行「- 引文："逐字原文" (Ayzenshtadt, 2016, p.N)」；
某节原文确实没有就写「- 论断：未涉及」，不留引文行。

引文要逐字、≥20 个英文字母、不跨页、页码取 <<<PAGE n>>> 的实际 n、
从句子开头起抄（不要图表标题或句中片段）、除引文外不出现英文双引号。
论断不许超过引文：每个可检验成分都要在本条引文里有对应表述，
不许补方法名/数值/否定性断言/因果/术语替换与属性添加（专有名词的定义也算内容）。
写不下就换一条能覆盖它的引文，不要拼相邻句。

不要读 full/ 下别的卡片、不要读 notes/、不要读任何 out_*.md、不要读别的文献。
写完停下，报「已写入 full/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md：N 节，M 条引文」。
```

## 五、抽取段的验收（我来做，不需要你判）

| # | 检查 | 通过标准 |
|---|---|---|
| 1 | 工作区污染 | `git status` 只多 `full/Ayzenshtadt2016_….md`（+ 它自己的 `_引文核验.md`） |
| 2 | 7 节结构 | `card-check` 20/20；节名逐字、每节恰 1 条论断 + 0/1 条引文、未涉及不带引文、无重复、页数对账 |
| 3 | 逐字与页码 | `verify` **131+N / 131+N** PASS（N = 新卡引文数，上限 7 → 138），逐字命中、PDF 物理页、标注 `(Ayzenshtadt, 2016, p.N)` 可对上 |
| 4 | 不漏审 | `card-coverage` **应该红**：新卡的 N 条引文还没落进任何批次输入 —— 这正是第二段要销的项 |
| 5 | 论断不越界 | 逐条按契约判据人工过一遍（重点第 ⑤ 类「术语替换与属性添加」，round-16 的 1 条边界就出在这） |

⚠️ 第 4 项**预期是红的**，别当成失败去手工改戳。第 5 项是唯一需要人开卷的一关，也是 `round-16` 说的「约 1/7 节会落在边界」的复测点。

## 六、第二段（抽取回报后我来做，你只需再派一次）

1. 从新卡片生成 `REST_B6.md`（7 节里带引文的 N 条，id `R6-01…N`），格式照 `REST_B5.md`；
2. `BATCHES.json` 注册 `rest_b6`：`REST_B6.md → out_R6.md`；
3. 跑 `gen_subagents.py` → 新 `auditor-rest-b6`（47 → 48），`gen --check` 同步；
4. `python litrev/litrev.py batch` 刷新（应显示 0 条变更，因为批次输入就是按当前卡片生成的）；
5. **你重启 OpenCode 第二次** → 派发 `auditor-rest-b6`，输出 `out_R6.md`；
6. 我按四条验收 → `check.py` 11/11 绿 → `audit-count` 从 **131 → 131+N**，判定表第一次真正收进一篇新文献。

> 两次重启是这套机制的固有成本（新 agent 只在启动时进注册表），且第二段依赖第一段的产物，
> 合成一次重启做不到。若你在第一段派发前定下 `B3-04` 选 A，`auditor-fix-b5` 会和第二段一起生成，
> 第二次重启可覆盖两个派发，不额外增加重启次数。

## 七、`B3-04` 选 A 的合并窗口（已预演，未落盘）

| 项 | 预演结果 |
|---|---|
| 改动 | 只删 `full/Borner1993_StructuralSimilarity_CBR.md` §6 论断的「，未给出数据集规模或指标数值」半句，**引文一字不动** |
| 批次输入 | `FRAG_B3.md` 戳 `18c979470b → e58bc1a19f`（已按 `_payload_stamp` 模拟算过） |
| 定点批次 | 另起 `FIX_B5.md`（1 条）→ `out_FIX_5.md` + `auditor-fix-b5`，**不能就地改 `out_B3.md`** |
| reseal 变更集 | 1 条（`B3-04`），第二道门槛可提前证完 |
| 参考集 | 与抽检/金标准/判例集冻结清单**零重叠**，分母保持 `15/12/10` |
| 预期口径 | `S131/P0/U0`（上限，非承诺） |

选 B（承认天然 `PARTIAL`、长期留账）则**什么都不用做**，口径停在 `S130/P1/U0`。
两案全文见 `HANDOFF-12 §八`。**现在说「选 A」我可以在第二段一并备好；派发完成后再定就要另起一轮。**

## 八、这次不做什么

- 不删除旧笔记（只 `git mv` 留档）、不把它当标准答案、不给子代理读
- 不预建 `REST_B6.md` 或 `out_R6.md`（引文还没抽出来，预填就是伪造证据）
- 不改 `AGENT_ROLES.md` / `CONTRACT.md` / 生成器 / 任何 `out_*.md`
- 不替你决定 `B3-04`，不重抽参考集，不动已封戳的批次
- 不宣称「抽取产物可直接进判定表」——这句话要等 §五 第 5 项人工过完才能说
