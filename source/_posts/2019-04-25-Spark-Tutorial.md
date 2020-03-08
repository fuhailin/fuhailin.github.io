---
title: Spark入门笔记—基本概念与单机环境配置
tags: Spark
categories: 大数据
description: Spark学习笔记
date: 2019-04-25 18:25:02
top:
---

本文通过收集Spark中的基本概念、在Mac上配置伪分布式环境并分别用Python、Scala、Java三种语言独立编程实现了分布式版的WordCount程序以进行测试学习，来熟悉Spark的常用操作。

<!-- more -->

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

本教程的具体运行环境如下：

- Hadoop 3.1.3
- Java JDK 1.8
- Spark 2.4.5

## 安装JDK与Hadoop
https://fuhailin.github.io/Hadoop-on-MacOS/
## 安装Spark
由于已经安装了Hadoop，所以，在“Choose a package type”后面需要选择“Pre-build with user-provided Hadoop [can use with most Hadoop distributions]”，然后，点击“Download Spark”后面的“spark-2.4.5-bin-without-hadoop.tgz”下载即可。
Spark部署模式主要有四种：

 - Local模式（单机模式）
 - Standalone模式（使用Spark自带的简单集群管理器）
 - YARN模式（使用YARN作为集群管理器）
 - Mesos模式（使用Mesos作为集群管理器）

这里介绍Local模式（单机模式）的 Spark安装。我们选择Spark 2.4.5 版本，并且假设当前使用用户名hadoop登录了Linux操作系统(MacOS可忽略这一步操作)。
```sh
sudo tar -zxf spark-2.4.2-bin-without-hadoop.tgz -C /usr/local/
cd /usr/local
sudo mv ./spark-2.4.2-bin-without-hadoop/ ./spark
sudo chown -R hadoop:hadoop ./spark          # 此处的 hadoop 为你的用户名，MacOS可忽略
```
安装后，还需要修改Spark的配置文件spark-env.sh
```sh
cd /usr/local/spark
cp ./conf/spark-env.sh.template ./conf/spark-env.sh
```
编辑spark-env.sh文件(vim ./conf/spark-env.sh)，添加你的Hadoop配置信息:
```sh
export SPARK_DIST_CLASSPATH=$(/usr/local/hadoop/bin/hadoop classpath)
```
有了上面的配置信息以后，Spark就可以把数据存储到Hadoop分布式文件系统HDFS中，也可以从HDFS中读取数据。如果没有配置上面信息，Spark就只能读写本地数据，无法读写HDFS数据。然后通过如下命令，修改环境变量`vim ~/.bashrc`，在.bashrc文件中添加如下内容：
```bash
# SPARK CONFIG
export SPARK_HOME=/Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12
export PATH=$PATH:$SPARK_HOME/bin

export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH
export PYSPARK_PYTHON=python3
export PATH=$HADOOP_HOME/bin:$SPARK_HOME/bin:$PATH
```
PYTHONPATH环境变量主要是为了在Python3中引入pyspark库，PYSPARK_PYTHON变量主要是设置pyspark运行的python版本。
.bashrc中必须包含`JAVA_HOME`,`HADOOP_HOME`,`SPARK_HOME`,`PYTHONPATH`,`PYSPARK_PYTHON`,`PATH`这些环境变量。如果已经设置了这些变量则不需要重新添加设置。
![SPARK_HOME环境变量](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-08-at-11.01.45-PM.png)
接着还需要让该环境变量生效，执行`source ~/.bashrc`。
配置完成后就可以直接使用，不需要像Hadoop运行启动命令。
通过运行Spark自带的示例，验证Spark是否安装成功。

```sh
run-example SparkPi
```
执行时会输出非常多的运行信息，输出结果不容易找到，可以通过 grep 命令进行过滤（命令中的 2>&1 可以将所有的信息都输出到 stdout 中，否则由于输出日志的性质，还是会输出到屏幕中）:
```sh
run-example SparkPi 2>&1 | grep "Pi is"
```
过滤后的运行结果如下图示，
![run-example SparkPi](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-04-25-18-01-05.png)

## 使用 Spark Shell 编写代码

**启动Spark Shell**：spark-shell，启动spark-shell后，会自动创建名为sc的SparkContext对象和名为spark的SparkSession对象,如图：

![Screen-Shot-2020-03-08-at-10.24.52-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-08-at-10.24.52-PM.png)

### 加载text文件

spark创建sc，可以加载本地文件和HDFS文件创建RDD。这里用Spark自带的本地文件README.md文件测试。

```scala
val textFile = sc.textFile("file:///Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12/README.md")
```

加载HDFS文件和本地文件都是使用textFile，区别是添加前缀(`hdfs://`和`file:///`)进行标识。

# PySpark独立应用程序编程

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
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-04-25-21-27-07.png)

创建 Python 脚本 `my_script.py`：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyspark import SparkContext


if __name__ == "__main__":
    sc = SparkContext( 'local', 'test')
    logFile = "file:///Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12/README.md"
    logData = sc.textFile(logFile, 2).cache()
    numAs = logData.filter(lambda line: 'a' in line).count()
    numBs = logData.filter(lambda line: 'b' in line).count()
    print('Lines with a: %s, Lines with b: %s' % (numAs, numBs))
```

#### 通过 spark-submit 运行程序

我们也可以直接将Python脚本通过 spark-submit 提交到 Spark 中运行了，命令如下：

```sh
spark-submit --class "SimpleApp" SimpleApp.py
```



### Scala on Spark独立应用编程

#### 1. 安装sbt

sbt是一款Spark用来对scala编写程序进行打包的工具，Spark 中没有自带 sbt，我通过到https://www.scala-sbt.org/download.html选择[sbt-1.3.8.zip](https://piccolo.link/sbt-1.3.8.zip)进行下载配置，将下载到的sbt-1.3.8.zip解压到某个目录并添加到环境变量当中：

```sh
# SBT
export SBT_HOME=/Users/vincent/opt/sbt
export PATH=$PATH:$SBT_HOME/bin
```

如果在国内网络环境，sbt的网络依赖可能会存在下载阻碍，可以单独配置更换国内源，通过新增`~/.sbt/repositories`文件，添加如下内容后执行`sbt --version`查看是否正常：

```
[repositories]
local
aliyun: http://maven.aliyun.com/nexus/content/groups/public/
typesafe: http://repo.typesafe.com/typesafe/ivy-releases/, [organization]/[module]/(scala_[scalaVersion]/)(sbt_[sbtVersion]/)[revision]/[type]s/[artifact](-[classifier]).[ext], bootOnly
sonatype-oss-releases
maven-central
sonatype-oss-snapshots
```
> (base) ➜  ~ sbt --version
> sbt version in this project: 1.3.8
> sbt script version: 1.3.8

#### 2. Scala编码
Scala是一种与Java兼容的、面向对象的、函数式的编程语言。Spark更是在Scala中实现的，因此Spark中已经包含了Scala的编译器，可以选择不单独配置Scala环境。 在目录`sparksrc/scalasrc/`新建一个`SimpleApp.scala`文件，添加如下内容：

```scala
/* SimpleApp.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
 
object SimpleApp {
    def main(args: Array[String]) {
        val logFile = "file:///Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12/README.md" // Should be some file on your system
        val conf = new SparkConf().setAppName("Simple Application")
        val sc = new SparkContext(conf)
        val logData = sc.textFile(logFile, 2).cache()
        val numAs = logData.filter(line => line.contains("a")).count()
        val numBs = logData.filter(line => line.contains("b")).count()
        println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
    }
}
```

同时新建一个sbt工程文件`build.sbt`  ：

```
name := "Simple Project"
version := "1.0"
scalaVersion := "2.11.12"
libraryDependencies += "org.apache.spark" %% "spark-core" % "2.4.0"
```

#### 3. 使用 sbt 打包 Scala 程序

进入`sparksrc/scalasrc/`目录，执行`sbt package`命令将整个应用程序打包成 JAR，如果首次运行会下载对应的依赖包，生成的 jar 包的位于生成的target目录中。

#### 4. 通过 spark-submit 运行程序

最后，我们就可以将生成的 jar 包通过 spark-submit 提交到 Spark 中运行了，命令如下：

```bash

spark-submit --class "SimpleApp" ./target/scala-2.11/simple-project_2.11-1.0.jar
# 上面命令执行后会输出太多信息，可以不使用上面命令，而使用下面命令查看想要的结果
spark-submit --class "SimpleApp" ./target/scala-2.11/simple-project_2.11-1.0.jar 2>&1 | grep "Lines with a:"
```

最终得到的结果如下：

```
Lines with a: 61, Lines with b: 30
```

自此，就完成了我的第一个 Spark Scala应用程序了。

### Java on Spark独立应用编程

#### 1. 安装maven

Maven 是一个项目管理工具，可以对 Java 项目进行构建、依赖管理。Spark 中没有自带 Maven，我通过到http://maven.apache.org/download.cgi选择[ apache-maven-3.6.3-bin.zip](http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.zip)进行下载配置，将下载到的apache-maven-3.6.3-bin.zip解压到某个目录并添加到环境变量当中：

```sh
# MAVEN
export MAVEN_HOME=/Users/vincent/opt/maven/apache-maven-3.6.3
export PATH=$PATH:$MAVEN_HOME/bin
```

同样可以为Maven配置更换国内源加速依赖文件下载，通过新增`~/.m2/setting.xml文件`，添加如下内容后执行`mvn --version`查看是否正常：

```xml
<mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
</mirror>
```

> (base) ➜  ~ mvn --version
> Apache Maven 3.6.3 (cecedd343002696d0abb50b32b541b8a6ba2883f)
> Maven home: /Users/vincent/opt/maven/apache-maven-3.6.3
> Java version: 1.8.0_242, vendor: AdoptOpenJDK, runtime: /Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home/jre
> Default locale: en_CN, platform encoding: UTF-8
> OS name: "mac os x", version: "10.15.3", arch: "x86_64", family: "mac"

2. Java编码

在 ~/sparksrc/javasrc 下建立一个名为 SimpleApp.java 的文件（vim ~/sparksrc/javasrc/SimpleApp.java），添加代码如下：

```java
/* SimpleApp.java */
import org.apache.spark.api.java.function.FilterFunction;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.Dataset;

public class SimpleApp {
    public static void main(String[] args) {
        String logFile = "file:///Users/vincent/opt/spark/spark-2.4.5-bin-without-hadoop-scala-2.12/README.md"; // Should be some file on your system
        SparkSession spark = SparkSession.builder().appName("Simple Application").getOrCreate();
        Dataset<String> logData = spark.read().textFile(logFile).cache();

        long numAs = logData.filter((FilterFunction<String>) s -> s.contains("a")).count();
        long numBs = logData.filter((FilterFunction<String>) s -> s.contains("b")).count();

        System.out.println("Lines with a: " + numAs + ", lines with b: " + numBs);

        spark.stop();
    }
}

```

同时新建一个Maven工程文件`pom.xml`：

```xml
<project>
    <groupId>fuhailin.github.io</groupId>
    <artifactId>simple-project</artifactId>
    <modelVersion>4.0.0</modelVersion>
    <name>Simple Project</name>
    <packaging>jar</packaging>
    <version>1.0</version>
    <repositories>
        <repository>
            <id>jboss</id>
            <name>JBoss Repository</name>
            <url>http://repository.jboss.com/maven2/</url>
        </repository>
    </repositories>
    <dependencies>
        <dependency> <!-- Spark dependency -->
            <groupId>org.apache.spark</groupId>
            <artifactId>spark-core_2.11</artifactId>
            <version>2.4.5</version>
        </dependency>
    </dependencies>
</project> 
```

#### 3. 使用 maven 打包 Java 程序

进入`sparksrc/javasrc/`目录，执行`mvn package`命令将整个应用程序打包成 JAR，如果首次运行同样会下载对应的maven依赖包，生成的 jar 包的位于生成的target目录中。

![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-08-at-10.00.24-PM.png)


#### 4. 通过 spark-submit 运行程序

最后，可以通过将生成的jar包通过spark-submit提交到Spark中运行，如下命令：

```sh
spark-submit --class "SimpleApp" ./target/simple-project-1.0.jar
# 上面命令执行后会输出太多信息，可以不使用上面命令，而使用下面命令查看想要的结果
spark-submit --class "SimpleApp" ./target/simple-project-1.0.jar 2>&1 | grep "Lines with a"
```

这样我们就完成了Spark伪分布式环境的配置以及Spark中支持的三种编程语言的独立程序测试。

关注我的公众号"赵大寳Note"（ID：StateOfTheArt），回复“**HelloSpark**”下载本文中的Python、Scala、Java全部实例工程。
![关注公众号赵大寳Note，回复“HelloSpark”下载本文全部代码](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9naXRlZS5jb20vZnVoYWlsaW4vT2JqZWN0LVN0b3JhZ2UtU2VydmljZS9yYXcvbWFzdGVyL3dlY2hhdF9jaGFubmVsLnBuZw?x-oss-process=image/format,png)

一些学习资料：
[Spark性能优化指南——基础篇](https://tech.meituan.com/2016/04/29/spark-tuning-basic.html)
[PySpark_SQL_Cheat_Sheet_Python.pdf](PySpark_SQL_Cheat_Sheet_Python.pdf)

**References**:
1. [大数据之Spark入门教程(Python版)|厦门大学数据库](http://dblab.xmu.edu.cn/blog/1709-2/)
2. https://spark.apache.org/examples.html#
3. https://spark.apache.org/docs/latest/quick-start.html
4. [Apache Spark Example: Word Count Program in Java](https://www.journaldev.com/20342/apache-spark-example-word-count-program-java)
5. https://docs.scala-lang.org/getting-started/
6. [How to integrate Apache Spark, Intellij Idea and Scala](http://blog.miz.space/tutorial/2016/08/30/how-to-integrate-spark-intellij-idea-and-scala-install-setup-ubuntu-windows-mac/)
7. https://www.runoob.com/scala/scala-intro.html

