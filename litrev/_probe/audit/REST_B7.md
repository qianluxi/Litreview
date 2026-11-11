# 新文献 Lin2022 审计批次 B7（7 条，闭卷）

> 判定标准：`litrev/_probe/AUDIT_CONTRACT.md`（v1.2，含 §八 自足轴三族边界）。
> 全部条目已通过 `verify`：逐字存在、页码为 PDF 物理页。**不要判真伪与页码**，只判论断层。
> 不要读任何 PDF、`texts/*.txt` 或 `full/*.md`。只依据下面给出的论断与引文判定。
> **本批是中文文献**：引文为中文原文（不是译文），照原句判「论断是否被引文支撑」；
> 术语替换与属性添加同样受硬规则 9 第 ⑤ 类约束（「矢量相似度Similarity」这类中英并写算同一个词，
> 但把「相似度」换成「距离」、「点积」换成「余弦」属于替换，要照判）。
> **自足轴独立判**：只管主语与指代在引文内是否站得住，不判引文内容是否完整回答了节名。
> 快照 sha1: 09829c47c9

输出：只输出表格 + 一行合计，行序与本文件条目顺序一致。

| id | 支撑 | 自足 | 引文里的依据（≤15字，引文原词，连续片段） | 缺什么/需补的一句 |
|----|------|------|----------------------------------------|--------------------|

### R7-01 ・ Lin2022_BERT_DisasterTweet ・ 一句话主张 ・ p.1

- 论断：针对传统文本分类模型的不足，提出了一种基于 BERT 预训练模型的灾害推文分类方法。
- 引文："Given the shortcomings of the traditional text classification model, a disaster tweet classification method was proposed based on the pre-trained model of bidirectional encoder representations from transformers (BERT)." (Lin, 2022, p.1)
- 源文件：第 7 行

### R7-02 ・ Lin2022_BERT_DisasterTweet ・ 问题域 ・ p.1

- 论断：社交媒体已成为发布和传播灾害信息的重要媒介，对其信息的有效识别与利用对灾害应急管理具有重要意义。
- 引文："Social media has become an important medium for the release and dissemination of disaster information, the effective identification and utilization of which is of great significance to disaster emergency management." (Lin, 2022, p.1)
- 源文件：第 11 行

### R7-03 ・ Lin2022_BERT_DisasterTweet ・ 案例或数据的表示形式 ・ p.4

- 论断：文本表示是将文字表示为向量作为模型输入数据的方法，典型方法包括不考虑词序、语法的词袋模型、TF-IDF 以及 Word2vec 等。
- 引文："文本表示是将文字表示为向量作为模型输入数据的方法，典型的文本表示方法包括不考虑词序、语法的词袋模型[18]、词频-逆文档频度(term frequency-inverse document frequency，TF-IDF)[19]以及基于无监督学习的Word2vec (word to vector) 模型[20]等。" (Lin, 2022, p.4)
- 源文件：第 15 行

### R7-04 ・ Lin2022_BERT_DisasterTweet ・ 相似性或检索机制 ・ p.3

- 论断：计算矢量相似度（Similarity）的函数有多种形式，该机制中通常采用向量点积。
- 引文："其中，计算矢量相似度Similarity 的函数有多种形式，该机制中通常采用向量点积。" (Lin, 2022, p.3)
- 源文件：第 19 行

### R7-05 ・ Lin2022_BERT_DisasterTweet ・ 系统形态 ・ p.1

- 论断：本研究经数据清洗与预处理、通过对比分析，在 BERT 基础上构建了基于 LSTM-CNN 的文本分类模型。
- 引文："After data cleaning and preprocessing, this study constructed a text classification model based on long short-term memory-convolutional neural network (LSTM-CNN) through comparative analysis, based on BERT." (Lin, 2022, p.1)
- 源文件：第 23 行

### R7-06 ・ Lin2022_BERT_DisasterTweet ・ 评价方式 ・ p.1

- 论断：在 Kaggle 竞赛平台的推文数据集上的实验表明，所提分类模型优于传统朴素贝叶斯分类模型和常见的微调模型，识别率最高可达 85%。
- 引文："Experiments on the tweet datasets of the Kaggle competition platform showed that the proposed classification model outperforms the traditional Naive Bayesian classification model and the common fine-tuning model, with the recognition rate up to 85%." (Lin, 2022, p.1)
- 源文件：第 27 行

### R7-07 ・ Lin2022_BERT_DisasterTweet ・ 明确写出的局限 ・ p.6

- 论断：作者指出训练所用数据规模较小、数据有限。
- 引文："由于训练所用数据规模较小，数据有限，这也是解决小样本文本分类的一种有效方法。" (Lin, 2022, p.6)
- 源文件：第 31 行
