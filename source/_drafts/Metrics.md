---
title: Metrics
tags:
categories:
top:
---
# 排序指标NDCG
在推荐和搜索等排序任务中有时需要为用户返回一个推荐列表，直观的思想会想到，用户最想要的那个相关条目应该排在列表的最前方，NDCG(Normalized Discounted Cumulative Gain，归一化折损累计增益)的思想便是衡量推荐多个条目时结果的排序的相关程度。一个推荐系统返回一些项并形成一个列表，每一项都有一个相关的评分值，通常这些评分值是一个非负数，这就是gain（增益）。此外，对于这些没有用户反馈的项，我们通常设置其增益为0。我们把这些分数相加，也就是Cumulative Gain（累积增益）。
$$
C G_{k}=\sum_{i=1}^{k} rel_{i}
$$

其中， $rel_{i}$ 表示位置$i$的推荐结果的相关性，$k$表示推荐列表的大小。

CG没有考虑每个推荐结果处于不同位置对整个推荐结果的影响，例如，我们总是希望相关性大大的结果排在前面，相关性低的排在前面会影响用户体验。

**DCG**在CG的基础上引入了位置影响因素，计算公式如下：
$$
D C G_{k}=\sum_{i=1}^{k} \frac{2^{r e l_{i}}-1}{\log _{2}(i+1)}
$$
从上面的式子可以得出：1）推荐结果的相关性越大，DCG越大。2）相关性好的排在推荐列表前面的话，推荐效果越好，DCG越大。

DCG针对不同的推荐列表之间很难进行横向评估，而我们评估一个推荐系统不可能仅使用一个用户的推荐列表及相应结果进行评估，而是对整个测试集中的用户及其推荐列表结果进行评估。那么，不同用户的推荐列表的评估分数就需要进行归一化，也就是NDCG。

其中IDCGIDCG是指ideal DCG，也就是完美结果下的DCG。因此DCG的值介于 (0,IDCG] ，故NDCG的值介于(0,1]，那么用户u的NDCG@K定义为：
$$
N D C G_{u} @ k=\frac{D C G_{u} @ k}{I D C G_{u}}
$$
平均NDCG的值为：
$$
N D C G @ k=\frac{\sum_{u \in U} N D C G_{u} @ k}{I D C G_{u}}
$$


在推荐任务中，我们给出的预测结果形式可能是用户会选择的物品，这时候预测结果里面没有相关分数怎么办呢？以Kaggle竞赛[Airbnb New User Bookings](https://www.kaggle.com/c/airbnb-recruiting-new-user-bookings/overview/evaluation)为例，处理策略是：用户选择的物品相关度置为1，否则为0.

```python
def dcg_at_k(r, k, method=1):
    """Score is discounted cumulative gain (dcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    >>> dcg_at_k(r, 1)
    3.0
    >>> dcg_at_k(r, 1, method=1)
    3.0
    >>> dcg_at_k(r, 2)
    5.0
    >>> dcg_at_k(r, 2, method=1)
    4.2618595071429155
    >>> dcg_at_k(r, 10)
    9.6051177391888114
    >>> dcg_at_k(r, 11)
    9.6051177391888114
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Discounted cumulative gain
    """
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_k(r, k=5, method=1):
    """Score is normalized discounted cumulative gain (ndcg)
    Relevance is positive real values.  Can use binary
    as the previous methods.
    Example from
    http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
    >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
    >>> ndcg_at_k(r, 1)
    1.0
    >>> r = [2, 1, 2, 0]
    >>> ndcg_at_k(r, 4)
    0.9203032077642922
    >>> ndcg_at_k(r, 4, method=1)
    0.96519546960144276
    >>> ndcg_at_k([0], 1)
    0.0
    >>> ndcg_at_k([1], 2)
    1.0
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
        k: Number of results to consider
        method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
    Returns:
        Normalized discounted cumulative gain
    """
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max


def score_predictions(preds, truth, n_modes=5):
    """
    preds: pd.DataFrame
      one row for each observation, one column for each prediction.
      Columns are sorted from left to right descending in order of likelihood.
    truth: pd.Series
      one row for each obeservation.
    """
    assert (len(preds) == len(truth))
    r = pd.DataFrame(0, index=preds.index, columns=preds.columns, dtype=np.float64)
    for col in preds.columns:
        r[col] = (preds[col] == truth) * 1.0

    score = pd.Series(r.apply(ndcg_at_k, axis=1), name='score')
    return score
  
preds = pd.DataFrame([['US', 'FR', 'CN'], ['FR', 'US', 'CN'], ['FR', 'FR', 'CN']])
truth = pd.Series(['US', 'CN', 'FR'])
print('predictions: \n', preds)
print('\n\n truth: \n', truth)
print('\n\n scores: \n', score_predictions(preds, truth))
```

# Hit Ratio(HR)

在top-K推荐中，HR是一种常用的衡量召回率的指标，其计算公式如下：
$$
H R @ K=\frac{\text {NumberofHits } @ K}{|G T|}
$$
分母是所有的测试集合，分子式每个用户top-K推荐列表中属于测试集合的个数的总和。举个简单的例子，三个用户在测试集中的商品个数分别是10，12，8，模型得到的top-10推荐列表中，分别有6个，5个，4个在测试集中，那么此时HR的值是 (6+5+4)/(10+12+8) = 0.5。

```python
def hit(gt_items, pred_items):
    count = 0
    for item in pred_items:
        if item in gt_items:
            count += 1
    return count
```





# Mean Reciprocal Rank (MRR)

如果我

们只对排序中的第一个正确的答案感兴趣，MRR则为评价推荐列表的一个合理选择，**对于一个query，若第一个正确答案排在第n位，则MRR得分就是 1/n 。**
$$
M R R=\frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{r a n k_{i}}
$$
其中，Q为样本query集合，|Q|表示Q中query个数， ranki 表示在第i个query中，第一个正确答案的排名

```python
def mrr(gt_items, pred_items):
    for index,item in enumerate(pred_items):
        if item in gt_items:
            return 1/index
```

