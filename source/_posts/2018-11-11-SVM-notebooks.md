---
title: 支持向量机SVM完全笔记
date: 2018-11-11 13:09:46
tags: Machine Learning
mathjax: true
categories: 机器学习与算法
---

支持向量机，因其英文名为support vector machine，故一般简称SVM，通俗来讲，它是一种二分类模型，其基本模型定义为特征空间上的间隔最大的线性分类器，其学习策略便是间隔最大化，最终可转化为一个凸二次规划问题的求解。

<!--more-->

## 分类标准的起源：Logistic回归

理解SVM，咱们必须先弄清楚一个概念：线性分类器。

给定一些数据点，它们分别属于两个不同的类，现在要找到一个线性分类器把这些数据分成两类。如果用x表示数据点，用y表示类别（y可以取1或者-1，分别代表两个不同的类），一个线性分类器的学习目标便是要在n维的数据空间中找到一个超平面（hyper plane），这个超平面的方程可以表示为（ wT中的T代表转置）：

$$w^{T}x+b=0$$

可能有读者对类别取1或-1有疑问，事实上，这个1或-1的分类标准起源于logistic回归。

Logistic回归目的是从特征学习出一个0/1分类模型，而这个模型是将特性的线性组合作为自变量，由于自变量的取值范围是负无穷到正无穷。因此，使用logistic函数（或称作sigmoid函数）将自变量映射到(0,1)上，映射后的值被认为是属于y=1的概率。

假设函数

$$h_{\theta }=g(\theta ^{T}x)=\frac{1}{1+e^{-\theta ^{T}x}}$$

其中x是n维特征向量，函数g就是logistic函数。而 $g(z)=\frac{1}{1 + e^{-z}}$ 的图像是 ![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/logistic.webp)










































SVM 与 LR的优缺点对比：
