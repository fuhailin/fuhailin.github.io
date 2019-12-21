---
title: Ubuntu、macOS必备软件配置记录帖
date: 2019-01-14 17:36:36
tags: [Linux,macOS]
categories: [Linux,Tools]
top:
description: Ubuntu必备软件配置记录帖
---
# For Ubuntu
## 安装编辑器&编译器

### 1、安装Sublime Text 3：
https://www.sublimetext.com/docs/3/linux_repositories.html
apt Install the GPG key:

> wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -

Ensure apt is set up to work with https sources:
sudo apt-get install apt-transport-https

> echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
> sudo apt-get update
> sudo apt-get install sublime-text

终端使用Sublime，输入: subl
### 2、安装Atom：
We can download the [Atom .deb package](https://atom.io/download/deb) and install it directly:
```bash
# Install Atom
sudo dpkg -i atom-amd64.deb
# Install Atom's dependencies if they are missing
sudo apt-get -f install
```

### 3、安装PyCharm：

 - Copy the **pycharm-2017.3.3.tar.gz** to the desired installation location
   (make sure you have rw permissions for that directory)
 - Unpack the **pycharm-2017.3.3.tar.gz** using the following command:
```bash
tar -xzf pycharm-2017.3.3.tar.gz
```
 - Remove the **pycharm-2017.3.3.tar.gz** to save disk space (optional)
 - Run pycharm.sh from the bin subdirectory
```bash
./pycharm.sh
```
【Tip】: Pycharm的快捷启动方式
```bash
sudo subl /usr/share/applications/Pycharm.desktop
```
然后输入以下内容，注意Exec和Icon需要找到正确的路径

> [Desktop Entry]
Type=Application
Name=Pycharm
GenericName=Pycharm3
Comment=Pycharm3:The Python IDE
Exec="/XXX/pycharm-community-3.4.1/bin/pycharm.sh" %f
Icon=/XXX/pycharm-community-3.4.1/bin/pycharm.png
Terminal=pycharm
Categories=Pycharm;
### Shadowsock
#### 安装Shadowsock-server
VPS ：https://my.vultr.com/
Setting：https://medium.com/@zoomyale/%E7%A7%91%E5%AD%A6%E4%B8%8A%E7%BD%91%E7%9A%84%E7%BB%88%E6%9E%81%E5%A7%BF%E5%8A%BF-%E5%9C%A8-vultr-vps-%E4%B8%8A%E6%90%AD%E5%BB%BA-shadowsocks-fd57c807d97e
Shadowsocks Python版一键安装脚本： https://teddysun.com/342.html

#### 安装Shadowsock-qt5

~~$ sudo add-apt-repository ppa:hzwhuang/ss-qt5~~
~~$ sudo apt-get update~~
~~$ apt-get install shadowsocks-qt5~~

下载[Shadowsocks-Qt5-3.0.1-x86_64.AppImage](https://github.com/shadowsocks/shadowsocks-qt5/releases)
```bash
$chmod a+x Shadowsocks-Qt5-x86_64.AppImage
$./Shadowsocks-Qt5-x86_64.AppImage
```

全局pac配置：
`pip install genpac`

`genpac --format=pac --pac-proxy="SOCKS5 127.0.0.1:1080" --output="autoproxy.pac"`

genpac 的详细使用说明见 GitHub - Wiki：
https://github.com/JinnLynn/GenPAC

设置全局代理
点击：System settings > Network > Network Proxy，选择 Method 为 Automatic，设置 Configuration URL 为 autoproxy.pac 文件的路径，点击 Apply System Wide。
格式如：file:///home/{user}/Downloads/shadowsocks/autoproxy.pac

![这里写图片描述](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/screenshot_from_2019-01-14_20-28-26.png)

### 5、安装Anaconda：
download the [Anaconda installer for Linux](http://anaconda.com/downloads.html) and install it:
```bash
bash ~/Downloads/Anaconda3-5.0.1-Linux-x86_64.sh
```
配置环境变量：
```bash
subl ~/.profile
```
在最后加入：
```bash
#Anaconda
export "PATH=/home/vincent/anaconda3/bin:$PATH"
```
保存后更新环境变量即可使用
```bash
source ~/.profile
```

### 6、安装NodeJS：
https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions

download the [node-v8.9.4-linux-x64.tar.xz](https://nodejs.org/en/download/) and extra it to right directory:
```python
tar -xf node-v8.9.4-linux-x64.tar.xz ~/Programs/nodejs #解压文件到指定路径
```
配置环境变量：
```bash
vi ~/.bashrc
```
在最后加入：
```bash
#NODEJS
export PATH="/home/vincent/Programs/node-v8.10.0-linux-x64/bin:$PATH"
```

~~#NODEJS
export NODEJS_HOME=/home/vincent/Programs/nodejs/node-v8.9.4-linux-x64
export \$NODEJS_HOME/bin:\$PATH~~

保存后更新环境变量即可使用
```bash
source ~/.profile
```
```bash
node --version
v10.15.0
npm --version
6.4.1
```
### 7、安装Git：
```bash
sudo apt-get install git
```
### 8、安装tmux：
```bash
sudo apt-get install tmux
sudo apt-get update
```

## 安装数据库

### 安装MySQL：
```bash
sudo apt-get update
sudo apt-get install mysql-server
mysql_secure_installation
```
### 安装MS SQL Server：
[Quickstart: Install SQL Server and create a database on Ubuntu](https://docs.microsoft.com/en-us/sql/linux/quickstart-install-connect-ubuntu)
```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/16.04/mssql-server-2017.list)"
sudo apt-get update
sudo apt-get install -y mssql-server
sudo /opt/mssql/bin/mssql-conf setup
systemctl status mssql-server
```
## 开发工具
### Docker
```bash
# 如果你过去安装过 docker，先删掉
sudo apt-get remove docker docker-engine docker.io
# 安装依赖
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common
# 信任 Docker 的 GPG 公钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# 对于 amd64 架构的计算机，添加软件仓库:
sudo add-apt-repository \
   "deb [arch=amd64] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install docker-ce
```

[How To Install and Use Docker on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
![这里写图片描述](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/20180319151255921)

[Docker Community Edition 镜像使用帮助](https://mirror.tuna.tsinghua.edu.cn/help/docker-ce/)

**********
### JAVA
```bash
sudo apt-get update
sudo apt-get install default-jre default-jdk
```
vim ~/.bashrc: `export JAVA_HOME=/usr/lib/jvm/default-java`
```shell
source ~/.bashrc    # 使变量设置生效
echo $JAVA_HOME     # 检验变量值
java -version
$JAVA_HOME/bin/java -version  # 与直接执行java -version一样
```
至此，就成功安装了Java环境
[Hadoop安装教程_单机/伪分布式配置_Hadoop2.6.0/Ubuntu14.04:第2种安装JDK方式]http://dblab.xmu.edu.cn/blog/install-hadoop/
*********
### Hadoop
Hadoop3：https://fuhailin.github.io/Hadoop-Install/
************
### Scala
http://www.cnblogs.com/wrencai/p/3867460.html
************
### Spark
http://fuhailin.github.io/Spark-Tutorial/#Spark%E7%9A%84%E5%AE%89%E8%A3%85

*********
## 安装中文输入法

```bash
sudo apt install -y fcitx-bin
# google pinyin
sudo apt install -y fcitx-googlepinyin
# sogou pinyin
wget "http://cdn2.ime.sogou.com/dl/index/1524572264/sogoupinyin_2.2.0.0108_amd64.deb?st=qC_O2p5443g1a2TJR_rSdA&e=1533163019&fn=sogoupinyin_2.2.0.0108_amd64.deb" -O sogoupinyin.deb && \
    yes | sudo gdebi sogoupinyin.deb && \
    rm sogoupinyin.deb
```
![](http://blog.zedyeung.com/2018/08/05/Ubuntu-18-04-fcitx-chinese-input-setup-google-and-sogou/input1.png)
**Reboot之后**

第一步               |                第二步      |               第三步
:-------------------------:|:-------------------------:|:-------------------------:
![](http://blog.zedyeung.com/2018/08/05/Ubuntu-18-04-fcitx-chinese-input-setup-google-and-sogou/input2.png)|![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Screenshot_from_2019-01-15_10-55-12.png) | ![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/Screenshot_from_2019-01-15_10-55-36.png) 

 <kbd>Ctrl</kbd>+<kbd>Space</kbd>切换中英文输入

[Ubuntu 18.04 fcitx chinese input setup(google and sogou)](http://blog.zedyeung.com/2018/08/05/Ubuntu-18-04-fcitx-chinese-input-setup-google-and-sogou/)
[ubuntu 18.04 英文环境安装搜狗输入法](https://blog.csdn.net/f_c_g_/article/details/81265589)

*********
## 升级16.04到18.04
https://linuxconfig.org/how-to-upgrade-to-ubuntu-18-04-lts-bionic-beaver
**********
## 其他专业软件
### Latex
首先更换国内清华大学开源软件镜像站：https://mirror.tuna.tsinghua.edu.cn/help/ubuntu/
#### Texlive
LaTeX有很多发型版，TeX Live就是其中一种。TeX Live 是 TUG (TeX User Group) 维护和发布的 TeX 系统，可说是「官方」的 TeX 系统。TeX Live可以保持在跨操作系统平台、跨用户的一致性。而且TeX Live在Ubuntu18.04上的安装也比较方便。
Texlive需要的安装空间较大，需要在根目录预留4G的额外空间
```bash
sudo apt-get install texlive-full
# 安装XeLaTeX编译引擎
sudo apt-get install texlive-xetex
# 安装中文支持包，使用的是xeCjK，中文处理技术也有很多，xeCJK是成熟且稳定的一种。
sudo apt-get install texlive-lang-chinese

```
安装Texlive前               |                安装Texlive后
:-------------------------:|:-------------------------:
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/20180718112621899)|![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/20180718112717961)
[Ubuntu18.04安装LaTeX并配置中文环境](https://blog.csdn.net/qq_41814939/article/details/82288145)
[Ubuntu18 + VSCode + TexLive 配置中文Latex环境](http://jun369.me/2018/10/22/latex/)
[Ubuntu 18.04 LTS 安装 Tex Live](https://vanxnf.top/2018/09/15/Ubuntu-18-04-LTS-%E5%AE%89%E8%A3%85-Tex-Live/)
******************************
### Nextcloud
Nextcloud是一款开源的功能强大的私有云平台搭建框架，甚至还提供跨平台的各类终端。
命令行安装过程
```bash
sudo apt-get update
sudo apt-get install snap
sudo apt-get install snapd
sudo snap install nextcloud
```
安装完成通过IP地址直接访问

Nextcloud Web界面               |                Nextcloud iOS界面
:-------------------------:|:-------------------------:
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/netxcloud-web.png)|![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/nextcloud-mobile.png)
[Nextcloud](https://nextcloud.com/)
[基于 Ubuntu + nextCloud 搭建自己的私人网盘](https://cloud.tencent.com/developer/labs/lab/10287)
[nextcloud打开链接Apache2 Ubuntu Default Page问题](https://www.jianshu.com/p/9b2332a90337)
**************
### navi: An interactive cheatsheet tool for the command-line
https://github.com/denisidoro/navi

### fzf: A command-line fuzzy finder
https://github.com/junegunn/fzf

### Linuxbrew: Homebrew on Linux (un)installer
https://github.com/Linuxbrew/install


# For macOS
## Homebrew
https://brew.sh/
```sh
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

**Homebrew Cask**
HomeBrew是通过源码的方式来安装软件，但是有时候我们安装的软件是GUI程序应用宝(.dmg/.pkg)，这个时候我们就不能使用HomeBrew了，所以有了HomeBrew Cask的出现

brew cask 是在brew 的基础上一个增强的工具，用来安装Mac上的Gui程序应用包（.dmg/.pkg）, 比如qq、chrome等。它先下载解压到统一的目录中（/opt/homebrew-cask/Caskroom），省掉了自己去下载、解压、拖拽（安装）等步骤，同样，卸载相当容易与干净。然后再软链到~/Applications/目录下, 非常方便，而且还包含很多在 AppStore 里没有的常用软件。

brew cask的官网是：http://caskroom.io

github地址是：https://github.com/caskroom/homebrew-cask

## Htop
```sh
brew install htop
```
## iterm2
https://www.iterm2.com/index.html
[iterm2 cheatsheet](https://gist.github.com/squarism/ae3613daf5c01a98ba3a )

## Oh My Zsh
```sh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

vim ~/.zshrc
```sh
source ~/.bash_Profile
```
https://ohmyz.sh/

**zsh-syntax-highlighting**: 配置语法高亮
https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md

https://tonyxu.io/zh/posts/2018/ultimate-way-to-beautify-mac-terminal-and-recommendations-for-plugins/

## Node.js & NPM
```sh
brew install node
node -v
npm -v
```

## Atom
```sh
brew cask install atom
```

## Aria2
```sh
# For Ubuntu
$ sudo apt install aria2
# For macOS
$ brew install aria2
```

## Bazel
https://docs.bazel.build/versions/master/install-os-x.html#install-on-mac-os-x-homebrew
