# Napps2021_BIM_VariantRetrieval_CBR

- 抽取范围：全文 p.1–8（正文见 p.1–7；p.1 为封面页，p.8 为参考文献）

## 1. 一句话主张
- 论断：提出一种建立在 IFC 标准之上、用案例推理（CBR）结合模式匹配在建筑设计早期阶段检索合适方案变体的方法。
- 引文："This paper presents a solution for finding suitable variants in the early design phases of buildings, using the case-based reasoning (CBR) approach based on the IFC standard." (Napps, 2021, p.1)

## 2. 问题域
- 论断：早期设计阶段建筑师只能凭个人隐性经验手工比选平面方案，难以获取和复用其他建筑师已有的相似方案经验。
- 引文："A challenge is to be able to access the experience of other architects." (Napps, 2021, p.1)

## 3. 案例或数据的表示形式
- 论断：BIM 模型按 IFC 标准表示为图结构，节点与边承载 IFC 实体、属性以及由此得到的几何信息。
- 引文："In this, the BIM model is represented based on the IFC standard with the different entities, attributes and, consequently, the geometry." (Napps, 2021, p.2)

## 4. 相似性或检索机制
- 论断：采用 Richard Hemming 的广义相似度对任意数量属性值加权并归一化，再以图模式匹配（精确与非精确）从图数据库检索变体。
- 引文："The concept of generalized similarity determines the similarity of two cases for any number of attribute values, which can be weighted and normalized (1)." (Napps, 2021, p.3)

## 5. 系统形态
- 论断：已实现的原型——在 Neo4j 图数据库中用 Cypher 查询按给定偏差检索产品变体（门）。
- 引文："In the given case the user is able to find an optional product variant (door) out of Neo4j based on specific deviations." (Napps, 2021, p.7)

## 6. 评价方式
- 论断：以一个简化算例（办公用途首层）对两个候选变体计算相似度（0.694 与 0.86），据此判定变体二更合适；未做专家评审或与其他方法的量化对比。
- 引文："In this case, it indicates that variant two has a greater similarity to the problem and thus results as the more suitable solution regarding this issue." (Napps, 2021, p.6)

## 7. 明确写出的局限
- 论断：作者承认示例中可用的变体数量相当有限，只够演示对简化问题的检索过程。
- 引文："In the presented example the number of variants is quite limited, but sufficient to show the retrieval process of finding a suitable variant for a simplified given problem." (Napps, 2021, p.7)
