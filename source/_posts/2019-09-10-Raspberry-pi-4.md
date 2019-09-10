---
title: 树莓派4B 玩转指南
tags:
  - Raspberry
  - Linux
categories: Linux
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

`sudo apt install vim tmux git python3 python3-pip`

`curl -sLf https://spacevim.org/install.sh | bash`：配置SpaceVim

## 关机与重启

`sudo shutdown`：一分钟之后关机，`shutdown -c`取消关机
`sudo shutdown now`：立即关机
`sudo reboot`、`sudo shutdown -r`：重新启动
`sudo shutdown 11:00`：上午11:00定时关机
`sudo shutdown +10`：10分钟后关机

## 打造树莓派路由器

[billz/**raspap-webgui**](https://github.com/billz/raspap-webgui)
