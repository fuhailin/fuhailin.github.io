---
title: 如何通过反向代理远程访问内网主机
date: 2019-05-07 18:49:23
tags: Linux
categories:
top:
---
首先一定需要一台固定IP的服务器做转发代理，而且保证我们需要连接的目标主机能够通过SSH连接这台主机。原理在这里


**2019年5月7日19:00:39 更新 目前已发现一款优秀的开源反向代理软件[FRP](https://github.com/fatedier/frp)，使用体验很稳定，已经基本抛弃ssh进行命令行操作的方式，ssh的方式很不稳定。**

<!-- more -->

# FRP
分为Server端配置和Client配置，详见frp readme。

## 配合Supervisor守护FRP
使用Supervisor来做进程的监控，让服务器重启或者FRP down掉之后还能自动重新连接

安装Supervisor：`sudo apt install supervisor`
编辑FRP client的配置文件：`vim /etc/supervisord.d/frpc.ini`：
```
[program:frps]
command = ./frp_0.24.1_linux_amd64/frpc -c ./frp_0.24.1_linux_amd64/frpc.ini
autostart = true
```
重启Supervisor后配置生效：`sudo service supervisord restart`
# SSH

主要使用命令如下：

## 在目标主机上执行如下命令：
`ssh -fCNR B_port:localhost:22 B_username@B_IP`
其中`B_username`表示代理服务器的用户名，`B_IP`表示代理服务器IP地址，`B_port`表示与目标主机建立直接转发连接的代理服务器端口，这里我使用的是代理服务器1234端口，**某些云主机还需要添加安全规则使B_port能够被外网访问**

测试转发连接是否建立成功：
**在代理服务器上查看`ss -ant` ：**
![这里写图片描述](20180729122546729)

在目标主机上查看 `ps aux | grep ssh` ：
![这里写图片描述](20180729123244214)


## 在代理服务器上执行如下命令:
`ssh -fCNL *:1235:localhost:1234 localhost`

## 稳定方式
在目标主机上运行：`autossh -M 1235 -NR 1234:localhost:22 ubuntu@193.112.140.**`，意思是在中转主机上的端口`1235`上建立监听，保持连接。

然后我们在本地就可以通过ssh，经过代理服务器转发来登陆远程内网服务器了：
`ssh -p 1235 A_username@B_IP`
其中A_username是目标主机的用户名


References:
https://www.cnblogs.com/eshizhan/archive/2012/07/16/2592902.html
