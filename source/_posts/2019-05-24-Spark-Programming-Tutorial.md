---
title: Spark编程指南
date: 2019-05-24 18:34:02
tags: Spark
categories: 大数据
top:
---
Spark编程指南、API文档：  https://spark.apache.org/docs/latest/#spark-overview
<!-- more -->
# 文件读写
Spark支持的文件读写来源有：文件系统(本地文件系统、HDFS、远程Amazon S3)、数据库(MySQL、HBase、Hive)
SPark支持支持很多其他常见的文件格式：文本文件、JSON、CSV、SequenceFile，以及protocol buffer
![](1136325-20170915111603547-1070150402.png)

## 读取本地文件系统
要加载本地文件，必须采用`file:///`开头的这种格式;
`Spark 将传入的路径作为目录对待，会在那个目录下输出多个文件`
如果路径简写为`path/to/somewhere`，`sc.textFile()`将默认认为其为HDFS路径
```py
myRdd = sc.textFile("file:///home/holden/repos/spark/README.md") #读取本地文本文件

outputFile = "file:///home/holden/repos/spark/result.txt" # 保存为本地文本文件
myRdd.saveAsTextFile(outputFile)

myRdd = sc.textFile("hdfs://master:9000/user/root/people.txt") # 从HDFS加载数据

myRdd = sc.textFile("s3://your_bucket/") # 从 AWS s3 加载数据
myRDD.saveAsTextFile("s3://your_bucket/test/")  # 将数据保存到 AWS s3

jsonRdd = sc.textFile("file:///usr/local/people.json") # 加载JSON文件

myRdd = sc.read.format('csv')
               .options(header='true', inferSchema='true')
               .load('/diamonds.csv') # 读取CSV文件

df.write.parquet("output/proto.parquet")
# using SQLContext to read parquet file
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

df = sqlContext.read.parquet("output/proto.parquet")
```
[File System Shell Guide](https://hadoop.apache.org/docs/r1.2.1/file_system_shell.html)
