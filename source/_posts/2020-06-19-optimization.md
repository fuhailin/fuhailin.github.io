---
title: optimization
date: 2020-06-19 16:09:43
tags:
categories:
top:
---

模型优化方法的选择直接关系到最终模型的性能。有时候效果不好，未必是特征的问题或者模型设计的问题，很可能是优化算法的问题，而且好的优化算法还能够帮助加速训练模型。

深度学习模型的发展进程：
SGD -> SGDM ->NAG -> AdaGrad -> AdaDelta -> Adam -> Nadam

<!-- more -->

1.整体框架
首先定义：
待优化参数$w$, 目标函数：$f(w)$，学习率$\alpha$
每次迭代：

计算目标函数关于参数的梯度：$gt=▽f(wt)$
根据历史梯度计算一阶动量和二阶动量：
$mt=ϕ(g1,g2,...,gt),Vt=ψ(g1,g2,...,gt)$

计算当前时刻的下降梯度：$ηt=α⋅m_t / \sqrt{V_t}$

根据下降梯度对参数进行更新：$wt+1=wt−ηt$


步骤3、4对于各个算法都是一致的，主要的差别就体现在1和2上。


## 1. 梯度下降法SGD

最基本的优化方法，沿着负梯度的方向更新参数，实现如下：

```python
# 梯度下降法
w += - learning_rate * dw
```

其中learning_rate是**超参数**代表学习率，被更新的**变量**为w，其梯度为dw，梯度->位置，很好理解。

**缺点：**

- 有可能会陷入局部最小值,容易被困在鞍点；
- 容易产生震荡不收敛，最终会一直在最小值附近波动，并不会达到最小值并停留在此；
- 下降速度慢，迟迟不能到达全局最优值；
- 选择合适的learning rate比较困难；
- 在所有方向上统一的缩放梯度，不适用于稀疏数据

## 2. 动量法Momentum

动量法是一类从物理中的动量获得启发的优化方法，可以简单理解为：当我们将一个小球从山上滚下来时，没有阻力的话，它的动量会越来越大，但是如果遇到了阻力，速度就会变小。实现如下：

```python
# 动量法
w += beta * w - learning_rate * (1-beta) * dw  # 梯度影响速度
```

**变量**v的初始值被定为0，**超参数**mu在优化过程中被视为动量，其物理意义可以视为摩擦系数，加入的这一项，可以使得梯度方向不变的维度上速度变快，梯度方向有所改变的维度上的更新速度变慢，这样就可以加快收敛并减小震荡。和之前不同的是梯度不会直接对位置造成影响，梯度->速度->位置。

**优点**：

- 增加了稳定性；
- 收敛速度更快；
- 还有一定摆脱局部最优的能力。

## 3. RMSprop

RMSprop(Root Mean Square prop)是一种自适应学习率方法，依旧是基于梯度对位置进行更新。为了消除梯度下降中的摆动，加入了梯度平方的指数加权平均。梯度大的指数加权平均就大，梯度小的指数加权平均就小，保证各维度的梯度都在一个良机，进而减少摆动。
关于指数加权平均的通俗理解可以参考[https://zhuanlan.zhihu.com/p/29895933](https://www.lizenghai.com/goto/?url=https://zhuanlan.zhihu.com/p/29895933)

```
# RMSprop
cache = decay_rate * cache + (1 - decay_rate) * dw**2 # 梯度平方的指数加权平均
w += - learning_rate * dw / (np.sqrt(cache) + eps) # 基于梯度更新
```

其中decay_rate和eps都是**超参数**，每一步的**变量**cache的值都不同，所以可以看做自适应得对学习率进行调整。
还有一些其他效果较好的优化器，由于这些前置知识已经足够理解Adam了，所以在此不做过多介绍。



# Adam

Adam可以看做动量法和RMSprop的结合

```
# Adam
m = beta1*m + (1-beta1)*dx
v = beta2*v + (1-beta2)*(dx**2)
x += - learning_rate * m / (np.sqrt(v) + eps)
```

对于m和v的处理，同样使用了指数加权平均。相比于RMSprop，梯度换为了平滑的m，而cache的处理基本没有变化。**超参数**beta1和beta2的初始值接近于1，因此，计算出的偏差项接近于0。

# AdamW

AdamW是在Adam+L2正则化的基础上进行改进的算法。
使用Adam优化带L2正则的损失并不有效。如果引入L2正则项，在计算梯度的时候会加上对正则项求梯度的结果。那么如果本身比较大的一些权重对应的梯度也会比较大，由于Adam计算步骤中减去项会有除以梯度平方的累积，使得减去项偏小。按常理说，越大的权重应该惩罚越大，但是在Adam并不是这样。而权重衰减对所有的权重都是采用相同的系数进行更新，越大的权重显然惩罚越大。在常见的深度学习库中只提供了L2正则，并没有提供权重衰减的实现。

![img](https://upload-images.jianshu.io/upload_images/19036657-526f2e6d75337b2b.png)
Adam+L2 VS AdamW

图片中红色是传统的Adam+L2 regularization的方式，绿色是Adam+weightdecay的方式。可以看出两个方法的区别仅在于“系数乘以上一步参数值“这一项的位置。再结合代码来看一下AdamW的具体实现。

以下代码来自[https://github.com/macanv/BERT-BiLSTM-CRF-NER/blob/master/bert_base/bert/optimization.py](https://www.lizenghai.com/goto/?url=https://github.com/macanv/BERT-BiLSTM-CRF-NER/blob/master/bert_base/bert/optimization.py)中的AdamWeightDecayOptimizer中的apply_gradients函数中，BERT中的优化器就是使用这个方法。在代码中也做了一些注释用于对应之前给出的Adam简化版公式，方便理解。可以看出update += self.weight_decay_rate * param这一句是Adam中没有的，也就是Adam中绿色的部分对应的代码，weightdecay这一步是是发生在Adam中需要被更新的参数update计算之后，并且在乘以学习率learning_rate之前，这和图片中的伪代码的计算顺序是完全一致的。总之一句话，如果使用了weightdecay就不必再使用L2正则化了。

```
      # m = beta1*m + (1-beta1)*dx
      next_m = (tf.multiply(self.beta_1, m) + tf.multiply(1.0 - self.beta_1, grad))
      # v = beta2*v + (1-beta2)*(dx**2)
      next_v = (tf.multiply(self.beta_2, v) + tf.multiply(1.0 - self.beta_2, tf.square(grad)))
      # m / (np.sqrt(v) + eps)
      update = next_m / (tf.sqrt(next_v) + self.epsilon)
      # Just adding the square of the weights to the loss function is *not*
      # the correct way of using L2 regularization/weight decay with Adam,
      # since that will interact with the m and v parameters in strange ways.
      #
      # Instead we want ot decay the weights in a manner that doesn't interact
      # with the m/v parameters. This is equivalent to adding the square
      # of the weights to the loss with plain (non-momentum) SGD.
      if self._do_use_weight_decay(param_name):
        update += self.weight_decay_rate * param
      update_with_lr = self.learning_rate * update
      # x += - learning_rate * m / (np.sqrt(v) + eps)
      next_param = param - update_with_lr
```

原有的英文注释中也解释了Adam和传统Adam+L2正则化的差异，好了到这里应该能理解Adam了，并且也能理解AdamW在Adam上的改进了。

# Lookahead，RAdam?

Lookahead和RAdam都是比较新的优化器，具体原理在此不过多介绍。**但是我有疑问需要大神来解答一下。**
在BERT中引入优化器的源码中有这样一句注释

```
  # It is recommended that you use this optimizer for fine tuning, since this
  # is how the model was trained (note that the Adam m/v variables are NOT
  # loaded from init_checkpoint.)
```

也就是说在微调BERT的时候强烈建议使用AdamW优化器。在自己的NER数据集上使用6层BERT，AdamW能得到98%左右的F1值，我尝试使用了RAdam，Lookahead+RAdam和Lookahead+AdamW，还有Ranger，得到的效果都非常差，要不就0的F1值，要不就是30%左右，好像完全没有效果。

**项目参考源码**：[https://github.com/macanv/BERT-BiLSTM-CRF-NER](https://www.lizenghai.com/goto/?url=https://github.com/macanv/BERT-BiLSTM-CRF-NER)
**RAdam,Lookahead**:[https://github.com/lifeiteng/Optimizers](https://www.lizenghai.com/goto/?url=https://github.com/lifeiteng/Optimizers)
[https://github.com/michaelrzhang/lookahead](https://www.lizenghai.com/goto/?url=https://github.com/michaelrzhang/lookahead)
**Range**r:[https://github.com/jyhengcoder/Ranger_tensorflow](https://www.lizenghai.com/goto/?url=https://github.com/jyhengcoder/Ranger_tensorflow)

# LazyAdam

它是Adam optimizer的变种，可以更有效地处理稀疏更新（sparse updates）。

原始的Adam算法为每个训练变量（tranable variable）维护着两个moving-average累加器；该累加器会在每个step上被更新。该class为稀疏变量（sparse variables）的梯度更新提供了lazier handling机制。它只会为出现在当前batch中的稀疏变量（sparce variable indices）更新移动平均累积，而非为所有indices更新累积。对比原始的Adam optimizer，它可以为一些应用在模型训练吞吐上提供大的提升。然而，它与原始Adam算法有一些不同的语义，可能会导致不同的期望结果（empirical results）。

注意，当前不支持amsgrad，该参数只能为False。


# 参考资料

[https://www.zhihu.com/question/323747423/answer/790457991](https://www.lizenghai.com/goto/?url=https://www.zhihu.com/question/323747423/answer/790457991)
[https://www.cnblogs.com/guoyaohua/p/8542554.html](https://www.lizenghai.com/goto/?url=https://www.cnblogs.com/guoyaohua/p/8542554.html)
[https://zhuanlan.zhihu.com/p/63982470](https://www.lizenghai.com/goto/?url=https://zhuanlan.zhihu.com/p/63982470)
[https://zhuanlan.zhihu.com/p/38945390](https://www.lizenghai.com/goto/?url=https://zhuanlan.zhihu.com/p/38945390)

https://www.jianshu.com/p/e17622b7ffee

https://blog.csdn.net/yinyu19950811/article/details/90476956

https://ruder.io/optimizing-gradient-descent/index.html



https://mooc.study.163.com/learn/2001281003?tid=2403023002&_trace_c_p_k2_=a20d455215c44c419594a999c46400ee#/learn/content
