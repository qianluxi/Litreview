# C4 审计批次 B1（16 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（含第五节口径修订）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF 或 `full/*.md`。只依据下面给出的论断与引文判定。
> 快照 sha1: 81c78be532

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词） | 缺什么/需补的一句 |
|----|------|------|--------------------------------|--------------------|

### B1-01 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 一句话主张 ・ p.1

- 论断：作者把本文贡献概括为两方面，其中第一项是提出名为 a.SCatch 的基于草图的系统。
- 引文："The contribution of this article is twofold. First, we propose a sketch-based system, namely the a.SCatch" (Ahmed et al., 2013, p.1)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### B1-02 ・ Ahmed2013_Analysis_SketchRetrieval_FloorPlans ・ 系统形态 ・ p.8

- 论断：系统形态是一个为 Touch & Write 实现的原型。
- 引文："the prototype is implemented for the Touch & Write" (Ahmed et al., 2013, p.8)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-03 ・ Borner1993_StructuralSimilarity_CBR ・ 一句话主张 ・ p.10

- 论断：作者的核心主张是，只有在存在可据以把旧解正确改编到当前问题的知识时，才进行结构相似性评估。
- 引文："Structural similarity is assessed if and only if there is knowledge available to adapt old solutions correctly to the current problem of interest" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 7 行）

### B1-04 ・ Borner1993_StructuralSimilarity_CBR ・ 相似性或检索机制 ・ p.6

- 论断：对新问题的初始分析可以通过基于属性描述的、成本不高的表面相似性评估来完成。
- 引文："The rst initial analysis of the new problem can be done by an inexpensive surface similarity assessment based on the attribute based descriptions" (Borner, 1993, p.6)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### B1-05 ・ Borner1993_StructuralSimilarity_CBR ・ 明确写出的局限 ・ p.10

- 论断：作者明确写出，修改规则条件或权重的学习在本实现中未被处理。
- 引文："Learning e g the storage of new cases new rules and the application of techniques like Knuth Bendix completion to guarantee completeness of struc tural knowledge or learning of modi cation rule conditions or weights are not addressed in this implementation" (Borner, 1993, p.10)
- 形式特征：未以句末标点结尾（源文件第 31 行）

### B1-06 ・ Liao1998_SimilarityMeasures_CBR ・ 问题域 ・ p.2

- 论断：该文以 CBR 案例检索中的相似度度量为主题，并以失效分析为示例应用领域。
- 引文："This article focuses on the similarity measuring methods for CBR and comprises two parts. The rst part reviews the existing methods for measuring similarity in the literature based on more than 100 CBR project studies and some general similarity measures seen in other applications. In the second part, a hybrid similarity measure is proposed for comparing cases with a mixture of crisp and fuzzy features. Its application to the domain of failure analysis is illustrated." (Liao et al., 1998, p.2)
- 形式特征：完整句（源文件第 11 行）

### B1-07 ・ Liao1998_SimilarityMeasures_CBR ・ 系统形态 ・ p.13

- 论断：有一个 CBR 系统正在开发中，用于存储失效分析。
- 引文："than 20 years. A CBR system is being developed to store failure analysis" (Liao et al., 1998, p.13)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-08 ・ MaherGomez1996_CBR_StructuralDesign ・ 问题域 ・ p.1

- 论断：作者从结构设计项目的资料中定位案例来源，资料来自悉尼一家工程咨询公司。
- 引文："We began our CBR projects by locating a source of information on structural design projects-a well-known engineering consulting firmthat has worked on many medium- to high-rise buildings in Sydney." (Maher and Gomez, 1996, p.1)
- 形式特征：完整句（源文件第 11 行）

### B1-09 ・ MaherGomez1996_CBR_StructuralDesign ・ 系统形态 ・ p.2

- 论断：CaseCAD 使用 Framekit。
- 引文："CaseCAD using Framekit, a frame-based" (Maher and Gomez, 1996, p.2)
- 形式特征：未以句末标点结尾（源文件第 23 行）

### B1-10 ・ Rodrigues2017_Clustering_FloorPlans ・ 相似性或检索机制 ・ p.4

- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as" (Rodrigues et al., 2017, p.4)
- 形式特征：未以句末标点结尾（源文件第 19 行）

### B1-11 ・ SriramMaherFenves1985_KBES_StructuralDesign ・ 系统形态 ・ p.7

- 论断：文中举例 HI-RISE 在 PSRL 中实现，PSRL 是框架式产生式系统。
- 引文："buildings (HI-RISE) [18]. HI-RISE is implemented in PSRL [24], a frame based production system" (Sriram et al., 1985, p.7)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 23 行）

### B1-12 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 一句话主张 ・ p.1

- 论断：作者主张该智能案例检索方法能克服学习能力差、检索效率低、智能水平不足等缺陷，并为高层结构 IFO 的案例检索提供更科学的方法。
- 引文："The result shows. this intelligent CRM can overcome such shortcomings as poor learning ability, low searching efficiency and intelligent level, etc., providing comparatively more scientific method for the CRM of high-rise structure IFO." (Zhang, 2006, p.1)
- 形式特征：完整句（源文件第 7 行）

### B1-13 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 相似性或检索机制 ・ p.2

- 论断：相似度度量采用以属性相对欧氏加权距离为基础的方法。
- 引文："To solve this problem and to be able to take into consideration everything important and necessary such as concurrence of quality, quantitative and fuzzy attributes and difference in dimension, this paper established a new similarity measure method based on the relative Euclidean weight distance of attributes (see expression (5))." (Zhang, 2006, p.2)
- 形式特征：完整句（源文件第 19 行）

### B1-14 ・ Zhang2006_BP_CaseRetrieval_HighriseStructureForm ・ 明确写出的局限 ・ p.2

- 论断：作者明确指出网络拓扑结构的确定缺乏成熟、系统的理论。
- 引文："There are only some experimental conclusions concerning ascertainment of topological structure of networks instead of mature and systematic theory." (Zhang, 2006, p.2)
- 形式特征：完整句（源文件第 31 行）

### B1-15 ・ Zhao2023_ShearWall_GNN ・ 相似性或检索机制 ・ p.9

- 论断：相似性以 IoUpixel 衡量，比较对象是 GNN 生成结果与真值结果在像素图像上的重合。
- 引文："shear wall design results generated by the GNN model and the ground-truth shear wall design results in pixel images, i.e., IoUpixel, is" (Zhao et al., 2023, p.9)
- 形式特征：首字母小写+未以句末标点结尾（源文件第 19 行）

### B1-16 ・ Zhao2023_ShearWall_GNN ・ 明确写出的局限 ・ p.11

- 论断：作者指出，由于剪力墙样本有限，过拟合更容易避免。
- 引文："easier to avoid overfitting owing to the limited shear wall samples." (Zhao et al., 2023, p.11)
- 形式特征：首字母小写（源文件第 31 行）
