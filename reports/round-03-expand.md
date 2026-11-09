# round-03 T1 扩句结果（完成，按用户选择 B）

- 任务：HANDOFF-03 T1（P2）14 条片段引文扩句。
- 用户裁决：Borner #5 选 **B**，允许 p.8–p.9 跨页；实现为同一字段下两条按页拆分的引文。
- 执行：
  - `qx-borner1993-structuralsimilarity-cbr`：`ses_e40831d5effeww8DkSZxAO0OJE`
  - `qx-zhang2006-bp-caseretrieval-highrisestructureform`：`ses_e40831c2affertsJPBbbSxWMia`
- 输入：`litrev/_probe/texts/<文献>.txt`（版面重建版）+ `litrev/_probe/full/<文献>.md`。
- 核验：`checker`，`ses_e407adcd4ffeOwAmXcJTkoBdE7`。

## 一、verify 结果

| 文件 | 条数 | PASS | 其他判定 | 退出码 |
|---|---:|---:|---|---:|
| `full/Borner1993_StructuralSimilarity_CBR.md` | 8 | 8 | 0 | 0 |
| `full/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md` | 7 | 7 | 0 | 0 |
| **合计** | **15** | **15** | **0** | **全 0** |

- 逻辑条目仍是 14 条；Borner #5 按 B 拆成 p.8 + p.9 两条引文，所以引文行是 15 条。
- 无 `PAGE` / `PARAPHRASE` / `MISSING` / `NOPAGE` / `ZHQUOTE`。

## 二、逐条对照

### Borner1993（7 个字段，8 条引文）

1. **一句话主张，p.10，PASS**
   - 旧：`Structural similarit y is assessed if and only if there is kno wledge a v ailable to adapt old solutions correctly`
   - 新：`Structural similarity is assessed if and only if there is knowledge available to adapt old solutions correctly to the current problem of interest`
2. **问题域，p.9，PASS**
   - 旧：`Both are in tegrated in a kno wledge based system whic h op erates in the domain of industrial building`
   - 新：`Both are integrated in a knowledge based system which operates in the domain of industrial building design Whereas the overall system provides user interfaces and a broader range of functionality SynTerm and SynGraph supply the system with solutions for special design problems`
   - 注：`Both` 的指代对象 `SynTerm` / `SynGraph` 已包进引文。
3. **案例或数据的表示形式，p.5，PASS**
   - 旧：`eac h ob ject circle or ellipse will b e represen ted b y its spatial dimensions and nine further attributes lik e time at whic h this ob ject w as created asp e ct whic h assumes one of return air fresh air etc and morpholo gy whic h refers to access connection etc`
   - 新：`Following the work of Ludger Hovestadt Hov each object circle or ellipse will be represented by its spatial dimensions and nine further attributes like time at which this object was created aspect which assumes one of return air fresh air etc and morphology which refers to access connection etc`
4. **相似性或检索机制，p.6，PASS**
   - 旧：`initial analysis of the new problem can b e done b y an inexp ensiv e surfac e similarity`
   - 新：`The rst initial analysis of the new problem can be done by an inexpensive surface similarity assessment based on the attribute based descriptions`
   - 注：`rst` 为版面重建后的原文断字，按原样保留。
5. **系统形态，p.8 + p.9，PASS（按 B 拆两条）**
   - 旧：`Our approac h is protot ypically implemen ted in SynT erm`
   - 新 p.8：`Our approach is prototypically implemented in SynTerm for Synthesis by using Term based knowledge representations and SynGraph for Synthesis by using`
   - 新 p.9：`Graph based representations`
6. **评价方式，p.10，PASS**
   - 旧：`The initial exp erimen tal results supp ort the claims`
   - 新：`The initial experimental results support the claims that the proposed ap proach o ers improved adaptation facilities in synthesis tasks together with a greater overall explanation performance`
7. **明确写出的局限，p.10，PASS**
   - 旧：`rule conditions or w eigh ts are not addressed`
   - 新：`Learning e g the storage of new cases new rules and the application of techniques like Knuth Bendix completion to guarantee completeness of struc tural knowledge or learning of modi cation rule conditions or weights are not addressed in this implementation`

> 说明：新 `texts/` 已经过版面重建，旧引文里的 `similarit y`、`kno wledge`、`a v ailable` 等断词空格在新 txt 中已不存在；qx 按新 txt 重建引文，因此旧引文不是新引文的字面连续子串。这是版面重建造成的，不是 qx 改写。

### Zhang2006（7 个字段，7 条引文）

1. **一句话主张，p.1，PASS**
   - 旧：`this intelligent CRM can overcome such shortcomings`
   - 新：`this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO.`
2. **问题域，p.1，PASS**
   - 旧：`High-rise structural form selection optimization is`
   - 新：`High-rise structural form selection optimization is an important strategic problem concerning synthetic performance of building structure.`
3. **案例或数据的表示形式，p.2，PASS**
   - 旧：`the input layer is inputting vectors {xik4m and {Yk}m (k`
   - 新：`the function of the input layer is inputting vectors {xik4m and {Yk}m (k [l,m] m c is the upper limit of m. ) of the m, m, two case samples Xi and Y.`
   - 注：原文双栏版面错序，`m c`、`m, m,` 按原样保留。
4. **相似性或检索机制，p.2，PASS**
   - 旧：`the relative Euclidean weight distance of attributes (see`
   - 新：`To solve this problem and to be able to take into consideration everything important and necessary such as concurrence of quality, quantitative and fuzzy attributes and difference in dimension, this paper established a new similarity measure method based on the relative Euclidean weight distance of attributes (see expression (5)).`
5. **系统形态，p.3，PASS**
   - 旧：`single-output, three-layer BP network.`
   - 新：`Thereupon we have built the multi-input-and- single-output, three-layer BP network.`
6. **评价方式，p.5，PASS**
   - 旧：`selection is the same with the practice engineering.`
   - 新：`This selection is the same with the practice engineering.`
7. **明确写出的局限，p.2，PASS**
   - 旧：`topological structure of networks instead of mature and`
   - 新：`experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory.`

## 三、T1 完成判定

- 引文层：**15/15 PASS**（逻辑 14 条；#5 拆两条）。
- 原 T1 完成条件里“14 条仍全部 PASS”按逻辑条目满足；按 verify 条数是 15，因为跨页拆分。
- 旧标 DEPENDENT 的两条：
  - Borner #2：`Both` 的指代对象已包进引文；
  - Zhang #5：新引文以 `Thereupon we...` 起首，已自带主语。
- 仍建议下一轮复核的自足性残留（它们旧标签是 SELF，不是 T1 的 DEPENDENT 必改项）：
  - Zhang #1 `this intelligent CRM...`
  - Zhang #6 `This selection...`
  - Zhang #7 `experimental conclusions...`（名词短语，无主语）
- 本轮只做引文层 verify；未重跑 C4 审计，旧 C4 判定仍是上一轮结果。
