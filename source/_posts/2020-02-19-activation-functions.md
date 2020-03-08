---
title: 激活函数
date: 2020-02-19 11:43:45
tags: 
categories: 机器学习与算法
top:
mathjax: true
---
  本文搜集整理了从Sigmoid、ReLU到Dice等十几种常见激活函数的原理与特点，并从底层用Numpy实现和Python绘制它们。
<!-- more -->
激活函数之性质

**1. 非线性：**即导数不是常数。保证多层网络不退化成单层线性网络。这也是激活函数的意义所在。

**2. 可微性：**保证了在优化中梯度的可计算性。虽然 ReLU 存在有限个点处不可微，但处处 subgradient，可以替代梯度。

**3. 计算简单：**激活函数复杂就会降低计算速度，因此 RELU 要比 Exp 等操作的激活函数更受欢迎。

**4. 非饱和性（saturation）：**饱和指的是在某些区间梯度接近于零（即梯度消失），使得参数无法继续更新的问题。最经典的例子是 Sigmoid，它的导数在 x 为比较大的正值和比较小的负值时都会接近于 0。RELU 对于 x<0，其梯度恒为 0，这时候它也会出现饱和的现象。Leaky ReLU 和 PReLU 的提出正是为了解决这一问题。

**5. 单调性（monotonic）：**即导数符号不变。当激活函数是单调的时候，单层网络能够保证是凸函数。但是激活函数如 mish 等并不满足单调的条件，因此单调性并不是硬性条件，因为神经网络本来就是非凸的。

**6. 参数少：**大部分激活函数都是没有参数的。像 PReLU 带单个参数会略微增加网络的大小。还有一个例外是 Maxout，尽管本身没有参数，但在同样输出通道数下 k 路 Maxout 需要的输入通道数是其它函数的 k 倍，这意味着神经元数目也需要变为 k 倍。

## Sigmoid激活函数

$$\sigma \left( x\right) =\dfrac {1} {1+e^{-x}}$$

其导数为：

$$\sigma'(x) = \sigma(x) \cdot (1 - \sigma(x))$$

```python
def Sigmoid(x):
    return 1. / (1 + np.exp(-x))
```

![sigmoid](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/sigmoid.png)

**优点：**

- 梯度平滑，求导容易
- Sigmoid函数的输出映射在(0,1)之间，单调连续，输出范围有限，优化稳定，可以用作输出层

**缺点：**

- 激活函数计算量大（在正向传播和反向传播中都包含幂运算和除法）；
- 梯度消失：输入值较大或较小（图像两侧）时，sigmoid导数则接近于零，因此在反向传播时，这个局部梯度会与整个代价函数关于该单元输出的梯度相乘，结果也会接近为 0 ，无法实现更新参数的目的；
- Sigmoid 的输出不是 0 为中心（zero-centered）。因为如果输入都是正数的话（如 $$f=w^{T}x+b$$ 中每个元素都 $$x>0$$ ），那么关于 $$w$$ 的梯度在反向传播过程中，要么全是正数，要么全是负数（具体依据整个表达式 $$f$$ 而定），这将会导致梯度下降权重更新时出现 z 字型的下降。当然，如果是按 batch 去训练，那么每个 batch 可能得到不同的信号，整个批量的梯度加起来后可以缓解这个问题。因此，该问题相对于上面的神经元饱和问题来说只是个小麻烦，没有那么严重。

## Tanh激活函数

$$
tanh(x) = \frac{e^{x} - e^{-x}}{e^{x} + e^{-x}}
$$
其导数为：
$$
tanh'(x) = 1 - tanh(x)^{2}
$$

```python
def tanh(x):
    return np.sinh(x)/np.cosh(x)
```

![tanh](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/tanh.png)

**优点：**

- 比Sigmoid函数收敛速度更快
- tanh(x) 的梯度消失问题比 sigmoid 要轻
- 相比Sigmoid函数，输出是以 0 为中心 zero-centered

**缺点：**

- 还是没有改变Sigmoid函数的最大问题——由于饱和性产生的梯度消失。



## 整流线性单元(ReLU)

| Function                                                     | Derivative                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $\begin{split}ReLU(x) = \begin{Bmatrix} x & x > 0 \\ 0 & x <= 0 \end{Bmatrix}\end{split}$ | $\begin{split}ReLU'(x) = \begin{Bmatrix} 1 & x>0 \\ 0 & x<0 \end{Bmatrix}\end{split}$ |

```python
def ReLU(x):
    return x * (x > 0)
```

![ReLU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/relu.png)

**优点：**

- 计算与收敛速度非常快：不涉及指数等运算；
- 一定程度**缓解梯度消失**问题：因为导数为 1，不会像 sigmoid 那样由于导数较小，而导致连乘得到的梯度逐渐消失。

**缺点：**

**Dying ReLU**：某些神经元可能永远不会被激活，导致相应的参数永远不能被更新。有两个主要原因可能导致这种情况产生: (1) 非常不幸的参数初始化，这种情况比较少见 (2) learning rate太高导致在训练过程中参数更新太大，不幸使网络进入这种状态。解决方法是可以采用Xavier初始化方法，以及避免将learning rate设置太大或使用adagrad等自动调节learning rate的算法。

尽管存在这两个问题，ReLU目前仍是最常用的activation function，在搭建人工神经网络的时候推荐优先尝试！

前面说了一大堆的 ReLU 的缺点，有很多大牛在此基础上做了改进，如 Leaky ReLU、PReLU(Parametric ReLU)等。

我整理了本文涉及到的全部十几种常见激活函数的底层实现代码Python版，关注我的公众号"赵大寳Note"（ID：StateOfTheArt）回复关键词：激活函数  下载收藏。

![关注公众号趙大寳Note，回复“激活函数”下载全部代码](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/wechat_channel.png)

## 指数线性单元(ELU)

| Function                                                     | Derivative                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $\begin{split}ELU(x) = \begin{Bmatrix} x & x > 0 \\ α.( e^x – 1) & x <= 0 \end{Bmatrix}\end{split}$ | $\begin{split}ELU'(x) = \begin{Bmatrix} 1 & x>0 \\ α.e^x & x<0 \end{Bmatrix}\end{split}$ |

![ELU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/ELU.png)

**优点：**

- 能避免死亡 ReLU 问题：x 小于 0 时函数值不再是 0，因此可以避免 dying relu 问题；
- 能得到负值输出，这能帮助网络向正确的方向推动权重和偏置变化。

**缺点：**

- 计算耗时：包含指数运算；
- α 值是超参数，需要人工设定

## SELU

SELU 源于论文 ***Self-Normalizing Neural Networks\***，作者为 Sepp Hochreiter，ELU 同样来自于他们组。

SELU 其实就是 ELU 乘 lambda，关键在于这个 lambda 是大于 1 的，论文中给出了 lambda 和 alpha 的值：

- lambda = 1.0507
- alpha = 1.67326

$$
\operatorname{selu}(x)=\lambda\left\{\begin{array}{ll}{x} & {\text { if } x>0} \\ {\alpha e^{x}-\alpha} & {\text { if } x \leqslant 0}\end{array}\right.
$$

![SELU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/SELU.png)

**优点：**

- SELU 激活能够对神经网络进行自归一化（self-normalizing）；
- 不可能出现梯度消失或爆炸问题，论文附录的定理 2 和 3 提供了证明。

**缺点：**

- 应用较少，需要更多验证；
- lecun_normal 和 Alpha Dropout：需要 lecun_normal 进行权重初始化；如果 dropout，则必须用 Alpha Dropout 的特殊版本。

## Leaky ReLU

Leaky ReLU 是为解决“ ReLU 死亡”问题的尝试。

| Function                                                     | Derivative                                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| $\begin{split}R(x) = \begin{Bmatrix} x & x > 0 \\ \alpha x & x <= 0 \end{Bmatrix}\end{split}$ | $\begin{split}R'(x) = \begin{Bmatrix} 1 & x>0 \\ \alpha & x<0 \end{Bmatrix}\end{split}$ |

![Leaky_ReLU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/Leaky_ReLU.png)

**优点：**

- 类似于 ELU，能避免死亡 ReLU 问题：x 小于 0 时候，导数是一个小的数值，而不是 0；
- 与 ELU 类似，能得到负值输出；
- 计算快速：不包含指数运算。

**缺点：**

- 同 ELU，α 值是超参数，需要人工设定；
- 在微分时，两部分都是线性的；而 ELU 的一部分是线性的，一部分是非线性的。

## Parametric ReLU (PRELU)

形式上与 Leak_ReLU 在形式上类似，不同之处在于：PReLU 的参数 alpha 是可学习的，需要根据梯度更新。

- alpha=0：退化为 ReLU
- alpha 固定不更新，退化为 Leak_ReLU

![PReLU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/ParametricReLU.png)

**优点：**

与 ReLU 相同。

**缺点：**

在不同问题中，表现不一。

## Gaussian Error Linear Unit(GELU)

高斯误差线性单元激活函数在最近的 Transformer 模型（谷歌的 BERT 和 OpenAI 的 GPT-2）中得到了应用。GELU 的论文来自 2016 年，但直到最近才引起关注。
$$
\operatorname{GELU}(x)=0.5 x\left(1+\tanh \left(\sqrt{2 / \pi}\left(x+0.044715 x^{3}\right)\right)\right)
$$
![GELU](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/GELU.png)

优点：

- 似乎是 NLP 领域的当前最佳；尤其在 Transformer 模型中表现最好；
- 能避免梯度消失问题。

缺点：

- 这个2016 年提出的新颖激活函数还缺少实际应用的检验。

## Swish

Swish激活函数诞生于Google Brain 2017的论文 [Searching for Activation functions](https://arxiv.org/abs/1710.05941)中，其定义为：
$$
f(x) = x · \text{sigmoid}(βx)
$$
β是个常数或可训练的参数.Swish 具备无上界有下界、平滑、非单调的特性。

![Swish](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/Swish.png)

Swish 在深层模型上的效果优于 ReLU。例如，仅仅使用 Swish 单元替换 ReLU 就能把 Mobile NASNetA 在 ImageNet 上的 top-1 分类准确率提高 0.9%，Inception-ResNet-v 的分类准确率提高 0.6%。
当β = 0时,Swish变为线性函数$f(x) ={x\over 2}$.
β → ∞, $σ(x) = (1 + \exp(−x))^{−1}$为0或1. Swish变为ReLU: f(x)=2max(0,x)
所以Swish函数可以看做是介于线性函数与ReLU函数之间的平滑函数.

## Data Adaptive Activation Function(Dice)

Dice激活函数诞生于alibaba 2018 的CTR论文***Deep Interest Network***中，根据 Parametric ReLU 改造而来，ReLU类函数的阶跃变化点再x=0处，意味着面对不同的输入这个变化点是不变的，DIN中改进了这个控制函数，让它根据数据的分布来调整，选择了统计神经元输出的均值和方差(实际上就是*Batch_Normalization*,CTR中BN操作可是很耗时的，可以推测Dice复杂的计算快不起来不会大规模引用)来描述数据的分布：
$$
f(s)=p(s) . s+(1-p(s)) \cdot \alpha s, p(s)=\frac{1}{1+e^{-\frac{s-E(s)}{\sqrt{\operatorname{Var}(s)+\epsilon}}}}
$$
优点：

- 根据数据分布灵活调整阶跃变化点，具有BN的优点(解决Internal Covariate Shift)，原论文称效果好于Parametric ReLU。

缺点：

- 具有BN的缺点，大大加大了计算复杂度。

## Maxout

Maxout 是对 ReLU 和 Leaky ReLU 的一般化归纳，它的函数公式是（二维时）：
$$
Maxout(x) = \max \left( w_{1}^{T}x+b_{1},W_{2}^{T}x+b_{2}\right)
$$
ReLU 和 Leaky ReLU 都是这个公式的特殊情况（比如 ReLU 就是当 $$w_{1},b_{1}=0$$时）。

![Maxout](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/Maxout.png)

优点：

- Maxout 神经元拥有 ReLU 单元的所有优点（线性和不饱和），而没有它的缺点（死亡的 ReLU 单元）

缺点：

- 和 ReLU 对比，它每个神经元的参数数量增加了一倍，这就导致整体参数的数量激增。

## Softplus

$$
softplus(x)=\log \left(1+e^{x}\right)
$$

![Softplus](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/softplus.png)

softplus可以看作是ReLu的平滑，不常见。

## Softmax

Sigmoid函数只能处理两个类别，这不适用于多分类的问题，所以Softmax可以有效解决这个问题。Softmax函数很多情况都运用在神经网路中的最后一层网络中，使得每一个类别的概率值在(0, 1)之间。
$$
s\left(x_{i}\right)=\frac{e^{x_{i}}}{\sum_{j=1}^{n} e^{x_{j}}}
$$

```python
def softmax(x):
    return np.exp(x) / sum(np.exp(x))
```

![Softmax](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/activation-function/softmax.png)

## 如何选择激活函数？

通常来说，很少会把各种激活函数串起来在一个网络中使用的。

如果使用 ReLU ，那么一定要小心设置 learning rate ，而且要注意不要让你的网络出现很多 “ dead ” 神经元，如果这个问题不好解决，那么可以试试 Leaky ReLU 、 PReLU 或者 Maxout.

最好不要用 sigmoid ，可以试试 tanh ，不过可以预期它的效果会比不上 ReLU 和 Maxout.

****************

看到这里你已经知道了足够多的激活函数，那你还记得你学习激活函数的初衷吗？我们为什么需要激活函数，激活函数的作用呢？为什么SVM这类算法没有激活函数也能进行非线性分类呢？一起思考

References:

[1]: *([1](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html#id2), [2](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html#id4))* http://cs231n.github.io/neural-networks-1/

[2]: [ML Glossary | Activation Functions](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html#activation-functions)

[3]: [机器之心 | 激活函数](https://www.jiqizhixin.com/graph/technologies/1697e627-30e7-48a6-b799-39e2338ffab5)

[4]: [激活函数(ReLU, Swish, Maxout)](https://www.cnblogs.com/makefile/p/activation-function.html)
