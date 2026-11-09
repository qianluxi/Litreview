# 变异集 v1（8 条：5 条注入变异 + 3 条原样对照）

用途：测审计员的**灵敏度**，而不是只测它会不会一律放行。变异条目的引文一律取自真实原文（已 PASS），只改论断。顺序已打散，审计员不会被告知哪条是变异。

| id | 出处 | 页 | 论断 | 引文 |
|---|---|---|---|---|
| R1 | Napps 2021 | p.7 | 作者指出该案例库中的变体数量充足，足以支撑规模化的检索实验 | In the presented example the number of variants is quite limited, but sufficient to show the retrieval process of finding a suitable variant for a simplified given problem. |
| R2 | Maher & Gomez 1997 | p.2 | 设计案例召回（design-case recall）被分解为索引、检索、选择三个子任务 | it decomposes into the subtasks of indexing, retrieval, and selec- tion (see Figure 2a). |
| R3 | Ayzenshtadt 2016 | p.5 | 多智能体检索系统普遍采用容器化结构，每个检索容器都是独立自治的子系统 | For the actual building design retrieval step of our approach, we use a container-based structure, where each retrieval container during its activity can be seen as a completely autonomous multi-agent sub-system that is nested inside a parent MAS |
| R4 | Ayzenshtadt 2016 | p.1 | 系统名称为 MetisCBR，面向建筑设计（architectural design）领域 | In this work we present the distributed retrieval system MetisCBR for the architectural design domain |
| R5 | Maher & Gomez 1997 | p.2 | 索引是设计案例召回中唯一决定相关性的环节 | Indexing identifies the features a previous design should have to be relevant to the new design problem. |
| R6 | Napps 2021 | p.3 | 相似度计算落在 IFC 数据结构上，即基于 IFC 标准实现，对 IFC 的 quantity 与 property definition 分别定义相似度度量 | According to this approach, the similarities are used for all entities stored in the IFC data structure. Depending on the type of entities, similarity measures can be defined for both IFC quantities and property definitions. |
| R7 | Ayzenshtadt 2016 | p.1 | 用户的查询建立在 BIM 标准这一语义描述模型之上 | user queries built with a semantic description model Semantic Fingerprint |
| R8 | Napps 2021 | p.4 | 该文在全部实验中均未出现相似度计算失败的情形 | A difference of zero corresponds to the similarity measure one, that means, that the attributes are equal to each other. |
