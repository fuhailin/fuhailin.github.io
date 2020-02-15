---
title: Linux上配置Jupyter Notebook远程访问
date: 2019-03-02 22:57:49
tags: [Linux,Jupyter,Python]
categories: Linux
top:
---
现在运行深度学习的程序基本需要比较高配置的GPU服务器，所以一般会通过自己的电脑远程访问服务器。但是服务器上没有浏览器，我想在服务器上运行Jupyter Notebook该怎么访问呢？
<!-- more -->
# 安装ipython, jupyter
```bash
pip install ipython
pip install jupyter
```
如果是在Anaconda虚拟环境中运行Jupyter的话还需要安装`conda install notebook ipykernel`（**Python3适用**）
# 生成配置文件
```bash
jupyter notebook --generate-config
# /home/hailin/.jupyter/jupyter_notebook_config.py
```
# 生成密码
```py
hailin@601GPU /]$ ipython
Python 3.5.2 |Continuum Analytics, Inc.| (default, Jul  2 2016, 17:53:06)
Type "copyright", "credits" or "license" for more information.

IPython 5.1.0 -- An enhanced Interactive Python.
?         -> Introduction and overview of IPython's features.
%quickref -> Quick reference.
help      -> Python's own help system.
object?   -> Details about 'object', use 'object??' for extra details.

In [1]: from notebook.auth import passwd

In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:43b95b731276:5d330ee6f6054613b3ab4cc59c5048ff7c70f549'
```
# 修改默认配置文件

```bash
vi /home/hailin/.jupyter/jupyter_notebook_config.py

c.NotebookApp.ip='*' #设置访问notebook的ip，*表示所有IP，这里设置ip为都可访问  
c.NotebookApp.allow_remote_access = True
c.NotebookApp.password = 'sha1:5df252f58b7f:bf65d53125bb36c085162b3780377f66d73972d1' #填写刚刚生成的密文  
c.NotebookApp.open_browser = False # 禁止notebook启动时自动打开浏览器(在linux服务器一般都是ssh命令行访问，没有图形界面的。所以，启动也没啥用)  
c.NotebookApp.port =8888 #指定访问的端口，默认是8888
```

# 启动jupyter notebook
```bash
jupyter notebook
```

# 本地浏览器访问远程
http://202.116.46.256:8888/tree?
![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-03-02-232043.png)
