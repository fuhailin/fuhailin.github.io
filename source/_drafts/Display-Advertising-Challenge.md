---
title: Display Advertising Challenge
tags:
---
## 数据集

本文使用的是Kaggle公司举办的[Display Advertising Challenge](https://www.kaggle.com/c/criteo-display-ad-challenge)中所使用的Criteo数据集。

每一行是一次广告展示的特征，第一列是一个标签，表示这次广告展示是否被点击。总共有39个特征，其中13个特征采用整型值，另外26个特征是类别类特征。测试集中是没有标签的。

下载数据集：

```bash
cd data && ./download.sh && cd ..
```

## 数据准备
处理原始数据集，整型特征使用min-max归一化方法规范到[0, 1]，类别类特征使用了one-hot编码。原始数据集分割成两部分：90%用于训练，其他10%用于训练过程中的验证。
