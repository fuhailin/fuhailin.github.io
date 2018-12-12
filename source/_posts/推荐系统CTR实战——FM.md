---
title: 推荐系统CTR实战——FM
date: 2018-11-10 01:06:51
tags:
  - CTR
  - Recommender system
  - Machine Learning
categories: Machine Learning
mathjax: true
---
FM主要目标是：**`解决数据稀疏的情况下，特征怎样组合的问题`**

<!--more-->

FM有一下三个优点：
1. 可以在非常稀疏的数据中进行合理的参数估计
2. FM模型的时间复杂度是线性的
3. FM是一个通用模型，它可以用于任何特征为实值的情况

假设样本中有$n$个特征，对特征$\mathbf{x}$，FM的输出 $\hat{y}$ 为：
$$
\hat { y } ( \mathbf {x} ) : = w_{0} + \sum _ {i=1}^{n} w_{i} x_{i} + \sum _ {i=1}^{n} \sum _ {j=i+1}^{n} \left\langle \mathbf {v}_{i} , \mathbf {v} _ {j} \right\rangle x_{i} x_{j}
$$

其中：
$$
\left\langle \mathbf { v } _ { i } , \mathbf { v } _ { j } \right\rangle : = \sum _ { f = 1 } ^ { k } v _ { i , f } \cdot v _ { j , f }
$$
可以看到为了得到$\hat{y}$，会有两层循环，这个形式的时间复杂度为

$$
\sum_{i=1}^{n}\sum_{j=i+1}^n<V_i,V_j> x_ix_j
=\frac{1}{2}\sum_{f=1}^{k}((\sum_{i=1}^nv_{if}x_i)(\sum_{j=1}^nv_{jf}x_j) - \sum_{i=1}^nv_{if}^2x_i^2)
$$
