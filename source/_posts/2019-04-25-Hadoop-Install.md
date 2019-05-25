---
title: Ubuntu18.04下Hadoop 3的安装与配置（伪分布式环境）
date: 2019-04-25 11:33:41
tags: [Hadoop,HDFS]
categories: 大数据
top:
---
本教程使用 Ubuntu 18.04 64位 作为系统环境（Ubuntu16.04 也行，32位、64位均可），请自行安装系统。如果用的是 CentOS/RedHat 系统，请查看相应的[CentOS安装Hadoop教程_单机伪分布式配置](http://dblab.xmu.edu.cn/blog/install-hadoop-in-centos/)。
本教程基于原生最新 Hadoop 3，在 Hadoop 3.1.2 (stable) 版本下验证通过，可适合任何 Hadoop 3.x.y 版本，其他版本类似。
<!-- more -->
# 准备
## 创建hadoop用户
如果你安装 Ubuntu 的时候不是用的 “hadoop” 用户，那么需要增加一个名为 hadoop 的用户。
```Shell
sudo useradd -m hadoop -s /bin/bash  #创建hadoop用户，并使用/bin/bash作为shell
sudo passwd hadoop                   #为hadoop用户设置密码，之后需要连续输入两次密码
sudo adduser hadoop sudo             #为hadoop用户增加管理员权限
su - hadoop                          #切换当前用户为用户hadoop
sudo apt-get update                  #更新hadoop用户的apt,方便后面的安装
```
## 安装SSH,设置SSH无密码登陆
```bash
sudo apt-get install openssh-server   #安装SSH server
ssh localhost                         #登陆SSH，第一次登陆输入yes
exit                                  #退出登录的ssh localhost
cd ~/.ssh/                            #如果没法进入该目录，执行一次ssh localhost
ssh-keygen -t rsa　　
cat ./id_rsa.pub >> ./authorized_keys #加入授权
ssh localhost                         #此时已不需密码即可登录localhost，并可见下图。如果失败则可以搜索SSH免密码登录来寻求答案
```

# 安装Java环境
此处参考 https://fuhailin.github.io/Essential-Apps-for-Ubuntu/#JAVA
# 安装 Hadoop 3
通过Apache Hadoop官方下载页面( https://hadoop.apache.org/releases.html )选择最新的Binary版本进行下载（截止2019年4月25日，Hadoop最新稳定版本为3.1.2）。
Binary版本是编译好的二进制版本，可以直接解压安装；另一个包含 src 的则是 Hadoop 源代码，需要进行编译才可使用。
下面进行安装：
```bash
wget http://ftp.cuhk.edu.hk/pub/packages/apache.org/hadoop/common/hadoop-3.1.2/hadoop-3.1.2.tar.gz
sudo tar -zxvf  hadoop-3.1.2.tar.gz -C /usr/local    #解压到/usr/local目录下
cd /usr/local
sudo mv ./hadoop-3.1.2/ ./hadoop                      #重命名为hadoop
sudo chown -R hadoop ./hadoop                        #修改文件权限
```
给hadoop配置环境变量，将下面代码添加到.bashrc文件:
```bash
export HADOOP_HOME=/usr/local/hadoop
export CLASSPATH=$($HADOOP_HOME/bin/hadoop classpath):$CLASSPATH
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```
执行source ~./bashrc使设置生效，并查看hadoop是否安装成功
![hadoop version](hadoop-version.png)

# 伪分布式配置
Hadoop 可以在单节点上以伪分布式的方式运行，Hadoop 进程以分离的 Java 进程来运行，节点既作为 NameNode 也作为 DataNode，同时，读取的是 HDFS 中的文件。

Hadoop 的配置文件位于 /usr/local/hadoop/etc/hadoop/ 中，伪分布式需要修改2个配置文件 core-site.xml 和 hdfs-site.xml 。Hadoop的配置文件是 xml 格式，每个配置以声明 property 的 name 和 value 的方式来实现。
首先将`JDK`的路径(echo $JAVA_HOME)添加到hadoop-env.sh文件，修改`vim ./etc/hadoop/hadoop-env.sh`:
![](2019-04-25 14 56 11.png)

接下来修改配置文件 `./etc/hadoop/core-site.xml`:
```xml
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```
修改配置文件 `./etc/hadoop/hdfs-site.xml`：
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/tmp/dfs/data</value>
    </property>
</configuration>
```
## Hadoop配置文件说明
Hadoop 的运行方式是由配置文件决定的（运行 Hadoop 时会读取配置文件），因此如果需要从伪分布式模式切换回非分布式模式，需要删除 core-site.xml 中的配置项。

此外，伪分布式虽然只需要配置 fs.defaultFS 和 dfs.replication 就可以运行（官方教程如此），不过若没有配置 hadoop.tmp.dir 参数，则默认使用的临时目录为 /tmp/hadoo-hadoop，而这个目录在重启时有可能被系统清理掉，导致必须重新执行 format 才行。所以我们进行了设置，同时也指定 dfs.namenode.name.dir 和 dfs.datanode.data.dir，否则在接下来的步骤中可能会出错。

配置完成后，执行 NameNode 的格式化:
`./bin/hdfs namenode -format`
![./bin/hdfs namenode -format](namenode-format.png)
启动namenode和datanode进程，并查看启动结果
`./sbin/start-dfs.sh`
启动完成后，可以通过命令 `jps` 来判断是否成功启动，若成功启动则会列出如下进程: “NameNode”、”DataNode” 和 “SecondaryNameNode”
![](2019-04-25 15 38 08.png)
成功启动后，可以访问 HDFS的Web 界面 http://localhost:9870 查看 NameNode 和 Datanode 信息，还可以在线查看 HDFS 中的文件。
![HDFS Web界面](2019-04-25 15 52 37.png)
至此，hadoop的安装就已经完成啦！enjoy it！
# 运行Hadoop伪分布式实例
由于前面已经配置了Hadoop的环境变量，Hadoop和HDFS的命令已经包含在了系统当中，HDFS有三种shell命令方式：
 - hadoop fs         ： 适用于任何不同的文件系统，比如本地文件系统和HDFS文件系统
 - hadoop dfs        ： 只能适用于HDFS文件系统
 - hdfs dfs          ： 跟hadoop dfs的命令作用一样，也只能适用于HDFS文件系统

上面的单机模式，grep 例子读取的是本地数据，伪分布式读取的则是 HDFS 上的数据。要使用 HDFS，首先需要在 HDFS 中创建用户目录：
```shell
hdfs dfs -mkdir -p /user/hadoop
```
接着将 ./etc/hadoop 中的 xml 文件作为输入文件复制到分布式文件系统中，即将 /usr/local/hadoop/etc/hadoop 复制到分布式文件系统中的 /user/hadoop/input 中。我们使用的是 hadoop 用户，并且已创建相应的用户目录 /user/hadoop ，因此在命令中就可以使用相对路径如 input，其对应的绝对路径就是 /user/hadoop/input:
```shell
hdfs dfs -mkdir input
hdfs dfs -put ./etc/hadoop/*.xml input
```
复制完成后，可以通过如下命令查看文件列表：
```shell
hdfs dfs -ls input
```
伪分布式运行 MapReduce 作业的方式跟单机模式相同，区别在于伪分布式读取的是HDFS中的文件（可以将单机步骤中创建的本地 input 文件夹，输出结果 output 文件夹都删掉来验证这一点）。
```
hadoop jar ./share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar grep input output 'dfs[a-z.]+'
```
查看运行结果的命令（查看的是位于 HDFS 中的输出结果）：
```
hdfs dfs -cat output/*
```
结果如下，注意到刚才我们已经更改了配置文件，所以运行结果不同。
![](2019-04-25 16 21 24.png)
我们也可以将运行结果取回到本地：
```shell
rm -r ./output    # 先删除本地的 output 文件夹（如果存在）
hdfs dfs -get output ./output     # 将 HDFS 上的 output 文件夹拷贝到本机
cat ./output/*
```
Hadoop 运行程序时，输出目录不能存在，否则会提示错误 “org.apache.hadoop.mapred.FileAlreadyExistsException: Output directory hdfs://localhost:9000/user/hadoop/output already exists” ，因此若要再次执行，需要执行如下命令删除 output 文件夹:
```
hdfs dfs -rm -r output    # 删除 output 文件夹
```
若要关闭 Hadoop，则运行
```./sbin/stop-dfs.sh```
下次启动 hadoop 时，无需进行 NameNode 的初始化，只需要运行 `./sbin/start-dfs.sh` 就可以！

**References**:
1. [Hadoop安装教程_单机/伪分布式配置_Hadoop2.6.0/Ubuntu14.04](http://dblab.xmu.edu.cn/blog/install-hadoop/)
2. [Ubuntu16.04 下 hadoop的安装与配置（伪分布式环境）](https://www.cnblogs.com/87hbteo/p/7606012.html)
3. [Install a Hadoop Cluster on Ubuntu 18.04.1](https://dzone.com/articles/install-a-hadoop-cluster-on-ubuntu-18041)
