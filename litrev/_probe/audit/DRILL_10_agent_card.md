# Napps2021_BIM_VariantRetrieval_CBR

- 抽取范围：全文 p.1–8（正文见 p.1–7；p.8 为参考文献）

## 1. 一句话主张
- 论断：提出一种基于 IFC 标准、用案例推理在建筑早期设计阶段查找合适变体的方案。
- 引文："This paper presents a solution for finding suitable variants in the early design phases of buildings, using the case-based reasoning (CBR) approach based on the IFC standard." (Napps, 2021, p.1)

## 2. 问题域
- 论断：问题在于难以获取其他建筑师的经验，这类信息目前不可得，且难以从一个项目迁移到下一个项目。
- 引文："A challenge is to be able to access the experience of other architects. Currently, this information is not available and is difficult to transfer from one project to the next." (Napps, 2021, p.1)

## 3. 案例或数据的表示形式
- 论断：数据结构采用图表示，BIM 模型按 IFC 标准以不同实体、属性及相应几何来表达。
- 引文："For the research in this topic, a graph-based representation of the data structure is chosen [10]. In this, the BIM model is represented based on the IFC standard with the different entities, attributes and, consequently, the geometry." (Napps, 2021, p.2)

## 4. 相似性或检索机制
- 论断：采用广义相似度计算两个案例在任意数量属性值上的相似性，属性值可加权并可归一化。
- 引文："The concept of generalized similarity determines the similarity of two cases for any number of attribute values, which can be weighted and normalized (1)." (Napps, 2021, p.3)

## 5. 系统形态
- 论断：形态为基于 Neo4j 图数据库的实现，用户可用给定的 cypher 查询按具体偏差（墙洞的深度、高度、宽度）检索可选的门产品变体。
- 引文："In the given case the user is able to find an optional product variant (door) out of Neo4j based on specific deviations. By using the given cypher query, the database is searched for a door that fits into a given wall opening (depth, height, width)." (Napps, 2021, p.7)

## 6. 评价方式
- 论断：评价按相似度计算结果判断，变体二与问题的相似度更高，因而被视为针对该问题更合适的解。
- 引文："In this case, it indicates that variant two has a greater similarity to the problem and thus results as the more suitable solution regarding this issue." (Napps, 2021, p.6)

## 7. 明确写出的局限
- 论断：作者承认示例中的变体数量相当有限，仅足以演示为简化问题寻找合适变体的检索过程。
- 引文："In the presented example the number of variants is quite limited, but sufficient to show the retrieval process of finding a suitable variant for a simplified given problem." (Napps, 2021, p.7)
