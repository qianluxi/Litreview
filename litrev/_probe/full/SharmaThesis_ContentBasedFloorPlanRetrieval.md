# SharmaThesis_ContentBasedFloorPlanRetrieval

- 抽取范围：摘要 p.21–22；第 3 章 §3.5 Graph Spectral Embedding 与 §3.6 Experiments and Results p.50–57；第 7 章 Conclusions（§7.1–7.3）p.142–145。

## 1. 一句话主张
- 论断：论文提出面向建筑平面图的内容检索方法，从平面图中抽取不同特征以支持检索。
- 引文："In this thesis, techniques to analyse architectural floor plans and extraction of different features to aid in content based retrieval in floor plans is proposed." (Sharma, 2018, p.21)

## 2. 问题域
- 论断：研究问题是建筑设计早期阶段对相似平面图的检索。
- 引文："Efficient retrieval of similar floor plan images is a critical component of early design phase of construction as it is the primary reason of delay in the design/ conceptualization phase." (Sharma, 2018, p.142)

## 3. 案例或数据的表示形式
- 论断：采用图谱嵌入，把前一步生成的房间布局图表示到模式空间中。
- 引文："Graph Spectral Embedding [Luo et al., 2003] approach is adopted to represent the room layout graphs created in the previous stage in a pattern-space." (Sharma, 2018, p.50)

## 4. 相似性或检索机制
- 论断：提出两阶段匹配与检索，即房间布局匹配与房间装饰匹配。
- 引文："A two phase matching and retrieval, Room Layout Matching (RLM) and Room Decor Matching (RDM) is proposed." (Sharma, 2018, p.52)

## 5. 系统形态
- 论断：论文还提出了交互式图形用户界面，帮助用户选择、分析并检索相似平面图。
- 引文："An interactive graphical user interface to aid users to select, analyse and retrieve similar floor plans is also proposed in this thesis." (Sharma, 2018, p.21)

## 6. 评价方式
- 论断：在 ROBIN 数据集上以 Mean Average Precision（MAP）评价；仅考虑房间布局时，检索得到的 MAP 值为 0.247。
- 引文："The Mean Average Precision (MAP) value obtained during retrieval on the ROBIN dataset was observed to be 0.247 in case only room layout was considered while retrieval, on the other hand incorporating both room layout and room decor features made retrieval quite specific." (Sharma, 2018, p.143)

## 7. 明确写出的局限
- 论断：作者指出，拓扑与房间装饰特征虽有助于区分和检索相似平面图，但总体上不足以完整分析一个平面图。
- 引文："We observed that although, topology and room decor features help in distinguishing two floor plans and retrieving similar ones, but inclusively are not a good enough measure to analyse a floor plan completely." (Sharma, 2018, p.143)
