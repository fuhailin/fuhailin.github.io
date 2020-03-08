---
title: 配置HBase伪分布式娱乐环境
date: 2020-03-03 15:35:19
tags: [HBase,Hadoop,HDFS]
categories: 大数据
top:
---

HBase是运行在Hadoop分布式文件系统HDFS上进行数据存储的开源非关系型分布式数据库，2020年我尝试在Mac上配置一个伪分布式的v2.2.3 HBase环境，看看能不能进行一些基本的读写操作，以便熟悉一下分布式数据库有什么特点。

<!-- more -->

# 三种运行模式

**单机模式**

1. Hbase不使用HDFS,仅使用本地文件系统

2. ZooKeeper与Hbase运行在同一个JVM中


**伪分布式模式**

1. 所有进程运行在同一个节点上,不同进程运行在不同的JVM当中
2. 比较适合实验测试

**完全分布式模式**

1. 进程运行在多个服务器集群中
2. 分布式依赖于HDFS系统，因此布署Hbase之前一定要有一个正常工作的HDFS集群

那么HBase伪分布式环境部署要分几步呢？我们现在梳理一下。

1. JDK 1.8
2. [Hadoop环境](https://fuhailin.github.io/Hadoop-Install/)
3. HBase环境


截止目前(2020年03月03日)我使用最新的stable HBase版本2.2.3进行配置。

# JDK 1.8

HBase是使用Java开发的，因此配置需要JDK环境，目前长期稳定版LTS只支持到JDK 8(LTS JDK支持进度可到 https://hbase.apache.org/book.html#java 查看)

![Screen-Shot-2020-03-03-at-5.39.03-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-03-at-5.39.03-PM.png)

可以翻阅我之前的博客查看在Ubuntu和MacOS上安装JDK 8的过程，这里不再细述。

# Hadoop

在MacOS上配置伪分布式环境的详细办法可以查看我的上一篇博文👉🏻https://fuhailin.github.io/Hadoop-on-MacOS/ 。HBase是运行在HDFS之上的分布式数据库，所以在启动HBase之前必须先启动HDFS，运行`$HADOOP_HOME//sbin/start-dfs.sh`启动HDFS。

# HBase


## Zookeeper
顾名思义 Zookeeper 就是动物园管理员，它是用来管 Hadoop（大象）、Hive(蜜蜂)、Pig(小猪)的管理员， Apache Hbase 和 Apache Solr 的分布式集群都用到了 Zookeeper；Zookeeper是一个分布式的、开源的程序协调服务，是 Hadoop 项目下的一个子项目，它提供的主要功能包括：配置维护、域名服务、分布式同步、集群管理。

> ```
> 注：如果为了简单的话，可以选择不安装Zookeeper集群，就跟Spark默认提供自己的Scala一样，HBase默认配置自己提供的Zookeeper支持。
> ```

## HBase安装

很多资料提到可以使用Hombrew直接通过'brew install hbase'进行HBase的下载配置，但是由于之前Hadoop的安装过程中Homebrew总是下载最新的JDK依赖这让我无法掌控是否兼容，于是我就直接在官网(https://hbase.apache.org/downloads.html)下载编译好的二进制版HBase进行配置。将下载好的hbase-2.2.3-bin.tar.gz解压到程序存放目录，然后将得到的`bin`路径添加到环境变量里，我是这样做的，`vim ~/.bash_profile`，添加：

```sh
# HBASE
export HBASE_HOME=/Users/vincent/opt/hbase/hbase-2.2.3
export PATH=$PATH:$HBASE_HOME/bin
```

## 伪分布式配置

1. 将`JAVA_HOME`的路径添加到hbase-env.sh文件，修改`vim $HBASE_HOME/conf/hbase-env.sh`:

```sh
# The java implementation to use.  Java 1.8+ required.
export JAVA_HOME=/Library/Java/JavaVirtualMachines/adoptopenjdk-8.jdk/Contents/Home
```

2. 在hbase-site.xml中添加如下内容：
```xml
<configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.unsafe.stream.capability.enforce</name>
        <value>false</value>
    </property>
</configuration>
```

hbase.rootdir：该参数制定了HReion服务器的位置，即数据存放的位置。主要端口号要和Hadoop相应配置一致。
hbase.cluster.distributed：HBase的运行模式。false是单机模式，true是分布式模式。若为false, HBase和Zookeeper会运行在同一个JVM里面，默认为false。

## 启动HBase

如果完成了以上步骤，通过`source ~/.bash_profile`操作使修改的环境变量生效并启动了Hadoop(`$HADOOP_HOME/bin/start-dfs.sh`)，就可以通过`$HBASE_HOME/bin/start-hbase.sh`脚本来启动HBase了，启动完成后通过`jps`命令检查HBase进程：

![Screen-Shot-2020-03-03-at-7.32.34-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-03-at-7.32.34-PM.png)

启动成功后可以看到几个正在运行的Java进程，包括Hadoop(DataNode、NameNode)、Zookeeper(HQuorumPeer)和HBase(HMaster、HRegionServer)。

通过`hbase version`命令查看HBase是否正常运行打印版本信息：

![1583235497008](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/1583235497008.jpg)

成功启动后，可以访问 HBase的Web 界面 [http://localhost:16020](http://localhost:16020/) 查看集群的运行状态信息。

![Screen-Shot-2020-03-04-at-2.21.55-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-04-at-2.21.55-PM.png)


进入HBase交互式界面`hbase shell`，`status`命令查看HBase集群运行状态，`list`命令列出HBase库中的表：

![Screen-Shot-2020-03-04-at-11.13.50-AM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-04-at-11.13.50-AM.png)

> 【注意】：我几次在尝试hbase shell交互式编程时遇到`ERROR: KeeperErrorCode = NoNode for /hbase/master`的错误信息，通过查看`$HBASE_HOME/logs/`中日志可以查看详细异常信息，怀疑是HBase自带的Zookeeper存在管理问题，重启HBase后又没有问题，但还没有找出错误的规律，可以尝试单独下载配置Zookeeper程序，有线索的朋友欢迎留言

这里启动关闭Hadoop和HBase的顺序一定是：
启动Hadoop—>启动HBase—>关闭HBase—>关闭Hadoop

# HBase Shell 编程实践

#### 1.1 HBase建表

HBase中用create命令创建表，具体如下：

```bash
  create 'student','Sname','Ssex','Sage','Sdept','course'
```

![Screen-Shot-2020-03-04-at-12.16.47-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-04-at-12.16.47-PM.png)

#### 1.2 HBase增删查改

**添加数据**
HBase中用put命令添加数据，注意：一次只能为一个表的一行数据的一个列，也就是一个单元格添加一个数据，所以直接用shell命令插入数据效率很低，在实际应用中，一般都是利用编程操作数据。

```sh
# 为student表添加了学号为95001，名字为LiYing的一行数据，其行键为95001
put 'student','95001','Sname','LiYing'
# 为95001行下的course列族的math列添加了一个数据
put 'student','95001','course:math','80'
```



**删除数据**
在HBase中用delete以及deleteall命令进行删除数据操作，它们的区别是：1. delete用于删除一个数据，是put的反向操作；2. deleteall操作用于删除一行数据。

```sh
# 删除一个数据，是put的反向操作
delete 'student','95001','Ssex'
# 删除student表中的95001行的全部数据
deleteall 'student','95001'
```

**查看数据**
HBase中有两个用于查看数据的命令：1. get命令，用于查看表的某一行数据；2. scan命令用于查看某个表的全部数据

```sh
# 查看‘student’表‘95001’行的数据
get 'student','95001'
# 查看‘student’表的全部数据
scan 'student'
```

![Screen-Shot-2020-03-04-at-7.59.26-PM](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/hadoop/Screen-Shot-2020-03-04-at-7.59.26-PM.png)

**删除表**
删除表有两步，第一步先让该表不可用，第二步删除表。

```sh
#先禁用表
disable 'student'
#删除表
drop 'student'
```

至此我们已经完成了HBase的伪分布式配置与基本的增删查改操作，那它能替换我们的MySQL和Oracle吗？

## HBase与传统关系数据库对比分析：

HBase与传统的关系数据库的区别主要体现在以下几个方面：

1. 数据类型：关系数据库采用关系模型，具有丰富的数据类型和存储方式，HBase则采用了更加简单的数据模型，它把数据存储为未经解释的字符串。
2. 数据操作：关系数据库中包含了丰富的操作，其中会涉及复杂的多表连接。HBase操作则不存在复杂的表与表之间的关系，只有简单的插入、查询、删除、清空等，因为HBase在设计上就避免了复杂的表和表之间的关系。
3. 存储模式：关系数据库是基于行模式存储的。HBase是基于列存储的，每个列族都由几个文件保存，不同列族的文件是分离的。
4. 数据索引：关系数据库通常可以针对不同列构建复杂的多个索引，以提高数据访问性能。HBase只有一个索引——行键，通过巧妙的设计，HBase中的所有访问方法，或者通过行键访问，或者通过行键扫描，从而使得整个系统不会慢下来。
5. 数据维护：在关系数据库中，更新操作会用最新的当前值去替换记录中原来的旧值，旧值被覆盖后就不会存在。而在HBase中执行更新操作时，并不会删除数据旧的版本，而是生成一个新的版本，旧有的版本仍然保留。
6. 可伸缩性：关系数据库很难实现横向扩展，纵向扩展的空间也比较有限。相反，HBase和BigTable这些分布式数据库就是为了实现灵活的水平扩展而开发的，能够轻易地通过在集群中增加或者减少硬件数量来实现性能的伸缩

# HBase的适用业务场景

1. **写密集型应用**：每天写入量巨大，而相对读数量较小的应用，比如IM的历史消息、游戏的日志等等
2. **不需要复杂查询条件来查询数据的应用**：HBase只支持基于rowkey的查询，对于HBase来说，单条记录或者小范围的查询是可以接受的，大范围的查询由于分布式的原因，可能在性能上有点影响，而对于像SQL的join等查询，HBase无法支持。
3. **对性能和可靠性要求非常高的应用**：由于HBase本身没有单点故障，可用性非常高。
4. **海量数据，而且增长量无法预估的应用**：HBase支持在线扩展，即使在一段时间内数据量呈井喷式增长，也可以通过HBase横向扩展来满足功能。


**References**:

1. [Hbase的伪分布式安装|SlowTech](https://www.cnblogs.com/ivictor/p/5906433.html)

2. [HBase2.2.2安装和编程实践指南|林子雨](http://dblab.xmu.edu.cn/blog/2442-2/)

3. [HBase技术原理|曹世宏](https://cshihong.github.io/2018/05/17/HBase%E6%8A%80%E6%9C%AF%E5%8E%9F%E7%90%86/)

4. [Apache HBase ™ Reference Guide](https://hbase.apache.org/book.html)