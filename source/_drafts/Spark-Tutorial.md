---
title: Spark Tutorial
tags: Spark
categories: 大数据
top:
---
# Spark中的基本概念

### Spark Shell
Spark的shell提供了一个简单的API可供学习, 其也是一个用于分析数据的强有力交互工具。

### RDD(Resilient Distributed Dataset)
RDD（Resilient Distributed Dataset）叫做**弹性分布式数据集**，是Spark中最基本的数据结构。它是一个不可变的分布式对象集合。在RDD中的每一个数据集被划分进逻辑分区，不同的部分将在集群的不同节点上进行计算。RDD能够包含任意类型的对象，包括Python、Java、Scala甚至用户自定义类型。

# Spark中的组件
Spark组件使Apache Spark快速和可靠。为了解决使用Hadoop MapReduce时出现的问题，很多Spark组件被构建出来。 Apache Spark具有以下组件：
1. Spark Core
2. Spark Streaming
3. Spark SQL
4. GraphX
5. MLlib (Machine Learning)

### Spark Core
*Spark Core*是大规模并行计算和分布式数据处理的基本引擎。它负责：
1. 内存管理和故障恢复
2. 在群集上调度，分发和监视作业
3. 与存储系统交互

### Spark Streaming
*Spark Streaming* 是Spark用于处理实时流数据的组件。它支持实时数据流的高吞吐量和容错流处理。基本流单元是 *DStream* ，其基本上是一系列用于处理实时数据的RDD（弹性分布式数据集）。

### Spark SQL
*Spark SQL* 是Spark中的一个新模块，它将关系处理与Spark的函数式编程API集成在一起。 它支持通过SQL或Hive查询语言查询数据。以下是Spark SQL的四个库：
1. Data Source API
2. DataFrame API
3. Interpreter & Optimizer
4. SQL Service

### GraphX
*GraphX*是用于图形和图形并行计算的Spark API。 因此，它使用弹性分布式属性图(Resilient Distributed Property Graph)扩展了Spark RDD。

### MLlib
*MLlib* 代表机器学习库Machine Learning Library。Spark MLlib用于在Apache Spark中执行机器学习。

**References**:
1. [大数据之Spark入门教程(Python版)|厦门大学数据库](http://dblab.xmu.edu.cn/blog/1709-2/)
