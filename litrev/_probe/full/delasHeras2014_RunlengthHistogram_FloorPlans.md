# delasHeras2014_RunlengthHistogram_FloorPlans

- 抽取范围：全文 1–12 页（PDF 物理页）

## 1. 一句话主张
- 论断：作者主张本文提出了一个用于描述建筑平面图绘图风格的感知模型。
- 引文："In this paper we have proposed a perceptual model to describe the drawing style in architectural plans." (de las Heras et al., 2014, p.10)

## 2. 问题域
- 论断：问题域是建筑平面图这类线绘图在检索场景下的图形识别与视觉美学。
- 引文："This paper is an early attempt to introduce visual aesthetics in graphics recognition, in particular in line drawings of architectural plans in a retrieval scenario." (de las Heras et al., 2014, p.2)

## 3. 案例或数据的表示形式
- 论断：图像表示是对前景层与背景层分别在水平、垂直和两条对角线方向统计 runlength 得到的直方图。
- 引文："A histogram of runs is calculated in the horizontal, vertical and both diagonals for both, foreground and background layers." (de las Heras et al., 2014, p.4)

## 4. 相似性或检索机制
- 论断：两幅平面图签名之间的相似度用 χ2 距离计算。
- 引文："Let P and Q be the signatures of two diﬀerent ﬂoor plan images. Their similarity is calculated by means of the χ2 distance:" (de las Heras et al., 2014, p.5)

## 5. 系统形态
- 论断：系统形态是查询示例（query by example）式的检索框架。
- 引文："The retrieval model proposed is a query by example framework." (de las Heras et al., 2014, p.3)

## 6. 评价方式
- 论断：评价时将系统结果与三套 ground truth 模型对比并报告平均精度均值，对照 gtA、gtB、gtAB 的 mAP 分别为 0.67、0.63 和 0.66。
- 引文："In retrieval terms, the mean average precision (mAP) obtained also varies depending on the ground truth model. Thus, the mAP scores are 0.67 when compared to gtA, 0.63 to gtB, and 0.66 to gtAB." (de las Heras et al., 2014, p.8)

## 7. 明确写出的局限
- 论断：作者写出已与建筑师有过一些交流，但仍应由专家开展严格验证。
- 引文："Although some exchanges have been done with architects, a rigorous validation should be carried on with experts." (de las Heras et al., 2014, p.12)
