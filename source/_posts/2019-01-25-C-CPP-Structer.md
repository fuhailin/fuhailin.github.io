---
title: C/C++中结构体的定义以及实例化
date: 2019-01-25 20:58:02
tags: [CPP]
categories: C++
top:
description: 如何在C/C++中定义结构体，以及进行实例化
---

# Difference between C structures and C++ structures
在C\++中，struct和class基本上是一个东西，除了struct默认是public权限，class默认是private权限。
在C和C++结构体之间还有重要的区别：
 1. 结构体中的成员函数：在C的结构体中不能有成员函数，在C++的结构体中可以有成员函数和数据成员。
 2. 直接初始化：在C中不能直接初始化结构体的数据成员，但是在C++中可以。
```c
// C program to demonstrate that direct member initialization is not possible in C
#include <stdio.h>
struct Record {
    int x = 7;  # Compiler Error
};
int main()
{
    struct Record s;
    printf("%d", s.x);
    return 0;
}
```

```cpp
// CPP program to initialize data member in c++
#include <iostream>
using namespace std;
struct Record {
    int x = 7;
};
int main()
{
    Record s;
    cout << s.x << endl;
    return 0;
}
```

 3. 使用struct关键字：在C中，必须使用struct关键字声明一个结构体变量；在C++中，struct关键字并不是必须的。
 4. 静态成员：C中不能有静态成员，但C++中是可以的。
```c
// C program with structure static member
struct Record {
    static int x;
};
/* 6:5: error: expected specifier-qualifier-list
   before 'static'
     static int x;
     ^*/
```
```cpp
// C++ program with structure static member
struct Record {
    static int x;
};
```
 5. 结构体中的Constructor creation：在C的结构体中不能有constructor，但是C++ 中可以有。

```cpp
// CPP program to initialize data member in c++
#include <iostream>
using namespace std;
struct Student {
    int roll;
    Student(int x)
    {
        roll = x;
    }
};
int main() // Driver Program
{
    struct Student s(2);
    cout << s.roll;
    return 0;
}
```
 6. sizeof操作：在C中对一个空的结构体执行`sizeof`将返回**0**，在C++中则是**1**.

```c
// empty structure
struct Record {
};
```
 7. 数据隐藏: C中的结构体不允许数据隐藏的概念，但是C\++中却允许；因为C\++是一个面向对象的语言而C并不是。
 8. 访问修饰符Access Modifiers：C结构体不支持访问修饰符, C++语言中内置了结构体对访问修饰符的支持。

 # typedef struct VS struct definitions

 1.如果使用typedef来定义结构体时：型如typedef struct aaa { ..}bbb;
 其中aaa是可以省略的，那么用bbb（如果有的话）来定义一个结构体变量时，可以直接用bbb xxx;就行。但用aaa来定义一个结构体变量时，则需要使用struct aaa xxx;
 2.不使用typedef来定义结构体时，声明该类型变量都需要加上struct，即struct aaa xxx;

# 结构体的实例化malloc() vs new

为了更方便地理解我们以单链表节点为例定义一个结构体：
```c
struct variable
{
      int data;
      struct variable *next;
};
```
当声明一个结构体的指针时：
```cpp
struct variable *ptr;
```
结构体被定义，内存被分配(在32位机中4字节的内存分配给了这个指针)。而且`ptr`是一个automatic变量，也就是说它所在的内存位于栈区并且它的初始值为`garbage`(无效地址)。假设`ptr`目前的值是`0x1000`，如果你尝试**de-reference**间接引用这个指针，执行以下的操作会发生什么？
```cpp
ptr->data = 30; //(access to 0x1000)
ptr->next = NULL; //(access to 0x1004
```
CPU会尝试根据虚拟地址来访问物理内存地址，而在cache中又没有找到这个地址时，CPU会继续向操作系统请求这个地址。

但是上述的进程不见得在地址`0x1000`或`0x1004`有一个有效的(虚拟的)内存。所以操作系统经过检查然后告诉进程这是一个无效的内存访问。于是**Segmentation Fault**错误发生，操作系统杀掉了这个无效的内存访问。

为了使上述这个指针有用，我们应该把它指向一个有效的内存地址。在C语言中使用**malloc**函数是为指针指向一个有效地址的合理方法：
```c
ptr = (struct variable *)malloc(sizeof(struct variable));
```
而在C++中我们可以根据C++特有的动态内存分配来实例化一个对象：
```cpp
variable *ptr = new variable();
```
 1. new/delete是C++操作符，malloc/free是C/C++函数。
 2. 使用new操作符申请内存分配时无须指定内存块的大小，编译器会根据类型信息自行计算，而malloc则需要显式地指出所需内存的大小。
 3. new/delete会调用对象的构造函数/析构函数以完成对象的构造/析构，而malloc只负责分配空间。
 4. new 操作符内存分配成功时，返回的是对象类型的指针，类型严格与对象匹配，无须进行类型转换，故new是符合类型安全性的操作符。而malloc内存分配成功则是返回void * ，需要通过强制类型转换将 void* 指针转换成我们需要的类型。
 5. 效率上：malloc的效率高一点，因为只分配了空间。
 6. operator new /operator delete 可以被重载，而 malloc/free 并不允许重载。

Reference：
 1. [](https://www.quora.com/Is-it-necessary-to-use-malloc-for-creating-a-structure-pointer-variable-What-happens-if-I-just-declare-struct-variable-*ptr-instead-of-struct-variable-*ptr-struct-variable-*-malloc-sizeof-struct-variable-and-try-to-access-the-structure-members)
