---
title: kafka HelloWorld
date: 2020-03-09 10:39:07
tags:
categories:
top:
---

# 核心概念

下面介绍Kafka相关概念,以便运行下面实例的同时，更好地理解Kafka.
\1. Broker
Kafka集群包含一个或多个服务器，这种服务器被称为broker
\2. Topic
每条发布到Kafka集群的消息都有一个类别，这个类别被称为Topic。（物理上不同Topic的消息分开存储，逻辑上一个Topic的消息虽然保存于一个或多个broker上但用户只需指定消息的Topic即可生产或消费数据而不必关心数据存于何处）
\3. Partition
Partition是物理上的概念，每个Topic包含一个或多个Partition.
\4. Producer
负责发布消息到Kafka broker
\5. Consumer
消息消费者，向Kafka broker读取消息的客户端。
\6. Consumer Group
每个Consumer属于一个特定的Consumer Group（可为每个Consumer指定group name，若不指定group name则属于默认的group）

<!-- more -->

# 什么是kafka？

**Kafka**是由[Apache软件基金会](https://baike.baidu.com/item/Apache软件基金会)开发的一个开源流处理平台，由[Scala](https://baike.baidu.com/item/Scala)和[Java](https://baike.baidu.com/item/Java/85979)编写。Kafka是一种高吞吐量的[分布式](https://baike.baidu.com/item/分布式/19276232)发布订阅消息系统，它可以处理消费者在网站中的所有动作流数据。
简单地说就是一个实现消息的发送与高效消费的一个消息中间件。

# kafka可以帮助我们做什么？或者是解决什么问题？

- 日志收集：一个公司可以用Kafka可以收集各种服务的log，通过kafka以统一接口服务的方式开放给各种consumer，例如Hadoop、Hbase、Solr等；
- 消息系统：解耦和生产者和消费者、缓存消息等；
- 用户活动跟踪与审计数据收集：Kafka经常被用来记录web用户或者app用户的各种活动，如浏览网页、搜索、点击等活动，这些活动信息被各个服务器发布到kafka的topic中，然后订阅者通过订阅这些topic来做实时的监控分析，或者装载到Hadoop、数据仓库中做离线分析和挖掘；
- 运营指标：Kafka也经常用来记录运营监控数据。包括收集各种分布式应用的数据，生产各种操作的集中反馈，比如报警和报告；
- 流式处理；

启动Zookeeper服务

```sh
zookeeper-server-start.sh config/zookeeper.properties
```

启动Kafka服务：

```sh
kafka-server-start.sh config/server.properties
```

创建一个自定义topic，并命名为“wordsendertest”：

```sh

```

这个topic叫`test`，2181是zookeeper默认的端口号，partition是topic里面的分区数，replication-factor是备份的数量，在kafka集群中使用，这里单机版就不用备份了

列出所有创建的Topics：

```sh
kafka-topics.sh --list --zookeeper localhost:2181
```

sass绑定Toptic生产消息：

```sh
kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

绑定Toptic，并从头开始接收消息：

```sh
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

停止kafka-producer，然后删除Topic：

删除Topic下的消息数据：

```sh
kafka-topics.sh --zookeeper localhost:2181 --alter --topic test --config retention.ms=1000
```

To purge the Kafka topic, you need to change the retention time of that topic. The default retention time is 168 hours, i.e. 7 days. So, you have to change the retention time to 1 second, after which the messages from the topic will be deleted. Then, you can go ahead and change the retention time of the topic back to 168 hours.



```sh
kafka-topics.sh --zookeeper localhost:2181 --delete --topic test
```



**References**:

1. https://kafka.apache.org/documentation.html
