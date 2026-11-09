# P1 结构化抽取契约（CONTRACT_P1，v1）

本文件是 T4 全量抽取的**唯一契约来源**。动手前先读完本文件；执行中不得改口径。
本契约把上一轮的「3 条命题」升级为 `参考文献原文/文献综述_结构化提问清单.md` 中 **P1 的 7 个字段**。

## 〇、输入通道的变更（先读）

T0 实测：当前模型通过 `read` 工具打开 PDF 时返回
`ERROR: Cannot read pdf (this model does not support pdf input)`。
按 `HANDOFF.md` T0 的失败处理，改由**主控统一预导出**带页标记的 txt，格式与 `_probe/texts/` 既有文件一致。

因此：抽取工**只读 txt**，不读 PDF，不运行 `python` / `pdftotext` / OCR，不做任何文本转换。

## 一、输入

`litrev/_probe/texts/<文献名>.txt`，格式固定：

```
# SOURCE: <原始 PDF 文件名>
# PDF 物理页数: N

<<<PAGE 1>>>
第 1 页正文
<<<PAGE 2>>>
第 2 页正文
```

- `<<<PAGE n>>>` 标记的是 **PDF 物理页**，从 1 开始；正文里的期刊印张页码一律不用。
- `<文献名>` = PDF 文件名去掉 `.pdf`（例：`SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign`）。

## 二、输出

`litrev/_probe/full/<文献名>.md`，**一篇一个文件，不得合并**。固定结构：

```markdown
# <文献名>

- 抽取范围：<全文 1–N 页；SharmaThesis 必须写明抽了哪几节与页范围>

## 1. 一句话主张
- 论断：<中文一句话；只写引文能直接支撑的内容>
- 引文："<逐字原文>" (<Author>, <Year>, p.<N>)

## 2. 问题域
- 论断：...
- 引文："..." (..., p.N)

## 3. 案例或数据的表示形式
- 论断：...
- 引文："..." (..., p.N)

## 4. 相似性或检索机制
- 论断：...
- 引文："..." (..., p.N)

## 5. 系统形态
- 论断：...
- 引文："..." (..., p.N)

## 6. 评价方式
- 论断：...
- 引文："..." (..., p.N)

## 7. 明确写出的局限
- 论断：...
- 引文："..." (..., p.N)
```

**每个字段两条**：`论断` + `引文`。

- 字段在文献中确实不存在 → 只写 `- 论断：未涉及`，**不要**给引文行，不要为凑格式编引文。
- 字段看起来存在但找不到可逐字引用的句子 → 写 `- 引文：NOT_FOUND: <原因>；查过页：p.x–p.y`，**不要加引号**。

## 三、7 个字段（P1 原文口径）

| # | 字段 | 要写什么 |
|---|---|---|
| 1 | 一句话主张 | 作者认为自己的贡献是什么；论断用中文一句话，引文尽量保留作者的原文措辞。 |
| 2 | 问题域 | 建筑设计 / 结构方案 / 通用方法；按原文判断，不按你的印象。 |
| 3 | 案例或数据的表示形式 | 符号特征 / 向量 / 图像 / 图 / 规则 / 本体；写原文实际用的表示。 |
| 4 | 相似性或检索机制 | 若有：距离度量、图匹配、子图同构、嵌入、生成模型；写具体机制名。 |
| 5 | 系统形态 | 可运行原型 / 理论框架 / 综述 / 纯算法验证。 |
| 6 | 评价方式 | 数据集规模、指标名称、是否有工程或人工标注的真值；有数字就写数字。 |
| 7 | 明确写出的局限 | 只写作者**明确写出**的局限，不写你的推断，也不要把通用套话当局限。 |

## 四、硬性规则（违反任一条，产出判为不合格）

1. **引文必须逐字**：从 txt 原样复制；不得改词、补词、拼接不相邻片段、省略中间部分。连字符、连字（如 `artiﬁcial` 的 `ﬁ`）原样保留。
2. **引文长度 ≥ 20 个英文字母**：少于 20 个字母会被核验工具静默跳过，等于没抽。
3. **不得跨页**：一条引文必须完整落在同一个 `<<<PAGE n>>>` 段内。
4. **页码取实际所在页**：照 `<<<PAGE n>>>` 的 n，不估算、不用期刊印张页码。
5. **一条引文必须写在一行内**：不得含换行；单条引文 ≤ 500 字符（核验工具的解析上限）。若原句超过 500 字符，截取其中 ≤ 500 字符的**连续**片段，仍须逐字、同页、≥20 字母。
6. **除引文外不得出现任何英文双引号**：全文英文双引号对数 = 实际写出的引文条数（最多 7 对）。术语需要强调时用中文引号或不加引号。
7. **找不到就写 NOT_FOUND 并列出查过的页**；字段缺失写「未涉及」。**编一条凑数是最严重的失败。**
8. **只写自己那一个文件**：不改别人的文件、不改契约、不读 `_index/`、不读 `litrev.py`、不运行 `python`。
9. **论断不得超出引文**：不要添加原文没有的限定词、因果、最高级或范围放大；宁可写「未涉及」，也不要写引文撑不住的话。

## 五、引用标签表（作者标注照此写，避免 AUTHOR 判定）

| 文献文件（去 .pdf） | 标注写法 |
|---|---|
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm | (Zhang, 2006, p.N) |
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans | (Ahmed et al., 2013, p.N) |
| SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | (Soibelman et al., 2000, p.N) |
| vanEngelenburg2023_SSIG_FloorPlan | (van Engelenburg et al., 2023, p.N) |
| delasHeras2014_RunlengthHistogram_FloorPlans | (de las Heras et al., 2014, p.N) |
| Borner1993_StructuralSimilarity_CBR | (Borner, 1993, p.N) |
| MaherGomez1996_CBR_StructuralDesign | (Maher and Gomez, 1996, p.N) |
| Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | (Sabri et al., 2017, p.N) |
| Roith2017_GraphBasedDesign_FederatedDB_VisEng | (Roith et al., 2017, p.N) |
| Xia2025_CoDesign_ShearWallBeam_GNN | (Xia et al., 2025, p.N) |
| Rodrigues2017_Clustering_FloorPlans | (Rodrigues et al., 2017, p.N) |
| Gu2024_ShearWall_Diffusion | (Gu et al., 2024, p.N) |
| Maher1987_ExpertSystems_StructuralDesign | (Maher, 1987, p.N) |
| AamodtPlaza1994_CBR_Foundations | (Aamodt and Plaza, 1994, p.N) |
| Liao1998_SimilarityMeasures_CBR | (Liao et al., 1998, p.N) |
| SriramMaherFenves1985_KBES_StructuralDesign | (Sriram et al., 1985, p.N) |
| Zhao2023_ShearWall_GNN | (Zhao et al., 2023, p.N) |
| Survey2025_FloorPlanRetrieval_MDPI | (Ling et al., 2025, p.N) |
| SharmaThesis_ContentBasedFloorPlanRetrieval | (Sharma, 2018, p.N) |

## 六、SharmaThesis 特别规定

- 151 页学位论文，**不许全文扫**。
- 先读摘要与目录，选定「摘要 + 与平面检索直接相关的 2–3 节」。
- 在文件顶部 `- 抽取范围：` 写明节名与 PDF 物理页范围（例：`摘要 p.1–2；第 3 章 p.30–45；第 5 章 p.80–95`）。
- 7 个字段的证据只能来自这些范围；范围外不抽。

## 七、常见错法（都算不合格）

| 错法 | 例子 | 为什么错 |
|---|---|---|
| 用通用知识替代原文 | 原文写 `based on the IFC standard`，抄成 `based on BIM standards` | 逐字校验必挂，且是幻觉的典型形态 |
| 把概括当原文 | 原文写 `agents work in groups (containers)`，抄成 `agents are organized into containers` | 语义没错，但不是原文 |
| 拼接跨页句子 | 上半句在第 4 页末、下半句在第 5 页首，拼成一条 | 页码无法唯一，读者按标注查不到 |
| 论断超出引文 | 引文说 `can be defined`，论断写「分别定义了」 | 引文真实但撑不住论断，审计层会判 PARTIAL |

## 八、提交前自检

- [ ] 7 个字段标题齐全；缺失字段写「未涉及」，无引文行
- [ ] 每条引文能在 txt 里字符串命中，且只命中一页
- [ ] 每条引文首尾在同一个 `<<<PAGE n>>>` 段内，页码与标记一致
- [ ] 每条引文 ≥ 20 个英文字母、≤ 500 字符、不含换行
- [ ] 全文英文双引号对数 = 引文条数（没有多余引号）
- [ ] 作者标注与本契约第五节的表一致
- [ ] 没有改词、补词、拼接、省略；断词连字符原样保留
