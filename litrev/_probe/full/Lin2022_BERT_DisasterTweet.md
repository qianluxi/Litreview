# Lin2022_BERT_DisasterTweet

- 抽取范围：全文 p.1–7（正文见 p.1–7；p.7 后半为参考文献）

## 1. 一句话主张
- 论断：针对传统文本分类模型的不足，提出了一种基于 BERT 预训练模型的灾害推文分类方法。
- 引文："Given the shortcomings of the traditional text classification model, a disaster tweet classification method was proposed based on the pre-trained model of bidirectional encoder representations from transformers (BERT)." (Lin, 2022, p.1)

## 2. 问题域
- 论断：社交媒体已成为发布和传播灾害信息的重要媒介，对其信息的有效识别与利用对灾害应急管理具有重要意义。
- 引文："Social media has become an important medium for the release and dissemination of disaster information, the effective identification and utilization of which is of great significance to disaster emergency management." (Lin, 2022, p.1)

## 3. 案例或数据的表示形式
- 论断：文本表示是将文字表示为向量作为模型输入数据的方法，典型方法包括不考虑词序、语法的词袋模型、TF-IDF 以及 Word2vec 等。
- 引文："文本表示是将文字表示为向量作为模型输入数据的方法，典型的文本表示方法包括不考虑词序、语法的词袋模型[18]、词频-逆文档频度(term frequency-inverse document frequency，TF-IDF)[19]以及基于无监督学习的Word2vec (word to vector) 模型[20]等。" (Lin, 2022, p.4)

## 4. 相似性或检索机制
- 论断：计算矢量相似度（Similarity）的函数有多种形式，该机制中通常采用向量点积。
- 引文："其中，计算矢量相似度Similarity 的函数有多种形式，该机制中通常采用向量点积。" (Lin, 2022, p.3)

## 5. 系统形态
- 论断：本研究经数据清洗与预处理、通过对比分析，在 BERT 基础上构建了基于 LSTM-CNN 的文本分类模型。
- 引文："After data cleaning and preprocessing, this study constructed a text classification model based on long short-term memory-convolutional neural network (LSTM-CNN) through comparative analysis, based on BERT." (Lin, 2022, p.1)

## 6. 评价方式
- 论断：在 Kaggle 竞赛平台的推文数据集上的实验表明，所提分类模型优于传统朴素贝叶斯分类模型和常见的微调模型，识别率最高可达 85%。
- 引文："Experiments on the tweet datasets of the Kaggle competition platform showed that the proposed classification model outperforms the traditional Naive Bayesian classification model and the common fine-tuning model, with the recognition rate up to 85%." (Lin, 2022, p.1)

## 7. 明确写出的局限
- 论断：作者指出训练所用数据规模较小、数据有限。
- 引文："由于训练所用数据规模较小，数据有限，这也是解决小样本文本分类的一种有效方法。" (Lin, 2022, p.6)
