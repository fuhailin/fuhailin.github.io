---
title: Cross Entropy Loss Derivative
date: 2020-12-29 14:29:16
tags:
categories:
top:
---

## Logistic regression backpropagation with a single training example

In this part, you are using the Stochastic Gradient Optimizer to train your Logistic Regression. Consequently, the gradients leading to the parameter updates are computed on a single training example.

<!-- more -->

### a) Forward propagation equations

Before getting into the details of backpropagation, let’s spend a few minutes on the forward pass. For one training example $x=\left(x_{1}, x_{2}, \ldots, x_{n}\right)$ of dimension , the forward propagation is:
$$
\begin{array}{l}
z=w x+b \\
\hat{y}=a=\sigma(z) \\
L=-(y \log (\hat{y})+(1-y) \log (1-\hat{y}))
\end{array}
$$

### b) Dimensions of the variables in the forward propagation equations

It’s important to note the shapes of the quantities in the previous equations:

$x = (n,1)$, $w = (1,n)$, $b = (1,1)$, $z = (1,1)$, $a = (1,1)$, $L$ is a scalar.

### c) Backpropagation equations

Training our model means updating our weights and biases, W and b, using the gradient of the loss with respect to these parameters. At every step, we need to calculate :
$$
\frac{\partial L}{\partial w} \quad \frac{\partial L}{\partial b}
$$
To do this, we will apply the chain rule.
$$
\begin{aligned}
\frac{\partial L}{\partial w} &=\frac{\partial L}{\partial z} \frac{\partial z}{\partial w} \\
\frac{\partial L}{\partial b} &=\frac{\partial L}{\partial z} \frac{\partial z}{\partial b}
\end{aligned}
$$
So we need to calculate the following derivatives :
$$
\frac{\partial L}{\partial a} \quad \frac{\partial L}{\partial w}
$$
We will calculate those derivatives to get an expression of$\frac{\partial L}{\partial a}$ and $\frac{\partial L}{\partial w}$.
$$
\begin{aligned}
\frac{\partial L}{\partial a} &=-\left(y \frac{\partial \log (a)}{\partial a}+(1-y) \frac{\partial \log (1-a)}{\partial a}\right) \\
&=-\left(y \frac{1}{a}+(1-y) \frac{1}{1-a}(-1)\right) \\
&= \frac{a-y}{ a(1-a)} \\
\frac{\partial L}{\partial z}&=-\left(y \frac{1}{a} a(1-a)+(1-y) \frac{1}{a-1} a(1-a)\right) \\
&=-\left(y \frac{1}{a} a(1-a)+(1-y) \frac{1}{a-1} a(1-a)\right) \\
&=-y(1-a)+a(1-y) \\
&=a-y\\
\frac{\partial L}{\partial w} &= \frac{\partial L}{\partial z} \frac{\partial z}{\partial w}=(a-y) X^{T}
\end{aligned}
$$
Why did we choose $X^{T}$ rather than $X$ ? We can have a look at the following dimensions without forgetting that the dimensions of the derivative of a term are the same as the dimensions of the term.
$$
\begin{array}{llll}
\frac{\partial L}{\partial w} & \frac{\partial z}{\partial w} & a-y & X^{T} \\
(1, n) & (1, n) & (1,1) & (1, n)
\end{array}
$$

$$
\frac{\partial L}{\partial b}=\frac{\partial L}{\partial z} \frac{\partial z}{\partial b}=(a-y) \cdot 1
$$

Then :
$$
\begin{array}{l}
w=w-\alpha(a-y) X^{T} \\
b=b-\alpha(a-y) \cdot 1
\end{array}
$$

## Backpropagation for a batch of m training examples

In this part, you are using a Batch Gradient Optimization to train your Logistic Regression. Consequently, the gradients leading to the parameter updates are computed on the entire batch of m  training examples.

a) Write down the forward propagation equations leading to J .

b) Analyze the dimensions of all the variables in your forward propagation equations.

c) Write down the backpropagation equations to compute  .

### a) Forward propagation equations

Before getting into the details of backpropagation, let’s study the forward pass. For a batch of m  training examples, each of dimension n , the forward propagation is:
$$
\begin{array}{l}
z=w X+b \\
\hat{y}=a=\sigma(z) \\
L^{(i)}=-(y^{(i)} \log (\hat{y}^{(i)})+(1-y^{(i)}) \log (1-\hat{y}^{(i)})) \\
J=\sum_{i=1}^{m} L^{(i)}
\end{array}
$$

### b) Dimensions of the variables in the forward propagation equations

It’s important to note the shapes of the quantities in equations (1) and (2). w = ℜ , ,  , but is really of shape  and broadcasted to 1×n X = ℜ n×m b = ℜ 1×m 1 × 1 1 × m z = ℜ  and  and J is a scalar.

### c) Backpropagation equations

To train our model, we need to update our weights and biases $w$ and $b$, using the gradient of the loss with respect to these parameters. In other words, we need to calculate $\frac{\partial J}{\partial w}$ and $\frac{\partial J}{\partial b}$.

To do this, we will apply the chain rule.

We can write $\frac{\partial J}{\partial w}$ as $\frac{\partial J}{\partial a} \frac{\partial a}{\partial z} \frac{\partial z}{\partial w}$

The first step is to calculate $\frac{\partial J}{\partial a} \frac{\partial a}{\partial z}$.



## sigmoid_cross_entropy_with_logits

当Sigmoid和binary crossentry一起使用时，存在数学简化路径

假设Sigmoid函数的输入为 $x$，labels记为$y$，那么logloss经过Sigmoid和binary crossentry之后为：
$$
\begin{array}{rl}
& y* -\log (\operatorname{sigmoid}(x))+(1-y) *-\log (1-\operatorname{sigmoid}(x)) \\
=& y*-\log (\frac{1}{1+e^{-x}})+(1-y) *-\log (\frac{e^{-x}}{1+e^{-x}}) \\
=& y*-\log (\frac{1}{1+e^{-x}}) - \log (\frac{e^{-x}}{1+e^{-x}}) + y * \log (\frac{e^{-x}}{1+e^{-x}}) \\
=& -log(e^{-x})+ log(1+e^{-x})-y*log1+y*log(1+e^{-x})+y*log(e^{-x})-y*log(1+e^{-x}) \\
=& x + log(1+e^{-x}) - y*x
\end{array}
$$
For $x < 0$, to avoid overflow in $e^{-x}$, we reformulate the above
$$
\begin{array}{rl}
& x + log(1+e^{-x}) - y*x \\
=& log(e^{x}) - x*y + log(1+e^{-x}) \\
=& -x*y + log(1+e^{x})
\end{array}
$$
Hence, to ensure stability and avoid overflow, the implementation uses this equivalent formulation
$$
max(x, 0) - x*y + log(1+e^{-|x|})
$$
Reference from https://www.tensorflow.org/api_docs/python/tf/nn/sigmoid_cross_entropy_with_logits

## Backpropagation sigmoid_cross_entropy_with_logits
