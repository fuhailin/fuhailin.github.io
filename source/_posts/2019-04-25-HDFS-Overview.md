---
title: HDFS学习笔记
tags:
  - HDFS
  - Hadoop
categories: 大数据
date: 2019-04-25 16:52:13
top:
---

**Hadoop Distributed File System**——HDFS，是世界上最可靠的存储系统。 HDFS是Hadoop的文件系统，是Hadoop不可缺少的一部分，其为2003年Google发表的Google文件系统GFS的克隆版。
{% asset_img https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Hadoop-Architecture.jpg HDFS in Hadoop %}
Hadoop文件系统使用分布式文件系统设计开发，设计原则是存储较少数量的大文件而不是大量的小文件。用于存储在硬件集群上运行的非常大的文件。不像其他的分布式系统，HDFS是高度容错以及使用低成本的硬件设计。
<!-- more -->

## HDFS的特点
 - 分布式存储和处理超大型的数据量。
 - 单个文件冗余式存储避免单节点失效可能造成的数据损失
 - Hadoop提供的命令接口与HDFS进行交互。
 - 名称节点和数据节点的帮助用户内置的服务器能够轻松地检查集群的状态。
 - 流式访问文件系统数据。
 - HDFS提供了文件的权限和验证。
 - 不依赖硬件，能够运行在普通廉价的机器上


## HDFS架构
下面给出是Hadoop的文件系统的体系结构。
  ![HDFS架构](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/HDFS-Architecture.jpg)
HDFS遵循主/从式架构，它具有以下元素。

### 命名节点 - Namenode
一个HDFS集群会有一个NameNode（简称NN）命名节点，该节点作为主服务器存在（master server），它执行以下任务：
 - 管理文件系统命名空间
 - 调节客户端对文件的访问。
 - 它也执行文件系统操作，如重命名，关闭和打开的文件和目录。

### 数据节点 - Datanode
一个HDFS集群还会有多个DataNode（简称DN）数据节点，数据节点作为从节点存在（slave server），它执行以下任务：
 - Datanode根据客户的请求在文件系统上执行读写操作。
 - 根据Namenode的指令执行操作，如块的创建，删除和复制。

### 数据块
往HDFS中写入的任何文件，都会分成称为**块**的小块数据。 HDFS的默认块大小为128 MB，可根据要求增加，即便一个数据块大小为130M，也会被拆分为2个Block，一个大小为128M，一个大小为2M。 这些块以分布式方式存储在集群中的不同节点上。这为MapReduce提供了一种在集群中并行处理数据的机制。默认情况下，每个数据块都会有三个副本，每个副本都会被存放在不同的机器上，而且每一个副本都有自己唯一的编号。这就提供了容错、可靠性和高可用性。如下图：
![HDFS副本机制](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/7e142940a0feb4c119be2d8df7fad13c.png)

[Hadoop HDFS Command Cheatsheet.pdf](http://images.linoxide.com/hadoop-hdfs-commands-cheatsheet.pdf)

**References**:
1. [HDFS Tutorial – A Complete Hadoop HDFS Overview](https://data-flair.training/blogs/hadoop-hdfs-tutorial/)
2. [HDFS伪分布式环境搭建](https://blog.51cto.com/zero01/2090716)
3. [Java操作HDFS开发环境搭建以及HDFS的读写流程](https://blog.51cto.com/zero01/2090901)
4. [HDFS Architecture官方文档](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
5. [Hadoop HDFS操作](https://www.yiibai.com/hadoop/hadoop_hdfs_operations.html#article-start)
