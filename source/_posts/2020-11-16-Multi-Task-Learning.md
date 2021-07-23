---
title: Multi Task Learning
date: 2020-11-16 14:51:32
tags:
categories:
top:
---
0、背景

一般来说，在推荐系统应用场景下，最基础的目标就是提升用户的CTR，即推荐给用户看的物品尽可能是用户想要去点击的。但这样简单做了之后，反而暴露出一个粗俗的问题，即推荐给用户的物品会产生越来越多的标题党，因为这类标题党往往尝试利用人性的弱点，通过文字或图片的暗示的内容骗取高的点击率，但提供的内容于用户无益，甚至会造成用户流失、涉及黄赌毒等违法内容，于平台会是大大的损害。

![](https://lh3.googleusercontent.com/proxy/olSbi_yzkF75t66ZhG4DYOA_OjF30RisW4WJ4Cqyb69JyVjxhwrXj5tvIZEnbDH3EJSDyOxIcz06FSrCaF_Q6W08uY7BuR-z_jcLeibVsbumAy3C4VA_LbeEmA)

<!-- more -->

因此优秀的产品经理发现单纯优化CTR这个业务目标不行之后又提出了其他业务目标，比如在短视频场景会有完播率、点赞率、分享率；在电商场景会有购买率；在游戏、广告领域会有转化率等等。加上这类业务目标限制，推荐系统再产生标题党之类虚假点击率高的item将难以完成其他业务目标了，于是多目标同时优化的思路应运而生。




ESMM（Entire Space Multi-Task Model）

ESMM是在建模有任务序列依赖关系的多任务优化过程中提出的，例如点击率、转化率有明显的序列依赖关系，毕竟item impression之后才会知道用户会不会click，而用户click之后才会知道用户会不会conversion。在此之前行业流行的做法是分别构建一个CTR模型（利用全部曝光数据）和一个CVR模型（利用全部click数据）。但这么做留下了两个问题：

sample selection bias（SSB）：CVR模型训练时候使用click数据，但上线serving时候面对将是全部impression数据，所以CVR模型这么做存在特征穿越风险它已知的样本都是被click过的，论文作者称之为sample selection bias。

data sparsity (DS)：CVR模型的训练空间是click样本，这与CTR模型使用的impression样本空间大小是数量级上的差别，CVR模型能使用的数据量不够深度学习发挥潜力。

ESMM怎么解决这两个问题的呢？

利用CTR模型 $p C T R=p(y=1 \mid x)$和CVR模型 $p C V R=p(z=1 \mid y=1, x)$ ，提出新的概念$p CTCVR=p(z=1, y=1\mid x)$，那么有
$$
\underbrace{p(y=1, z=1 \mid x)}_{p C T C V R}=\underbrace{p(y=1 \mid x)}_{p C T R} \times \underbrace{p(z=1 \mid y=1, x)}_{p C V R}
$$
CTCVR模型是建立在全量impression样本空间的，于是借助CTCVR模型和CTR模型，在全量impression样本空间下，可以得到CVR模型：
$$
p(z=1 \mid y=1, x)=\frac{p(y=1, z=1 \mid x)}{p(y=1 \mid x)}
$$
但这样直接做有一个问题，实际应用中 $pCTR$ 的值可能会很小，除以该值的话可能导致数值上的不稳定（可能大于1）。ESMM为了避免这种情况使用了乘法的形式，于是
