# Napps2021_BIM_VariantRetrieval_CBR

- 条目 1：该文没有给出案例库的文献篇数或样本条数，检索实验只是一个简化案例：以一个问题对两个备选变体做相似度比较，作者并明确承认案例库中的变体数量相当有限。
  - "After these steps, the similarity measure between the problem and two possible variants can be calculated." (Napps et al., 2021, p.5)
  - "In the presented example the number of variants is quite limited, but sufficient to show the retrieval process of finding a suitable variant for a simplified given problem." (Napps et al., 2021, p.7)
  - NOT_FOUND: 全文第 1–8 页均无以数字给出的数据集规模，案例库只以 n 个变体图泛指、未给具体数量，故文献篇数、案例总数、测试样本条数这三类数值均不存在；上两条只是该文仅有的规模描述。
- 条目 2：该文没有报告 accuracy、precision、recall 一类检索准确率，只定义了相似度的归一化区间：差异为零对应相似度一，差异为一对应相似度零，相似度取值落在零到一之间。
  - "Using this formula, the similarity between a problem p and a possible variant v, with non-negative weights, is a value between zero and one." (Napps et al., 2021, p.3)
  - "A difference of zero corresponds to the similarity measure one, that means, that the attributes are equal to each other." (Napps et al., 2021, p.4)
