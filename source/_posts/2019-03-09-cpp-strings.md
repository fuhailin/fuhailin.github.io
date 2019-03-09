---
title: C++ 字符串
date: 2019-03-09 16:40:13
tags: [CPP]
categories: C++
top:
---

C++ 提供了以下两种类型的字符串表示形式：
 - **C 风格字符串**
 - **C++ 引入的 string 类类型**

<!-- more -->

# C 风格字符串

C 风格的字符串起源于 C 语言，并在 C++ 中继续得到支持。字符串实际上是使用 null 字符 '\0' 终止的一维字符数组。因此，一个以 null 结尾的字符串，包含了组成字符串的字符。

下面的声明和初始化创建了一个 "Hello" 字符串。由于在数组的末尾存储了空字符，所以字符数组的大小比单词 "Hello" 的字符数多一个。

`char greeting[6] = {'H', 'e', 'l', 'l', 'o', '\0'};`


依据数组初始化规则，您可以把上面的语句写成以下语句：

`char greeting[] = "Hello";`

以下是 C/C++ 中定义的字符串的内存表示：
![](http://www.runoob.com/wp-content/uploads/2014/08/string_representation.jpg)
其实，您不需要把 `null` 字符放在字符串常量的末尾。C++ 编译器会在初始化数组时，自动把 `'\0'` 放在字符串的末尾。让我们尝试输出上面的字符串
```c
#include <iostream>
using namespace std;
int main ()
{
   char greeting[6] = {'H', 'e', 'l', 'l', 'o', '\0'};
   cout << "Greeting message: ";
   cout << greeting << endl;
   return 0;
}
```

C++ 中有大量的函数用来操作以 null 结尾的字符串：

### strcpy(s1, s2);
 复制字符串 s2 到字符串 s1。
### strcat(s1, s2);
 连接字符串 s2 到字符串 s1 的末尾。
### strlen(s1);
 返回字符串 s1 的长度。
### strcmp(s1, s2);
 如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回值小于 0；如果 s1>s2 则返回值大于 0。
### strchr(s1, ch);
 返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置。
### strstr(s1, s2);
 返回一个指针，指向字符串 s1 中字符串 s2 的第一次出现的位置

*******************

# string类

C++ 标准库提供了 string 类类型，支持上述所有的操作，另外还增加了其他更多的功能。我们将学习 C++ 标准库中的这个类，现在让我们先来看看下面这个实例：

现在您可能还无法透彻地理解这个实例，因为到目前为止我们还没有讨论类和对象。所以现在您可以只是粗略地看下这个实例，等理解了面向对象的概念之后再回头来理解这个实例。

string类提供了一系列针对字符串的操作，比如：

### 获取字符串长度
 - **str.length()**: `int len = "fuhailin".length();`// len = 8
 - **str.size()**: `int len = "fuhailin".size();` // len = 8

### 字符串连接
 - **append()**: `str1.append(str2);` //在字符串的末尾添加字符
 - **+** 连接符 : `str3 = str1 + str2;` // 连接 str1 和 str2

 ```cpp
 #include <string>
 string str = "fuhailin";
 str.append(".github"); // str = "fuhailin.github"
 str = str + ".io"; // str = "fuhailin.github.io"
 ```

### 字符串查找

 **2. find()** -- 在字符串中查找字符串
```cpp
#include <iostream>
#include <string>
#include <typeinfo>
using namespace std;
int main()
{
	string str = "fuhailin";
	string::size_type position1, position2;
	position1 = str.find('a');
	position2 = str.find("ia");
	if (position1 != str.npos)  //如果没找到，返回一个特别的标志c++中用npos表示，我这里npos取值是4294967295，
		printf("position is : %d\n", position1);
	else
		printf("Not found the flag\n");
	if (position2 != str.npos)
		printf("position is : %d\n", position2);
	else
		printf("Not found the flag\n");
	cout << typeid(position1).name() << '\t' << typeid(position2).name() << endl;
	return 0;
}
```
> position is : 3
> Not found the flag
> unsigned int    unsigned int

### 字符串插入
`string& string::insert (size_type idx, const string& str)`
```cpp
string str = "fuhailin";
str.insert(5, 5, '%'); // str = "fuhai%%%%%lin"
```

### 字符串替换
`string& string::replace (size_t pos, size_t len, const string& str)`
```cpp
string str = "fuhailin";
str.replace(5, 1, "Hello"); // str = "fuhaiHelloin"
```

### 字符串截取
`string substr (size_t pos = 0, size_t len = npos) const;`
```cpp
string str = "fuhailin";
string str1 = str.substr(5, 2);
// str = "fuhailin"
// str1 = "li"
```
