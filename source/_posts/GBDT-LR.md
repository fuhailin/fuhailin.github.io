---
title: 推荐系统CTR实战——GBDT+LR
date: 2018-11-10 01:11:24
tags:
  - CTR
  - Recommender system
  - Machine Learning
categories: 机器学习与算法
---

推荐系统CTR实战系列：
 1. [推荐系统CTR实战——FM](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94FM/)
 2. [推荐系统CTR实战——FFM](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94FFM/)
 3. [推荐系统CTR实战——DeepFM](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94DeepFM/)
 4. [推荐系统CTR实战——Wide & Deep](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Wide-Deep/)
 5. [推荐系统CTR实战——Deep & Cross](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Deep-Cross/)
 6. [推荐系统CTR实战——Deep Interest Network](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Deep-Interest-Network/)
 7. [推荐系统CTR实战——GBDT+LR](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94GBDT-LR/)
 8. [推荐系统CTR实战——xDeepFM](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94xDeepFM/)
 9. [推荐系统CTR实战——Product-based Neural Network(PNN)](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Product-based-Neural-Network-PNN/)
 10. [推荐系统CTR实战——Neural Factorization Machines(NFM)](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Neural-Factorization-Machines-NFM/)
 11. [推荐系统CTR实战——Attentional Factorization Machines(AFM)](https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Attentional-Factorization-Machines-AFM/)

**首先祭出推荐系统CTR实战——GBDT+LR Demo的Python实现代码：**
*https://github.com/fuhailin/DeepRec/tree/master/GBDT%2BLR*

 # 1、 背景

       CTR预估（Click-Through Rate Prediction）是互联网计算广告中的关键环节，预估准确性直接影响公司广告收入。CTR预估中用的最多的模型是LR（Logistic Regression），LR是广义线性模型，与传统线性模型相比，LR使用了Logit变换将函数值映射到0~1区间，映射后的函数值就是CTR的预估值。LR这种线性模型很容易并行化，处理上亿条训练样本不是问题，但线性模型学习能力有限，需要大量特征工程预先分析出有效的特征、特征组合，从而去间接增强LR的非线性学习能力。

       LR模型中的特征组合很关键， 但又无法直接通过特征笛卡尔积解决，只能依靠人工经验，耗时耗力同时并不一定会带来效果提升。如何自动发现有效的特征、特征组合，弥补人工经验不足，缩短LR特征实验周期，是亟需解决的问题。Facebook 2014年的文章介绍了通过GBDT（Gradient Boost Decision Tree）解决LR的特征组合问题[^1]，随后Kaggle竞赛也有实践此思路[4][5]，GBDT与LR融合开始引起了业界关注。

       GBDT（Gradient Boost Decision Tree）是一种常用的非线性模型，它基于集成学习中的boosting思想，每次迭代都在减少残差的梯度方向新建立一颗决策树，迭代多少次就会生成多少颗决策树。GBDT的思想使其具有天然优势可以发现多种有区分性的特征以及特征组合，决策树的路径可以直接作为LR输入特征使用，省去了人工寻找特征、特征组合的步骤。这种通过GBDT生成LR特征的方式（GBDT+LR），业界已有实践（Facebook，Kaggle-2014），且效果不错，是非常值得尝试的思路。下图1为使用GBDT+LR前后的特征实验示意图，融合前人工寻找有区分性特征（raw feature）、特征组合（cross feature），融合后直接通过黑盒子（Tree模型GBDT）进行特征、特种组合的自动发现。


# GBDT与LR融合现状
GBDT和LR的融合方案，FaceBook的paper中有个例子：
![](/uploads/20150827190225375)
图中Tree1、Tree2为通过GBDT模型学出来的两颗树，x为一条输入样本，遍历两棵树后，x样本分别落到两颗树的叶子节点上，每个叶子节点对应LR一维特征，那么通过遍历树，就得到了该样本对应的所有LR特征。由于树的每条路径，是通过最小化均方差等方法最终分割出来的有区分性路径，根据该路径得到的特征、特征组合都相对有区分性，效果理论上不会亚于人工经验的处理方式。

GBDT模型的特点，非常适合用来挖掘有效的特征、特征组合。业界不仅GBDT+LR融合有实践，GBDT+FM也有实践，2014 Kaggle CTR竞赛冠军就是使用GBDT+FM，可见，使用GBDT融合其它模型是非常值得尝试的思路。

调研了Facebook、Kaggle竞赛关于GBDT建树的细节，发现两个关键点：采用ensemble决策树而非单颗树；建树采用GBDT而非RF（Random Forests）。解读如下：

      1） 为什么建树采用ensemble决策树？

      一棵树的表达能力很弱，不足以表达多个有区分性的特征组合，多棵树的表达能力更强一些。GBDT每棵树都在
      学习前面棵树尚存的不足，迭代多少次就会生成多少颗树。按paper以及Kaggle竞赛中的GBDT+LR融合方式，
      多棵树正好满足LR每条训练样本可以通过GBDT映射成多个特征的需求。

      2） 为什么建树采用GBDT而非RF？

      RF也是多棵树，但从效果上有实践证明不如GBDT。且GBDT前面的树，特征分裂主要体现对多数样本有区分度的特征；后面的树，
      主要体现的是经过前N颗树，残差仍然较大的少数样本。优先选用在整体上有区分度的特征，再选用针对少数样本有区分度的特征，
      思路更加合理，这应该也是用GBDT的原因。

然而，Facebook和Kaggle竞赛的思路是否能直接满足现在CTR预估场景呢？

按照Facebook、Kaggle竞赛的思路，不加入广告侧的ADID特征？但是现CTR预估中，AD ID类特征是很重要的特征，故建树时需要考虑AD ID。直接将AD ID加入到建树的feature中？但是AD ID过多，直接将AD ID作为feature进行建树不可行。下面第三部分将介绍针对现有CTR预估场景GBDT+LR的融合方案。

# GBDT与LR融合方案

AD ID类特征在CTR预估中是非常重要的特征，直接将AD ID作为feature进行建树不可行，顾考虑为每个AD ID建GBDT树。但互联网时代长尾数据现象非常显著，广告也存在长尾现象，为了提升广告整体投放效果，不得不考虑**长尾广告**。在GBDT建树方案中，对于曝光充分训练样本充足的广告，可以单独建树，发掘对单个广告有区分度的特征，但对于曝光不充分样本不充足的长尾广告，无法单独建树，需要一种方案来解决长尾广告的问题。

综合考虑方案如下，**使用GBDT建两类树，非ID建一类树，ID建一类树**。1）非ID类树：不以细粒度的ID建树，此类树作为base，即便曝光少的广告、广告主，仍可以通过此类树得到有区分性的特征、特征组合。2）ID类树：以细粒度的ID建一类树，用于发现曝光充分的ID对应有区分性的特征、特征组合。

如何根据GBDT建的两类树，对原始特征进行映射？以如下图为例，当一条样本x进来之后，遍历两类树到叶子节点，得到的特征作为LR的输入。当AD曝光不充分不足以训练树时，其它树恰好作为补充。

![](https://raw.githubusercontent.com/PnYuan/Practice-of-Machine-Learning/master/imgs/Kaggle_CTR/gbdt-lr/gbdt-lr_ad-id.png)


# 总结GBDT-LR方案的好处如下：
 - GBDT作为一种Boosting集成模型，其建模过程以残差拟合为目的，相应的数据信息学习也是从主体到细节（到噪声）。于是，对于GBDT序列化的子模型，其叶节点索引所对应的新特征的重要性是递减的，这事实上为我们提供了一套特征排序
 - GBDT实现了显示的特征转换，通过设置合理的子模型数量，既保留数据主体信息，又控制特征空间维度，提高数据效用和训练效率；
 - 在广告推荐中，广告ID是一个易被忽略的重要特征。采用GBDT-LR的方案可将其很好的利用起来。一般而言，ID取值多且呈现长尾分布，常用作法是对一些大广告（曝光充分，样本充足）建立专属GBDT，其它构建共用GBDT，其思路如下图示：


**Refenences**

[^1]: [Practical Lessons from Predicting Clicks on Ads at Facebook](http://quinonero.net/Publications/predicting-clicks-facebook.pdf)
[^2]: [duboya/CTR-Prediction|Github](https://github.com/duboya/CTR-Prediction/tree/46c303986ec57092d9eb4478a3583fa019d18efd/Algorithm%20Practice/GBDT%20%2B%20LR)
[^3]: [Kaggle滑水 - CTR预估（GBDT-LR）](https://pnyuan.github.io/blog/ml_practice/Kaggle%E6%BB%91%E6%B0%B4%20-%20CTR%E9%A2%84%E4%BC%B0%EF%BC%88GBDT-LR%EF%BC%89/)
[^4]: [Practical Lessons from Predicting Clicks on Ads at Facebook (GBDT + LR) 模型實踐](https://www.itread01.com/content/1546797307.html)
[^5]: [CTR预估中GBDT与LR融合方案|CSDN](https://blog.csdn.net/lilyth_lilyth/article/details/48032119)
[^6]: [推荐系统遇上深度学习(十)--GBDT+LR融合方案实战|简书](https://www.jianshu.com/p/96173f2c2fb4)
[^7]: [GBDT+LR算法解析及Python实现](https://www.cnblogs.com/wkang/p/9657032.html)
