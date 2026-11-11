# C2 自足轴判例集映射（主控侧留档，不贴给任何人）

> 由 `python tools/audit_prep.py cases` 生成，与 `CASES_SELF_C2.md` 同源；条目清单来自 `CASES_SELF_C2_IDS.txt`。
> 判定表总条目 138 · 本集 14 条（表内 DEPENDENT 2 + 阴性对照 12）。
> 输入快照戳：`3c036c65ae`
> **本文件是答案键**：记录每条 C id 对应的原批次 id 与表内现判；判定者填表时读不到本文件。
> 人填完后跑 `python tools/audit_prep.py verify-cases`，输出自足轴一致率与方向。
> 下方 `<!-- picks -->` 是冻结清单：判定表事后被裁决修改，本文件不失效，`cases --check` 仍按清单复现。

<!-- picks: total=138,R2-12,B2-10,R2-14,R3-05,R3-04,R5-09,R1-11,R3-14,B2-03,R4-02,B1-09,R5-04,R4-11,B1-15 -->

## 对照表（C id → 表内现判）

| C id | 原批次 id | 文献 | 节 | 表内支撑 | 表内自足 | 表内依据 | 表内缺什么 |
|---|---|---|---|---|---|---|---|
| C01 | R2-12 | SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 相似性或检索机制 | SUPPORTED | SELF | "subset of cases" | — |
| C02 | B2-10 | SriramMaherFenves1985_KBES_StructuralDesign | 一句话主张 | SUPPORTED | DEPENDENT | "applications of" | 自足缺主谓：引文是介词短语+名词短语，主谓落在引号外，引用时需补主语与谓语 |
| C03 | R2-14 | Xia2025_CoDesign_ShearWallBeam_GNN | 一句话主张 | SUPPORTED | SELF | "co-design" | — |
| C04 | R3-05 | Rodrigues2017_Clustering_FloorPlans | 系统形态 | SUPPORTED | SELF | "are studied as" | — |
| C05 | R3-04 | Maher1987_ExpertSystems_StructuralDesign | 系统形态 | SUPPORTED | SELF | "combination of" | — |
| C06 | R5-09 | SharmaThesis_ContentBasedFloorPlanRetrieval | 案例或数据的表示形式 | SUPPORTED | SELF | "is adopted" | — |
| C07 | R1-11 | SriramMaherFenves1985_KBES_StructuralDesign | 相似性或检索机制 | SUPPORTED | SELF | "uses backward chaining" | — |
| C08 | R3-14 | Xia2025_CoDesign_ShearWallBeam_GNN | 明确写出的局限 | SUPPORTED | SELF | "potential beams" | — |
| C09 | B2-03 | Borner1993_StructuralSimilarity_CBR | 问题域 | SUPPORTED | SELF | "not restricted" | — |
| C10 | R4-02 | Gu2024_ShearWall_Diffusion | 问题域 | SUPPORTED | SELF | "shear wall" | — |
| C11 | B1-09 | MaherGomez1996_CBR_StructuralDesign | 系统形态 | SUPPORTED | DEPENDENT | "using Framekit" | 自足缺主谓：引文为分词短语，需补主语成句（如 CaseCAD is a system using Framekit） |
| C12 | R5-04 | Maher1987_ExpertSystems_StructuralDesign | 明确写出的局限 | SUPPORTED | SELF | "restricted to" | — |
| C13 | R4-11 | SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign | 评价方式 | SUPPORTED | SELF | "hypothetical" | — |
| C14 | B1-15 | Zhao2023_ShearWall_GNN | 相似性或检索机制 | SUPPORTED | SELF | "i.e., IoUpixel" | — |

> 共 14 条。

## 原文存档（抽样时点，返工后按此复现）

> 判定时点给出的论断与引文原文。稿件返工后**本节不改写**：`CASES_SELF.md` 的条目详情按本节复现，
> `verify-cases` 用本节 vs 当前批次输入比对，把判后被返工的条目列为「失效」并从分母剔除。

### C01 ・ R2-12

- 论断：检索由 Caspian 执行，索引检索完成后可运行两种模式，启用案例匹配器时程序扫描案例子集并找出权重值最高的案例。
- 引文："After the index search has been completely successfully, Caspian can be run in two different modes: with or without case matcher. If the case matcher is invoked, the program scans the subset of cases to ﬁnd the one with the highest weight value." (Soibelman et al., 2000, p.5)

### C02 ・ B2-10

- 论断：本文介绍 KBES 在 preliminary design、analysts 与 detailed design 的应用。
- 引文："In this paper applications of KBES to the preliminary design, analysts, and detailed design" (Sriram et al., 1985, p.3)

### C03 ・ R2-14

- 论断：作者提出将剪力墙与梁的耦合潜在位置统一表示为图，并用图神经网络（GNN）驱动剪力墙与梁的协同设计。
- 引文："This study constructed a graph representation of the coupled potential positions for shear walls and beams and proposed a co-design method driven by a graph neural network (GNN)." (Xia et al., 2025, p.1)

### C04 ・ R3-05

- 论断：本文在同一设置下把四种形状表示作为平面图设计描述子加以研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)

### C05 ・ R3-04

- 论断：HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文："HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language." (Maher, 1987, p.6)

### C06 ・ R5-09

- 论断：采用图谱嵌入，把前一步生成的房间布局图表示到模式空间中。
- 引文："Graph Spectral Embedding [Luo et al., 2003] approach is adopted to represent the room layout graphs created in the previous stage in a pattern-space." (Sharma, 2018, p.50)

### C07 ・ R1-11

- 论断：系统的推理机制采用反向链，对目标树进行深度优先搜索。
- 引文："The inference mechanism uses backward chaining that produces a depth-first search of a goal tree." (Sriram et al., 1985, p.11)

### C08 ・ R3-14

- 论断：作者明确指出梁的生成依赖潜在梁的布置，因此仍需探索更好的潜在梁生成方法，例如引入更多工程经验规则与硬编码规则。
- 引文："Although case studies show that the algorithms of co-design have achieved good results, considering that the generation of beams depends on the arrangement of potential beams, it is still necessary to explore better methods for generating potential beams, such as introducing more engineering experience rules and hard-coding rules, to further optimize the generation of potential beams." (Xia et al., 2025, p.15)

### C09 ・ B2-03

- 论断：方法本身不限于特定领域；示例取自工业建筑设计领域。
- 引文："Although our approach is more theoretical in nature and not restricted to a speci c domain we will give an example taken from the domain of industrial building design" (Borner, 1993, p.1)

### C10 ・ R4-02

- 论断：研究面向剪力墙布置方案的生成设计。
- 引文："This study proposes a shear wall layout generation method based on a diffusion process." (Gu et al., 2024, p.2)

### C11 ・ B1-09

- 论断：CaseCAD 使用 Framekit。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)

### C12 ・ R5-04

- 论断：作者明确指出 HI-RISE 目前局限于矩形周边和简单矩形结构网格的建筑。
- 引文："HI-RISE is currently restricted to buildings with a rectangular perimeter and a simple rectangular structural grid." (Maher, 1987, p.7)

### C13 ・ R4-11

- 论断：评价方式是开发原型并以一个假设的波士顿办公楼设计为例，展示原型如何运行及其设计建议，以检验模型的可行性。
- 引文："To test the feasibility of the proposed model, an M-RAM prototype was developed. To see how the prototype works and its design recommendations, consider, for example, the design of a hypothetical ofﬁce building in Boston, Massachusetts." (Soibelman et al., 2000, p.7)

### C14 ・ B1-15

- 论断：相似性以 IoUpixel 衡量，比较对象是 GNN 生成结果与真值结果在像素图像上的重合。
- 引文："shear wall design results generated by the GNN model and the ground-truth shear wall design results in pixel images, i.e., IoUpixel, is" (Zhao et al., 2023, p.9)
