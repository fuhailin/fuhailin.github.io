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
 1. 推荐系统CTR实战——FM：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94FM/
 2. 推荐系统CTR实战——FFM:https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94FFM/
 3. 推荐系统CTR实战——DeepFM:https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94DeepFM/
 4. 推荐系统CTR实战——Wide & Deep：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Wide-Deep/
 5. 推荐系统CTR实战——Deep & Cross：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Deep-Cross/
 6. 推荐系统CTR实战——Deep Interest Network：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Deep-Interest-Network/
 7. 推荐系统CTR实战——GBDT+LR：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94GBDT-LR/
 8. 推荐系统CTR实战——xDeepFM：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94xDeepFM/
 9. 推荐系统CTR实战——Product-based Neural Network(PNN)：https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Product-based-Neural-Network-PNN/
 10. 推荐系统CTR实战——Neural Factorization Machines(NFM): https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Neural-Factorization-Machines-NFM/
 11. 推荐系统CTR实战——Attentional Factorization Machines(AFM): https://fuhailin.github.io/%E6%8E%A8%E8%8D%90%E7%B3%BB%E7%BB%9FCTR%E5%AE%9E%E6%88%98%E2%80%94%E2%80%94Attentional-Factorization-Machines-AFM/

 # 1、 背景

       CTR预估（Click-Through Rate Prediction）是互联网计算广告中的关键环节，预估准确性直接影响公司广告收入。CTR预估中用的最多的模型是LR（Logistic Regression）[1]，LR是广义线性模型，与传统线性模型相比，LR使用了Logit变换将函数值映射到0~1区间[2]，映射后的函数值就是CTR的预估值。LR这种线性模型很容易并行化，处理上亿条训练样本不是问题，但线性模型学习能力有限，需要大量特征工程预先分析出有效的特征、特征组合，从而去间接增强LR的非线性学习能力。

       LR模型中的特征组合很关键， 但又无法直接通过特征笛卡尔积解决，只能依靠人工经验，耗时耗力同时并不一定会带来效果提升。如何自动发现有效的特征、特征组合，弥补人工经验不足，缩短LR特征实验周期，是亟需解决的问题。Facebook 2014年的文章介绍了通过GBDT（Gradient Boost Decision Tree）解决LR的特征组合问题[3]，随后Kaggle竞赛也有实践此思路[4][5]，GBDT与LR融合开始引起了业界关注。

       GBDT（Gradient Boost Decision Tree）是一种常用的非线性模型[6][7][8][9]，它基于集成学习中的boosting思想[10]，每次迭代都在减少残差的梯度方向新建立一颗决策树，迭代多少次就会生成多少颗决策树。GBDT的思想使其具有天然优势可以发现多种有区分性的特征以及特征组合，决策树的路径可以直接作为LR输入特征使用，省去了人工寻找特征、特征组合的步骤。这种通过GBDT生成LR特征的方式（GBDT+LR），业界已有实践（Facebook，Kaggle-2014），且效果不错，是非常值得尝试的思路。下图1为使用GBDT+LR前后的特征实验示意图，融合前人工寻找有区分性特征（raw feature）、特征组合（cross feature），融合后直接通过黑盒子（Tree模型GBDT）进行特征、特种组合的自动发现。

 ![](uploads/GBDT+LR_1.png)


Refenences:
 1. [Practical Lessons from Predicting Clicks on Ads at Facebook](http://quinonero.net/Publications/predicting-clicks-facebook.pdf)
 2. [duboya/CTR-Prediction|github](https://github.com/duboya/CTR-Prediction/tree/46c303986ec57092d9eb4478a3583fa019d18efd/Algorithm%20Practice/GBDT%20%2B%20LR)
 3.
