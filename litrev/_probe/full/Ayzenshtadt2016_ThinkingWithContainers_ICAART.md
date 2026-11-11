# Ayzenshtadt2016_ThinkingWithContainers_ICAART

- 抽取范围：全文 p.1–8（正文见 p.1–8；p.1 为标题与摘要页，p.8 含结论与参考文献）

## 1. 一句话主张
- 论断：本文提出面向建筑设计领域的分布式检索系统 MetisCBR，其中智能体以分组（容器）方式解析由语义描述模型 Semantic Fingerprint 构建的用户查询。
- 引文："In this work we present the distributed retrieval system MetisCBR for the architectural design domain, where agents work in groups (containers) on resolving of user queries built with a semantic description model Semantic Fingerprint." (Ayzenshtadt, 2016, p.1)

## 2. 问题域
- 论断：当前的数字语义建筑模型已无法充分表达现代建筑项目日益增长的复杂性。
- 引文："However, current digital semantic building models are no longer able to adequately represent the increasing complexity of modern architectural projects." (Ayzenshtadt, 2016, p.2)

## 3. 案例或数据的表示形式
- 论断：待检索的案例位于底层基于属性-值的 CBR 域模型的案例库中。
- 引文："CBR retrieval agents execute the last and most important part of the retrieval process – they apply CBR retrieval methods for determination of the most similar cases to the query or its parts in the case base(s) of the underlying attribute-value based CBR domain model (described in detail in (Ayzenshtadt et al., 2015))." (Ayzenshtadt, 2016, p.6)

## 4. 相似性或检索机制
- 论断：平面图检索的相似度计算会把元数据与附加数据的每一个属性都纳入考量。
- 引文："Floor plan agent works with following query types: Floorplan Query – every attribute of the meta data and additional data will be taken into account for the similarity measurement." (Ayzenshtadt, 2016, p.6)

## 5. 系统形态
- 论断：该原型使用 Java 语言框架 JADE（用于实现所描述的智能体系统）与 myCBR 来开发。
- 引文："Java language based frameworks JADE (for the implementation of the described agent system) and myCBR were used to develop the prototype." (Ayzenshtadt, 2016, p.7)

## 6. 评价方式
- 论断：评价过程用一个由 5 个房间和 6 条连接边构成的示例查询来查询系统，并采用带属性加权与不带属性加权两种不同的相似度度量。
- 引文："The evaluation process included the querying of the system with an exemplary query consisting of 5 rooms and 6 connecting edges with two different similarity measures: with and without attribute weighting." (Ayzenshtadt, 2016, p.7)

## 7. 明确写出的局限
- 论断：在这一开发阶段，用于当前查询的相似度度量是手工设定的。
- 引文："The retrieval agent(s) retrieved the case base with the similarity measure that was set for the current query (manually, on this stage of development)." (Ayzenshtadt, 2016, p.7)
