---
title: Python中super()有什么用
date: 2018-12-04 21:44:00
tags: Python
categories: Python
description: Python中的super()方法有什么用？如何用它来初始化父类属性
---

# 描述
super() 函数是用于调用父类(超类)的一个方法。
<!-- more -->
super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。

MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。

# 语法
以下是 super() 方法的语法:

super(type[, object-or-type])

Python3.x 和 Python2.x 的一个区别是: Python 3 可以使用直接使用 `super().xxx` 代替 `super(Class, self).xxx`.


在继承方法中，有以下两种子类继承方式，都可以完成父类继承
```python
class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        /* super(ChildB, self).__init__() */
        super().__init__()

ChildA()
ChildB()
```
哪一种好呢？

我推荐用super()完成子类继承。理由是如果你的子类有多个父类，父类又有父类的话，使用super()方法就可以顺序继承了。
