---
title: Spark学习笔记之Broadcast Join性能调优
date: 2019-05-07 11:06:40
tags: Spark
categories: 大数据
top:
description: spark-sql或者hive-sql 很多业务场景都会有表关联的的操作，在hive中有map side join优化，对应的在spark-sql中也有map side join。spark中如果在参与join的表中存在小表，可以采用cache broadcast的方式进行优化，避免数据的shuffle，从而一定程度上可以避免数据倾斜，增加spark作业的执行速度。本文主要阐述怎么使用spark sql的map side join进行优化，及使用过程需要注意的内容，同时mark自己研究spark的过程。 
---
