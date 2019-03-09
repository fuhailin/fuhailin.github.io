---
title: Difference between the dot(.) and the arrow(->) operator in C++?
date: 2019-01-24 21:05:54
tags: C++
categories: C++
top:
---
structure.attribute
pointer->method
Use `->` when you have pointer. Use `.` when you have structure (class).
<!-- more -->
C++语言将箭头操作符（`->`）定义为间接引用(dereference)指针(pointer)的同义词，然后在该地址上使用(`.`)运算符。
例如：
如果你有一个对象`anObject`，和一个指针`aPointer`:
```cpp
SomeClass anObject = new SomeClass();
SomeClass *aPointer = &anObject;
```
为了使用其中一个对象方法，您可以dereference指针并对该地址执行方法调用：
```cpp
(*aPointer).method();
```
也可以用箭头操作符写成如下的形式：
```cpp
aPointer->method();
```
箭头操作符存在的主要原因是它缩短了一个非常常见的指针方法调用的拼写，因为你很容易忘记指针dereference周围的括号。
如果你忘记了括号，`(*aPointer).method();`就等价成了`*(aPointer.method());`，这肯定不是我们的目的。
