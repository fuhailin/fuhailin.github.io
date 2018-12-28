---
title: 推荐系统CTR实战——Wide & Deep
date: 2018-11-10 01:08:33
tags:
  - CTR
  - Recommender system
  - Deep Learning
categories: 机器学习与算法
mathjax: true
description: Wide and deep 模型是 TensorFlow 在 2016 年 6 月左右发布的一类用于分类和回归的模型，并应用到了 Google Play 的应用推荐中。wide and deep 模型的核心思想是结合线性模型的记忆能力（memorization）和 DNN 模型的泛化能力（generalization），在训练过程中同时优化 2 个模型的参数，从而达到整体模型的预测能力最优。
---

Wide & Deep模型结构如下：
![Wide & Deep Network](/uploads/wide_and_deep.webp)
最左边的线性模型和最右边的深度模型联手结盟打造出中间的wide and deep。


Wide & Deep的主要特点:
本文提出Wide & Deep模型，旨在使得训练得到的模型能够同时获得记忆（memorization）和泛化（generalization）能力：

-   **记忆（memorization）即从历史数据中发现item或者特征之间的相关性；哪些特征更重要——Wide部分**。
-   **泛化（generalization）即相关性的传递，发现在历史数据中很少或者没有出现的新的特征组合；——Deep部分**。
在推荐系统中，记忆体现的准确性，而泛化体现的是新颖性。


## Wide部分
wide部分就是一个广义线性模型，输入主要由两部分，一部分是原始特征，另一部分是交互特征，我们可以通过cross-product transformation的形式来构造K组交互特征：
$$
\phi _ { k } ( \mathbf { x } ) = \prod _ { i = 1 } ^ { d } x _ { i } ^ { c _ { k i } } \quad c _ { k i } \in \{ 0,1 \}
$$

## Deep部分
Deep部分就是一个DNN的模型，每一层计算如下：

$$
a ^ { ( l + 1 ) } = f \left( W ^ { ( l ) } a ^ { ( l ) } + b ^ { ( l ) } \right)
$$

## 联合训练
Wide & Deep模型采用的是联合训练的形式，而非集成。二者的区别就是联合训练公用一个损失函数，然后同时更新各个部分的参数，而集成方法是独立训练N个模型，然后进行融合。因此，模型的输出为：
$$
P ( Y = 1 | \mathbf { x } ) = \sigma \left( \mathbf { w } _ { w i d e } ^ { T } [ \mathbf { x } , \phi ( \mathbf { x } ) ] + \mathbf { w } _ { d e e p } ^ { T } a ^ { \left( l _ { f } \right) } + b \right)
$$

## 使用Wide and Deep模型的App推荐系统架构
当一个用户访问app商店时，此时会产生一个请求，请求到达推荐系统后，推荐系统为该用户返回推荐的apps列表。
![](/uploads/wide_and_deep_overview.png)
在实际的推荐系统中，通常将推荐的过程分为两个部分，即上图中的Retrieval和Ranking，Retrieval负责从数据库中检索出与用户相关的一些apps，Ranking负责对这些检索出的apps打分，最终，按照分数的高低返回相应的列表给用户。

模型的训练之前，最重要的工作是训练数据的准备以及特征的选择，在apps推荐中，可以使用到的数据包括用户和曝光数据。
每一条样本对应了一条曝光数据，同时，样本的标签为1表示安装，0则表示未安装。

对于类别特征，通过词典（Vocabularies）将其映射成向量；对于连续的实数特征，将其归一化到区间[0,1]。

![](/uploads/wide_and_deep_structure.png)

## TensorFlow官方实现代码

https://github.com/tensorflow/models/tree/master/official/wide_deep

**References**:
1. Cheng H T, Koc L, Harmsen J, et al. Wide & Deep Learning for Recommender Systems[J]. 2016:7-10.
2. [Wide and Deep,双剑合璧](https://www.jianshu.com/p/71cf3d1f579d)
3. [Wide & Deep | Ryan_Fan's Blog]http://blog.leanote.com/post/ryan_fan/wide-and-deep-Model
<!-- 4. -->
