---
title: 交叉验证Cross Validation
date: 2019-06-23 20:29:35
tags: Cross Validation
categories: 机器学习与算法
top:
---

模型效果评估是机器学习开发中相当重要的一步，无论使用哪种最先进的state-of-the-art算法来构建假设函数并训练机器学习模型，都必须评估其性能后才能继续使用它。Evaluate模型最简单、最快捷的方法就是将数据集拆分为训练和测试集，使用训练集数据训练模型，并通过计算accuracy检查其准确性。并且在执行拆分之前不要忘记对数据集进行shuffle。但是这种方法并不能保证万无一失，简单来说，在最终确定模型时不能完全依赖这种方法。你可知道为什么？
<!-- more -->
举个例子：
在进行垃圾邮件分类的案例中，数据中包含98％的垃圾邮件和2％的非垃圾邮件有效电子邮件是很常见的情况。在这种情况下，即使你没有创建任何模型，只是将每个输入分类为垃圾邮件，都将获得98%的准确性。这种情况称为**准确性悖论accuracy paradox**。
想象一下如果这是肿瘤细胞或胸部X射线分类的模型会发生什么，而你已经将这个98％准确性模型推向市场，这样的算法可没法对患者产生任何帮助。
# 划分数据集的作用
**训练集**
用来训练模型内参数的数据集，Classfier直接根据训练集来调整自身获得更好的分类效果，比如SGD算法在训练集上计算梯度寻找权重调整方向，树模型在训练集上计算信息增益或残差寻找最佳分裂点。

**验证集**
​用于在训练过程中检验模型的状态，收敛情况。验证集通常用于调整超参数(那些需要手动设定的参数)，根据几组模型验证集上的表现决定哪组超参数拥有最好的性能，这是其在交叉验证部分的主要作用。

​同时验证集在训练过程中还可以用来监控模型是否发生过拟合，一般来说验证集表现稳定后，若继续训练，训练集表现还会继续上升，但是验证集会出现不升反降的情况，这样一般就发生了过拟合。所以验证集也用来判断何时停止训练(Early stopping)。

**测试集**
测试集用来评价模型泛化能力，即之前模型使用验证集确定了超参数，使用训练集调整了参数，最后使用一个从没有见过的数据集来判断这个模型是否Work。

# 交叉验证是什么？
Cross Validation是一种评估模型性能的重要方法，主要用于在多个模型中（不同种类模型或同一种类不同超参数组合）挑选出在当前问题场景下表现最优的模型（model selection）。根据分成不同数据组的数量主要分为以下三大类：
## Train/Test spilt: # groups =2
在拿到数据之后通常会将所有数据分成两组，一组**train_set**用于训练模型;另一组用作保持集**holdout set**，用于检查模型在完全看不见的数据中的行为方式。下图总结了执行拆分的整个想法。
{% asset_img traing_test.png 400 200 %}

```py
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42, shuffle = True, stratify = y)
```
`X`是原始全体数据的特征，`y`是全体数据的标签，`shuffle`为True则会将所有样本先随机洗牌再切分，`stratify`用于处理不平衡的样本，将样本按照标签的不同进行分层采样。
好处：处理简单，只需随机把原始数据分为两组即可
坏处：但没有达到交叉的思想，由于是随机的将原始数据分组，所以最后验证集分类准确率的高低与原始数据的分组有很大的关系，得到的结果并不具有说服性。

## K折交叉验证，K-Fold Cross Validation: # groups =K
在训练集（train set）上训练得到的模型表现良好，但在测试集（test set）的预测结果不尽如人意，这就说明模型可能出现了过拟合（overfitting），bias低而variance高，在未知数据上的泛化能力差。
一个改进方案是，在训练集的基础上进一步划分出新的训练集和验证集（validate set），在新训练集训练模型，在验证集测试模型，不断调整初始模型（超参数等），使得训练得到的模型在验证集上的表现最好，最后放到测试集上得到这个最优模型的评估结果。
这个方案的问题在于模型的表现依赖于验证集的划分，可能使某些特殊样本被划入验证集，导致模型的表现出现异常（偏好或偏差）。而且训练集划了一部分给验证集后，训练模型能得到的数据就变少了，也会影响训练效果。因为通常来说，训练数据越多，越能反映出数据的真实分布，模型训练的效果就越好，越可能得到无偏估计。
交叉验证思想应运而生，交叉验证可以充分使用所有的训练数据用于评估模型。
{% asset_img holdout.webp 500 400 %}
K折交叉验证是最基本的cv方法，具体方法为，将训练集随机等分为k份，取其中一份为验证集评估模型，其余k-1份为训练集训练模型，重复该步骤k次，每次都取一份不同的子集为验证集，最终得到k个不同的模型（不是对一个模型迭代k次）和k个评分，综合这k个模型的表现（平均得分或其他）评估模型在当前问题中的优劣。
{% asset_img K-fold.webp 500 400 K-Fold Cross Validation %}
> K值的选取很有讲究，K越大，在训练集上的Bias就会越小，但训练集越大会导致Variance越大，同时花费的时间越长，所以选取适当大小的K很重要，经验值（empirical value）是K=5或10。

```py
# scikit-learn k-fold cross-validation
from numpy import array
from sklearn.model_selection import KFold
# data sample
data = array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
# prepare cross validation
kfold = KFold(n_splits=3, shuffle = True, random_state= 1)
# enumerate splits
for train, test in kfold.split(data):
    print('train: %s, test: %s' % (data[train], data[test]))
```

## 留一法，Leave one out（LOO）: # groups = len(dataset)
考虑一种极端情况，将K设为样本总数N，留一法每次在训练集的N个样本中选一个不同的样本作为验证集，其余样本为训练集，训练得到N-1个不同的模型。LOOCV是特殊的K-fold。

## 嵌套交叉验证，Nested Cross Validation
嵌套交叉验证（Nested Cross Validation）将调参和模型选择结合起来比较好的方式是嵌套交叉验证，其挑选的模型在训练集和测试集上的误差估计几乎没有出入。
嵌套交叉验证流程图如下（也被称作5*2 cross-validation）：
{% asset_img Nested_cv.webp 500 400 Nested Cross Validation %}
内层交叉验证（innner loop）：用于模型选择，可以进行特征工程处理数据。
外层交叉验证（outer loop）：用于模型评估，使用所有数据集进行分割，而不仅是训练集，且用Stratified K-Fold保证类别比例不变。外层每一折都使用内层得到的最优参数组合进行训练。
演示代码：
```py
gs = GridSearchCV(estimator=pipe_svc, ... param_grid=param_grid, ... scoring='accuracy', ... cv=2)
scores = cross_val_score(gs, X_train, y_train, ... scoring='accuracy', cv=5)
```
嵌套交叉验证可以看做是GridSearchCV的升级版，普通GridSearchCV训练的模型只在一部分数据上进行测试，而嵌套交叉验证可以使模型在全部数据上进行测试，能更好的说明模型的泛化能力。

# 选择合适的数据划分策略
在大多数数据划分工具包中，默认采用随机划分进行交叉验证。但是随机的结果并不总是最好的答案，有时候甚至是错误的。
在进行分类问题时，我们需要保证每一个类别都有样本出现在训练集和测试集当中，即使有些类别数量很少。而纯随机采样的划分策略有可能会导致某一部分数据并不包含某个类别。当这部分数据做了训练集，CV算法将崩溃，因为测试集当中包含模型从没见过的类别。如果遇到某类别数量很少的问题，则需要使用分层采样策略：每种类别按比例随机采样。

同样，比如在进行时间序列建模时，使用随机方法将在不知不觉的日期混合中打破训练集和测试集的时间连续性。在这类问题中，训练集代表我们现在拥有的数据，测试集代表未来的数据，我们需要确保当每个数据区用于测试时，只有先前的样本用于训练。一种方法是按年/月划分，然后对划分的每部分，仅使用时间较早的数据进行训练。

这种有目的地划分的策略对于**时间序列**问题是很有必要的，在其他情况下也可带来启发。例如，我们可以按城市划分数据，看看模型如何适用于以前从未见过的新城市，或者如果之前只看过少量城市，那么模型将如何运作。不同类型的分区策略会请求我们模型不同的问题，让我们能了解它在不同情况下的表现，掌握这一点就不会被生产中模型性能的变化感到意外了。

**为什么不使用cv过程中产生的最优模型？**
交叉验证并非用于建立具体模型，而是用于模型选择（model selection），cv中间过程产生的误差最小的模型并不一定是最优的，可能只是表面现象，因为只使用了一部分数据进行训练模型，且验证集的划分也不一定客观。当选定模型后，需要在**全部训练集上重新训练模型**。

{% ghcode https://scikit-learn.org/stable/_downloads/plot_nested_cross_validation_iris.py %}

References:
[1] Wayne Folta. *Nested Cross Validation: When Cross Validation Isn’t Enough.* Oct. 2017. URL: https://www.elderresearch.com/blog/nested-cross-validation.
[2] scikit-learn.org. *Nested versus non-nested cross-validation*. June 2019. URL: https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html.
[3] 行走的程序猿. *cross validation - 机器学习中的交叉验证法探究*. May 2018. URL: https://www.jianshu.com/p/cdf6df99b44b.
