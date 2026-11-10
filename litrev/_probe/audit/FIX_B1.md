# C4 改稿后定点重判（8 条，闭卷，第二次）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（v1.2，含 §八 自足轴三族边界）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。
> 这 8 条的论断已按复核建议收窄，逐字读，不要凭印象套上一轮的结论。
> **依据列必须是从引文中逐字连续截取的一段（≤15 字），不得拼接、缩写、改写**；
> 例如引文写 `the AIStructure application programming interface (API)`，就只能填 `AIStructure` 或
> `application programming interface`，不能填 `AIStructure API`。
> 快照 sha1: 3961e704f7

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词，连续片段） | 缺什么/需补的一句 |
|----|------|------|----------------------------------------|--------------------|

### R1-01 ・ AamodtPlaza1994_CBR_Foundations ・ 一句话主张 ・ p.1

- 论断：本文提出一个通用的描述框架，后续的描述与讨论都参照该框架。
- 引文："Initially, a general framework is defined, to which the subsequent descriptions and discussions will refer." (Aamodt and Plaza, 1994, p.1)
- 源文件：第 7 行

### R1-02 ・ AamodtPlaza1994_CBR_Foundations ・ 评价方式 ・ p.17

- 论断：1990 年 12 月至 1991 年 9 月间处理了 20,000 个 non-conformance。
- 引文："In the period December 90 - September 91 20.000 non-conformances were handled." (Aamodt and Plaza, 1994, p.17)
- 源文件：第 27 行

### R1-14 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 系统形态 ・ p.13

- 论断：系统形态为设计—分析流程的实现：研究中调用 AIStructure 接口快速布置楼板并施加荷载，再用 PKPM API 完成自动建模与力学分析。
- 引文："This study utilized the AIStructure application programming interface (API) [30] to realize the rapid arrangement of floor slabs and application of loads to the beams and slabs. Subsequently, the PKPM API software development tool was employed to achieve automated structural modeling and mechanical analysis." (Xia et al., 2025, p.13)
- 源文件：第 23 行

### R1-16 ・ vanEngelenburg2023_SSIG_FloorPlan ・ 问题域 ・ p.1

- 论断：平面图是建筑设计中用于交流与思考的最负盛名的媒介之一。
- 引文："Floor plans, as one of the most celebrated media for communicating and thinking in architectural design, are horizontal orthographic projections of a particular building’s ﬂoor." (van Engelenburg et al., 2023, p.1)
- 源文件：第 11 行

### R2-01 ・ AamodtPlaza1994_CBR_Foundations ・ 问题域 ・ p.7

- 论断：作者指出，并不存在适用于每一个应用领域的通用案例推理方法。
- 引文："As for AI in general, there are no universal CBR methods suitable for every domain of application." (Aamodt and Plaza, 1994, p.7)
- 源文件：第 11 行

### R2-06 ・ Rodrigues2017_Clustering_FloorPlans ・ 案例或数据的表示形式 ・ p.6

- 论断：各聚类过程使用的向量长度相同（100 个值），因此形状表示类型不影响算法性能。
- 引文："As the vector in every clustering process had the same length (100 values), the type of shape representation did not affect the performance of the algorithm." (Rodrigues et al., 2017, p.6)
- 源文件：第 15 行

### R2-15 ・ Xia2025_CoDesign_ShearWallBeam_GNN ・ 评价方式 ・ p.13

- 论断：评价采用交并比（SIoU、BIoU）对比协同设计与顺序设计方法：协同设计方法 SIoU 0.625、BIoU 0.548，顺序设计方法 0.544、0.404。
- 引文："The SIoU and BIoU obtained using the proposed co-design method were 0.625 and 0.548, respectively, whereas those obtained using the successive design method were 0.544 and 0.404, respectively." (Xia et al., 2025, p.13)
- 源文件：第 27 行

### R4-03 ・ Maher1987_ExpertSystems_StructuralDesign ・ 一句话主张 ・ p.3

- 论断：论文第二部分介绍卡内基梅隆大学开发的四个专家系统，用以探索并界定初步设计阶段所做的决策。
- 引文："The second part presents four expert systems, developed at Carnegie Mellon University, that explore and define the decisions made during preliminary design." (Maher, 1987, p.3)
- 源文件：第 7 行
