# Roith2017_GraphBasedDesign_FederatedDB_VisEng

- 抽取范围：全文 p.1–17

## 1. 一句话主张
- 论断：作者描述了一个名为 Coordinator 的中间件的设计与实现，该中间件支持基于图的平面图检索。
- 引文："We have described the design and implementation of the Coordinator, a middleware to support graph-based floorplan retrieval." (Roith et al., 2017, p.16)

## 2. 问题域
- 论断：面向建筑设计过程，系统让用户以在手绘或多点触控设备上绘制的建筑草图检索相似的建筑模型。
- 引文："This paper describes an information retrieval system that allows users to search for building models that are similar to a hand-drawn sketch of a building or parts of a building on a multi-touch device to support the design process of architects." (Roith et al., 2017, p.2)

## 3. 案例或数据的表示形式
- 论断：建筑平面图指纹被形式化为图，并用一种公共 schema（AGraphML）编码，以表示空间构型。
- 引文："Our federated database system is queried using semantic building floorplan fingerprints, which are formalized as graphs and encoded in a common schema, like our AGraphML, to represent spatial configurations and perform graph matching." (Roith et al., 2017, p.1)

## 4. 相似性或检索机制
- 论断：作者目前定义了 12 个指纹，用于检查节点属性、边属性或完全图同构。
- 引文："We have currently defined 12 fingerprints that check, for example, properties of nodes, edges or full graph isomorphism (Weber et al. 2011)." (Roith et al., 2017, p.7)

## 5. 系统形态
- 论断：作者实现了原型，使用户能把可视化构造的查询发送到 Coordinator 中间件，以交互式检索相似建筑平面图的描述。
- 引文："Our prototypes enable users to interactively retrieve descriptions of similar building floorplans by sending queries which are constructed visually to a Coordinator middleware." (Roith et al., 2017, p.5)

## 6. 评价方式
- 论断：评价中请七位建筑师从自身角度指明若干属性对基于手绘图纸检索的重要性。
- 引文："Seven architects were asked to specific the importance of certain properties for searching based on freehand drawings from their point of view." (Roith et al., 2017, p.15)

## 7. 明确写出的局限
- 论断：作者明确写出过滤器式 agent 的一项局限：输入集需要通过网络复制到 agent。
- 引文："Another limitation of filters is that the input set needs to be copied over the network into the agent." (Roith et al., 2017, p.12)
