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

- `\password`：设置密码
- `\q`：退出
- `\h`：查看SQL命令的解释，比如\h select。
- `\?`：查看psql命令列表。
- `\l`：列出所有数据库。
- `\c` [database_name]：连接其他数据库。
- `\d`：列出当前数据库的所有表格。
- `\d [table_name]`：列出某一张表格的结构。
- `\du`：列出所有用户。
- `\e`：打开文本编辑器。
- `\conninfo`：列出当前数据库和连接的信息。
- `psql -U postgres -c 'SHOW config_file'`：显示postgresql.conf位置
- `sudo /etc/init.d/postgresql start` ：  # 开启
- `sudo /etc/init.d/postgresql stop`  ：  # 关闭
- `sudo /etc/init.d/postgresql restart`： # 重启
- ``


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
### Python连接PostgreSQL

**配置允许远程访问**

1. 修改postgresql.conf

`vim /etc/postgresql/xx/main/postgresql.conf`，这里的x取决于你安装PostgreSQL的版本号，编辑`listen_addresses`一行，使PostgreSQL可以接受来自任意IP的连接请求。
```
listen_addresses = '*'
```

2. 修改pg_hba.conf

`vim /etc/postgresql/xx/main/pg_hba.conf`，位置与postgresql.conf相同，虽然上面配置允许任意地址连接PostgreSQL，但是这在pg中还不够，我们还需在pg_hba.conf中配置服务端允许的认证方式。任意编辑器打开该文件，编辑或添加下面一行。
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    all             all             0.0.0.0/0               md5
```


```py
import psycopg2
import sys
import os
import numpy as np
import pandas as pd
import pandas.io.sql as psql

## ****** LOAD PSQL DATABASE ***** ##

PGHOST = '192.168.1.4'
PGDATABASE = 'postgres'
PGUSER = 'postgres'
PGPASSWORD = '********'

# Set up a connection to the postgres server.
conn_string = "host=" + PGHOST + " port=" + "5432" + " dbname=" + PGDATABASE + " user=" + PGUSER \
    + " password=" + PGPASSWORD
conn = psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()


def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print(sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)

```
