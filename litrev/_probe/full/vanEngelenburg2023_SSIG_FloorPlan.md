# vanEngelenburg2023_SSIG_FloorPlan

- 抽取范围：全文 1–10 页

## 1. 一句话主张
- 论断：作者把 IoU 与 GED 合并成一个名为 SSIG 的度量，以此作为克服既有度量不足的方案。
- 引文："We overcome the shortcomings by combining IoU and GED into one metric, called SSIG." (van Engelenburg et al., 2023, p.8)

## 2. 问题域
- 论断：论文面向建筑设计中的平面图，认为建筑的构图结构是建筑品质的关键因素。
- 引文："The compositional structure of a building is a key factor in the architectural quality." (van Engelenburg et al., 2023, p.1)

## 3. 案例或数据的表示形式
- 论断：文献把平面图表示为显式建模形状、比例与位置的几何体，以及建模细分区域之间关系的图。
- 引文："Floor plans are digitally represented in various ways that each emphasize different components of interest e.g. as images allowing to model ﬁne-grained details such as materialization and furniture [21, 5], geometries that explicitly model the shapes, proportions and locations of the shapes of the subdivisions [13], and graphs that model the relations between the subdivisions [9, 13, 18, 12]." (van Engelenburg et al., 2023, p.2)

## 4. 相似性或检索机制
- 论断：SSIG 被表述为基于 IoU 的相似度与基于 nGED 的相似度之间的加权平均。
- 引文："Coined as SSIG (Structural Similarity by IoU and GED), 7 essentially computes a weighted average between a IoU-based and a nGED-based similarity metric." (van Engelenburg et al., 2023, p.5)

## 5. 系统形态
- 论断：产出形态是一个用 SSIG 对大规模平面图库排序的高效算法，作者称代码将公开。
- 引文："In addition, an efﬁcient algorithm is developed that uses SSIG to rank a large-scale ﬂoor plan database." (van Engelenburg et al., 2023, p.1)

## 6. 评价方式
- 论断：评价使用 RPLAN 这一大规模平面图数据集，其含逾 80k 套带语义分割区域的亚洲单户公寓。
- 引文："RPLAN is a large-scale dataset containing ﬂoor plan images with semantically segmented areas, consisting of >80k single-unit apartments across Asia." (van Engelenburg et al., 2023, p.5)

## 7. 明确写出的局限
- 论断：作者明确写出本文只考察 IoU 与 GED，未考虑其他常见的图像与图相似度度量。
- 引文："This work is however limited to investigating IoU and GED and does not consider other well-known image- and graph-based similarity metrics." (van Engelenburg et al., 2023, p.8)
