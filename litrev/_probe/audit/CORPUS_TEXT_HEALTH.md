# 语料文字层健康度（诊断报告）

> 目的：复核 `native-run-02` 核验报告 §4 的发现——48 条片段中 14 条的根源在 PDF 文字层，不在论断层。
> 方法：直接统计 `litrev/_probe/texts/*.txt` 的非空正文行、词数、短行（≤3 词）占比；不改 `litrev.py`。行定义与第三方核验略有差异（第三方给 Zhang2006 2.93 词/行，本表 3.08），不影响结论。

| 文献 | 正文行 | 词数 | 词/行 | 短行占比 |
|---|---:|---:|---:|---:|
| AamodtPlaza1994_CBR_Foundations | 2357 | 14452 | 6.13 | 28.4% |
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 1117 | 7936 | 7.10 | 35.3% |
| Ayzenshtadt2016_ThinkingWithContainers_ICAART | 843 | 5779 | 6.86 | 18.9% |
| Borner1993_StructuralSimilarity_CBR **←** | 5280 | 5453 | 1.03 | 99.6% |
| delasHeras2014_RunlengthHistogram_FloorPlans | 495 | 4396 | 8.88 | 26.7% |
| Gu2024_ShearWall_Diffusion | 1049 | 8860 | 8.45 | 51.9% |
| Liao1998_SimilarityMeasures_CBR | 1822 | 8181 | 4.49 | 63.4% |
| Maher1987_ExpertSystems_StructuralDesign | 664 | 5656 | 8.52 | 40.5% |
| MaherGomez1996_CBR_StructuralDesign | 1338 | 7076 | 5.29 | 26.9% |
| MaherGomez1997_CBR_in_Design | 1233 | 7158 | 5.81 | 19.3% |
| Napps2021_BIM_VariantRetrieval_CBR | 790 | 4496 | 5.69 | 36.2% |
| Rodrigues2017_Clustering_FloorPlans | 1442 | 10466 | 7.26 | 36.7% |
| Roith2017_GraphBasedDesign_FederatedDB_VisEng | 1031 | 8440 | 8.19 | 8.4% |
| Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 811 | 5574 | 6.87 | 26.5% |
| SharmaThesis_ContentBasedFloorPlanRetrieval | 5012 | 48014 | 9.58 | 31.6% |
| SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 987 | 8636 | 8.75 | 10.4% |
| SriramMaherFenves1985_KBES_StructuralDesign | 708 | 6335 | 8.95 | 29.2% |
| Survey2025_FloorPlanRetrieval_MDPI | 1728 | 13926 | 8.06 | 35.6% |
| vanEngelenburg2023_SSIG_FloorPlan | 809 | 6541 | 8.09 | 12.4% |
| Xia2025_CoDesign_ShearWallBeam_GNN | 941 | 8683 | 9.23 | 46.7% |
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm **←** | 991 | 3054 | 3.08 | 71.0% |
| Zhao2023_ShearWall_GNN | 938 | 9215 | 9.82 | 43.2% |

## 48 条片段中来自 Borner / Zhang 的条目

| 篇 | 条数 | 条目 id |
|---|---:|---|
| Borner1993_StructuralSimilarity_CBR | 7 | F07, F08, F09, F10, F11, F12, F13 |
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 7 | F34, F35, F36, F37, F38, F39, F40 |

## 结论
- `Borner1993` 与 `Zhang2006` 的文字层词/行显著低于其余文献，短行占比高；这两篇的 14 条片段不是「笔记截断」，而是「源文字层碎」。
- 对这 14 条继续派 auditor 判 `DEPENDENT`、再派 extractor 扩句，方向错误：扩句只会把碎串变长（B3-03 已从 10 词扩成 266 字符碎串）。

---

## 修复：版面重建（2026-11-09，覆盖上节结论）

上节「在重新抽取/视觉抄录之前只能记为已知问题」**已被推翻一半**：PDF 里的词是完整的，问题只在
`page.get_text()` 把每个词（甚至半个词）当成独立「行」输出——按行取句必然得到碎片。

### 方法（`litrev/litrev.py` 新增 `text` 子命令）

1. **以 block 为原子单位**保留段落边界，避免左右两栏互相穿插；
2. block 内按 **y 坐标**聚成视觉行，行内按 x 排序；相邻词间距 < 1pt **不插空格**（修 `Similarit`+`y` 这类被拆开的词）；
3. block 之间用 **XY-cut**：先找不被任何 block 跨越的栏缝竖切，再按 y 间距横切；
4. `index` 同页存两份键：`k`（raw）与 `kb`（版面），`verify` 两键都试 → 换语料不会推翻已有判定。

```bash
python litrev/litrev.py text --only Borner1993_StructuralSimilarity_CBR,Zhang2006_BP_CaseRetrieval_HighriseStructureForm
```

### 复测（同一统计口径）

| 文献 | 修复前 词/行 | 修复后 词/行 | 修复前 短行占比 | 修复后 短行占比 |
|---|---:|---:|---:|---:|
| Borner1993_StructuralSimilarity_CBR | 1.03 | **7.60** | 99.6% | 33.9% |
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 3.08 | **6.33** | 71.0% | 25.8% |
| WangHoward1991_IntegratedCBR_StructuralDesign | 0.00 | 2.00 | 100% | 100%（130 页扫描件，无文字层） |

全库 26 篇：24 篇持平或改善，0 篇变差，1 篇（WangHoward1991）仍不可用，已由生成器排除、不生成抽取工。

**回归**：重建索引后对 19 份笔记的 131 条引文重跑 `verify`，`PASS 131/131`，与改前逐篇一致
（`k`/`kb` 双键 + 键值本就抹掉空白，断词与否不影响键）。

### 仍未解决的一半：Type3 字体丢连字

`Borner1993` 使用 Type3 字体，`fi / fl / ff` 连字没有 ToUnicode 映射，被丢成空格：
`modi cation`、`speci c`、`e ect`、`o ers`。**版面重建救不了这个**——词本身就缺字母。

实测 3935 词中 37 个（0.9%）受影响（`modi` 22、`speci` 6、` rst` 3……）。含义：

- 含这些词的句子现在可以正常扩句，但抄出来必须是 `modi cation` 这种**带缺口**的原样形式；
- **不许补字母**（补一个 `f` 就从 PASS 变成 PARAPHRASE，属于伪造引文）；
- 要拿到干净引文，只能对这 11 页做视觉抄录。

### 修订后的处置

| 项 | 旧处置 | 新处置 |
|---|---|---|
| F07–F13 / F34–F40（14 条） | 记为已知语料问题，无法修 | 派 `qx-borner1993-…` / `qx-zhang2006-…` 扩句；扩句后 `verify` 逐条回查 |
| 扩句约束 | — | 连字缺口词按原样保留；不得跨页；不得拼接不相邻片段 |
| WangHoward1991 | 未提及 | 无文字层，**不派抽取工**（生成器已排除），如需引用走 OCR |

- 在重新抽取/视觉抄录之前，这 14 条只能记为「已知语料问题」，不能记为「已处理」。