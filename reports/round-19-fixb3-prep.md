# round-19：FIX_B3 准备 —— 13 条换引文（派发前）

> 2026-11-11 · 基线 `69b676a`（round-18 收口）· 本轮只改卡片与批次输入，**不改判定表**
> 定点批次 `FIX_B3.md`（戳 `a154464802`）· 输出 `out_FIX_3.md` · agent `auditor-fix-b3`

## 一、范围

14 条非 SUPPORTED 里，13 条是**引文侧**问题：C 类 11（截断/缺主语）、E 类 1（`B1-06` 方向不符）、
`B1-08` 1（round-18 判回 PARTIAL 时暴露「改法错」——删论断删不出主谓）。
剩下 `B3-04` 是证明否定，需定口径，不在本批（HANDOFF-12 §八给了 A/B 两案）。

做法：在 `litrev/_probe/texts/*.txt` 逐条定位**含主谓的完整句**，按 OCR 原样抄录替换 `- 引文：` 行；
5 条论断做最小改写以贴齐新引文；其余 8 条论断一字未动。

## 二、13 条逐条对照

| id | 文献 · 节 · 页 | 旧引文（截断处） | 新引文（开头） | 论断 |
|---|---|---|---|---|
| `B1-06` | Liao1998 · 问题域 · p.2 | `analysis (Esaklul, 1990) is used to illustrate that applications with a mixture` | `This article focuses on the similarity measuring methods for CBR and comprises two parts.…` | 改 |
| `B1-08` | MaherGomez1996 · 问题域 · p.1 | `information on structural design projects` | `We began our CBR projects by locating a source of information on structural design projects-a…` | 改 |
| `B1-12` | Zhang2006 · 一句话主张 · p.1 | `this intelligent CRM can overcome such shortcomings as poor…` | `The result shows. this intelligent CRM can overcome such shortcomings as poor learning ability…` | 改 |
| `B2-11` | SriramMaherFenves1985 · 明确写出的局限 · p.19 | `expert system development tools, notably in the areas of user interfaces…` | `However, their full-scale practical implementation will require higher- level expert system development tools…` | 否 |
| `B3-01` | Ahmed2013 · 相似性或检索机制 · p.3 | `As for the retrieval algorithm, subgraph matching approaches` | `As for the retrieval algorithm, subgraph matching approaches seem to be promising.` | 改 |
| `B3-05` | Liao1998 · 一句话主张 · p.3 | `applications. In the second part, a hybrid similarity measure is proposed for comparing` | `In part 2, a hybrid similarity measure is proposed to compare cases having a mixture of crisp and fuzzy features.` | 否 |
| `B3-07` | MaherGomez1996 · 一句话主张 · p.1 | `Toward that end, this article presents four` | `Toward that end, this article presents four "cases" of case-based building design sys- tems…Demex.` | 否 |
| `B3-08` | MaherGomez1996 · 相似性或检索机制 · p.4 | `a given problem by finding matches between` | `The system measures a model's or a case's relevance to a given problem by finding matches between…` | 否 |
| `B3-09` | MaherGomez1996 · 明确写出的局限 · p.10 | `when case memory contains a limited` | `This approach is appropriate when case memory contains a limited num- ber of cases and inappropriate…` | 否 |
| `B3-10` | SriramMaherFenves1985 · 问题域 · p.4 | `structural design are not amenable to purely algorithmic solutions. These problems are often ill-` | `However, a number of problems encountered in structural design… These problems are often ill- structured…` | 否 |
| `B3-11` | Survey2025 · 系统形态 · p.3 | `This paper thoroughly examines these feature retrieval methods and introduces advanced fusion…` | `This paper aims to comprehensively investigate key aspects of building plan feature retrieval technology…` | 改 |
| `B3-15` | Zhao2023 · 评价方式 · p.10 | `Ten-fold cross-validation… the validation-set average and standard` | `…standard deviation of IoUpixel obtained from the ten-fold training sessions are used as specific evaluation indicators…` | 否 |
| `R4-16` | vanEngelenburg2023 · 评价方式 · p.5 | `RPLAN is a large-scale dataset containing ﬂoor plan images…` | `In this paper, RPLAN [26] is used for analysis and eval- uation. RPLAN is a large-scale dataset…` | 否 |

**逐字纪律**：`rst`（first）、`ﬂ`（fl 连字）、`firmthat`、`spec- ification`、`ill- structured`、
`num- ber`、`eval- uation` 这类扫描件断词/连字/跨行连字符一律原样保留，不补字母。
每条新引文都先过 `find_quote` 确认 `exact=True` 且页码为 PDF 物理页，最长 472 字符（<500 的解析上限）。

`B3-15` 的引文在语料里命中两份文件（`Intelligent Design…pdf` p.8 与 `Zhao2023_ShearWall_GNN.pdf` p.10），
`verify` 按作者标注 `(Zhao et al., 2023, p.10)` 选后者，实测 PASS。

## 三、机械验证（全部可复现）

```
verify 全库              131/131 PASS
card-check               19/19（131 条引文恰等于判定表条数）
card-coverage            ✓ 每一条带引文的节都落进某个批次输入
batch --check            刷新前 13/131 待刷新 → 刷新后 0/131
gen_subagents --check    ✓ 45 个文件与 AGENT_ROLES.md 一致
FIX_B3.md                13 条 · 头部戳 a154464802 = 内容戳
reseal 变更集预演       B1 3 · B2 1 · B3 8 · R4 1 = 13，与 FIX_B3 双向为空、同 id 逐字一致
```

`check.py` 当前 **7 绿 4 红**：`audit-stale` + 三个参考集 `--check`，原因是 `batch` 刷新了
B1/B2/B3/R4 四个批次的输入戳而 `out_*.md` 尚未重封 —— 与 round-18 派发前完全同型，`reseal` 后自愈。

## 四、两个被门禁抓到的自伤（记下来，别再犯）

1. **批量替换吞掉换行**：脚本里用 `re.search(..., re.M)` 匹配 `- 引文：` 行时，尾部写了 `\s*$`，
   `\s` 含 `\n`，把行尾换行连同下一节前的空行一起吃掉，8 张卡片出现 `…) (Author, p.1)## 2. 问题域`，
   节被合并。`card-check` 立刻报「8/19 张不合格 · 应有 7 节实有 4~6 节 / 某节 2 行论断 / 节编号错」。
   修：把 `)## ` 统一还原成 `)\n\n## `（11 处）。**若只跑 `verify` 会发现不了**——它只数引号对，
   结构门禁才是这道网的第二层。
2. **重复引文**：`B3-11` 初版选了摘要里的 `This paper presents a comprehensive exploration…`，
   但同一张卡片的「一句话主张」节已经用了这句。`card-check` 报「同一句引文被复用在多节」。
   改用 p.3 的 `This paper aims to comprehensively investigate key aspects…`，论断同步改为
   「综合考察…关键方面」，删掉引文里没有的「综述」「融合技术」。

两条都印证同一件事：**改完必须跑全套门禁，不能只验自己改的那一维**。

## 五、参考集受损面（派发前机械核对）

| 参考集 | 现有效分母 | 与 13 条重叠 | 派发+reseal 后 |
|---|---|---|---|
| 抽检 S1 | 10 | 0 | 10，不受影响 |
| 金标准 | 17 | `B1-06`、`B1-12` | **15**（引文+论断都变 → 判后返工剔除） |
| 判例集 | 16 | `B1-08`(已返工)、`B2-11`、`B3-08`、`B3-09`、`B3-11` | **12**（引文变了，自足样本不再是同一条） |

金标准从 25 一路剔到 15，判例集从 20 剔到 12 —— **补抽 + 人开卷重判已经是硬需求**，
不是「有空再说」。round-18 之后参考集的一致率只能当粗读，不能当精确可信度。

## 六、派发后我做什么

1. 四条验收（戳同源 / 13 行 id 严格相等 / 依据逐字命中**新引文** / 工作区只多一个文件）
2. `reseal --fix-input FIX_B3.md --fix-out out_FIX_3.md`（显式传参，默认还指向 `FIX_B2`）
3. 复跑 `check.py`，预期 4 项红全转绿；再跑 `verify-golden` / `verify-cases` 看剔除后读数
4. 上限 `S130/P1/U0`，非 SUPPORTED 1/131（只剩 `B3-04`）；**上限非承诺**

## 七、仍待决定

`B3-04` 的缺席命题口径（HANDOFF-12 §八）。推荐 A：删掉「未给出数据集规模或指标数值」半句，
观察移到综述正文转述，判定表只留能被引文正面支撑的成分。
