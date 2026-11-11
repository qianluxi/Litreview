<!-- 作废存档：本文件是 C2 第一次回写的原始状态，判定对象被理解成「论断能否读懂」，
     得到自足轴 8/14。按契约 §五.1「自足轴只管主语」复算应为 14/14（差异 6 条全部来自判据层级不同）。
     保留原文仅为可追溯，**不要拿本文件的一致率当参考集读数**。现行文件见 CASES_SELF_C2.md。 -->

# 自足轴判例集 C2（14 条，开卷裁定）

> 由 `python tools/audit_prep.py cases` 生成；条目清单见 `CASES_SELF_C2_IDS.txt`（冻结，抽完不再重抽）。  
> **这是给人填的表**：不进 `BATCHES.json`、不生成 agent、`auditor-*` 的 read 白名单不含本文件。  
> 只判**自足轴**：论断脱离引文与上下文能不能独立读懂。可读卡片原文（开卷），但不要读 `out_*.md`、  
> `SAMPLE_S1_KEYS.md`、`GOLDEN.md`、`CASES_SELF_C2_KEYS.md`。  
> 填法：每行填 自足（`SELF` / `DEPENDENT`）、引文里的依据（≤15 字，必须是引文原词）、  
> 缺什么（`DEPENDENT` 必须写明缺的是哪个指代/专有名词；`SELF` 填 `—`）。  
> 快照 sha1: 3c036c65ae

## 待填判定表（人填）

| id  | 自足        | 引文里的依据（≤15 字，必须是引文原词）                                                    | 缺什么 / 需补的一句                |
| --- | --------- | ------------------------------------------------------------------------ | -------------------------- |
| C01 | SELF      | <span style="background-color:rgb(235, 235, 235)">Caspian</span>         |                            |
| C02 | SELF      | <span style="background-color:rgb(235, 235, 235)">In this paper</span>   |                            |
| C03 | SELF      | <span style="background-color:rgb(235, 235, 235)">GNN</span>             |                            |
| C04 | SELF      | <span style="background-color:rgb(235, 235, 235)">same settings</span>   |                            |
| C05 | SELF      | <span style="background-color:rgb(235, 235, 235)">implemented in</span>  |                            |
| C06 | DEPENDENT | <span style="background-color:rgb(235, 235, 235)">previous stage</span>  | 缺“前一步”指哪个阶段/步骤，先行词在引文外     |
| C07 | DEPENDENT | <span style="background-color:rgb(235, 235, 235)">goal tree</span>       | 缺“系统”指哪个系统，先行词在引文外         |
| C08 | SELF      | <span style="background-color:rgb(235, 235, 235)">potential beams</span> |                            |
| C09 | DEPENDENT | <span style="background-color:rgb(235, 235, 235)">domain</span>          | 缺“方法”指哪种方法，先行词在引文外         |
| C10 | SELF      | <span style="background-color:rgb(235, 235, 235)">shear wall</span>      |                            |
| C11 | SELF      | <span style="background-color:rgb(235, 235, 235)">using Framekit</span>  |                            |
| C12 | SELF      | <span style="background-color:rgb(235, 235, 235)">restricted to</span>   |                            |
| C13 | DEPENDENT | <span style="background-color:rgb(235, 235, 235)">M-RAM prototype</span> | 缺“原型/模型”指代：指 M-RAM，先行词在上下文 |
| C14 | SELF      | <span style="background-color:rgb(235, 235, 235)">IoUpixel</span>        |                            |

## 条目详情（判定时可读卡片原文，开卷）

### C01 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 相似性或检索机制 ・ p.5

- 论断：检索由 Caspian 执行，索引检索完成后可运行两种模式，启用案例匹配器时程序扫描案例子集并找出权重值最高的案例。
- 引文："After the index search has been completely successfully, Caspian can be run in two different modes: with or without case matcher. If the case matcher is invoked, the program scans the subset of cases to ﬁnd the one with the highest weight value." (Soibelman et al., 2000, p.5)
- 卡片：`litrev/_probe/full/SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign.md`（可读原文上下文）

### C02 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 一句话主张 ・ p.3

- 论断：本文介绍 KBES 在 preliminary design、analysts 与 detailed design 的应用。
- 引文："In this paper applications of KBES to the preliminary design, analysts, and detailed design" (Sriram et al., 1985, p.3)
- 卡片：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md`（可读原文上下文）

### C03 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 一句话主张 ・ p.1

- 论断：作者提出将剪力墙与梁的耦合潜在位置统一表示为图，并用图神经网络（GNN）驱动剪力墙与梁的协同设计。
- 引文："This study constructed a graph representation of the coupled potential positions for shear walls and beams and proposed a co-design method driven by a graph neural network (GNN)." (Xia et al., 2025, p.1)
- 卡片：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md`（可读原文上下文）

### C04 ・ Rodrigues2017_Clustering_FloorPlans ・ 系统形态 ・ p.2

- 论断：本文在同一设置下把四种形状表示作为平面图设计描述子加以研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)
- 卡片：`litrev/_probe/full/Rodrigues2017_Clustering_FloorPlans.md`（可读原文上下文）

### C05 ・ Maher1987_ExpertSystems_StructuralDesign ・ 系统形态 ・ p.6

- 论断：HI-RISE 在 PSRL 中实现，PSRL 是产生式系统与框架表示语言的组合。
- 引文："HI-RISE is implemented in PSRL [7], a combination of a production system and frame representation language." (Maher, 1987, p.6)
- 卡片：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md`（可读原文上下文）

### C06 ・ SharmaThesis_ContentBasedFloorPlanRetrieval ・ 案例或数据的表示形式 ・ p.50

- 论断：采用图谱嵌入，把前一步生成的房间布局图表示到模式空间中。
- 引文："Graph Spectral Embedding [Luo et al., 2003] approach is adopted to represent the room layout graphs created in the previous stage in a pattern-space." (Sharma, 2018, p.50)
- 卡片：`litrev/_probe/full/SharmaThesis_ContentBasedFloorPlanRetrieval.md`（可读原文上下文）

### C07 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 相似性或检索机制 ・ p.11

- 论断：系统的推理机制采用反向链，对目标树进行深度优先搜索。
- 引文："The inference mechanism uses backward chaining that produces a depth-first search of a goal tree." (Sriram et al., 1985, p.11)
- 卡片：`litrev/_probe/full/SriramMaherFenves1985_KBES_StructuralDesign.md`（可读原文上下文）

### C08 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 明确写出的局限 ・ p.15

- 论断：作者明确指出梁的生成依赖潜在梁的布置，因此仍需探索更好的潜在梁生成方法，例如引入更多工程经验规则与硬编码规则。
- 引文："Although case studies show that the algorithms of co-design have achieved good results, considering that the generation of beams depends on the arrangement of potential beams, it is still necessary to explore better methods for generating potential beams, such as introducing more engineering experience rules and hard-coding rules, to further optimize the generation of potential beams." (Xia et al., 2025, p.15)
- 卡片：`litrev/_probe/full/Xia2025_CoDesign_ShearWallBeam_GNN.md`（可读原文上下文）

### C09 ・ Borner1993_StructuralSimilarity_CBR ・ 问题域 ・ p.1

- 论断：方法本身不限于特定领域；示例取自工业建筑设计领域。
- 引文："Although our approach is more theoretical in nature and not restricted to a speci c domain we will give an example taken from the domain of industrial building design" (Borner, 1993, p.1)
- 卡片：`litrev/_probe/full/Borner1993_StructuralSimilarity_CBR.md`（可读原文上下文）

### C10 ・ Gu2024_ShearWall_Diffusion ・ 问题域 ・ p.2

- 论断：研究面向剪力墙布置方案的生成设计。
- 引文："This study proposes a shear wall layout generation method based on a diffusion process." (Gu et al., 2024, p.2)
- 卡片：`litrev/_probe/full/Gu2024_ShearWall_Diffusion.md`（可读原文上下文）

### C11 ・ MaherGomez1996_CBR_StructuralDesign ・ 系统形态 ・ p.2

- 论断：CaseCAD 使用 Framekit。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)
- 卡片：`litrev/_probe/full/MaherGomez1996_CBR_StructuralDesign.md`（可读原文上下文）

### C12 ・ Maher1987_ExpertSystems_StructuralDesign ・ 明确写出的局限 ・ p.7

- 论断：作者明确指出 HI-RISE 目前局限于矩形周边和简单矩形结构网格的建筑。
- 引文："HI-RISE is currently restricted to buildings with a rectangular perimeter and a simple rectangular structural grid." (Maher, 1987, p.7)
- 卡片：`litrev/_probe/full/Maher1987_ExpertSystems_StructuralDesign.md`（可读原文上下文）

### C13 ・ SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign ・ 评价方式 ・ p.7

- 论断：评价方式是开发原型并以一个假设的波士顿办公楼设计为例，展示原型如何运行及其设计建议，以检验模型的可行性。
- 引文："To test the feasibility of the proposed model, an M-RAM prototype was developed. To see how the prototype works and its design recommendations, consider, for example, the design of a hypothetical ofﬁce building in Boston, Massachusetts." (Soibelman et al., 2000, p.7)
- 卡片：`litrev/_probe/full/SoibelmanPenaMora2000_MRAM_ConceptualStructuralDesign.md`（可读原文上下文）

### C14 ・ Zhao2023_ShearWall_GNN ・ 相似性或检索机制 ・ p.9

- 论断：相似性以 IoUpixel 衡量，比较对象是 GNN 生成结果与真值结果在像素图像上的重合。
- 引文："shear wall design results generated by the GNN model and the ground-truth shear wall design results in pixel images, i.e., IoUpixel, is" (Zhao et al., 2023, p.9)
- 卡片：`litrev/_probe/full/Zhao2023_ShearWall_GNN.md`（可读原文上下文）
