---
title: >-
  C++ Error C2678: no operator found which takes a left-hand operand of type
  'const_ty'
date: 2019-01-29 18:24:36
tags: C++
categories: 数据结构与算法
top:
---
今天在Windows平台下面用Visual Studio编写C++程序时遇到了一个这样的错误：
> Severity	Code	Description	Project	File	Line	Suppression State
> Error	C2678	binary '<': no operator found which takes a left-hand operand of type 'const _Ty' (or there is no acceptable conversion)

<!-- more -->

error的定位指向了
`c:\program files (x86)\microsoft visual studio\2017\community\vc\tools\msvc\14.15.26726\include\xstddef`文件的`141`行。
起初看这个错误很奇怪，不知道是哪里代码有问题，后来一行一行测试代码，定位到这是包含自定义`struct`的`set`初始化时出错！于是我大概就明白了。

这里我构造了一个简单的例子来复现这个error, 尝试将struct `Edge`放入set中：
```cpp
#include <iostream>
#include <set>
using namespace std;
struct Edge
{
	int src, dest;
};

int main(int argc, char const *argv[])
{
	Edge edge = { 0,1 };
	set<Edge> edges = { edge };
	return 0;
}
```

C++ STL 中的`set`容器的特点是：
 1. set集合中不存在重复元素；
 2. set集合中的元素都为有序排列，不管插入的顺序如何；
 3. set不支持下标的操作。

所以插入set中元素需是可排序类型，上面我们定义的struct `Edge` CPP的比较运算`<`无法直接处理。解决办法就是**通过重载 `<` 运算符来支持对我们自定义的struct的比较**：
```cpp
#include <iostream>
#include <set>
using namespace std;
struct Edge
{
	int src, dest;
	// compare for order.
	bool operator <(const Edge& pt) const
	{
		return (src < pt.src) || ((!(pt.src < src)) && (dest < pt.dest));
	}
};

int main(int argc, char const *argv[])
{
	Edge edge = { 0,1 };
	set<Edge> edges = { edge };
	return 0;
}
```

References:

 1. [How to create std::set of structures](https://stackoverflow.com/questions/41648480/how-to-create-stdset-of-structures?rq=1)
 2. [How to have a set of structs in C++](https://stackoverflow.com/questions/5816658/how-to-have-a-set-of-structs-in-c)
