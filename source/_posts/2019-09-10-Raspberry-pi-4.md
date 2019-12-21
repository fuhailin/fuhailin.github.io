---
title: 树莓派4B 玩转指南
tags:
  - Raspberry
  - Linux
categories: [操作系统,Raspbian]
date: 2019-09-10 23:32:11
top:
---

我的新玩具树莓派4B到手啦，我选择的是2GB RAM版本，刷上系统先，开干!

<!-- more -->

## 安装轻量级无图形界面系统

树莓派开发板没有配置板载FLASH，因为它支持SD卡启动，所有我们需要下载相应镜像，并将其烧写在SD上，启动系统即可。(这个镜像里包含了我们通常所说的bootloader、kernel、文件系统)

树莓派由于其开源特性，支持非常多的系统类型：

Raspbian、Arch Linux ARM、Debian Squeeze、Firefox OS、Gentoo Linux、OpenWRT、
Google Chrome OS、Raspberry Pi Fedora Remix、Slackware ARM
QtonPi、Slackware ARM、WebOS、RISC OS、FreeBSD、NetBSD、Android 4.0(Ice Cream Sandwich)

树莓派4B暂时只提供官方raspbian系统

树莓派官网的下载地址：http://www.raspberrypi.org/downloads

我下载安装的轻量化无图形界面系统为 **Raspbian Buster Lite** Minimal image based on Debian Buster。使用的镜像刻录工具是 **balenaEtcher-1.5.56-x64.AppImage**。

## 启动树莓派
烧写完后把MicroSD卡直接插入树莓派的MicroSD卡插槽，另外我们给莓派连接显示器、电源、鼠标、键盘，打开数据线上的电源开关以后，就可以进入树莓派系统了。正常情况下红色电源灯常亮，绿色信号灯不规律闪烁。红灯偶尔出现灭的情况可能是供电不足，只要系统可以正常进入就可以了。

## 连接WiFi

`sudo raspi-config`：选择【2 Network Options】->【N2 Wi-fi】->输入SSID、密码。
`sudo iwlist wlan0 scan`：扫描树莓派已经识别的wifi

## 启用SSH
`sudo raspi-config`：选择【5 Interface Options】->[SSH]进行SSH的启用

## 更换国内源

```
# 编辑 `/etc/apt/sources.list` 文件，删除原文件所有内容，用以下内容取代：
deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib
deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib

# 编辑 `/etc/apt/sources.list.d/raspi.list` 文件，删除原文件所有内容，用以下内容取代：
deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui
```

使用`sudo apt-get update`进行更新

## 显示CPU温度

`cat /sys/class/thermal/thermal_zone0/temp`：返回值除以1000极为当前CPU温度

## 必备软件安装

`sudo apt install vim tmux git`：安装VIM、tmux、git
安装Python3：
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh
chmod +x Miniconda3-latest-Linux-armv7l.sh
./Miniconda3-latest-Linux-armv7l.sh

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes

```

`curl -sLf https://spacevim.org/install.sh | bash`：配置SpaceVim

**安装Docker**:
```bash
curl -sL get.docker.com | sed 's/9)/10)/' | sh
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sudo pip3 install docker-compose
```
更换Docker清华镜像
`sudo vim /etc/apt/sources.list.d/docker.list`:
```
deb [arch=armhf] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/raspbian buster stable
```
[Docker Community Edition 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/docker-ce/)

## 关机与重启

`sudo shutdown`：一分钟之后关机，`shutdown -c`取消关机
`sudo shutdown now`：立即关机
`sudo reboot`、`sudo shutdown -r`：重新启动
`sudo shutdown 11:00`：上午11:00定时关机
`sudo shutdown +10`：10分钟后关机

## 打造树莓派路由器

[billz/**raspap-webgui**](https://github.com/billz/raspap-webgui)

```bash
sudo docker run -d --name=gitea -p 1008x:3000 -v /var/lib/gitea:/data --restart unless-stopped kunde21/gitea-arm:latest
```

## 打造私人git服务器
**安装Gitea**
```bash
docker pull gitea/gitea:latest

sudo usermod -aG docker $USER

sudo mkdir -p /var/lib/gitea

docker run -d --name=gitea -p 10022:22 -p 10080:3000 -v /var/lib/gitea:/data gitea/gitea:latest
```

## 打造家用云服务器
**安装NextCloudPi**
```
# Start docker with custom storage volume with:
sudo mkdir /media/ncdata
# 主机80端口已被raspap-webgui占用
docker run -d -p 4443:4443 -p 443:443 -p 81:80 -v /media/ncdata:/data --name nextcloudpi ownyourbits/nextcloudpi-armhf $DOMAIN
# 观察nextcloudpi的安装进度
docker logs -f nextcloudpi
```


Login with user `pi` and password `raspberry`(<- For default).
**进入系统设置**
`sudo raspi-config`
**进入nextcloud app 设置**
`sudo sudo ncp-config`
https://docs.nextcloudpi.com/en/how-to-get-started-with-ncp-docker/

## 挂载移动硬盘并设置Samba共享
**挂载硬盘**
我的硬盘之前安装过Ubuntu系统，因此为ext4文件系统，树莓派的是Debian系统可以直接读取ext4文件系统，因此挂载后可以直接读取，如果是Windows的NTFS系统需要另外处理
插上硬盘，查看状态：sudo fdisk -l
新建一个目录 ，让树莓派将硬盘挂载到创建的目录：
```sh
sudo mkdir /mnt/toshiba
sudo mount /dev/sda2  /mnt/data
```
还可以设置开机自动挂载

**Samba**
sudo apt install samba samba-common-bin
sudo vim /etc/samba/smb.conf
```
[pi]           # Name will show on Internet
path = /mnt/data
valid users = pi
browseable = yes
public = yes
writable = yes
```
设置`pi`用户的密码：sudo smbpasswd -a pi
重启Samba服务：sudo systemctl restart smbd.service

打开MacOS的finder，从`Go`选项中点击`Connect to Server…`，输入树莓派Samba地址：`192.168.1.3/pi`输入用户名密码即可完成连接。

*************

https://docs.gitea.io/zh-tw/install-with-docker/

https://docs.gitea.io/zh-cn/install-with-docker/
