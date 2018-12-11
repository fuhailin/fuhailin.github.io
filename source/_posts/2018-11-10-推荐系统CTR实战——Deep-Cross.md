---
title: 推荐系统CTR实战——Deep & Cross
date: 2018-11-10 01:03:39
tags:
  - CTR
  - Recommender system
  - Deep Learning
categories: Machine Learning
mathjax: true
description: Deep & Cross Network(DCN)[1]是来自于 2017 年 google 和 Stanford 共同完成的一篇工作，对比同样来自 google 的工作 Wide & Deep[2]，DCN 不需要特征工程来获得高阶的交叉特征，对比 FM 系列[3][4]的模型，DCN 拥有更高的计算效率并且能够提取到更高阶的交叉特征。
---
特征工程一直是很多预测模型效果突出的关键，人工设计等影响因素往往决定这这一环节的好坏，深度学习可以自动学习特征，却很难学到一些交叉特征。本文提出了一种交叉的网络结构的深度学习模型DCN，Deep & Cross Network，可以有效的寻找交叉特征，在CTR预估方面可以取得较好的效果。

# 嵌入层处理类别特征

在大规模推荐系统中，如CTR预测，通常会有大量的类别特征需要处理，如“country=usa”。为了将这些信息变成计算机能处理的特征，通常使用one_hot编码处理成独热向量如“[ 0,1,0 ]”；然而，这些大量的词汇往往导致处理后的特征空间维度过高。

为了减少维数，一种常用的做法是采用嵌入过程将这些离散特征转换成实数值的稠密向量（通常称为嵌入向量）：

$$
\mathbf { x } _ { \text { embed, } i } = W _ { \text { embed, } , i } \mathbf { x } _ { i }
$$

然后，我们将嵌入向量与连续特征向量叠加起来形成一个向量：
$$
x_0=[x_{\text{embed,1}}^T,\cdots,x_{\text{embed,k}}^T,x_{\text{dense}}^T]
$$

拼接起来的向量$X0$将作为我们Cross Network和Deep Network的输入.

# Cross Network

在广告场景下，特征交叉的组合与点击率是有显著相关的，例如，“USA”与“Thanksgiving”、“China”与“Chinese New Year”这样的关联特征，对用户的点击有着正向的影响。换句话说，来自“China”的用户很可能会在“Chinese New Year”有大量的浏览、购买行为，而在“Thanksgiving”却不会有特别的消费行为。这种关联特征与label的正向相关性在实际问题中是普遍存在的，如“化妆品”类商品与“女性”，“球类运动配件”的商品与“男性”，“电影票”的商品与“电影”品类偏好等。因此，引入特征的组合是非常有意义的。而这部分正是FM存在的意义。

DCN的特点之一就在于提出了一个创新的结构来计算组合特征：
![](/uploads/cross_layer.webp)
可以看到，交叉网络的特殊结构使交叉特征的程度随着层深度的增加而增大。多项式的最高程度（就输入X0而言）为L层交叉网络L + 1。如果用Lc表示交叉层数，d表示输入维度。然后，参数的数量参与跨网络参数为：d * Lc * 2 (w和b)




**References**:
1. [推荐系统遇上深度学习(五)--Deep&Cross Network模型理论和实践|石晓文的学习日记](https://www.jianshu.com/p/77719fc252fa)
2. [Deep & Cross 与广告不得不说的秘密](https://zhuanlan.zhihu.com/p/38461541)
3. http://blog.leanote.com/post/ryan_fan/Deep-Cross-Network
4. https://www.jiqizhixin.com/articles/2018-07-16-17
