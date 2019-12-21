---
title: 使用数据库连接池提升读写性能
date: 2019-12-02 11:41:27
tags: [Python,数据库连接池]
categories:
top:
---
以我目前使用较多的Python语言编程为例，可以使用`PyMysql`来连接MySQL数据库并进行“query、insert、update”等操作，但是这样的方案你每次请求连接MySQL都会有一个单独的连接，这很浪费资源，特别是当请求的数量达到一定数量时会对MySQL的性能产生明显的影响。因此在实际使用中，数据库连接池技术通常被用来进行数据库连接中的资源复用。

# Solution：DBUtils
DBUtils是一个允许在非线程安全数据库接口周围使用线程安全包装器的Python数据库连接池工具包。
