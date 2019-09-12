---
title: Elasticsearch
date: 2019-08-14 16:58:15
tags: elasticsearch
categories: 
top:
---
# 简介
Elasticsearch是一个基于Apache Lucene(TM)的开源搜索引擎。无论在开源还是专有领域，Lucene可以被认为是迄今为止最先进、性能最好的、功能最全的搜索引擎库。
# Linux上的安装
> jdk至少需要在1.8.0_73以上版本

<!-- more -->
解压文件`tar -zxvf elasticsearch-x.x.x.tar.gz`，`./bin/elasticsearch`为启动文件，但如果此时直接启动elasticsearch的话，会报错
![](Image 3.png)
原因是elasticsearch默认不支持root用户运行，因为正式环境用root运行可能会有安全风险，不建议用root来跑。我们可以单独为elasticsearch单独创建一个用户
```bash
sudo useradd -m elastic -s /bin/bash          #创建elastic用户，并使用/bin/bash作为shell
sudo passwd elastic                           #为elastic用户设置密码，之后需要连续输入两次密码
sudo adduser elastic sudo                     #为elastic用户增加管理员权限
chown -R elastic:elastic  elasticsearch-x.x.x #为elastic添加文件权限
su - elastic                                  #切换当前用户为用户elastic
cd elasticsearch-x.x.x                        #切换目录
./bin/elasticsearch                           #执行
```
如果你想把 Elasticsearch 作为一个守护进程在后台运行，那么可以在后面添加参数 `-d` 。
如果你是在 Windows 上面运行 Elasticseach，你应该运行 `bin\elasticsearch.bat` 而不是 `bin\elasticsearch` 。
使用 `curl http://localhost:9200/` 查看是否运行，如果返回如下信息则标示运行正常：
```json
{
  "name" : "RjxKv_d",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "SYM-Wb6xR3mqGLx4bHtBNA",
  "version" : {
    "number" : "6.1.3",
    "build_hash" : "af51318",
    "build_date" : "2018-01-26T18:22:55.523Z",
    "build_snapshot" : false,
    "lucene_version" : "7.1.0",
    "minimum_wire_compatibility_version" : "5.6.0",
    "minimum_index_compatibility_version" : "5.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

[Elasticsearch在Centos 7上的安装与配置](https://www.biaodianfu.com/centos-7-install-elasticsearch.html)
[Elasticsearch权威指南](https://es.xiaoleilu.com/010_Intro/05_What_is_it.html)
