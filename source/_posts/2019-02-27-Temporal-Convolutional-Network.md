---
title: Temporal Convolutional Network (TCN与TrellisNet)
date: 2019-02-27 18:57:06
tags: [TCN,TrellisNet,Sequence Modeling]
categories: 机器学习与算法
top:
mathjax: true
---
《An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling》[^1]论文阅读笔记。说来惭愧，这篇论文去年4月份就曾在技术圈里刷屏，号称横扫序列模型中如RNN、GRU、LSTM等基本模型，当时第一时间就听说了，但是一直没有弄懂技术原理，这一年来的面试中，有两次对方提到了CNN用来序列建模的优点，然而我却没有深入去理解它，今天就来攻克它。

<!-- more -->

![An Overview of TCNs](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-02-27-192324.png)
# Temporal Convolutional Network简介
本文就序列建模, 对 CNN 和 RNN 进行了比较. 按照文章的说法, 在 RNN 的主场打了一架, 结果 CNN 完胜. 使用的模型包括针对序列建模特殊构造的CNN, 称为 Temporal Convolutional Network, TCN 和普通 RNN, GRU, LSTM.

为了比较 RNN 和 CNN 在 Sequence Modeling 上的性能, 文章构造了一种能用于序列建模的简单通用的 CNN 架构 TCN, 结合了 causal convolution, residual connection 和 dilation convolution.

> TCN 的典型特点是:
>  1. 卷积是 causal 的, 意味着不会存在“信息泄露leakage”，未来的信息不会泄漏到过去;
>  2. 能将任意长度的序列**如同RNN那样映射为相同长度的输出序列**.

为实现第二个目标, TCN 使用一维全卷积结构, 通过 zero padding 使各层保持相同长度.
## Causal Convolution因果卷积
而**所谓 causal convolution, 就是计算 t 时刻的输出时, 仅对前一层 t 时刻及之前的状态进行卷积**.

Causal convolution 的叠加, 高层的感受野野/历史信息与网络层数呈线性关系. 对于超长序列, 网络必须很深, 才能捕捉到足够长的历史信息. 针对这个问题, 文中使用了 dilation convolution, 使得随网络的加深, 高层的感受野呈指数扩大.

{% gist b8af96d5d36dc12226cc9129c410afeb causal_conv1d.py %}

## Dilated Convolutions扩张卷积
使用Dilated Convolutions[^2]的关键是为了通过较少的参数和较少的层数实现更大的 *感受野 (receptive field)* 。 考虑一个由`$k\times k$`个卷积组成，没有池化层pooling的普通卷积网络，很容易得出每一个单元 *感受野* 的大小(影响激活的像素点)是`$l*(k-1)+k$`，其中$l$是第几层，所以有效感受野的单元数与层数成正比。这样得到的感受野是非常有限的，特别是对于高分辨率输入图像。

卷积Dilated Convolutions的出现拯救了这一问题，
Dilation convolution[^2] 的运算如下:  `$F ( s ) = \left( \mathbf { x } * _ { d } f \right) ( s ) = \sum _ { i = 0 } ^ { k - 1 } f ( i ) \cdot \mathbf { x } _ { s - d \cdot i }$`( `$\mathbf { x }$`表示输入序列, $f$ 表示 filter, $d$ 是 dilation factor, $k$ 是 filter size,  `$s - d \cdot i $`意味着只对过去的状态作卷积). 看图最直观.
![A dilated causal convolution with dilation factors d = 1, 2, 4 and filter size k = 3](causal-convolution.png)
和传统卷积不同的是，扩张卷积允许卷积时的输入存在间隔采样，采样率受图中的d控制。 最下面一层的d=1，表示输入时每个点都采样，中间层d=2，表示输入时每2个点采样一个作为输入。一般来讲，越高的层级使用的d的大小越大。所以，扩张卷积使得有效窗口的大小随着层数呈指数型增长。这样卷积网络用比较少的层，就可以获得很大的感受野。
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Screen-Shot-2016-05-12-at-09-47-12.png)
> (a). 普通卷积，1-dilated convolution，卷积核的感受野为`$3 \times 3 = 9$`
> (b). 扩张卷积，2-dilated convolution，卷积核的感受野为`$7 \times 7 = 49$`
> (c). 扩张卷积，4-dilated convolution，卷积核的感受野为`$15 \times 15 = 225$`
一个扩张率为2的3×3卷积核，感受野与5×5的卷积核相同，但参数数量仅为$9$个，是5×5卷积参数数量的`$36%$`。

## Residual Connections残差链接
TCN 的感受野依赖于上式中的 dilation factor d 和 filter/kernel size k, 以及网络深度 n. 为获得足够大的感受野, TCN 还是不得不增加网络的深度, 因此它构造了残差单元来训练更深的网络. (残差单元在 ResNet 的笔记中有详细介绍)
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-02-27-222900.png)
残差链接被证明是训练深层网络的有效方法，它使得网络可以以跨层的方式传递信息。本文构建了一个残差块来代替一层的卷积。如上图所示，一个残差块包含两层的卷积和非线性映射，在每层中还加入了WeightNorm和Dropout来正则化网络。

## 讨论和总结
总体来讲，TCN模型上的创新并不是很大，因果卷积和扩展卷积也并不是本论文提出来，本文主要是将TCN的结构梳理了一下，相比于wavenet中的结构，去掉了门机制，加入了残差结构，并在很多的序列问题上进行了实验。实验效果如下：
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-02-27-223110.png)
在多个任务上，都比标准的LSTM、GRU等效果好。

## TCN优缺点

**TCN 在序列建模方面的优势是**:
 1. 可并行性 (只要抛弃了 RNN, 神经网络基本都具有了这一优点);
 2. 通过调整 n, k, d, 可灵活地控制感受野, 能适应不同任务 (有些任务要求解决超长期依赖, 有些任务更依赖短期依赖);
 3. 稳定的梯度 (同样地, 只要抛弃了 RNN, 时间传播方向上的梯度爆炸/消失问题就自然解决了);
 4. 训练时的低内存占用，特别是面对长输入序列 (参数共享, 以及只存在沿网络方向的反向传播带来的裨益).

**TCN 的缺点**:
 1. 推断时, 需要更多的内存 (此时 RNN 只需要维护一个 hidden state, 每次接受一个输入; 而 TCN 要保持一个足够长的序列, 以保留历史状态);
 2. 迁移的困难性 (不同领域任务对感受野的大小不同, 使用小 k 和小 d 学好的模型难以应用于需要大 k 和大 d 的任务).

## Show Me the Code

> PyTorch: https://github.com/locuslab/TCN
> TensorFlow: https://github.com/Songweiping/TCN-TF
> Keras: https://github.com/philipperemy/keras-tcn
> Notebook: https://colab.research.google.com/drive/1la33lW7FQV1RicpfzyLq9H0SH1VSD4LE

# Trellis Networks for Sequence Modeling
在写《An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling》查阅资料的过程中又发现了TCN作者同一个实验室对TCN改进的工作：《Trellis Networks for Sequence Modeling》[^3]

> TrellisNet PyTorch: https://github.com/locuslab/trellisnet

本文延续在序列模型上的探索，提出了一种新的结构，称为trellis networks，一方面，这种结构与TCN有些类似，但是在权值共享机制和隐层状态计算过程上有所不同；另一方面，作者严格证明了这种结构与某种特殊的截断循环神经网络之间是等价的，这个发现的意义在于证明trellis network同时吸取了两种结构的优势，可以某种程度上解释它的优越性能，并可以增加将CNN和RNN的一些改进融入到这个结构中。

## TrellisNet与TCN的区别
TrellisNet本质上也是一种特殊的时序卷积网络。时序网络有两个重要的特征：a) **因果卷积**，满足因果性，即时刻t的结果只与t时刻之前的状态有关，不存在t时刻之后的信息泄露；b) **扩张卷积**，逐层堆叠以逐渐增大感知野，建模长期依赖关系。这两个特性都可以在TrellisNet中得到满足，但是不同于TCN，TrellisNet有两个显著的不同，**a) 在所有层之间进行权值共享；b) 输入序列作为每层输入的一部分**。

Reference:
[^1]: [An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling](https://arxiv.org/abs/1803.01271)
[^2]: [Dilated Convolutions and Kronecker Factored Convolutions](https://www.inference.vc/dilated-convolutions-and-kronecker-factorisation/)
[^3]: [Trellis Networks for Sequence Modeling](https://arxiv.org/abs/1810.06682)
 [TCN论文阅读](https://zhuanlan.zhihu.com/p/52477665)
 [\[Tensorflow\] Implementing Temporal Convolutional Networks](https://medium.com/the-artificial-impostor/notes-understanding-tensorflow-part-3-7f6633fcc7c7)
 [论文分享：Trellis Networks for Sequence Modeling](https://zhuanlan.zhihu.com/p/47422814)
