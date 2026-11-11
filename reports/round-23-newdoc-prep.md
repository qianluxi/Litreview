# round-23 · 第 2 步备料：新文献端到端（第一段就位，待派发）

> 2026-11-11 · 承接 `e2afe25`（FIX_B4 收口）与 `round-22` 给出的「生产还差 4 步」
> 本轮推进 **第 2 步**（唯一从没做过的一步）的**准备段**：把一篇从未进过判定表的文献，
> 变成生成器眼里可派 `ex-` 的新文献，并把派发单与第二段路径全部备齐。
> 不改判定表、不改契约、不改生成器、不动 `B3-04` 口径。

---

## 一、先撞上的一个事实：库里没有现成的新文献

按 `tools/gen_subagents.py` 的实际分支逐篇核 26 篇 txt：

| 生成器判定 | 篇数 | 明细 |
|---|---|---|
| 已入库 `full/` | 19 | 卡片已存在 → `done`，不生成 `ex-`（它只有创建权限，派了只会撞文件） |
| `notes/` 有旧条目式卡片 | 3 | `Ayzenshtadt2016`、`MaherGomez1997`、`Napps2021` → 落点指 `notes/`，**永远进不了 131 口径** |
| `duplicate_of` 重复下载副本 | 3 | 三个「Intelligent…」txt 分别对应已入库的 `Xia2025` / `Zhao2023` / `Gu2024` |
| 文字层 0.0 词/行 | 1 | `WangHoward1991`（130 页空文本扫描件），生成器按 `wpl < 3` 拒派 |

生成器注释里也写明了这个设计：「`notes/` 下已有的 3 篇早期基线不迁移、也不另建副本——原地返工，路径仍指 `notes/`」。
所以 **「挑一篇 texts/ 里有 txt、full/ 里没卡片的文献」这句话本身不足以跑通链路**：那 3 篇虽然 `full/` 没卡片，
生成器也不给它们 `ex-`。

**处置**：把其中一篇的旧笔记「转正」——`git mv` 留档，生成器即视为新文献、落点自动变 `full/`。
这沿用 `HANDOFF-09` 的先例（那次移出 `Napps2021` 做演练、结束后还原），区别是**这次不还原，正式入库**。
比另找一篇新 PDF 更贴近真实生产场景（已有草笔记要正式纳入判定表），且不需要用户提供素材。

## 二、选篇依据

选 `Ayzenshtadt2016_ThinkingWithContainers_ICAART`（*Thinking With Containers: A Multi-Agent Retrieval Approach for the Case-Based Semantic Search of Architectural Designs*）：

| 项 | 值 | 为什么重要 |
|---|---|---|
| 版面 | `wpl=7.2` 词/行、8 页 / 5779 词 | 远高于 3 词/行拒派线；不用碰 OCR/公式区 |
| 演练史 | **零** | `Napps2021` 已做过 `DRILL_08/09/10` 三次，再用测不出泛化 |
| 作者年份 | `aliases.json` 已登记 `Ayzenshtadt`、stem 含 `2016` | 生成器算出 `(Ayzenshtadt, 2016, p.N)`，不会因取不到而拒派 |
| 旧笔记 | 3 条条目式引文 | 可作**事后对照**，但明确不给子代理读、不作标准答案 |

## 三、落盘内容（机械证据）

```
git mv  notes/Ayzenshtadt2016_….md                 → audit/DRILL_11_baseline/Ayzenshtadt2016_legacy_card.md
git mv  notes/Ayzenshtadt2016_…_引文核验.md        → audit/DRILL_11_baseline/Ayzenshtadt2016_legacy_card_引文核验.md
新增    .opencode/agents/ex-ayzenshtadt2016-thinkingwithcontainers-icaart.md
改      qx-ayzenshtadt2016-…（target 从 notes/ 改指 full/）
改      litrev/_probe/.generated_agents.json、AGENT_MAP.md（生成器产物）
新增    HANDOFF-14.md、reports/round-23-newdoc-prep.md
```

新 `ex-` 的权限（已从文件逐行核对）：

```yaml
read:  "*": deny
       "litrev/_probe/CONTRACT.md": allow
       "litrev/_probe/texts/Ayzenshtadt2016_ThinkingWithContainers_ICAART.txt": allow
edit:  "*": deny
       "litrev/_probe/full/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md": allow
bash / grep / glob: "*": deny        # 工具不注册，不是调用时抛错
```

提示词里已注入 `(Ayzenshtadt, 2016, p.N)`，模型不猜作者年份。

**回归**：`check.py` **11/11 绿**，`gen --check` **47/47** 同步，`verify` 131/131、`card-check` 19/19、
`card-coverage` ✓、`audit-count` `S130/P1/U0` 全部不变。
原因：`verify`（`check.py:34`）、`card-check`（`litrev.py:1049`）、`card-coverage` 三者只扫 `full/`，
`notes/` 从来不进 131 口径 —— 移走旧笔记零波及。

## 四、两段式流程与两次重启

| 段 | 谁做 | 产出 | 重启 |
|---|---|---|---|
| 一（本轮就位） | 你派 `ex-ayzenshtadt2016-…` | `full/Ayzenshtadt2016_….md`（7 节、N 条引文） | **第 1 次** |
| 二（回报后） | 我建 `REST_B6.md` + 注册 `rest_b6` + 生成 `auditor-rest-b6`；你派一次 | `out_R6.md` → `audit-count` 131 → 131+N | **第 2 次** |

第二段依赖第一段的产物，合成一次重启做不到：审计批次输入里的论断/引文必须来自**真实的抽取产物**，
现在预填就是伪造证据。这一点在 `HANDOFF-14 §六` 明写，不绕。

第二段批次编号定为 `REST_B6.md → out_R6.md`、id `R6-01…N`、注册 `rest_b6`，理由：
`cmd_batch` / `parse_batch_inputs` 只认 `^(FRAG|REST)_B\d+\.md$`，现有最大到 `REST_B5` / `out_R5`，
`out_R6.md` 匹配 `audit-count` 的 `^out_[A-Z]+\d+\.md$`，会正确进 131 口径。

抽取段验收第 4 项 `card-coverage` **预期是红的**（新卡引文还没落进任何批次输入），
那正是第二段要销的项，不要手工改戳。第 5 项「论断不越界」是唯一需要人开卷的一关，
也是 `round-16` 留下的「约 1/7 节会落在边界」的复测点 —— 重点查硬规则 9 第 ⑤ 类
（术语替换与属性添加，**专有名词的定义也算内容**）。

## 五、`B3-04` 选 A 的影响面（只预演，未落盘）

不改任何文件，按 `cmd_reseal` 同一套逻辑算：

| 项 | 结果 |
|---|---|
| 改动 | `full/Borner1993_StructuralSimilarity_CBR.md` §6 论断删「，未给出数据集规模或指标数值」，**引文一字不动** |
| 批次输入 | `FRAG_B3.md` 戳 `18c979470b → e58bc1a19f`（`_payload_stamp` 模拟；已 `assert t2 != t` 防空跑） |
| 定点批次 | 另起 `FIX_B5.md`（1 条）→ `out_FIX_5.md` + `auditor-fix-b5`，**不能就地改已封戳的 `out_B3.md`** |
| reseal 变更集 | 1 条（`B3-04`），第二道门槛可提前证完 |
| 参考集 | 与抽检 / 金标准 / 判例集冻结清单**零重叠** → 分母保持 `15/12/10`，不掉 |
| 预期口径 | `S131/P0/U0`（上限，非承诺） |

历史文件 `C4_FRAG_RESULT.md`、`FRAGMENTS_v1.md`、`REVIEW_NONSUPPORTED.md` 里也有这句论断，
按冻结原则**不动**（归档不是当前口径来源）。

选 B 则什么都不用做，口径停在 `S130/P1/U0`。**决定权仍留给用户**；
若在第一段派发前定 A，`auditor-fix-b5` 可与第二段一起生成，第二次重启覆盖两个派发。

## 六、下一步与未完成

- 待用户：**重启 OpenCode** → 按 `HANDOFF-14 §四` 逐字派发一次抽取。
- 待抽取回报：§四 表里的第二段（我来做）+ 再派一次审计。
- 仍未做（不阻塞本段）：第 3 步补抽参考集 + 人开卷重判、第 4 步定漂移验收标尺、
  `B3-04` 口径决定、`primary` 无权限层（§七.1 OPEN）。
- 本轮**没有**宣称「抽取产物可直接进判定表」——那句话要等验收第 5 项人工过完才能说。
