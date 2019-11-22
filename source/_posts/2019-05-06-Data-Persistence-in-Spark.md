---
title: Cache() or not Cache() in Spark, 这是一个价值百万的问题
date: 2019-05-06 16:34:19
tags: Spark
categories: 大数据
top:
---
Spark一个重要的功能就是将RDD持久化到内存中。当对RDD进行持久化操作时，每个节点都会将自己操作的RDD的partition持久化到内存中，并在之后对RDD的反复使用中，直接使用内存中缓存的partition。这样的话，对于一个RDD反复执行的操作场景中，就只需要对RDD计算一次即可，而不需要反复计算RDD。巧妙使用RDD持久化,甚至在某种场景下，可以将Spark应用程序性能提升10倍。对于迭代式算法和快速交互应用来说，RDD的持久化是非常必要的。
<!-- more -->

要持久化一个RDD，只需要调用RDD的cache()或者persist()方法即可。在该RDD第一次被计算出来时，就会直接缓存到每个节点中。而且Spark的持久化机制还是自动容错的，如果持久化的RDD的任何partition丢失了，那么Spark会自动通过其源RDD,使用transformation操作重新计算该partition。

Spark自己在shuffle过程中，会进行数据的持久化，比如写在磁盘中，主要是为了在节点失败时，避免需要重新计算整个过程。

# cache()和presist()的区别
Spark提供了5中等级的持久化存储级别
 - MEMORY_ONLY
 - MEMORY_ONLY_SER
 - MEMORY_AND_DISK
 - MEMORY_AND_DISK_SER
 - DISK_ONLY

cache()和presist()的区别在于，cache()是persist()的一种简化方式，`cache()`的底层就是调用persist()的无参版本，即调用`persist(StorageLevel.MEMORY_ONLY)`,将数据持久化到内存中。如果需要从内存中清除缓存，那么可以使用`unpersist()`方法。


cache()=persist(StorageLevel.MEMORY_ONLY)   |  persist(StorageLevel.MEMORY_AND_DISK)
:------------------------------------------:|:-------------------------:
![MEMORY_ONLY](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/ekNcE.png)     |      ![MEMORY_AND_DISK](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/cjD3K.png)


# 什么时候应该持久化RDD或DataFrame？
在以下情况下，你绝对应该``cache()``RDD或DataFrame：
 - 在一个迭代循环中重复使用它们时，一定要cache()（ie. 机器学习算法中）
 - 在某个应用、任务中，一个RDD或DataFrame复用两次及以上的，一定要cache，避免不必要的重复计算。
 - 当重新计算生成RDD或DataFrame的成本很高时，请记住cache()（即HDFS，在一组复杂的map()，filter()等之后）如果Worker节点死亡，这有助于恢复过程。

要记住的是，当Worker节点内存不够用时，Spark将以LRU方式自动从Workers中替换RDD分区，并且这种替换在每个Worker上是独立发生。



![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/DInZf.png)

[What is the difference between cache and persist?](https://stackoverflow.com/questions/26870537/what-is-the-difference-between-cache-and-persist)
[spark 数据持久化与释放](https://www.jianshu.com/p/0b2ea4cfdc8a)
[TO CACHE OR NOT TO CACHE, THAT’S THE MILLION DOLLAR QUESTION](https://unraveldata.com/to-cache-or-not-to-cache/)
