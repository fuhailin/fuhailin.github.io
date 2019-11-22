---
title: Spark入门笔记—基本概念与环境配置
tags: Spark
categories: 大数据
description: Spark学习笔记
date: 2019-04-25 18:25:02
top:
---

# Spark中的基本概念
## Spark Shell
Spark的shell提供了一个简单的API可供学习, 其也是一个用于分析数据的强有力交互工具。

## RDD(Resilient Distributed Dataset)
RDD（Resilient Distributed Dataset）叫做**弹性分布式数据集**，是Spark中最基本的数据结构。它是一个不可变的分布式对象集合。在RDD中的每一个数据集被划分进逻辑分区，不同的部分将在集群的不同节点上进行计算。RDD能够包含任意类型的对象，包括Python、Java、Scala甚至用户自定义类型。
## Spark中的组件
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

# Spark的安装
Spark可以独立安装使用，也可以和Hadoop一起安装使用。这里我们采用和Hadoop一起安装使用，这样就可以让Spark使用HDFS存取数据。需要说明的是，当安装好Spark以后，里面就自带了Scala环境，不需要额外安装Scala.
## 安装Hadoop
https://fuhailin.github.io/Essential-Apps-for-Ubuntu/#Hadoop
## 安装Spark
由于我们已经自己安装了Hadoop，所以，在“Choose a package type”后面需要选择“Pre-build with user-provided Hadoop [can use with most Hadoop distributions]”，然后，点击“Download Spark”后面的“spark-2.4.2-bin-without-hadoop.tgz”下载即可。
Spark部署模式主要有四种：
 - Local模式（单机模式）
 - Standalone模式（使用Spark自带的简单集群管理器）
 - YARN模式（使用YARN作为集群管理器）
 - Mesos模式（使用Mesos作为集群管理器）

这里介绍Local模式（单机模式）的 Spark安装。我们选择Spark 2.4.2版本，并且假设当前使用用户名hadoop登录了Linux操作系统。
```sh
sudo tar -zxf spark-2.4.2-bin-without-hadoop.tgz -C /usr/local/
cd /usr/local
sudo mv ./spark-2.4.2-bin-without-hadoop/ ./spark
sudo chown -R hadoop:hadoop ./spark          # 此处的 hadoop 为你的用户名
```
安装后，还需要修改Spark的配置文件spark-env.sh
```sh
cd /usr/local/spark
cp ./conf/spark-env.sh.template ./conf/spark-env.sh
```
编辑spark-env.sh文件(vim ./conf/spark-env.sh)，在第一行添加以下配置信息:
```sh
export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
```
有了上面的配置信息以后，Spark就可以把数据存储到Hadoop分布式文件系统HDFS中，也可以从HDFS中读取数据。如果没有配置上面信息，Spark就只能读写本地数据，无法读写HDFS数据。然后通过如下命令，修改环境变量`vim ~/.bashrc`，在.bashrc文件中添加如下内容：
```bash
export JAVA_HOME=/usr/lib/jvm/default-java
export HADOOP_HOME=/usr/local/hadoop
export SPARK_HOME=/usr/local/spark
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
export PYSPARK_PYTHON=python3
export PATH=$HADOOP_HOME/bin:$SPARK_HOME/bin:$PATH
```
PYTHONPATH环境变量主要是为了在Python3中引入pyspark库，PYSPARK_PYTHON变量主要是设置pyspark运行的python版本。
.bashrc中必须包含`JAVA_HOME`,`HADOOP_HOME`,`SPARK_HOME`,`PYTHONPATH`,`PYSPARK_PYTHON`,`PATH`这些环境变量。如果已经设置了这些变量则不需要重新添加设置。
![SPARK_HOME环境变量](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-04-25-18-02-23.png)
接着还需要让该环境变量生效，执行`source ~/.bashrc`。
配置完成后就可以直接使用，不需要像Hadoop运行启动命令。
通过运行Spark自带的示例，验证Spark是否安装成功。
```sh
cd /usr/local/spark
bin/run-example SparkPi
```
执行时会输出非常多的运行信息，输出结果不容易找到，可以通过 grep 命令进行过滤（命令中的 2>&1 可以将所有的信息都输出到 stdout 中，否则由于输出日志的性质，还是会输出到屏幕中）:
```sh
bin/run-example SparkPi 2>&1 | grep "Pi is"
```
过滤后的运行结果如下图示，
![run-example SparkPi](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-04-25-18-01-05.png)

# Spark的使用(Python版PySpark)
学习Spark程序开发，建议首先通过pyspark交互式学习，加深Spark程序开发的理解。
PySpark提供了简单的方式来学习 API，并且提供了交互的方式来分析数据。你可以输入一条语句，PySpark会立即执行语句并返回结果，这就是我们所说的REPL（Read-Eval-Print Loop，交互式解释器），为我们提供了交互式执行环境，表达式计算完成就会输出结果，而不必等到整个程序运行完毕，因此可即时查看中间结果，并对程序进行修改，这样可以在很大程度上提升开发效率。

前面已经安装了Hadoop和Spark，如果Spark不使用HDFS和YARN，那么就不用启动Hadoop也可以正常使用Spark。如果在使用Spark的过程中需要用到 HDFS，就要首先启动 Hadoop（启动Hadoop的方法可以参考上面给出的[Hadoop安装教程](https://fuhailin.github.io/Hadoop-Install/)）。
这里假设不需要用到HDFS，因此，就没有启动Hadoop。现在我们直接开始使用Spark。

注意：如果按照上面的安装步骤，已经设置了PYSPARK_PYTHON环境变量，那么你直接使用如下命令启动pyspark即可。
`pyspark`
如果没有设置PYSPARK_PYTHON环境变量，则使用如下命令启动pyspark
```sh
PYSPARK_PYTHON=python3
pyspark
```
pyspark命令及其常用的参数如下：
```
pyspark --master <master-url>
```
Spark的运行模式取决于传递给SparkContext的Master URL的值。Master URL可以是以下任一种形式：
* local 使用一个Worker线程本地化运行SPARK(完全不并行)
* local[*] 使用逻辑CPU个数数量的线程来本地化运行Spark
* local[K] 使用K个Worker线程本地化运行Spark（理想情况下，K应该根据运行机器的CPU核数设定）
* spark://HOST:PORT 连接到指定的Spark standalone master。默认端口是7077.
* yarn-client 以客户端模式连接YARN集群。集群的位置可以在HADOOP_CONF_DIR 环境变量中找到。
* yarn-cluster 以集群模式连接YARN集群。集群的位置可以在HADOOP_CONF_DIR 环境变量中找到。
* mesos://HOST:PORT 连接到指定的Mesos集群。默认接口是5050。

需要强调的是，这里我们采用“本地模式”（local）运行Spark，关于如何在集群模式下运行Spark，可以参考后面的“在集群上运行Spark应用程序”。
在Spark中采用本地模式启动pyspark的命令主要包含以下参数：
–master：这个参数表示当前的pyspark要连接到哪个master，如果是local[*]，就是使用本地模式启动pyspark，其中，中括号内的星号表示需要使用几个CPU核心(core)；
–jars： 这个参数用于把相关的JAR包添加到CLASSPATH中；如果有多个jar包，可以使用逗号分隔符连接它们；

比如，要采用本地模式，在4个CPU核心上运行pyspark：
```
pyspark --master local[4]
```
或者，可以在CLASSPATH中添加code.jar，命令如下：
```
pyspark --master local[4] --jars code.jar
```
可以执行“pyspark –help”命令，获取完整的选项列表，具体如下：
```
pyspark --help
```
上面是命令使用方法介绍，下面正式使用命令进入pyspark环境，可以通过下面命令启动pyspark环境：
```sh
pyspark
```
该命令省略了参数，这时，系统默认是“bin/pyspark–master local[*]”，也就是说，是采用本地模式运行，并且使用本地所有的CPU核心。

启动pyspark后，就会进入“>>>”命令提示符状态,如下图所示：
![](2019-04-25-21-27-07.png)

# Spark独立应用程序编程
```py
from pyspark import SparkContext
sc = SparkContext( 'local', 'test')
logFile = "file:///usr/local/spark/README.md"
logData = sc.textFile(logFile, 2).cache()
numAs = logData.filter(lambda line: 'a' in line).count()
numBs = logData.filter(lambda line: 'b' in line).count()
print('Lines with a: %s, Lines with b: %s' % (numAs, numBs))
```

一些学习资料：
[Spark性能优化指南——基础篇](https://tech.meituan.com/2016/04/29/spark-tuning-basic.html)
[PySpark_SQL_Cheat_Sheet_Python.pdf](PySpark_SQL_Cheat_Sheet_Python.pdf)

**References**:
1. [大数据之Spark入门教程(Python版)|厦门大学数据库](http://dblab.xmu.edu.cn/blog/1709-2/)
