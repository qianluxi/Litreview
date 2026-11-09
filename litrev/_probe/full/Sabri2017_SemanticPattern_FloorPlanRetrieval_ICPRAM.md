# Sabri2017_SemanticPattern_FloorPlanRetrieval_ICPRAM

- 抽取范围：全文 1–11 页

## 1. 一句话主张
- 论断：作者主张其新颖性在于把 CBR、精确图匹配与不精确图匹配组合在同一个系统中，用于建筑平面图检索。
- 引文："The novelty of our approach is that it combines CBR, exact, and inexact graph matching in one system in the domain of retrieval of architectural ﬂoor plans." (Sabri et al., 2017, p.1)

## 2. 问题域
- 论断：问题域是建筑平面图的概念设计，以及在该阶段检索相似的平面图。
- 引文："Until today, for the conceptual design of architectural ﬂoor plans, architects widely follow the traditional pen and paper based method to draw the conceptual ﬂoor plans, and retrieve the similar ﬂoor plans in the printed reference collections." (Sabri et al., 2017, p.1)

## 3. 案例或数据的表示形式
- 论断：平面图数据用 AGraphML 这种基于 XML 的表示形式来描述。
- 引文："AGraphML is the XML-based representation for ﬂoor plans. The speciﬁcation (Langenhan, 2015) of AGraphML deﬁnes attributes for this representation." (Sabri et al., 2017, p.4)

## 4. 相似性或检索机制
- 论断：系统实现了三种匹配与检索技术：MetisCBR、以 VF2 为代表的精确图匹配、以及以 index-based 指称的不精确图匹配。
- 引文："This section presents the three matching and retrieval techniques implemented in Archistant: MetisCBR, exact graph matching (referred as VF2), and inexact graph matching (referred as index-based)." (Sabri et al., 2017, p.4)

## 5. 系统形态
- 论断：系统形态是一个完整的端到端系统，帮助建筑师在早期设计阶段检索相似的平面图。
- 引文："In this paper we present a complete end-to-end system that helps architects to retrieve similar ﬂoor plans in early design phases." (Sabri et al., 2017, p.1)

## 6. 评价方式
- 论断：评价采用定性分析，请参与者观察三种检索方法在 10 个查询上的结果。
- 引文："For this qualitative analysis we asked different participants to observe the results of each of the three retrieval methods, corresponding to each of the 10 queries." (Sabri et al., 2017, p.7)

## 7. 明确写出的局限
- 论断：作者明确写出，索引法的这些局限来自底层 Neo4j 数据库的内部超时错误。
- 引文："These limitations came from internal timeout errors of the underlying Neo4j database, most likely due to a congestion of the database system." (Sabri et al., 2017, p.7)
