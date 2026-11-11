# 生产批次 P2（R10）：英文围填海 / 海岸工程 5 篇审计（30 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（v1.2，含 §八 自足轴三族边界）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF、`texts/*.txt` 或 `full/*.md`。只依据下面给出的论断与引文判定。
> **本批全部是英文文献**（围填海 / 海岸工程 / 土性预测领域，与本项目既有 CBR/户型/剪力墙语料无关）。
> 论断为引文的中译，判定时**对照英文原句**，中译不影响支撑判断。
> **自足轴独立判**：只管主语与指代在引文内是否站得住，不判引文内容是否完整回答了节名。
> **「缺什么/需补的一句」一列的填法**：非 `SUPPORTED` **或** 自足=`DEPENDENT` 时都要填；
> 缺什么就写缺的那个成分（如「缺量化结果」「缺主语指代对象」）；两处都缺用分号隔开；两处都不缺才写「—」。
> 本批 5 篇中有 5 个节原文确实没写（Zhu 2 处、Qu 1 处、Lu 2 处），已按规程留空，不在表内。
> 快照 sha1: b2176b0a31

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词，连续片段） | 缺什么/需补的一句 |
|----|------|------|----------------------------------------|--------------------|

### R10-01 ・ Park2025_InSAR_Subsidence_Reclamation ・ 一句话主张 ・ p.4

- 论断：靠近 NDWI 与 BSI 变化峰值的区域表现出更高的沉降速率，且土壤供给与建筑施工之间的间隔越短，沉降持续的时间越长。
- 引文："The findings reveal that areas closer to peak NDWI and BSI changes exhibit higher subsidence rates, with shorter intervals between soil supply and building construction leading to prolonged subsidence." (Park, 2025, p.4)
- 源文件：第 7 行

### R10-02 ・ Park2025_InSAR_Subsidence_Reclamation ・ 问题域 ・ p.1

- 论断：持续监测对于确保建在填海区上的基础设施以及填海土地自身的稳定性是必要的。
- 引文："Continuous monitoring is therefore essential to ensure the stability of infrastructures built on reclaimed areas, as well as the stability of the reclaimed land itself." (Park, 2025, p.1)
- 源文件：第 11 行

### R10-03 ・ Park2025_InSAR_Subsidence_Reclamation ・ 案例或数据的表示形式 ・ p.1

- 论断：数据以 PS 点的平均速度与加速度值表示，这些值由 Sentinel-1 SAR 影像（2021–2023）导出，并沿西海岸映射到 20 个分段区块上。
- 引文："Mean velocity and acceleration values of Persistent Scatterer (PS) points were derived from Sentinel-1 Synthetic Aperture Radar (SAR) images (2021–2023) and mapped across 20 segmented patches along the west coast." (Park, 2025, p.1)
- 源文件：第 15 行

### R10-04 ・ Park2025_InSAR_Subsidence_Reclamation ・ 相似性或检索机制 ・ p.1

- 论断：位置相近且表现出相似沉降模式的 PS 点被归为一组，并为每组选出一个代表性 PS 点。
- 引文："PS points located in close proximity and exhibiting similar subsidence patterns were grouped, and a representative PS was selected for each group." (Park, 2025, p.1)
- 源文件：第 19 行

### R10-05 ・ Park2025_InSAR_Subsidence_Reclamation ・ 系统形态 ・ p.2

- 论断：为保证获得足够的 PS 点，地面位移采用 StaMPS 方法并配合 SBAS 型干涉像对配置计算。
- 引文："To guarantee sufficient PS points, ground displacement was calculated using the Stanford Method for Persistent Scatterers (StaMPS) technique with an small baseline subset(SBAS)-type interferogram pair configuration [1][9]." (Park, 2025, p.2)
- 源文件：第 23 行

### R10-06 ・ Park2025_InSAR_Subsidence_Reclamation ・ 评价方式 ・ p.2

- 论断：西海岸沿线 GNSS 站的垂直位移数据验证了各区块的位移估计。
- 引文："Vertical displacement data from GNSS stations along the west coast validated the displacement estimates across the patches." (Park, 2025, p.2)
- 源文件：第 27 行

### R10-07 ・ Park2025_InSAR_Subsidence_Reclamation ・ 明确写出的局限 ・ p.2

- 论断：2021 年后降轨方向的 Sentinel-1B 卫星失效，此后仅使用升轨的 Sentinel-1A 卫星影像估计视线向（LOS）位移。
- 引文："Following the failure of the Sentinel-1B satellite in the descending orbit after 2021, only Sentinel-1A satellite images in the ascending orbit were used to estimate Line-of-Sight (LOS) displacement." (Park, 2025, p.2)
- 源文件：第 31 行

### R10-08 ・ Elgaali2024_ANN_SoilProperties ・ 一句话主张 ・ p.1

- 论断：该研究设计并开发一个基于人工智能的工具（神经网络），用土体的物理性质（输入）模拟其工程性质（输出）。
- 引文："This project involves design and development of an artificial intelligence-based tool (Neural Network) to simulate soil’s engineering properties (output) from physical properties (input)." (Elgaali, 2024, p.1)
- 源文件：第 7 行

### R10-09 ・ Elgaali2024_ANN_SoilProperties ・ 问题域 ・ p.1

- 论断：确定土体的工程性质需要在现场和实验室进行繁重的工作。
- 引文："Determining engineering properties needs laborious work in the field and in the lab." (Elgaali, 2024, p.1)
- 源文件：第 11 行

### R10-10 ・ Elgaali2024_ANN_SoilProperties ・ 案例或数据的表示形式 ・ p.2

- 论断：每个数据点都测定了含水率（物理性质）与抗压强度（工程性质）两项。
- 引文："For each data point the moisture content (physical property) and the compressive strength (engineering property) were determined." (Elgaali, 2024, p.2)
- 源文件：第 15 行

### R10-11 ・ Elgaali2024_ANN_SoilProperties ・ 相似性或检索机制 ・ p.3

- 论断：输入到输出之间的映射由网络内部的逐层计算完成，每个隐层节点对输入做加权求和，经传递函数后传至下一层，直至输出层。
- 引文："Within each hidden layer node, a weighted sum of the inputs is computed, passed through the transfer function, and forwarded to the subsequent layer until reaching the output layer." (Elgaali, 2024, p.3)
- 源文件：第 19 行

### R10-12 ・ Elgaali2024_ANN_SoilProperties ・ 系统形态 ・ p.2

- 论断：该研究使用前馈神经网络，用土体抗压强度作目标、含水率作输入来建立二者的关系。
- 引文："This study utilizes a feedforward neural network, as depicted in Fig. 1, to establish the correlation between the soil’s compressive strength (target) and the soil’s moisture content (input)." (Elgaali, 2024, p.2)
- 源文件：第 23 行

### R10-13 ・ Elgaali2024_ANN_SoilProperties ・ 评价方式 ・ p.3

- 论断：该文用相关系数（R）评估模拟与实测抗压强度之间的线性相关程度，并指出其理想值为 1.0。
- 引文："The correlation coefficient (R) assesses the linear correlation between the simulated and measured compressive strength, ideally reaching a value of 1.0." (Elgaali, 2024, p.3)
- 源文件：第 27 行

### R10-14 ・ Elgaali2024_ANN_SoilProperties ・ 明确写出的局限 ・ p.3

- 论断：作者指出模型在验证阶段倾向于出现更小的 R 和更大的 RMSE 值。
- 引文："As expected, the model tends to have smaller R and larger RMSE values during validation." (Elgaali, 2024, p.3)
- 源文件：第 31 行

### R10-15 ・ Zhu2022_Hydrodynamics_Zhoushan_Reclamation ・ 一句话主张 ・ p.1

- 论断：围垦工程之后水下地形发生改变、水深变浅，流速与环流强度随之减小。
- 引文："After the reclamation project, the underwater topography was changed, and the water depth became shallower, which reduced the flow velocity and the circulation intensity." (Zhu, 2022, p.1)
- 源文件：第 7 行

### R10-16 ・ Zhu2022_Hydrodynamics_Zhoushan_Reclamation ・ 问题域 ・ p.1

- 论断：需要研究舟山群岛海域的环流特征与机制，以便为群岛的生态环境保护与海岸带管理提供科学依据。
- 引文："Therefore, it is necessary to study the ocean circulation characteristics and mechanism in Zhoushan Islands, so as to provide a scientific basis for the ecological environment protection and coastal zone management of the archipelago." (Zhu, 2022, p.1)
- 源文件：第 11 行

### R10-17 ・ Zhu2022_Hydrodynamics_Zhoushan_Reclamation ・ 案例或数据的表示形式 ・ p.2

- 论断：舟山群岛的复杂岸线以非结构三角网格配合水平面内的垂向 sigma 坐标来贴合。
- 引文："The unstructured triangular grid with a vertical sigma coordinate in the horizontal plane is used to fit the complex coastlines in Zhoushan Islands." (Zhu, 2022, p.2)
- 源文件：第 15 行

### R10-18 ・ Zhu2022_Hydrodynamics_Zhoushan_Reclamation ・ 系统形态 ・ p.2

- 论断：用非结构网格三维数值模型 FVCOM 复现舟山群岛的近岸环流。
- 引文："An unstructured-grid three-dimensional numerical model (FVCOM; Chen et al., 2003) was used to reproduce the coastal circulation in Zhoushan Islands." (Zhu, 2022, p.2)
- 源文件：第 22 行

### R10-19 ・ Zhu2022_Hydrodynamics_Zhoushan_Reclamation ・ 评价方式 ・ p.2

- 论断：根据验证结果，模型能较好地反映研究区的水动力特征，并为后续研究提供基础。
- 引文："According to the verification results, the model can well reflect the hydrodynamic characteristics of the study area and provide a foundation for subsequent research." (Zhu, 2022, p.2)
- 源文件：第 26 行

### R10-20 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 一句话主张 ・ p.1

- 论断：本文用不同时期的高分辨率影像快速提取堤线与平均高潮线，以此分析围垦对海岸地形的影响。
- 引文："The paper adopts higher resolution images in different periods to quickly extract border dike line and average high-tide line, which is used to analyse that reclamation influences on the coastal topography." (Qu, 2011, p.1)
- 源文件：第 7 行

### R10-21 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 问题域 ・ p.1

- 论断：沿海大规模围垦是导致淤泥质潮滩冲淤变化的重要原因。
- 引文："The large scale reclamation in coastal area is the important reason to cause scouring-silting change of muddy tidal flat." (Qu, 2011, p.1)
- 源文件：第 11 行

### R10-22 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 案例或数据的表示形式 ・ p.2

- 论断：研究选用了三景 Landsat TM/ETM 遥感影像。
- 引文："According to the research task requires, we chose Landsat TM/ETM three scene remote sensing image (see Table 1)." (Qu, 2011, p.2)
- 源文件：第 15 行

### R10-23 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 系统形态 ・ p.3

- 论断：上述工作是在 ARCGIS/ARCmap 软件中完成的。
- 引文："Above work is completed with ARCGIS/ARCmap software." (Qu, 2011, p.3)
- 源文件：第 22 行

### R10-24 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 评价方式 ・ p.4

- 论断：作者称结果显示该方法可行、效果良好。
- 引文："The results show that the method is feasible and has good effect." (Qu, 2011, p.4)
- 源文件：第 26 行

### R10-25 ・ Qu2011_CoastalTopography_SheyangEstuary ・ 明确写出的局限 ・ p.2

- 论断：作者指出缺少 Sheyang 河口附近海域的滩位信息，且潮滩坡度难以获取。
- 引文："However, we lack the beach position information of the sea area near the Sheyang estuary and it is difficult to get the slope of the tidal flat." (Qu, 2011, p.2)
- 源文件：第 30 行

### R10-26 ・ Lu2023_Settlement_Prediction_Reclamation ・ 一句话主张 ・ p.1

- 论断：三点法的预测结果持续高于实际观测结果，差值通常落在 30 mm 范围内。
- 引文："Research findings indicate that the predicted results are consistently higher than the actual observed results, with differences typically falling within the range of 30 mm." (Lu, 2023, p.1)
- 源文件：第 7 行

### R10-27 ・ Lu2023_Settlement_Prediction_Reclamation ・ 问题域 ・ p.1

- 论断：为使围垦区内回填料的回填高程与平整度得到有效控制，需要对回填料的沉降观测结果进行准确的预测分析。
- 引文："In order to effectively control the fill elevation and smoothness within the reclaimed area, accurate predictive analysis of the settlement observation results of the fill material is required." (Lu, 2023, p.1)
- 源文件：第 11 行

### R10-28 ・ Lu2023_Settlement_Prediction_Reclamation ・ 案例或数据的表示形式 ・ p.2

- 论断：数据表示为回填土在围垦区的沉降—时间曲线，该曲线由多次观测记录获得。
- 引文："Through multiple observation records, the settlement-time curve of the fill soil in the reclamation area was obtained." (Lu, 2023, p.2)
- 源文件：第 15 行

### R10-29 ・ Lu2023_Settlement_Prediction_Reclamation ・ 系统形态 ・ p.3

- 论断：本研究对回填土的实测沉降数据进行分析，并使用三点法对沉降曲线进行预测。
- 引文："The present study conducted an analysis of the measured settlement data of the fill soil and effectively predicted the settlement curve using the three-point method." (Lu, 2023, p.3)
- 源文件：第 22 行

### R10-30 ・ Lu2023_Settlement_Prediction_Reclamation ・ 评价方式 ・ p.2

- 论断：依据表 1，在既有沉降数据基础上，Hoshino 法预测的沉降值小于观测值，而三点法、Asaoka 法与双曲线法的预测值更大，呈保守趋势。
- 引文："According to Table 1, it could be observed that based on the existing settlement data, the settlement values predicted by the Hoshino method are smaller than the observed values, while the settlement values predicted by the three-point method, Asaoka method, and hyperbolic method were larger than the calculated values, indicating a conservative trend." (Lu, 2023, p.2)
- 源文件：第 26 行

