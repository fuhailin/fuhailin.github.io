---
title: Matrix Derivative
date: 2020-12-22 19:36:58
tags:
categories:
top:
---

矩阵求导（Matrix Derivative）也称作矩阵微分（Matrix Differential），在机器学习、图像处理、最优化等领域的公式推导中经常用到。矩阵求导实际上是多元变量的微积分问题，只是应用在矩阵空间上而已，即为标量求导的一个推广，他的定义为将自变量中的每一个数与因变量中的每一个数求导。

<!-- more -->

具体地，假设存在 $A_{m \times n}$ 和 $B_{p \times q}$ ，则 $\frac{\partial A}{\partial B}$ 会将 $A$ 中的每一个值对 $B$ 中的每一个值求导，最后一共会得到 $m \times n \times p \times q$ 个导数值。这么多的导数值，最后是排布成一个 $m \times(n \times p \times q)$ 的矩阵还是一个 $(m \times n \times p) \times q$ 的矩阵呢？矩阵求导的关键就在于规定如何排布这么多的导数值。

以分布布局为例子，一共有以下几个矩阵求导法则。分母布局是什么意思呢？简单的说就是以分母为一个基准，希望求导出来的结果和分母的维度相同。除了分母布局以外还有分子布局。分子布局和分母布局的求导结果通常相差一个转置。

### 基本法则

#### 法则 0 ：标量对标量求导

略。详细的请参考高等数学。

#### 法则 1 ：标量对向量求导

考虑我们有 $f$ 是一个标量，$x=\left[\begin{array}{llll}x_{1} & x_{2} & \cdots & x_{p}\end{array}\right]^{T}$ 是一个 $p \times 1$ 的列向量。则有：
$$
\frac{\partial f}{\partial x}=\left[\begin{array}{cccc}
\frac{\partial f}{\partial x_{1}} & \frac{\partial f}{\partial x_{2}} & \cdots & \frac{\partial f}{\partial x_{p}}
\end{array}\right]^{T}
$$
可以看得出，求导出来的结果维度是和分母 $x$ 相同的。若 $x$ 为行向量同理。

#### 法则 2 ：向量对标量求导

考虑我们有 是一个 的列向量， 是一个标量。则有：



可以看得出，这个时候求导出来的结果维度和分子 是相反的。若 为行向量同理。

#### 法则 3 ：向量对向量求导

考虑我们有 $f=\left[\begin{array}{llll}f_{1} & f_{2} & \cdots & f_{m}\end{array}\right]^{T}$ 是一个 $m \times 1$ 的列向量，  是$x=\left[\begin{array}{llll}x_{1} & x_{2} & \cdots & x_{p}\end{array}\right]^{T}$ 一个 $p \times 1$ 的列向量。则有：
$$
\frac{\partial f}{\partial x}=\left[\begin{array}{cccc}
\frac{\partial f_{1}}{\partial x_{1}} & \frac{\partial f_{2}}{\partial x_{1}} & \cdots & \frac{\partial f_{m}}{\partial x_{1}} \\
\frac{\partial f_{1}}{\partial x_{2}} & \frac{\partial f_{2}}{\partial x_{2}} & \cdots & \frac{\partial f_{m}}{\partial x_{2}} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_{1}}{\partial x_{p}} & \frac{\partial f_{2}}{\partial x_{p}} & \cdots & \frac{\partial f_{m}}{\partial x_{p}}
\end{array}\right]
$$
这时求导结果的维度为 $p \times m$ .

#### 法则 4 ：标量对矩阵求导

考虑我们有 $f$ 是一个标量，$x_{p \times q}$ 是一个矩阵。则有：
$$
\frac{\partial f}{\partial x}=\left[\begin{array}{cccc}
\frac{\partial f}{\partial x_{11}} & \frac{\partial f}{\partial x_{12}} & \cdots & \frac{\partial f}{\partial x_{1 q}} \\
\frac{\partial f}{\partial x_{21}} & \frac{\partial f}{\partial x_{22}} & \cdots & \frac{\partial f}{\partial x_{2 q}} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f}{\partial x_{p 1}} & \frac{\partial f}{\partial x_{p 2}} & \cdots & \frac{\partial f}{\partial x_{p q}}
\end{array}\right]
$$
同样，我们求导结果和分母 $x$ 的维度一致，是 $p \times q$ 。

#### 法则 5 ：矩阵对向量求导

考虑我们有 $f_{m \times n}$ 是一个矩阵，$x$ 是一个标量。则有：
$$
\frac{\partial f}{\partial x}=\left[\begin{array}{cccc}
\frac{\partial f_{11}}{\partial x} & \frac{\partial f_{21}}{\partial x} & \cdots & \frac{\partial f_{m 1}}{\partial x} \\
\frac{\partial f_{21}}{\partial x} & \frac{\partial f_{22}}{\partial x} & \cdots & \frac{\partial f_{m 2}}{\partial x_{2 q}} \\
\vdots & \vdots & \ddots & \vdots \\
\frac{\partial f_{n 1}}{\partial x} & \frac{\partial f_{n 2}}{\partial x} & \cdots & \frac{\partial f_{n m}}{\partial x}
\end{array}\right]
$$
我们求导的结果与分子相反，为 $n \times m$

#### 其余：向量与矩阵之间以及矩阵与矩阵之间的求导

当我们的自变量与因变量都为不为标量时，根据我们对矩阵求导实质的讨论，势必会得出大量的导数难以被排列。例如，一般情况下，假设我们有 $f m \times n$ 以及 $x_{p \times q}$ ，则求导后我们会得到 $m \times n \times p \times q$ 个导数结果。这时对这些导数一般有两种定义方法。

##### 第一种定义

我们按照之前的法则，将 $\frac{\partial f}{\partial x}$ 理解为对每一个 $f$ 中的标量，使其对 $x$ 求导，然后将其放回矩阵 中的原位。即我们使用 $\frac{\partial f_{i j}}{\partial x}$ 替换 $f_{i j}$ ，最后会得到一个 $m p \times n q$ 的导数矩阵。

##### 第二种定义（主流）

这种定义是将矩阵对矩阵求导问题归约到向量对向量求导。即对矩阵先做向量化处理，然后再求导：
$$
\frac{\partial f}{\partial x}=\frac{\partial v e c(f)}{\partial v e c(x)}
$$
其中，向量化的实现方法分为列向量化和行向量化。我们以列向量化为例，将 $f_{m \times n}$ 和 $x_{p \times q}$ 向量化为 $f_{m n \times 1}$ 和 $x_{p q \times 1}$ ，然后利用法则 3 求导得到维度为 $p q \times m n$ 的导数结果。

### 有用的公式

下列公式中，$A_{m \times 1}$ 和 $x_{m \times 1}$ 是列向量，$B_{m \times m}$ 是矩阵。下面 3 个公式在文末有证明。

| 编号 | 公式                                                         |
| :--- | :----------------------------------------------------------- |
| 1    | $$\frac{\partial x^{T} A}{\partial x}=\frac{\partial A^{T} x}{\partial x}=A $$ |
| 2    | $$ \frac{\partial x^{T} x}{\partial x}=x $$                  |
| 3    | $$ \frac{\partial x^{T} B x}{\partial x}=\left(B+B^{T}\right) x $$ |

下列公式是一些关于矩阵迹的公式。其中，$a$  是一个标量，$A$, $B$ , $C$ 分为三个矩阵。

| 编号 | 公式                                                         |
| :--- | :----------------------------------------------------------- |
| 1    | $\operatorname{tr}(a)=a$                                     |
| 2    | $\operatorname{tr}(A)=\operatorname{tr}\left(A^{T}\right)$   |
| 3    | $\operatorname{tr}(A B)=\operatorname{tr}(B A)$              |
| 4    | $\operatorname{tr}(A B C)=\operatorname{tr}(C A B)=\operatorname{tr}(B C A)$ |
| 5    | $\frac{\partial t r(A B)}{\partial A}=B^{T}$                 |
| 6    | $\frac{\partial t r\left(A B A^{T} C\right)}{\partial A}=C A B+C^{T} A B^{T}$ |

### 一些公式的证明

令：



#### 公式 1



因为 和 是列向量，所以 为一个标量，所以可以用法则 1 进行计算。



#### 公式 2

同理 公式 1

#### 公式 3



由题意可得， 为标量，则原式为标量对列向量求导，可以用法则 1 进行计算。



由导数法则有：



于是，原式继续有：





References:

https://soptq.me/2020/06/19/matrix-derivation/
