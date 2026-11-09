# Rodrigues2017_Clustering_FloorPlans

- 抽取范围：全文 1–18 页

## 1. 一句话主张
- 论断：作者主张四种描述子的感知分析中，Tangent Distance（TD）能更好地刻画平面图形状且离群更少。
- 引文："The perceptual analysis carried out on the four descriptors shows that Tangent Distance (TD) captures better ﬂoor plan shapes and presents fewer outliers." (Rodrigues et al., 2017, p.13)

## 2. 问题域
- 论断：问题域是建筑平面图——生成式设计方法会产出大量候选平面方案，超出决策者的处理能力。
- 引文："Generative design methods are able to produce a large number of potential solutions of architectural ﬂoor plans, which may be overwhelming for the decision-maker to cope with." (Rodrigues et al., 2017, p.1)

## 3. 案例或数据的表示形式
- 论断：每种描述子都表示成长度相同的数值向量（100 个值），因此表示类型不影响算法性能。
- 引文："As the vector in every clustering process had the same length (100 values), the type of shape representation did not affect the performance of the algorithm." (Rodrigues et al., 2017, p.6)

## 4. 相似性或检索机制
- 论断：聚类使用凝聚层次算法，采用 Ward 连接，并以欧氏距离作为度量。
- 引文："The dataset was clustered using an agglomerative hierarchical algorithm with Ward linkage [33] and the Euclidean distance as" (Rodrigues et al., 2017, p.4)

## 5. 系统形态
- 论断：本文形态是在同一设置下把四种形状表示作为平面图设计描述子进行对比的实验研究。
- 引文："In this paper, four shape representations are studied as ﬂoor plan design descriptors under the same settings." (Rodrigues et al., 2017, p.2)

## 6. 评价方式
- 论断：在 72 个合成平面图构成的数据集上，将聚类结果与参考聚类比较，并以 Rand 指数衡量，Tangent Distance 的 Rand 指数为 0.873。
- 引文："A hierarchical agglomerative clustering algorithm is used to cluster a synthetic dataset of 72 ﬂoor plans. When compared to a reference clustering, despite good perceptual results with the use of the Point Distance and Turning Function representations, the Tangent Distance descriptor (Rand index of 0.873) provides the best results." (Rodrigues et al., 2017, p.1)

## 7. 明确写出的局限
- 论断：作者明确写出 TD 描述子的一个局限：同一形状类型的设计可能因对外墙每次转折处线段尺寸的敏感度而被判为不同。
- 引文："Another issue was found with this descriptor. In some cases, when designs have the same shape type, it may consider distinct due to the sensitivity over the size of the segments in every turn of the exterior wall (see groups F and G in Fig. 9 as an example)." (Rodrigues et al., 2017, p.13)
