---
title: 利用Spark计算TF-IDF
date: 2019-04-30 14:43:03
tags: [Spark,Python]
categories: 大数据
top:
description: 在这篇文章中，我尝试使用Apache Spark中的Python版本Spark SQL API来写TF-IDF算法进行文本挖掘。
mathjax: true
---
# TF-IDF定义
TF-IDF(Term Frequency-Inverse Document Frequency，逆文档词频)是一项广为人知的文本挖掘算法，这一算法为文档中的每一项词赋予一个*权重weight* ，在一篇文档当中如果一个词语出现的频率越高说明这个词语在这篇文档当中的重要性越高，但是如果该词语普遍出现在众多的文档的当中，说明该词语是一个常用词，对于文档的特点并不具有代表性，那么这个词语的重要性又应该降低。
因此我们用TF，Term Frequency来计算词语在文档当中出现的词频，其计算方式如下：
<!-- more -->
$$
TF(x) = \frac{某个词x在文章中出现的次数} {文档总词数}
$$

而IDF(Inverse Document Frequency)表示逆向文件频率，来计算词语出现在了多少个文档当中，其计算方式如下：
$$
IDF(x) = log\frac{训练语料的总文档数}{出现词语x的文档数+1}
$$
这里的+1是一个平滑操作，防止出现`除零`操作。
最终TF-IDF值就是TF与IDF的权衡结果：$TF-IDF(x) = TF(x) * IDF(x)$。

下面直接给出单机、Python版的TF-IDF程序和分布式的、PySpark版的TF-IDF程序：

{% include_code lang:python Python版TF-IDF程序 tfidf.py %}

{% include_code lang:python PySpark版TF-IDF程序 tfidf-pyspark.py %}


**References**:
http://www.tfidf.com/
https://dzone.com/articles/calculating-tf-idf-with-apache-spark
https://towardsdatascience.com/sentiment-analysis-with-pyspark-bc8e83f80c35
http://hejunhao.me/archives/856
