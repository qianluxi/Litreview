# T3 片段扩句结果（7 条 / 5 篇）

- 对象：`litrev/_probe/audit/C4_FRAG_RESULT.md` §3.2 的 7 条 `SUPPORTED + DEPENDENT`，涉及 5 篇文献。
- 执行：5 个 `extractor` 在同一条消息内并列派发；每篇一个 extractor，避免同一 md 被两个会话同时改。
- 输入：`litrev/_probe/texts/<文献>.txt`（按 HANDOFF-02 §一.1 的纠正，不读 PDF，不重试 PDF 直读）。
- 修改范围：只改 `litrev/_probe/full/<文献>.md` 的指定「引文」行；不改论断、不改页码、不改其他条目。
- 结果：5 个文件各 `7/7 PASS`，`verify` 退出码全 0；扩句后总引文 35 条，无 `PAGE` / `PARAPHRASE` / `MISSING`。

## 一、扩句前后对照

| id | 文献 | 字段 | 页 | 旧引文 | 新引文 | 扩展词数 | 修改后行 |
|---|---|---|---|---|---:|---:|---:|
| B2-01 | Ahmed2013 | 问题域 | p.1 | "to guide solutions for similar architectural situations." | "These reference drawings are used to guide solutions for similar architectural situations." | +5 | L11 |
| B2-05 | Gu2024 | 相似性或检索机制 | p.6 | "methods for an image-prompt diffusion model with a mask tensor." | "To focus on the diffusion process features of the shear wall portion, this section introduces the construction, training, and inference methods for an image-prompt diffusion model with a mask tensor." | +20 | L19 |
| B2-08 | MaherGomez1996 | 案例或数据的表示形式 | p.6 | "uses attribute-value pairs to describe a case." | "and the primary object-based representation uses attribute-value pairs to describe a case." | +5 | L15 |
| B2-09 | MaherGomez1996 | 评价方式 | p.2 | "data from 14 design projects" | "Finally, we reviewed and collected data from 14 design projects." | +5 | L27 |
| B3-02 | Ahmed2013 | 明确写出的局限 | p.9 | "it is only able to ﬁnd the physical existent rooms." | "Furthermore, a weak point of our approach is that it is only able to ﬁnd the physical existent rooms." | +9 | L31 |
| B3-03 | Borner1993 | 案例或数据的表示形式 | p.5 | "represen ted b y its spatial dimensions and nine further attributes" | "eac h ob ject circle or ellipse will b e represen ted b y its spatial dimensions and nine further attributes lik e time at whic h this ob ject w as created asp e ct whic h assumes one of return air fresh air etc and morpholo gy whic h refers to access connection etc" | +45（净） | L15 |
| B3-16 | vanEngelenburg2023 | 案例或数据的表示形式 | p.2 | "geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions" | "Floor plans are digitally represented in various ways that each emphasize different components of interest e.g. as images allowing to model ﬁne-grained details such as materialization and furniture [21, 5], geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions [9, 13, 18, 12]." | +34 | L15 |

## 二、verify 结果（主控执行）

```powershell
cd F:\project\PyProject\Litreview\litrev
python litrev.py verify _probe/full/Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md
python litrev.py verify _probe/full/Gu2024_ShearWall_Diffusion.md
python litrev.py verify _probe/full/MaherGomez1996_CBR_StructuralDesign.md
python litrev.py verify _probe/full/Borner1993_StructuralSimilarity_CBR.md
python litrev.py verify _probe/full/vanEngelenburg2023_SSIG_FloorPlan.md
```

| 文件 | 条数 | PASS | 其他判定 | 退出码 |
|---|---:|---:|---|---:|
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans.md | 7 | 7 | 0 | 0 |
| Gu2024_ShearWall_Diffusion.md | 7 | 7 | 0 | 0 |
| MaherGomez1996_CBR_StructuralDesign.md | 7 | 7 | 0 | 0 |
| Borner1993_StructuralSimilarity_CBR.md | 7 | 7 | 0 | 0 |
| vanEngelenburg2023_SSIG_FloorPlan.md | 7 | 7 | 0 | 0 |
| **合计** | **35** | **35** | **0** | **全 0** |

- T3 后对 `_probe/full/` 全部 19 篇做一次复核：**131/131 PASS，退出码全 0**；确认扩句没有误改其他 14 篇。

## 三、机械检查

- 5 个文件仍各 31 行，7 个字段、7 条引文；行数未变。
- 7/7 条新引文都包含旧引文（`old in new` 为 True），说明是扩边界而不是换句。
- 7/7 条页码标注未变：p.1 / p.6 / p.6 / p.2 / p.9 / p.5 / p.2。
- 7/7 条论断文本未变（与 `C4_FRAG_RESULT.md` §3.2 的「现文论断」逐字一致）。
- 全文英文双引号对数仍为 7，无多余引号。

## 四、例外与说明

1. **MaherGomez1996 p.6（B2-08）没有从句子最开头起引**：原句跨 p.5–p.6，p.6 页首是 `and`；extractor 取了 p.6 段内含主语 `the primary object-based representation` 的最长连续片段，因此新引文以 `and` 开头。没有跨页拼接，也没有按「拆成两条」处理。`verify` PASS，自足轴的主语已进入引号；但严格按「完整句起点」口径，这条仍是例外，建议人工复核是否接受 `and` 起首，或改成 p.5+p.6 两条。
2. **Borner1993 p.5（B3-03）**：该 txt 有严重 OCR 断词（`eac h`、`ob ject`、`represen ted b y`、`whic h` 等），按 HANDOFF-02 §五.1 原样保留，未顺手改正字；新引文 266 字符，`verify` PASS。
3. **扩句后仍有 6 条片段未处理**：`C4_FRAG_RESULT.md` §3.2 的 7 条已处理，但 §3.1 的 20 条非 SUPPORTED 中仍有 `SUPPORTED` 以外的条目；它们不在 T3 自动处理范围，按纪律只列不改。

## 五、子会话

| 文献 | 子会话 id |
|---|---|
| Ahmed2013 | `ses_e41053364ffecqSufXn9HbymKX` |
| Gu2024 | `ses_e4105329affeN2SMhrtD7CUtuR` |
| MaherGomez1996 | `ses_e410531c7ffe6VEKiZk1oCslu3` |
| Borner1993 | `ses_e41053101fferRDRMMSpgQZ05i` |
| vanEngelenburg2023 | `ses_e41053030ffeYEHneOEuD11SCn` |
