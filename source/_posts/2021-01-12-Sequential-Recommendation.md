---
title: 序列建模在推荐系统中的应用
date: 2021-01-12 15:16:08
tags:
categories:
top:
---

在推荐领域 根据用户的历史活动记录预测用户下一次行为可能会选择什么项目也是一个重要 的问题，现有的推荐系统主要关注于找出用户或项目的近邻集，或者利 用隐式或显式信息 (如标签、评论、物品内容、用户属性) 来提升近邻感知能力。 然而，却少有工作利用数据当中的时序属性来参与构建推荐系统。在本篇文章中， 我将介绍数据的序列中其实包含着许多有价值的且激动人心的信息以及现代大型推荐系统是如何使用这种序列特性来提升推荐的质量的。以视频网站 为例，一个用户看了纪录片《河西走廊》第一集《使者》之后，接下来看的另一个 节目很有可能会是《河西走廊》第二集《通道》。甚至早在 2011 年举办的 Recsys 推荐系统大会上，来自音乐应用 Pandora1的研究人员给出的演讲上都提到了许多 用户听音乐具有时序特点。 在某些特别的应用场景下，常规的推荐系统甚至无法起作用。现有的推荐系 统都需要分析用户的数据，因此每个网站和应用的使用到需要让用户完成注册以 及登录，然而用户每次使用网站或者应用的服务时都不一定会愿意登录，这种场 景下对匿名用户的推荐显然挑战更大，常规的推荐策略显然无法起作用，基于匿 名用户本地浏览器和缓存的会话所蕴含的序列进行推荐则显现出很重要的实践意 义与价值。

<!-- more -->

# 序列建模的必要性

理解用户是搜索排序中一个非常重要的问题，工业级的推荐系统一般需要大量的`泛化特征`来较好的表达用户。这些泛化特征可以分为两类：

- 偏`静态`的特征，例如用户的基本属性（年龄、性别、职业等等）特征、长期偏好（品类、价格等等）特征；
- `动态`变化的特征，例如刻画用户兴趣的实时行为序列特征。

用户的实时行为特征能够明显加强不同样本之间的区分度，所以在模型中优化用户行为序列建模是让模型更好理解用户的关键环节。

推荐系统中的用户兴趣`变化非常剧烈`，比如电商推荐中，用户一会看看服饰，一会看看电子产品，若只使用静态特征进行推荐，每次推荐的内容是一样的，这无疑是不能满足用户需求，实时性需要保障。

大致来讲，用户行为序列建模包含以下几种方式：

- `Pooling方法`：特点是将用户历史行为看做一个无序集合，方法有sum/max pooling等；
- `Word2Vec方法`：利用Word2Vec预训练行为序列；
- `RNN模型`：将用户行为看做一个具有时间属性的序列，方法有RNN、LSTN、GRU等；
- `CNN模型`：将这些交互的所有嵌入信息放入一个矩阵中，然后将这个矩阵作为时间和潜在空间中的“图像”来处理;
- `Attention模型`：属于Pooling方法的一种，优点在于灵活的捕捉全局和局部的联系；
- `GNN方法`：将每个交互作为图中的一个节点，同时将每个序列映射到一条路径。
- 强化学习的方法。

# 序列编码方案

## Pooling

这种方式的特点是将用户历史行为序列看做一个无序集合，序列集合通常通过 embedding 层得到序列向量后，pooling 层将序列向量聚合为定长的向量，一方面后继全连接层的输入需要固定长度的向量，另一方面通过 pooling 层我们可以获取到用户历史行为序列的全局信息。pooling 层通常采用的方式有 sum pooling 或者是 average pooling。sum pooling 将序列中每个元素的向量进行累加，average pooling 则是将 sum pooling 得到的向量进行平均。Pooling方式获取到序列特征Embedding向量通常是随机初始化的，参与后继网络的全局训练一起更新参数。

代表工作有Google那篇[《Deep Neural Networks for YouTube Recommendations》](https://link.zhihu.com/?target=https%3A//static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/45530.pdf)，这篇文章提出的Deepmatch和Deep ranking model结构中，将用户观看过的视频序列取到embedding后，做了一个mean pooling作为用户历史兴趣的表达。

![img](https://coladrill.github.io/img/post/20200601/1.png)

这种Pooling方案无法提取序列中隐含时序先后顺序关系，因为改变序列集合中元素的先后顺序其实对pooling结果并没有影响，而且这一假设基于所有行为内的 item 对用户的兴趣都是等价的，因而会引入一些噪声，通常用来作为序列建模中简单好用的一个baseline方案。

## Word2Vec

在word2vec诞生之后，embedding的思想迅速从NLP领域扩散到几乎所有机器学习的领域，语言其实是词汇按照一定的规律构成的序列，我们既然可以对一个序列中的词进行embedding，那自然可以对用户购买序列中的一个商品、用户观看序列中的一个电影进行embedding。而广告、推荐、搜索等领域用户数据的稀疏性几乎必然要求在构建DNN之前对user和item进行embedding后才能进行有效的训练。

Word2vec本质上是一个只有两层的浅度MLP，利用skip-grams或CBOW方案进行无监督学习，在此不再赘述其原理。word2vec将所有的词向量化，词与词之间就可以定量的去度量他们之间的关系，挖掘词之间的联系，将这一特性迁移到推荐算法领域，自然可以联想到通过衡量不同物品Embedding后的向量相似度来做召回了，这方面有代表性的工作有Airbnb的《Real-time Personalization using Embeddings for Search Ranking at Airbnb》和Yahoo的《E-commerce in Your Inbox: Product Recommendations at Scale》。word2vec还有一个很好的特性：其本身的层次分类器或者采样方式实际上对热门item做了很大的惩罚，所以不会像一半的矩阵分解一样，最后算出来语义接近的都是热门词。word2vec的一个非常成功的应用场景是应用在用户app下载序列上，根据用户下载App的顺序，把App看做单词，训练每个App对应的向量，用这个向量计算App之间的相似度，这样能把真正内容相关的App聚合在一起，同时规避热门App的影响，在商品点击序列上也有类似的效果。

用户对于某个物品的相关行为会encode很多与物品相关的属性进去，这些属性是很难用直接的方式去显性衡量的。就比如说，Airbnb中，"architecture，style and feel"这个属性你要怎么定义？而word2vec算法能够有效地抽取出这些隐藏的属性，可以进行比较、分类，因此推荐效果更好。这套方法在Yahoo的广告CTR预估中有9%的提升，在Airbnb的物品CTR预估中有21%的提升。

![word embeddings](https://cdn-images-1.medium.com/max/1250/1*sXNXYfAqfLUeiDXPCo130w.png)

既然用word2vec处理用户行为序列后得到的浅层网络参数就是Embedding矩阵，用户的行为序列特征已经参数化到了Embedding当中，因此另一种合理的做法是将Word2Vec当做序列特征提取器，因此预训练思想也便迁移到了推荐算法领域，利用Word2Vec无监督学习用户行为序列得到的预训练Embedding替换Pooling方案的Embedding作为NN的特征输入说不定可以得到更好的性能和效果。

## RNN

为提取用户的行为序列特征，最最直观的想法便是套用NLP领域常用的RNN/LSTM/GRU方法来进行建模。从2016年开始，学术界开始涌现大量利用RNN及其变体进行召回任务的研究，既有将点击序列Embedding化后直接输入GRU，用softmax/hierarchical softmax预测概率的next item prediction任务，即召回任务；也有利用RNN/LSTM/GRU提取序列特征，结合其他静态特征的混合分类模型，我将这类工作统称为Session-based Recommendation

可以参考的论文有GRU4REC，将seesion中点击item的行为看做一个序列，使用GRU进行刻画。

![img](https://mmbiz.qpic.cn/mmbiz_png/zHbzQPKIBPjd0Az5UM4zLvRrOjeW9USSGAUF2sg6icTcPpnxfFYudaj6yMjEBwc0Cia6tjCpAthos7uqLyHMuAHA/640?wx_fmt=png)

RNN由于梯度消失只有短期记忆，而LSTM网络通过精妙的门控制，一定程度上缓解了梯度消失的问题。GRU是LSTM的一种变体，也是为了解决梯度消失（即长期记忆问题）而提出来的。相较于LSTM，GRU的网络结构更加简单

但受限于RNN/LSTM/GRU之类结构本身的缺陷，其存在梯度消失、难以训练收敛，更为致命的是，这类循环结构无法并行训练，在动辄需要训练上亿样本量Serving又需要低时延的推荐系统工业场景，基本对这类网络结构判了死刑。说来惭愧，我研究生阶段在刚刚入门推荐算法领域时（17~18年时），也借用NLP领域的类循环网络结构提出了一个自己的推荐算法召回模型，与一些前人的工作不谋而合，现在回头来看，我的这份工作根本无法应用于工业领域，”滤水“之后更多的是锻炼我的学术能力，写到这里希望不会有好事者前去挖坟。。。

## CNN

RNN 结构用于序列建模的优点是结构简单，训练和预测的资源占用小，缺点是随着序列变长容易出现梯度消失的问题，同时 RNN 的训练不容易实现并行，CNN 结构通过矩阵运算的并行性容易实现模型训练的并行化，同时相对不容易出现序列变长后的梯度消失问题。因此我们希望能够像 RNN 一样在整个时间序列上通过 CNN 进行建模，这样便产生了 TCN ( TemporalCNN ) [17]。TCN 采用多层的一维卷积架构在序列长度的维度进行卷积，通过 zero padding 保证每一层的长度相同。TCN 架构结合了 casual convolution ( 因果卷积 )，residual connection ( 残差连接 ) 以及 dilated convolution ( 空洞卷积 )，其特点包括：

1. 采用因果卷积，保证训练过程中未来的信息不会泄露到过去时间的建模中；
2. 将任意长度的序列如同 RNN 那样映射为相同长度的输出序列。

首先我们看看什么是因果卷积，如下图所示，在事件序列中每个时间步 t 的状态输出仅与前一层的 t 时刻以及 t 时刻之前的状态进行卷积：

![img](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/causal-convolution.png)

图22 TCN causual convolution

在具体实现因果卷积时，我们可以采用在序列的开头进行补齐的方法保证输出序列的长度与输入序列保持一致，每层输入补齐的长度是：

![img](https://mdimg.wxwenku.com/getimg/6b990ce30fa9193e296dd37902816f4bfbb8d24231b6dd6d7ecfdf18313c7c0b1cde1cc82e10dab58c5cab1c00b60a3a.jpg)

TCN能够捕获局部序列特征，通过多层的因果卷积网络叠加，高层的感受野的大小与网络层数呈线性关系增加，做深TCN的网络结构，加大TCN的感受野，也能够捕获长距离特征，虽然CNN相比于RNN的递归串行结构具有天生自带的高并行计算能力，但在上亿样本量的推荐系统场景下CNN结构还不是最简洁的。

## Attention

我们回到历史，在NLP的发展过程中，专家学者们在做机器翻译时发现，在Seq2Seq结构中，Encoder把所有的输入序列都编码成一个统一的语义向量context，然后再由Decoder解码。其中，context自然也就成了限制模型性能的瓶颈，当要翻译的句子较长时，一个 context 可能存不下那么多信息。同时，只使用编码器的最后一个隐藏层状态，似乎不是很合理。因此，引入了Attention机制（**将有限的认知资源集中到最重要的地方**）。在生成 Target 序列的每个词时，用到的中间语义向量 context 是 Source 序列通过Encoder的隐藏层的加权和，而不是只用Encoder最后一个时刻的输出作为context，这样就能保证在解码不同词的时候，Source 序列对现在解码词的贡献是不一样的。

以上的 RNN 和 TCN 模型在建立序列模型时没有显式的去考虑各个时刻行为之间的相互关系，而各个时刻事件之间的相关性在预测任务中也是比较重要的信息，为了捕获序列中历史事件之间的相互关系，推荐系统的工程师们迅速从NLP领域偷师到了Attention进行序列建模的独特优势，于是用**scaled dot-product attention** 把过去序列向量的平均变成序列向量的加权求和便是首先可以进行的尝试，使得推荐出来的物品能够根据用户的历史行为动态变化，并且对于对抗序列当中的噪音也具有一定的鲁棒性，这种对attention的尝试首先取得了收益。

既然attention based Pooling方法可以替换简单的sum-pooling方法并有效，那么引入集成学习思想的multi head attention用来提取序列特征也应该有效，性能瓶颈问题能解决的话，将序列建模SOTA武器Transformer引入到推荐领域也就是顺水推舟的事情，于是用Transformer对长、短序列进行建模，学习用户的各种长期、短期兴趣，再拼接各种其它静态特征的“积木”，搭建各大召回、精排场景的“模型”。

- [DIN](https://arxiv.org/abs/1706.06978) 引入注意力机制，考虑行为序列中不同 item 对当前预测 item 有不同的影响；
- [DIEN](https://arxiv.org/abs/1809.03672) 将网络分为兴趣提取层和兴趣演化层，解决了 DIN 无法捕捉用户兴趣动态变化的缺点；
- [DSIN](https://arxiv.org/abs/1905.06482) 针对 DIN 和 DIEN 没有考虑用户历史行为中的 Session 信息，因为每个 Session 中的行为是相近的，而在不同 Session 之间的差别很大，它在 Session 层面上对用户的行为序列进行建模；
- [BST](https://arxiv.org/abs/1905.06874) 模型通过 Transformer 模型来捕捉用户历史行为序列中的各个 item 的关联特征，与此同时，加入待预测的 item 来达到抽取行为序列中的商品与待推荐商品之间的相关性。
- [MIMN](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1905.09248)建模超长行为序列，设计了UIC(User Interest Center)模块，将用户兴趣表达模块单独进行拆分而不是每次请求进行计算。

Transformer应用模型的主要构成：

- 所有特征（user 维度、item 维度、query 维度、上下文维度、交叉维度）经过底层 Embedding Layer 得到对应的 Embedding 表示；
- 建模用户行为序列得到用户的 Embedding 表示；
- 所有 Embedding concat 一起送入到三层的 MLP 网络。

![Transformer应用于精排](https://coladrill.github.io/img/post/20200601/5.png)

输入部分：

- 分为短期行为序列和长期行为序列。
- 行为序列内部的每个行为原始表示是由商户 ID，以及一些商户泛化信息的 Embedding 进行 concat 组成。
- 每段行为序列的长度固定，不足部分使用零向量进行补齐。

输出部分：

- 对 Transformer Layer 输出的向量做 Sum-pooling （这里尝试过Mean-pooling、concat，效果差不多）得到行为序列的最终 Embedding 表示。

在推荐系统的发展过程中，现代大型推荐系统都趋向于解耦合，各模块负责的工作越来越细致，排序阶段没有明确考虑项目之间的相互影响以及用户的偏好或意图的差异，因此引入重排序为用户展现的推荐列表达到整体最优为优化目标。既然重排序的输入是一个推荐列表，输出是一个优化后的推荐列表，那这不就是NLP中sequence2sequence干的事情吗？

NLP领域sequence2sequence 的state of the art工具是哪一个？推荐系统的工程师们迅速把眼光投向了Transformer。因为在上面我们已经尝试过了利用self-attention计算候选物品与用户历史交互物品之间的距离，那么也可以利用self-attention计算重排阶段不同候选物品之间的距离，self-attention正是Transformer构成的基石，再利用position embedding编码重排序输入列表的顺序，Transformer本身可以并行化计算的特点使得该模块不至于成为性能的瓶颈，于是Transformer便完美迁移到了重排序领域。

![Transformer应用于重排序](https://static001.infoq.cn/resource/image/9f/34/9f961fa552445de7335d378283a56a34.png)

## GNN

以上对序列的表达策略都是从微观的角度对每条序列分别处理，不同序列之间的item联系如果通过传统的“Sequence Embedding”其实是观察不出来的，但当我们从宏观角度来观察不同用户产生的不同序列时，其实是隐含了一定的关系的，例如，如果我们把超市中每个用户的购物单当做一个序列，会发现买啤酒的人往往也会买尿布，Apriori算法就是从全局宏观的角度来挖掘这种不同item之间的关联规则，但是Apriori算法性能不足以应用到大规模的推荐系统领域。既然从宏观角度看item之间隐藏着联系，那么把item连接起来不就是图这种最基本的数据结构了吗？

把用户的行为序列转换为item 的图结构，DeepWalk首先做出了GNN建模序列特征的尝试，这里引用阿里论文中的一张图，来展现DeepWalk的算法流程：

![DeepWalk的算法流程（引自阿里论文）](https://pic1.zhimg.com/80/v2-d6ae91afd26e314dec105142f84ee4f4_1440w.jpg)



1. 第一步：构建用户的行为序列
2. 第二步：我们基于这些行为序列构建了物品关系图，可以看出，物品A，B之间的边产生的原因就是因为用户U1先后购买了物品A和物品B，所以产生了一条由A到B的有向边。如果后续产生了多条相同的有向边，则有向边的权重被加强。在将所有用户行为序列都转换成物品相关图中的边之后，全局的物品相关图就建立起来了。
3. 第三步：采用随机游走的方式随机选择起始点，重新产生物品序列。
4. 第四步：最终将这些物品序列输入word2vec模型，生成最终的物品Embedding向量

既然已经将序列特征建模到了Graph Embedding向量当中，再利用这个Graph Embedding向量是去做召回还是精排那就是各位算法工程师发挥才智的时候了，

- DeepWalk：使用DFS随机游走在图中进行节点采样，使用Word2Vec在采样的序列上学习图中节点的向量表示；

- LINE（Large-scale Information Network Embedding）使用BFS（Breath First Search，广度优先搜索）构造邻域进行采样；

- node2vec：调整随机游走权重的方法使Graph Embedding的结果更倾向于体现网络的同质性（homophily）或结构性（structural equivalence）
- EGES（Enhanced Graph Embedding with Side Information）算法：Embedding过程中引入带权重的补充信息（Side Information），从而解决冷启动的问题
- SR-GNN：利用GNN进行序列建模做召回

## 强化学习

时序推荐是基于用户的顺序行为，对未来的行为进行预测的任务。目前的工作利用深度学习技术的优势，取得了很好的效果。但是这些工作仅专注于所推荐商品的局部收益，并未考虑该商品对于序列长期的影响。强化学习（RL）通过最大化长期回报为这一问题提供了一个可能的解决方案<sup>【16】</sup>。

这一节我们换个角度去看序列推荐问题。如果我们将用户的行为序列看做是一个顺序的决策过程，那么我们可以用马尔科夫决策过程 ( MDP ) 来表示用户的行为序列。马尔科夫决策过程包含以下几个方面：

1. **状态空间 S**：在t时刻用户的状态 *St* 定义为用户在 t 时间之前的历史行为，如用户在 t 之前点击过的 N 个物品。马尔科夫决策过程中每个状态具有马尔科夫性,因此序列中用户在各个时刻的状态可以只根据前一时刻的状态得到;
2. **动作空间 A**：动作定义为可以给用户推荐的候选物品空间。agent 的一次推荐相当于在候选物品空间内选择一个或者多个物品返回给用户;
3. **奖励 R**：agent 推荐物品给用户之后，根据用户对推荐列表的反馈 ( 忽略或者点击 ) 来得到 ( 状态-行为 ) 的即时奖励 reward；
4. **转移概率 P**：agent 为用户推荐了 K 个物品， 如果用户忽略了推荐的全部物品，那么下一个时刻的状态 $S_{t+1}$ 和当前的状态保持一致。如果用户点击了其中一个推荐的物品，那么下一个时刻的状态 $S_{t+1}$ 是在当前状态 $$S_t$$ 的基础上，加入该点击的推荐物品并且将原来的 N 个物品中点击时间最久远的那个物品去掉 ( 可以理解为一个先进先出的队列 );
5. **折扣因子 $\gamma$**：实际情况下我们希望最大化的是长期回报而不仅是即时奖励。因此t时刻的回报为从该时间起的一个总折扣奖励;
6. **策略**：有了状态和行为，我们会用策略 ( policy ) 来形式化的刻画用户的决策过程。策略描述了用户在某个时间点的状态 s 下对候选物品 a 产生行为的概率;
7. **值函数**：用值函数来刻画行为的回报。

这证明了将强化学习应用于时序推荐任务的可行性，通过将该任务定义为 MDP 过程，赋予了时序预测模型捕获推荐商品长期收益的能力。

# 总结

我们在做推荐系统时，面临不同业务场景，不同优化的阶段，常常面临不同的问题，了解了各类解决问题的策略才能不焦虑。以序列建模为了，为了快速搭建起方案，可以先以sum Pooling方法作为baseline，逐步尝试使用word2vec得到预训练的sequence embedding；为了提升对历史序列噪音的鲁棒性又不拖累性能以及时延，可以直接尝试基于attention的方案；而近来基于GNN和强化学习的方案证明了序列建模还有广阔的未知领域能够探索。


References:

1. [Transformer 在美团搜索排序中的实践](https://tech.meituan.com/2020/04/16/transformer-in-meituan.html)

2. [内容推荐算法：异构行为序列建模探索](https://my.oschina.net/u/4662964/blog/4652280)

3. [BERT在美团搜索核心排序的探索和实践](https://tech.meituan.com/2020/07/09/bert-in-meituan-search.html)

4. [专题-序列建模](https://github.com/zhanzecheng/Interview_Notes-Chinese/blob/master/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0-%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0-NLP/NLP-%E5%BA%8F%E5%88%97%E5%BB%BA%E6%A8%A1.md)

5. [谈谈推荐系统中的用户行为序列建模](https://zhuanlan.zhihu.com/p/138136777)

6. [Behavior Sequence Transformer for E-commerce Recommendation in Alibaba](https://arxiv.org/pdf/1905.06874v1.pdf)

7. [推荐算法序列建模现状](https://zhuanlan.zhihu.com/p/261382944)

8. [推荐中的序列化建模：Session-based neural recommendation](https://zhuanlan.zhihu.com/p/30720579)

10. [用户行为序列推荐模型@旺剑](https://mp.weixin.qq.com/s/nqCJOstJlZv6CrMST-tH8g)

11. [广告行业中那些趣事系列11：推荐系统领域必学的Graph Embedding](https://zhuanlan.zhihu.com/p/144891038)

12. [放弃幻想，全面拥抱Transformer：自然语言处理三大特征抽取器（CNN/RNN/TF）比较](https://zhuanlan.zhihu.com/p/54743941)

13. [《Real-time Personalization using Embeddings for Search Ranking at Airbnb》学习笔记](https://blog.csdn.net/like_red/article/details/88389918)

14. [Temporal Convolutional Network (TCN与TrellisNet)](https://fuhailin.github.io/Temporal-Convolutional-Network/)

16. [Personalized Re-ranking for Recommendation](https://arxiv.org/abs/1904.06813)

17. [Session-based Recommendation with Graph Neural Networks](https://arxiv.org/abs/1811.00855)

18. [让知识来指引你：序列推荐场景中以知识为导向的强化学习模型](https://mp.weixin.qq.com/s/NCkKvpTc4KbJUh-SVXzn1A)

