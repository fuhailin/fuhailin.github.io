---
title: 配置ssh密钥登录与别名登录
date: 2019-05-04 16:33:45
tags: [Linux]
categories:
top:
---
通常我们在 Termianl 下用 ssh 链接远程主机的时候，每次都需要输入一长串的用户名加主机地址，是不是觉得很麻烦？那么好吧，这个 Tips 也需能帮你解决这一烦恼，让你通过密钥甚至别名快速登录远程主机。
<!-- more -->
# 通过密钥登录
## 查看local有没有公钥
`ls ~/.ssh/`
![ls ~/.ssh/](20180816111251441)

如果local没有公钥的话需要生成公钥
`ssh-keygen`：产生公钥与私钥对
![ssh-keygen](2019-05-04-16-51-01.png)
## 将公钥上传给主机
`ssh-copy-id` 将本机的公钥复制到目的机器的authorized_keys文件中
使用方式为：`ssh-copy-id -i .ssh/id_rsa.pub name@193.112.x.xxx`
![ssh-copy-id](2019-05-04-16-31-52.png)
我这里多出来的-oPort=xxxx参数是因为我配置了反向代理，所以需要指定登录端口号。

## 登录到远程机器不用输入密码
直接使用命令：`ssh hailin@193.112.x.xxx -oPort=xxxx`

# 配置ssh别名登录
`vi ~/.ssh/config`
![](20180809175741834)
登录到远程机器使用简短的别名：
`ssh GPU`
`ssh cloud`
即可登录！


https://blog.csdn.net/yanzhibo/article/details/75804619
https://blog.csdn.net/superbfly/article/details/66970114
https://stackoverflow.com/questions/48328446/id-rsa-pub-file-ssh-error-invalid-format
