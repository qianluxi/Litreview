# 金标准填写样例 G1（草拟，供审核修改）

> 这是一份**草拟样例**，不是金标准本身。由主控基于契约 v1.1 + 卡片原文对 25 条逐条判定生成。
> **它不构成独立金标准**——草拟者与判定表同源（同一模型），只能帮你把"从零填 25 条"降为"逐条确认/修改"。
> 真正的金标准是你填进 `GOLDEN.md` 并通过 `verify-golden` 的那份判定。

## 怎么用这份样例

1. 逐条看下面的「审核注记」，重点看标了 ⚠️ 的条。
2. 把你认可后的判定填进 `litrev/_probe/audit/GOLDEN.md` 的表格（首行原样抄 `> 快照 sha1: d46f9e7c3f`）。
3. 填完跑 `python tools/audit_prep.py verify-golden`，得到一致率与方向分布。
4. **不要读 `GOLDEN_MAP.md`**（那是答案键）；但本样例的审核注记里会标出原判定，方便你聚焦差异——这是给你裁用的，不是给子代理的。

## 草拟判定表（可直接复制到 GOLDEN.md，改你不同意的条）

| id  | 支撑 | 自足 | 引文里的依据（≤15 字，必须是引文原词） | 缺什么 / 需补的一句 |
| --- | -- | -- | --------------------- | ----------- |
| G01 | UNSUPPORTED | SELF | "to illustrate" | 引文未触及 CBR/相似度度量问题域，论断主体无依据 |
| G02 | PARTIAL | SELF | "being developed" | "案例"超出引文（止于 failure analysis），需补 cases |
| G03 | PARTIAL | SELF | "Ward linkage" | 引文止于 distance as，"度量"一词不在引文内 |
| G04 | PARTIAL | SELF | "implemented in" | "原型形态"无依据（引文无 prototype），范围放大 |
| G05 | PARTIAL | DEPENDENT | "can overcome" | such 指代对象不在引文内，"现有案例检索方法"需补 |
| G06 | SUPPORTED | SELF | "mature and systematic theory" | — |
| G07 | PARTIAL | SELF | "supply the system" | "子系统""构成"无依据，引文只说 supply |
| G08 | PARTIAL | SELF | "could be" | "取值"超出引文，could be 升级为实际 |
| G09 | SUPPORTED | SELF | "GNN-based shear wall" | — |
| G10 | SUPPORTED | SELF | "characteristic attributes" | — |
| G11 | PARTIAL | DEPENDENT | "the same with" | This 指代不在引文内，"验证依据"超出引文 |
| G12 | SUPPORTED | SELF | "frames and rules" | — |
| G13 | PARTIAL | SELF | "key factor" | "面向建筑设计中的平面图"引文无依据 |
| G14 | PARTIAL | SELF | "no universal" | "本文讨论通用方法论"引文无对应 |
| G15 | SUPPORTED | SELF | "combines CBR" | — |
| G16 | SUPPORTED | SELF | "conceptual design" | — |
| G17 | SUPPORTED | SELF | "0.247" | — |
| G18 | PARTIAL | SELF | "surface match" | PATDEX 不在引文内，论断主体为引文外专有名词 |
| G19 | SUPPORTED | SELF | "12 fingerprints" | — |
| G20 | SUPPORTED | SELF | "XML-based" | — |
| G21 | SUPPORTED | SELF | "tree editing distance" | — |
| G22 | SUPPORTED | SELF | "perceptual model" | — |
| G23 | PARTIAL | SELF | "can be encoded" | can be 可能性写成实际采用，情态升级 |
| G24 | SUPPORTED | DEPENDENT | "same shape type" | it 指代 this descriptor，需补主语 |
| G25 | SUPPORTED | SELF | "production rules" | — |

合计：25 条（SUPPORTED 13 / PARTIAL 11 / UNSUPPORTED 1；DEPENDENT 3）

> 草拟分布与判定表（S15/P9/U1）的差异：我降档了 G03、G18 两条（均 SUPPORTED→PARTIAL）。
> 这两条是真实争议，详见下方「重点争议」。如果你维持原判 SUPPORTED，分布会回到 S15/P9/U1。

## 审核注记（逐条）

分三档：✅ 绿灯（判定码与原判定一致，直接确认即可）/ ⚠️ 黄灯（边界，建议读卡片确认）/ 🔴 红灯（争议，我给了与原判定不同的码，必须裁决）。

### ✅ 绿灯（20 条，判定码与原判定一致）

这些条引文与论断的对应关系清楚，我草拟与原判定码一致。依据词我选了更核心的引文原词（原判定有的依据词偏次要，但不影响码）。逐条复核时可只看引文是否逐字覆盖论断核心成分。

- **G01** UNSUPPORTED/SELF：引文"analysis is used to illustrate that applications with a mixture"——论断核心"CBR 案例检索中的相似度度量"在引文里完全没有。主体不对应。原判定一致。
- **G02** PARTIAL/SELF：引文止于"failure analysis"，论断说"失效分析案例"——"案例(cases)"超出引文。"正在开发"有"being developed"支撑。原判定一致。
- **G04** PARTIAL/SELF：引文有"HI-RISE is implemented in PSRL"，但"原型形态(prototype)""文中系统"无依据，且只给一例。原判定一致。
- **G05** PARTIAL/DEPENDENT：引文"can overcome such shortcomings"——such 是指示代词（§七.1），指代对象不在引文内。原判定一致。
- **G06** SUPPORTED/SELF：引文逐字覆盖"mature and systematic theory""only some experimental conclusions""instead of"。原判定一致。
- **G08** PARTIAL/SELF：引文"could be associated with"——情态升级（§三.1），且止于 associated with，"取值"无依据。原判定一致。
- **G10** SUPPORTED/SELF：引文覆盖"characteristic attributes""transforms them into target cases"。them 指代 cases（引文内出现过）。原判定一致。
- **G11** PARTIAL/DEPENDENT：引文"This selection is the same with the practice engineering"——This 指代不在引文内；"验证依据"论断所加。原判定一致。
- **G12** SUPPORTED/SELF：引文逐字覆盖"frames and rules""Lisp functions""declarative/procedural knowledge"。完全支撑。原判定一致。
- **G13** PARTIAL/SELF：引文支撑"构图结构是品质关键因素"，但"面向建筑设计中的平面图"引文无对应。原判定一致。
- **G14** PARTIAL/SELF：引文支撑"不存在通用 CBR 方法"，但"本文讨论通用方法论"引文无对应（引文说的是"As for AI in general"）。原判定一致。
- **G15** SUPPORTED/SELF：引文逐字覆盖"novelty""combines CBR, exact, and inexact graph matching""floor plans"。完全支撑。原判定一致。
- **G16** SUPPORTED/SELF：引文覆盖"conceptual design of architectural floor plans""retrieve the similar floor plans"。原判定一致。
- **G17** SUPPORTED/SELF：引文逐字覆盖"MAP""ROBIN dataset""0.247""only room layout"。完全支撑。原判定一致。
- **G19** SUPPORTED/SELF：引文覆盖"12 fingerprints""properties of nodes, edges or full graph isomorphism"。原判定一致。
- **G20** SUPPORTED/SELF：引文覆盖"AGraphML""XML-based representation""floor plans"。原判定一致。
- **G21** SUPPORTED/SELF：引文覆盖"tree editing distance""metric for query similarity"。原判定一致。
- **G22** SUPPORTED/SELF：引文覆盖"proposed a perceptual model""drawing style""architectural plans"。原判定一致。
- **G23** PARTIAL/SELF：引文"can be encoded"——情态升级（§三.1）。原判定一致。
- **G24** SUPPORTED/DEPENDENT：引文"it may consider distinct"——it 指代 this descriptor（§三.5 补主语允许），支撑成分齐全。原判定一致。
- **G25** SUPPORTED/SELF：引文逐字覆盖"procedural knowledge""production rules and LISP functions"。完全支撑。原判定一致。

### ⚠️ 黄灯（3 条，边界，建议读卡片确认）

判定码与原判定一致，但有边界点值得你独立确认。

- **G07** PARTIAL/SELF：原判定依据用"special design"，我改用"supply the system"——因为"子系统""构成"无依据，引文核心是"supply the system"（供应系统），不是"special design"（专项设计）。码不变，但依据词更准。建议读 Borner 卡片确认 SynTerm/SynGraph 是否在原文里被称为"子系统"——如果原文确有 subsystem 字样，可升 SUPPORTED。
- **G09** SUPPORTED/SELF：原判定依据用"Figure 1"，我改用"GNN-based shear wall"——核心成分是方法本身，图 1 是附属。码不变。引文止于"consists of three"，三个什么未知，但不影响本条。确认无误即维持。
- **G10** SUPPORTED/SELF：引文"transforms them into target cases"——them 指代 selection 还是 cases 有轻微模糊（"cases to form selection and then transforms them"）。但 cases 在引文内出现过，倾向 SELF。确认无误即维持。

### 🔴 红灯（2 条，争议，我给了与原判定不同的码）

**这两条是我与判定表的真实分歧，必须由你裁决。** 如果同意我降档，verify-golden 会报"原表偏松 2 条"；如果维持原判，写 SUPPORTED。

#### G03：PARTIAL vs 原判定 SUPPORTED

- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as"
- 我降档理由：引文**止于"as"**，"度量(metric)"这个词不在引文内。论断说"作为度量"——引文只给了"distance as"，as 后面接什么没写完。按 §二 SUPPORTED 定义"论断的每个可检验成分都能在引文里找到对应表述"，"度量"这个成分无对应。
- 反方理由（维持 SUPPORTED）：三个核心成分（凝聚层次算法、Ward 连接、欧氏距离）逐字覆盖，"as"后接 metric 是语法必然，几乎是同一句话。按 §三.5 精神（补全合理），可判 SUPPORTED。
- 我的倾向：PARTIAL，因为严格闭卷下"度量"无对应。但这是边界，维持 SUPPORTED 也站得住。
- 卡片确认：读 `Rodrigues2017_Clustering_FloorPlans.md` p.4 上下文，看原文"as"后是否紧接 metric/similarity measure。

#### G18：PARTIAL vs 原判定 SUPPORTED

- 论断：PATDEX 使用一个依赖领域但全局的相似性度量，基于表层匹配来评估相似性。
- 引文："A domain-dependent, but global similarity metric is used to assess similarity based on surface match."
- 我降档理由：**PATDEX 这个专有名词在引文里完全没有出现**。引文主语是"A domain-dependent, but global similarity metric"，论断把主语换成"PATDEX"。§三.5 允许补主语，但那里举的是"it decomposes"补"设计案例召回"——补的是引文内已有代词的消解。PATDEX 是引文外的**新专有名词**，不是代词消解，严格说不落在 §三.5。
- 反方理由（维持 SUPPORTED）：PATDEX 确实是 Aamodt&Plaza 1994 论文里这个度量的使用者（卡片论断行即如此），补主语合理；且度量本身的描述逐字覆盖。
- 我的倾向：PARTIAL，因为闭卷读者单看引文不知道 PATDEX 是谁。但若你认为补系统名等同于补代词主语，维持 SUPPORTED。
- 卡片确认：已核实——PATDEX 只在卡片论断行出现，引文行内确实没有。读 `AamodtPlaza1994_CBR_Foundations.md` 相似性机制节确认 PATDEX 是否是该度量的使用者。

## 填写步骤

1. 打开 `litrev/_probe/audit/GOLDEN.md`，确认第 8 行戳 `> 快照 sha1: d46f9e7c3f`（不要改）。
2. 把上面「草拟判定表」的 25 行填进第 14–38 行的空表，**改掉你不同意的条**（至少 G03、G18 要明确选 SUPPORTED 还是 PARTIAL）。
3. 末尾加合计行：`合计：25 条（SUPPORTED x / PARTIAL y / UNSUPPORTED z；DEPENDENT w）`，按你最终填的数算。
4. 跑 `python tools/audit_prep.py verify-golden`。
   - 会输出：一致率、方向分布（原表偏松 / 抽检偏松 / 双向）、按批次集中度。
   - 退 0 = 全一致；退 1 = 有差异（差异不等于错，是给你看的）。
5. 一致率不是分数——金标准测的是判定表的**准确性**。即使你全维持原判（100% 一致），也只是说明判定表与你这次开卷判定一致；真正的价值在于你填的过程是独立于判定表做的。

## 一个诚实声明

这份草拟与原判定表在判定码上高度一致（25 条里 23 条同码）。这**不证明判定表准确**——只能证明判定表自洽。我是同一个模型，判定习惯与判定表同源，所以我的"独立判定"大概率趋同。这正是为什么金标准必须由**你**填：你的判定习惯与判定表不同源，你填出来的差异才是判定表准确性的真实信号。

所以：不要因为草拟与原判定高度一致就跳过审核。重点是那 2 条红灯 + 3 条黄灯——那里才是判定表可能偏松或偏紧的地方。
