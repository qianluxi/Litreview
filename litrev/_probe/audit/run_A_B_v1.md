# 第 1 轮原始输出（标定集 13 条）

## 审计员 A（按原序 01→13）

| id | 支撑 | 自足 | 引文里的依据 | 缺什么/需补的一句 |
|---|---|---|---|---|
| 01 | SUPPORTED | SELF | variant retrieval | 无；引文是"outlines a solution for"，写成"要解决的问题"可接受 |
| 02 | PARTIAL | SELF | is a possibility | 情态升级：引文只说 GPM 是"一种可能"，不能写成"方法就是 GPM" |
| 03 | PARTIAL | SELF | IFC data structure | 术语替换：data structure≠标准；"can be defined"不能写成"定义" |
| 04 | SUPPORTED | SELF | MetisCBR … architectural design | 无 |
| 05 | SUPPORTED | SELF | Semantic Fingerprint | 无 |
| 06 | PARTIAL | SELF | can be seen as | 情态升级："can be seen as"须降级；"we use a container-based structure"≠"agents 组织协作" |
| 07 | SUPPORTED | SELF | Two major considerations | 无 |
| 08 | SUPPORTED | DEPENDENT | it decomposes into | 自足需补主语"design-case recall" |
| 09 | SUPPORTED | SELF | Indexing identifies the features | 无 |
| 10 | PARTIAL | SELF | can be calculated | 混入缺席命题（篇数/条数）无全库证据；"数量有限"见 p.7 而非本条 |
| 11 | PARTIAL | SELF | quite limited | 同上；缺"没有给出篇数/条数"的缺席证据，"两个变体"见 p.5 |
| 12 | PARTIAL | SELF | between zero and one | 混入缺席命题"未报告 accuracy"需全库证据；"差异 0/1 对应"见 p.4 |
| 13 | PARTIAL | SELF | corresponds to … one | 同上；仅支撑"差异为零对应一"，"一到零""零到一"不在本条 |

合计：13 条（SUPPORTED 6 / PARTIAL 7 / UNSUPPORTED 0；DEPENDENT 1）

## 审计员 B（乱序 07→08）

| id | 支撑 | 自足 | 引文里的依据 | 缺什么/需补的一句 |
|---|---|---|---|---|
| 07 | SUPPORTED | SELF | Two major considerations | 无 |
| 03 | PARTIAL | SELF | IFC data structure | data structure 被替换为「IFC 标准」；can be defined 被写成「分别定义」 |
| 12 | PARTIAL | DEPENDENT | between zero and one | 「差异为零对一、差异为一对零」与取值区间不在本页；「未报告准确率」是缺席命题 |
| 05 | SUPPORTED | SELF | user queries built with | 无 |
| 09 | SUPPORTED | SELF | Indexing identifies | 无 |
| 01 | SUPPORTED | SELF | BIM-based variant retrieval | 无 |
| 13 | PARTIAL | SELF | A difference of zero | 「差异为一对应零」与「零到一」不在本页；缺席命题无引文依据 |
| 06 | PARTIAL | DEPENDENT | can be seen as | 「can be seen as」被升级为「是」；「agents 组织协作」引文未直说，其主语为 our approach |
| 02 | PARTIAL | SELF | is a possibility to find | 「a possibility」被升级为「是」；graph database 与 case base 被并成一句 |
| 10 | PARTIAL | DEPENDENT | the problem and two possible variants | 「篇数/样本条数」与「明确承认数量有限」均不在本页；「can be calculated」被写成做比较；缺席命题 |
| 04 | SUPPORTED | SELF | system MetisCBR | 无 |
| 11 | PARTIAL | SELF | the number of variants is quite limited | 「两个备选变体」「篇数/条数」不在本页；「只是」略强；缺席命题 |
| 08 | SUPPORTED | DEPENDENT | it decomposes into the subtasks of | 无（主语 it 需补为 design-case recall） |

合计：13 条（SUPPORTED 6 / PARTIAL 7 / UNSUPPORTED 0；DEPENDENT 4）
