---
title: 利用Spark计算TF-IDF
date: 2019-04-30 14:43:03
tags: [Spark,Python]
categories: 大数据
top:
description: 在这篇文章中，我尝试使用Apache Spark中的Python版本Spark SQL API来写TF-IDF算法进行文本挖掘。
mathjax: true
---
TF-IDF(Term Frequency-Inverse Document Frequency，逆文档词频)是一项广为人知的文本挖掘算法，这一算法为文档中的每一项词赋予一个*权重weight* ，在一篇文档当中如果一个词语出现的频率越高说明这个词语在这篇文档当中的重要性越高，但是如果该词语普遍出现在众多的文档的当中，说明该词语是一个常用词，对于文档的特点并不具有代表性，那么这个词语的重要性又应该降低。
因此我们用TF，Term Frequency来计算词语在文档当中出现的词频，其计算方式如下：
$$
TF_{i,j}=\frac{n_{i,j}}{\sum_{k}n_{i,j}}
$$
其中分子$n_{i,j}$代表词语在本篇文档当中出现的次数，分母表示该文档当中所有词语出现的总次数。
而IDF(Inverse Document Frequency)表示逆向文件频率，来计算词语出现在了多少个文档当中，其计算方式如下：
$$
IDF(x) = log\frac{N+1}{N(x)+1} + 1
$$
这里的+1是一个平滑操作，防止出现`除零`和`乘零`操作。
最终TF-IDF值就是TF与IDF的权衡结果：$TF-IDF(x) = TF(x) * IDF(x)$。
