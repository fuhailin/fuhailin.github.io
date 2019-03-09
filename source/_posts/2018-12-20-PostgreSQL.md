---
title: PostgreSQL
date: 2018-12-20 16:44:29
tags: [PostgreSQL,SQL]
categories: DataBase
top:
description: PostgreSQL是一个跨平台、开源的、对象关系型(object-relational)数据库
---

PostgreSQL的一些特点：PostgreSQL中可以插入重复数据，也就是说不需要唯一性主键。

# PostgreSQL在Ubuntu下的安装

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

安装完成后，默认会：

（1）创建名为"postgres"的Linux用户
（2）创建名为"postgres"、不带密码的默认数据库账号作为数据库管理员
（3）创建名为"postgres"的表

安装完成后的一些默认信息如下：

config /etc/postgresql/9.5/main
data /var/lib/postgresql/9.5/main
locale en_US.UTF-8
socket /var/run/postgresql
port 5432

## PostgreSQL在终端中的使用

```SQL
CREATE TABLE table_name
(
    column1 integer,
    column2 character varying(20),
    column3 numeric(19,3),
    column4 numeric
)
```

### PostgreSQL 中获取表名、数据库名称
①表名
```sql
SELECT tablename FROM pg_tables WHERE tablename NOT LIKE 'pg%' AND tablename NOT LIKE 'sql_%'
```

②数据库名

```sql
SELECT datname FROM pg_database;
```

③列名

```sql
select * from information_schema.columns where table_name = 'final_back_pg_lv10'
```
