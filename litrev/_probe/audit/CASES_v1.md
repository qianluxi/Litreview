# 标定集 v1（13 条，闭卷）

来源：`_probe/notes/` 下 4 份已产出笔记，全部已通过 `litrev.py verify`（引文真实、页码正确）。因此本集**不含引文真伪问题**，只含论断层问题。

| id | 出处 | 页 | 论断 | 引文 |
|---|---|---|---|---|
| 01 | Napps 2021 | p.1 | 论文要解决的问题是在建筑早期设计阶段对建筑设计的变体进行基于 BIM 的检索 | This paper outlines a solution for a BIM-based variant retrieval of a building design in early design phases using Case Based Reasoning (CBR) and Pattern Matching (PM). |
| 02 | Napps 2021 | p.3 | 做匹配与检索的方法是图模式匹配，即从图数据库中按模式查询由案例库选出匹配图 | The method of graph pattern matching (GPM) is a possibility to find (suitable) variants from a graph database. Based on a pattern query, matching graphs are selected from a case base that provide an answer to the existing request (problem). |
| 03 | Napps 2021 | p.3 | 相似度计算落在 IFC 数据结构上，即基于 IFC 标准实现，对 IFC 的 quantity 与 property definition 分别定义相似度度量 | According to this approach, the similarities are used for all entities stored in the IFC data structure. Depending on the type of entities, similarity measures can be defined for both IFC quantities and property definitions. |
| 04 | Ayzenshtadt 2016 | p.1 | 系统名称为 MetisCBR，面向建筑设计（architectural design）领域 | In this work we present the distributed retrieval system MetisCBR for the architectural design domain |
| 05 | Ayzenshtadt 2016 | p.1 | 用户的查询建立在 Semantic Fingerprint 这一语义描述模型之上 | user queries built with a semantic description model Semantic Fingerprint |
| 06 | Ayzenshtadt 2016 | p.5 | agents 以容器化结构组织协作，每个检索容器是嵌套在父级多智能体系统内部的自主子系统 | For the actual building design retrieval step of our approach, we use a container-based structure, where each retrieval container during its activity can be seen as a completely autonomous multi-agent sub-system that is nested inside a parent MAS |
| 07 | Maher & Gomez 1997 | p.2 | 把 CBR 用于设计有两个主要考虑——设计案例的表示，以及用于召回和改编设计案例的过程模型 | Two major considerations in a CBR approach to design are • representations of design cases and • process models for recalling and adapt- ing design cases. |
| 08 | Maher & Gomez 1997 | p.2 | 设计案例召回（design-case recall）被分解为索引、检索、选择三个子任务 | it decomposes into the subtasks of indexing, retrieval, and selec- tion (see Figure 2a). |
| 09 | Maher & Gomez 1997 | p.2 | 索引这一步做的是：确定以往的设计应具备哪些特征，才能与新的设计问题相关 | Indexing identifies the features a previous design should have to be relevant to the new design problem. |
| 10 | Napps 2021 | p.5 | 该文没有给出案例库的文献篇数或样本条数，检索实验只是一个简化案例：以一个问题对两个备选变体做相似度比较，作者并明确承认案例库中的变体数量相当有限 | After these steps, the similarity measure between the problem and two possible variants can be calculated. |
| 11 | Napps 2021 | p.7 | 该文没有给出案例库的文献篇数或样本条数，检索实验只是一个简化案例：以一个问题对两个备选变体做相似度比较，作者并明确承认案例库中的变体数量相当有限 | In the presented example the number of variants is quite limited, but sufficient to show the retrieval process of finding a suitable variant for a simplified given problem. |
| 12 | Napps 2021 | p.3 | 该文没有报告 accuracy、precision、recall 一类检索准确率，只定义了相似度的归一化区间：差异为零对应相似度一，差异为一对应相似度零，相似度取值落在零到一之间 | Using this formula, the similarity between a problem p and a possible variant v, with non-negative weights, is a value between zero and one. |
| 13 | Napps 2021 | p.4 | 该文没有报告 accuracy、precision、recall 一类检索准确率，只定义了相似度的归一化区间：差异为零对应相似度一，差异为一对应相似度零，相似度取值落在零到一之间 | A difference of zero corresponds to the similarity measure one, that means, that the attributes are equal to each other. |

注：10–13 的论断与引文来自反向测试笔记——命题问的是"实验数据集规模/检索准确率"，笔记回答的是"该文没有给出"。它们在 `verify` 里是 4/4 PASS。
