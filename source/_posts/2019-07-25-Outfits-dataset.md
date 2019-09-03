---
title: Outfits dataset
date: 2019-07-25 21:39:08
tags:
categories:
top:
---

# Task：

1、Fill in the blank

2、Outfit generation given texts or images

3、 Compatibility prediction

<!-- more -->

# Dataset：

**The Polyvore dataset**

[Polyvore.com]: https://www.ssense.com/en-cn/women?utm_source=polyvore.com&amp;utm_medium=redirect

是一个流行的时尚搭配网站，用户可以自由搭配喜欢的时装配饰等单品，并通过在线社区分享，同时了解其它用户的穿衣搭配。Polyvore数据集是从Polyvore.com上爬取的用户搭配方案与单品信息数据集，根据爬取的数量不同有多个不同的版本。网络上公开可用的The Polyvore dataset 有 [polyvore-dataset](https://github.com/xthan/polyvore-datasepolyvore-datasett) 等，其中包含的搭配Outfits方案数与单品Items数量如下：

> `#Outfits`: 21889 (17316 for training, 1497 for validation and 3076 for testing)
> `#Categories`: 380
> `#Items`: 164,379
> Max Items/Outfit: 8
> Average Items/Outfit: 6.5
> Text Available?: Titles & Descriptions

![](2019-07-25-23-05-54.png)

[polyvore-images.tar.gz](https://drive.google.com/drive/folders/0B4Eo9mft9jwoVDNEWlhEbUNUSE0) 是一个更大的版本（33,375 outfits），polyvore-dataset为其真子集。


## 论文中相关数据使用情况：
[Learning Fashion Compatibility with Bidirectional LSTMs](https://arxiv.org/abs/1707.05691) "只用了polyvore-dataset"
[Dressing as a Whole: Outfit Compatibility Learning Based on Node-wise Graph Neural Networks](https://arxiv.org/abs/1902.08009) "只用了polyvore-dataset"
[Learning Type-Aware Embeddings for Fashion Compatibility](https://arxiv.org/abs/1803.09196) "只用了自己爬取的更大的polyvore数据集"
[Outfit Compatibility Prediction and Diagnosis with Multi-Layered Comparison Network](https://github.com/WangXin93/fashion_compatibility_mcn):尚未公开论文，但从代码看就polyvore-dataset一个数据集

<!--
**The Fashion-Gen Outfits dataset**



**Amazon products dataset** -->
