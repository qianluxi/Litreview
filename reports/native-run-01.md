# OpenCode 原生 task 运行报告（native-run-01）

- 日期：2026-11-09
- 范围：`HANDOFF.md` 的 T0–T5；T6（矩阵校验）按 HANDOFF 暂缓。
- 执行：主控 `orchestrator` 派发；抽取/核验/审计分别由 `extractor` / `checker` / `auditor` 子会话执行；所有 `verify` 由主控或核验员独立运行。
- 结论：**T0 的 PDF 直读失败，已按 HANDOFF 的失败处理切换为主控预导出 txt；切换后 T0–T5 全部完成。引文层 143/143 PASS，退出码全 0；论断层只审了 run1 的 12 条（7 SUPPORTED / 5 PARTIAL / 0 UNSUPPORTED，2 DEPENDENT），全量 131 条尚未做 C4 审计。**

## 0. 总账（可机械复现）

| 阶段 | 对象 | 文件数 | 引文条数 | PASS | PAGE | AUTHOR | PARAPHRASE | MISSING | NOPAGE | ZHQUOTE | verify 退出码 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| T0+T1（run1） | run1 的 4 篇 | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 4 篇均 0 |
| T2（复核 run1，不新增条数） | run1 的 4 篇 | 4 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 4 篇均 0 |
| T4（full） | full 的 19 篇 | 19 | 131 | 131 | 0 | 0 | 0 | 0 | 0 | 0 | 19 篇均 0 |
| **合计（唯一引文）** | **run1 + full** | **23** | **143** | **143** | **0** | **0** | **0** | **0** | **0** | **0** | **全部 0** |

- 统计来源：`litrev/_probe/run1/*_引文核验.md`（4 份）与 `litrev/_probe/full/*_引文核验.md`（19 份）的「汇总」行及逐行判定；解析结果 `run1 AGG {'PASS': 12}`、`full AGG {'PASS': 131}`，合计 143。
- 未出现任何 `PAGE` / `AUTHOR` / `PARAPHRASE` / `MISSING` / `NOPAGE` / `ZHQUOTE`；因此 **verify 失败清单为空**。
- 上面 23 个对象中，`Zhang2006` 在 run1 与 full 各出现一次（T0 冒烟稿 3 条，T4 全量稿 7 条），不是重复计数错误。

---

## 1. T0 能力探测 + 单篇冒烟

### 1.1 派发

- 目标：`参考文献原文/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.pdf`（5 页，最短）。
- 输出：`litrev/_probe/run1/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md`。
- 子会话：`ses_e41ed396dffeLWlztYY2ymzE9U`（PDF 直读，失败）；`ses_e41ecbcb9ffebObTPHBsssXGgW`（预导出 txt，成功）。

### 1.2 PDF 直读结果：失败（原文）

extractor 只用了 `read` 工具直接打开 PDF，没有运行 python/OCR/转换工具。返回：

```
PDF read successfully
ERROR: Cannot read pdf (this model does not support pdf input). Inform the user.
```

结论：**当前模型在 OpenCode 的 `read` 工具链下无法读 PDF**。这与 HANDOFF 第〇节的未验证前提一致；WorkBuddy 上一轮能直读，不代表 OpenCode 原生 `task` 也能。

### 1.3 按 HANDOFF 失败处理切换

HANDOFF 写的是「停下来……改用主控预导出 txt（与 `_probe/texts/` 同一格式），不要自己发明第三条路」。主控据此做了两件事：

1. 用 PyMuPDF 按 `page.get_text()` 导出，格式与既有 `_probe/texts/` 完全一致：
   ```
   # SOURCE: Zhang2006_BP_CaseRetrieval_HighriseStructureForm.pdf
   # PDF 物理页数: 5

   <<<PAGE 1>>>
   ...
   ```
   导出脚本：`C:\Users\246\AppData\Local\Temp\opencode\export_zhang2006.py`（临时文件，不在仓库内）。
   输出：`litrev/_probe/texts/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.txt`（5 页、5 个页标记、19506 字节）。
2. 重新派 extractor 只读该 txt。子会话 `ses_e41ecbcb9ffebObTPHBsssXGgW` 写出 3 条引文，物理页为 p.1 / p.2 / p.2。

### 1.4 验收

命令与输出（工作目录 `F:\project\PyProject\Litreview\litrev`）：

```
python litrev.py verify _probe/run1/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md
OK  1. L4    PASS ...
OK  2. L6    PASS ...
OK  3. L8    PASS ...
汇总：PASS=3   合计 3
EXITCODE=0
```

- ① 文件生成且只生成这一个：T0 完成时 `run1/` 下只有该 md（`verify` 之后才多出 `_引文核验.md`）。
- ② 3 条引文均带 PDF 物理页：p.1、p.2、p.2。
- ③ 退出码 0。

---

## 2. T1 并行 3 篇

### 2.1 同一条消息内派发

同一条 assistant 消息里并列 3 个 `task`，分别处理：

| 篇 | 子会话 id | 起始 | 结束 | 输出 |
|---|---|---|---|---|
| Napps2021_BIM_VariantRetrieval_CBR | `ses_e41eb8173ffe2BW5hT47AxkQKA` | 10:12:56.605 | 10:13:57.581 | `run1/Napps2021_BIM_VariantRetrieval_CBR.md` |
| Ayzenshtadt2016_ThinkingWithContainers_ICAART | `ses_e41eb7fb0ffe8IrcjVJz2zcS5h` | 10:12:57.045 | 10:13:41.048 | `run1/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md` |
| MaherGomez1997_CBR_in_Design | `ses_e41eb7ef5ffeH7T2t878japZQR` | 10:12:57.232 | 10:14:52.296 | `run1/MaherGomez1997_CBR_in_Design.md` |

时间取自 `~/.local/share/opencode/opencode.db` 的 `part` 表（只读快照，`mode=ro`）；三条子会话的起始相差 ≤0.63 秒，时间区间互相重叠，**是原生并行，不是串行排队**。

### 2.2 verify

```
python litrev.py verify _probe/run1/Napps2021_BIM_VariantRetrieval_CBR.md          # EXITCODE=0, PASS=3
python litrev.py verify _probe/run1/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md  # EXITCODE=0, PASS=3
python litrev.py verify _probe/run1/MaherGomez1997_CBR_in_Design.md                # EXITCODE=0, PASS=3
```

**9/9 PASS**，无 `PARAPHRASE` / `MISSING` / `PAGE`，与基线 9/9 持平。

### 2.3 与 `_probe/notes/` 基线逐条比对

页码全部与基线一致；措辞差异如下：

| 篇 | 页码（基线→本轮） | 差异 |
|---|---|---|
| Napps2021 | 1/3/3 → 1/3/3 | 条目 3 的论断删掉了基线里的「即基于 IFC 标准实现」；引文完全相同。这是对基线「从 data structure 推到 standard」的修正，不是回归。 |
| Ayzenshtadt2016 | 1/1/5 → 1/1/5 | 条目 2 的引文由基线的名词短语 `user queries built with a semantic description model Semantic Fingerprint` 扩为 `where agents work in groups (containers) on resolving of user queries built with a semantic description model Semantic Fingerprint`；论断相应补了「代理按容器分组解析查询」。逐字与页码均 PASS。 |
| MaherGomez1997 | 2/2/2 → 2/2/2 | 条目 2 的引文由基线的 `it decomposes into the subtasks of indexing, retrieval, and selec- tion (see Figure 2a).` 扩为 `Design-case recall involves finding a rel- evant design experience; it decomposes into the subtasks of ...`；主语被包进引号，修掉了基线 `DEPENDENT` 的自足问题。 |

结论：本轮 3 篇不仅没有回归，反而把 `RESULT.md` 第三节点名的两类问题（Napps 术语外推、MaherGomez1997 引文不自足）修掉了，并顺带把 Ayzenshtadt 条目 2 的名词短语扩成带主谓的句子。

---

## 3. T2 核验（checker）

- 子会话：`ses_e41e926aaffeWYqnVh14txib8B`。
- 对象：`_probe/run1/` 下 4 个抽取稿（不含 `_引文核验.md`）。
- 命令与退出码：

```
python litrev.py verify _probe/run1/Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md          # 0
python litrev.py verify _probe/run1/Napps2021_BIM_VariantRetrieval_CBR.md                          # 0
python litrev.py verify _probe/run1/Ayzenshtadt2016_ThinkingWithContainers_ICAART.md               # 0
python litrev.py verify _probe/run1/MaherGomez1997_CBR_in_Design.md                                # 0
```

- 逐文件计数：4 篇均为 `3 条 / PASS 3 / 其余 0`；汇总 **12/12 PASS**。
- 待改清单：**无**（12 条全部 PASS）。
- 本次 `verify` 生成的报告（4 份，均在 `_probe/run1/`）：

```
Zhang2006_BP_CaseRetrieval_HighriseStructureForm_引文核验.md
Napps2021_BIM_VariantRetrieval_CBR_引文核验.md
Ayzenshtadt2016_ThinkingWithContainers_ICAART_引文核验.md
MaherGomez1997_CBR_in_Design_引文核验.md
```

- 边界声明（原文照录）：**本次未验证论断层**；`PASS` 只证明「逐字存在、页码正确、作者匹配」，不证明「引文支撑论断」。

---

## 4. T3 审计（auditor）

- 子会话：`ses_e41e82d3affeCgrb5t7GH9EUgd`。
- 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节 v1 口径修订），未临时改口径。
- 输入：run1 的 12 条五元组（id、论断、引文、页码、出处）；闭卷，未给 `run_A_B_v1.md`，避免锚定。

### 4.1 判定表（原文）

| id | 支撑 | 自足 | 引文里的依据（≤15 字，必须是引文原词） | 缺什么 / 需补的一句 |
|----|------|------|--------------------------------------|--------------------|
| 01 | SUPPORTED | SELF | "BIM-based variant retrieval" | — |
| 02 | PARTIAL | SELF | "is a possibility" | 引文只说 GPM "is a possibility"，论断"采用"属情态升级；应写"可能用于" |
| 03 | PARTIAL | SELF | "can be defined" | 引文是 "can be defined"，论断"给出度量/分别给出"属升级；应写"可定义" |
| 04 | SUPPORTED | SELF | "distributed retrieval system" | — |
| 05 | SUPPORTED | SELF | "Semantic Fingerprint" | — |
| 06 | PARTIAL | SELF | "can be seen as" | 引文 "can be seen as"，论断"是"属情态升级；应写"可视为" |
| 07 | SUPPORTED | SELF | "Two major considerations" | — |
| 08 | SUPPORTED | DEPENDENT | "decomposes into the subtasks" | 引文以 it 指代，论断补主语正确；引文本身不可直引 |
| 09 | SUPPORTED | SELF | "Indexing identifies the features" | — |
| 10 | PARTIAL | DEPENDENT | "analyzes the defects" | 引文未写"不能自学习、智能化程度低"及"高层结构智能选型"；且句首缺主语 |
| 11 | SUPPORTED | SELF | "relative Euclidean weight distance" | — |
| 12 | PARTIAL | SELF | "only some experimental conclusions" | 引文只讲缺成熟理论，"作者自行设定网络结构"无引文依据 |

`合计：12 条（SUPPORTED 7 / PARTIAL 5 / UNSUPPORTED 0；DEPENDENT 2）`

### 4.2 机械复核

「依据」列 12/12 都能在对应引文中逐字命中：

```
01 OK 'BIM-based variant retrieval'          07 OK 'Two major considerations'
02 OK 'is a possibility'                     08 OK 'decomposes into the subtasks'
03 OK 'can be defined'                       09 OK 'Indexing identifies the features'
04 OK 'distributed retrieval system'         10 OK 'analyzes the defects'
05 OK 'Semantic Fingerprint'                 11 OK 'relative Euclidean weight distance'
06 OK 'can be seen as'                       12 OK 'only some experimental conclusions'
```

### 4.3 与 `_probe/audit/run_A_B_v1.md` 的一致率

run1 的 01–09 与 `run_A_B_v1.md` 的 01–09 是同题；10–12 是新增的 Zhang2006。按同题 9 条逐条比：

| 轴 | 与审计员 A | 与审计员 B |
|---|---:|---:|
| 支撑（01–09） | 9/9 | 9/9 |
| 自足（01–09） | 9/9 | 8/9（仅 06 不同：本轮 SELF，B 判 DEPENDENT） |

- 参照值：`RESULT.md` 记录上一轮 run_A_B_v1 **支撑轴与人工基准 11/13**，A 与 B 之间 13/13 完全相同。
- 口径说明：本轮 02、03、05、06、08 的论断/引文曾被修订（见 2.3），所以 9/9 是「同题同判定」，不是拿旧标签强行套新文本。
- **待人工复核**：08 本轮引文已含主语 `Design-case recall`，按 `AUDIT_CONTRACT` 第五节「自足轴只管主语」，应可判 `SELF`；审计员仍判 `DEPENDENT`（理由写「引文以 it 指代」）。本报告不改判定，只标记为口径偏严的候选点。A 对基线 08 也判 DEPENDENT，说明这是旧口径的延续。

### 4.4 非 SUPPORTED 清单（只列，不改稿）

| id | 文献 | 现文（论断） | 引文里的依据（原文） | 位置 |
|---|---|---|---|---|
| 02 | Napps2021 | 匹配与检索采用图模式匹配（GPM）…… | `is a possibility to find (suitable) variants` | `_probe/run1/Napps2021...md` L6 |
| 03 | Napps2021 | ……按实体类型分别对 IFC 工程量与属性定义给出相似度度量。 | `can be defined` | `_probe/run1/Napps2021...md` L8 |
| 06 | Ayzenshtadt2016 | 每个检索容器……都是……完全自治的多智能体子系统。 | `can be seen as` | `_probe/run1/Ayzenshtadt2016...md` L8 |
| 10 | Zhang2006 | 论文针对……不能自学习、智能化程度低的问题，提出并建立…… | `analyzes the defects` | `_probe/run1/Zhang2006...md` L4 |
| 12 | Zhang2006 | ……作者只能依据既有信息与检索需要自行设定网络结构。 | `only some experimental conclusions` | `_probe/run1/Zhang2006...md` L8 |
| 08 | MaherGomez1997 | 设计案例召回被分解为索引、检索与选择三个子任务。 | `decomposes into the subtasks`（支撑 SUPPORTED，仅自足 DEPENDENT） | `_probe/run1/MaherGomez1997...md` L6 |

---

## 5. T4 全量抽取（19 篇，5 批）

### 5.1 先写契约，再派活

- 契约：`litrev/_probe/CONTRACT_P1.md`（v1），先把 P1 的 7 个字段、引文硬规则、SharmaThesis 范围限制、19 篇的引用标签表写定，再派第一批。
- 字段：一句话主张 / 问题域 / 案例或数据的表示形式 / 相似性或检索机制 / 系统形态 / 评价方式 / 明确写出的局限；每字段一条中文论断 + 一条逐字英文引文 + PDF 物理页。
- 契约里明确：缺失字段写「未涉及」；找不到引文写 `NOT_FOUND` 并列出查过的页；单条引文 ≤500 字符、单行、≥20 字母、不跨页。

### 5.2 输入：主控预导出 txt

- 脚本：`C:\Users\246\AppData\Local\Temp\opencode\export_p1_texts.py`（临时文件，不在仓库内）。
- 输出：`litrev/_probe/texts/` 下 19 篇，页标记数与 PDF 物理页数一致（5/10/10/10/12、11/11/11/17/17、18/20/21/21/23、22/22/27、151）。
- 原因：T0 已证明当前模型无法 `read` PDF；按 HANDOFF 的失败处理统一预导出，不让子 agent 自己转换。

### 5.3 分批与结果

每批都是**同一条消息内并列 N 个 `task`**；每批完成后立即跑 `verify`。

| 批 | 文献 | 篇数 | 引文 | PASS | verify 退出码 | 子会话（起始时间） |
|---|---|---:|---:|---:|---|---|
| B1 | Zhang2006 / Ahmed2013 / Soibelman2000 / vanEngelenburg2023 / delasHeras2014 | 5 | 35 | 35 | 5 篇均 0 | 10:19:27.206–10:19:28.071（5 会话起跑差 ≤0.87s） |
| B2 | Borner1993 / MaherGomez1996 / Sabri2017 / Roith2017 / Xia2025 | 5 | 35 | 35 | 5 篇均 0 | 10:22:43.660–10:22:45.326（差 ≤1.67s） |
| B3 | Rodrigues2017 / Gu2024 / Maher1987 / AamodtPlaza1994 / Liao1998 | 5 | 34 | 34 | 5 篇均 0 | 10:30:27.928–10:30:28.745（差 ≤0.82s） |
| B4 | Sriram1985 / Zhao2023 / Survey2025 | 3 | 20 | 20 | 3 篇均 0 | 10:34:05.665–10:34:06.229（差 ≤0.57s） |
| B5 | SharmaThesis | 1 | 7 | 7 | 0 | 10:36:14.835 |
| **合计** | **19 篇** | **19** | **131** | **131** | **全 0** | — |

说明：B3 少 1 条、B4 少 1 条，原因是两个字段写「未涉及」，不是失败（见 5.4）。

### 5.4 逐篇结果

| 文献 | 字段有引文数 | 引文 | PASS | 备注 |
|---|---:|---:|---:|---|
| Zhang2006_BP_CaseRetrieval_HighriseStructureForm | 7 | 7 | 7 | — |
| Ahmed2013_Analysis_SketchRetrieval_FloorPlans | 7 | 7 | 7 | — |
| SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 7 | 7 | 7 | — |
| vanEngelenburg2023_SSIG_FloorPlan | 7 | 7 | 7 | — |
| delasHeras2014_RunlengthHistogram_FloorPlans | 7 | 7 | 7 | — |
| Borner1993_StructuralSimilarity_CBR | 7 | 7 | 7 | txt 有逐词断行（如 `similarit y`），verify 归一化后 PASS |
| MaherGomez1996_CBR_StructuralDesign | 7 | 7 | 7 | 多条为句中片段，见遗留问题 |
| Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM | 7 | 7 | 7 | 印张偏移 +49，报的是物理页 |
| Roith2017_GraphBasedDesign_FederatedDB_VisEng | 7 | 7 | 7 | — |
| Xia2025_CoDesign_ShearWallBeam_GNN | 7 | 7 | 7 | — |
| Rodrigues2017_Clustering_FloorPlans | 7 | 7 | 7 | 印张偏移 +47，报的是物理页 |
| Gu2024_ShearWall_Diffusion | 7 | 7 | 7 | — |
| Maher1987_ExpertSystems_StructuralDesign | 7 | 7 | 7 | 印张偏移 -3，报的是物理页 |
| AamodtPlaza1994_CBR_Foundations | 7 | 7 | 7 | — |
| Liao1998_SimilarityMeasures_CBR | 6 | 6 | 6 | 字段 7「明确写出的局限」= 未涉及 |
| SriramMaherFenves1985_KBES_StructuralDesign | 6 | 6 | 6 | 字段 6「评价方式」= 未涉及；印张偏移 -3，报的是物理页 |
| Zhao2023_ShearWall_GNN | 7 | 7 | 7 | — |
| Survey2025_FloorPlanRetrieval_MDPI | 7 | 7 | 7 | 作者标注用 `Ling et al., 2025`（aliases.json） |
| SharmaThesis_ContentBasedFloorPlanRetrieval | 7 | 7 | 7 | 只抽 p.21–22、p.50–57、p.142–145，见 5.5 |

`NOT_FOUND` 数量：0；「未涉及」数量：2（Liao 字段 7、Sriram 字段 6）。

### 5.5 SharmaThesis 的范围合规

文件顶部原文：

```
- 抽取范围：摘要 p.21–22；第 3 章 §3.5 Graph Spectral Embedding 与 §3.6 Experiments and Results p.50–57；第 7 章 Conclusions（§7.1–7.3）p.142–145。
```

7 条引文的页码为 p.21 / p.142 / p.50 / p.52 / p.21 / p.143 / p.143，全部落在上述范围内，未全文扫描。

### 5.6 四个页码陷阱

HANDOFF 点名的 4 篇（Sriram1985、Rodrigues2017、MaherGomez1996、Sabri2017）印张页码与 PDF 物理页不一致。本轮 4 篇全部按 `<<<PAGE n>>>` 报物理页，verify 全部 PASS：

| 文献 | 印张偏移（manifest） | 本轮报的页 | 结果 |
|---|---:|---|---|
| SriramMaherFenves1985 | -3 | 3 / 4 / 8 / 11 / 7 / 19 | 6/6 PASS |
| Rodrigues2017 | +47 | 13 / 1 / 6 / 4 / 2 / 1 / 13 | 7/7 PASS |
| MaherGomez1996 | +41 | 1 / 1 / 6 / 4 / 2 / 2 / 10 | 7/7 PASS |
| Sabri2017 | +49 | 1 / 1 / 4 / 4 / 1 / 7 / 7 | 7/7 PASS |

---

## 6. 失败清单

### 6.1 引文层（verify）

**无。** 143 条中 0 条 `PAGE` / `AUTHOR` / `PARAPHRASE` / `MISSING` / `NOPAGE` / `ZHQUOTE`，所有 `verify` 退出码 0。

### 6.2 论断层（C4）

只审了 run1 的 12 条；非 SUPPORTED 的 6 条见 4.4（02、03、06、10、12 为 PARTIAL；08 为自足 DEPENDENT）。按 T3 纪律，**未改稿**，只列清单交人。全量 131 条未做 C4 审计，见 8.1。

---

## 7. 与上一轮基线的差异

1. **PDF 直读**：上一轮 WorkBuddy 能直读 PDF；本轮 OpenCode 原生 `read` 返回 `ERROR: Cannot read pdf (this model does not support pdf input)`。因此本轮所有抽取都走主控预导出 txt，这是流程差异，不是抽取质量问题。
2. **T1 质量**：上一轮 9/9 PASS；本轮 9/9 PASS，无回归。差异仅在措辞与引文长度：Napps 条目 3 删掉了「IFC 标准」外推；Ayzenshtadt 条目 2、MaherGomez1997 条目 2 扩了引文，修掉基线不自足的问题。
3. **T3 审计**：run1 同题 01–09 的支撑轴与 A、B 均 9/9；自足轴与 A 9/9、与 B 8/9（06）。上一轮 run_A_B_v1 的支撑轴与人工基准 11/13，A/B 内部 13/13。
4. **全量**：上一轮没有 19 篇全量产物；本轮新增 19 篇 131 条，全部 PASS；其中 SharmaThesis 按契约只抽指定范围，不是全文覆盖。
5. **路径口径**：HANDOFF 的派发模板写 `litrev/参考文献原文/<文献>.pdf`，实际 PDF 在项目根 `参考文献原文/`；`litrev.py` 的 `PDF_DIR = BASE.parent / "参考文献原文"` 也指向根目录。本轮按实际路径派发，未改 `litrev.py`。建议修正 HANDOFF 模板，避免下一轮照抄出错。

---

## 8. 遗留问题

1. **全量 131 条未做 C4 审计**。`verify` 只守 L1–L3（逐字、页码、作者），不守「引文是否撑得起论断」。本轮 T3 只覆盖 run1 的 12 条；用全量卡片写综述前，建议按 `AUDIT_CONTRACT.md` 对 19 篇做至少一次 C4 审计，尤其是 B2–B4 的短片段引文。
2. **部分全量引文是句中片段**，`verify` 能过，但学术上可能不自足。例：MaherGomez1996 的字段 1 `Toward that end, this article presents four`、字段 4 `a given problem by finding matches between`、字段 5 `CaseCAD using Framekit, a frame-based`、字段 6 `data from 14 design projects`、字段 7 `when case memory contains a limited`。这类条目在 C4 审计里大概率会被判 `DEPENDENT` 或 `PARTIAL`，写稿时应扩引文或改转述。
3. **Borner1993 的 txt 逐词断行严重**（`similarit y`、`kno wledge`、`protot ypically`）。verify 归一化后 PASS，但直接引用到成稿会很难看；建议另找干净文本或 OCR 后重新导出，再重跑该篇。
4. **PDF 直读通道不可用**。任何子 agent 若被直接指向 `.pdf`，都会失败；下一轮派发必须继续走主控预导出 txt，或换支持 PDF 输入的模型。这一条应写进 PIPELINE.md 的 T0 记录。
5. **权限隔离未启用**。「不读 `litrev.py` / `_index/`」目前只靠 prompt；HANDOFF 第五节风险 2 建议的 `permission` 块仍未加，需要重启 OpenCode，本轮未做。
6. **`verify` 会污染源目录**。`run1/` 与 `full/` 现有 23 份 `*_引文核验.md`（4 + 19）。清理命令（确认不再需要报告后）：
   ```powershell
   Remove-Item litrev\_probe\run1\*_引文核验.md
   Remove-Item litrev\_probe\full\*_引文核验.md
   ```
7. **T3 的 08 自足判定偏严**。引文已含主语 `Design-case recall`，按 v1 口径应可判 `SELF`；审计员判 `DEPENDENT`。未改判定，建议下一轮标定时把这条作为口径复核样本。
8. **SharmaThesis 只覆盖指定范围**（p.21–22、p.50–57、p.142–145），不是 151 页全文；如果综述需要论文其他章节（如文献综述章、附录），要另派一次带明确页码范围的抽取。
9. **WangHoward1991 仍未处理**：130 页纯扫描、无文字层，不在 19 篇内；要引它必须先 OCR。
10. **T6 未做**：`文献对比与系统特征表2.xlsx` 与稿件目录不在仓库，`matrix` 没有对象，按 HANDOFF 暂缓。

---

## 9. 产物与复现

### 9.1 产物

```
litrev/_probe/CONTRACT_P1.md                                  T4 契约
litrev/_probe/texts/*.txt                                     22 个（3 个 T1 基线 + 19 个 T4；Zhang2006 在 19 内）
litrev/_probe/run1/*.md                                        4 个抽取稿 + 4 个 *_引文核验.md
litrev/_probe/full/*.md                                       19 个抽取稿 + 19 个 *_引文核验.md
reports/native-run-01.md                                      本报告
```

临时脚本（不在仓库内，供复现）：

```
C:\Users\246\AppData\Local\Temp\opencode\export_zhang2006.py
C:\Users\246\AppData\Local\Temp\opencode\export_p1_texts.py
```

### 9.2 复现命令

```powershell
cd F:\project\PyProject\Litreview\litrev

# run1 逐篇
python litrev.py verify _probe/run1\Zhang2006_BP_CaseRetrieval_HighriseStructureForm.md
python litrev.py verify _probe/run1\Napps2021_BIM_VariantRetrieval_CBR.md
python litrev.py verify _probe/run1\Ayzenshtadt2016_ThinkingWithContainers_ICAART.md
python litrev.py verify _probe/run1\MaherGomez1997_CBR_in_Design.md

# full 逐篇（19 篇，文件名见 5.4）
python litrev.py verify _probe/full\<文献名>.md
```

### 9.3 取证脚本（可选）

本轮并行证据的取数方式（只读，不改库）：

```python
import sqlite3, os
p = os.path.expanduser(r"~\.local\share\opencode\opencode.db")
con = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
cur = con.cursor()
# 对每个 session_id 取 min(time_created) / max(time_updated)
```

---

## 10. 一句话交接

**技术层：T0 的 PDF 直读不可用，已按 HANDOFF 切到主控预导出 txt；T0–T5 全通，引文层 143/143 PASS，四个印张偏移陷阱全部报对物理页。质量层：run1 12 条 C4 审计 7 SUPPORTED / 5 PARTIAL / 0 UNSUPPORTED，全量 131 条还没审；下一轮最该做的不是再抽一批，而是给 19 篇全量卡片补 C4 审计，并把 MaherGomez1996 之类短片段引文扩到自足。**

---

**核验**：本报告已由第三方复核，见 `reports/native-run-01-verification.md`（2026-11-09）。两处需并读：§1.2 的 PDF 报错**归因不准确**——`read` 实为 `status=completed` 且 `metadata.loaded=[]`（工具自称成功、实际 0 页加载），报错只出现在模型侧附件，而非工具返回；§5.3 的 B3 起跑差实测为 0.840s（原文写 ≤0.82s）。其余数字均经双路径复现。
