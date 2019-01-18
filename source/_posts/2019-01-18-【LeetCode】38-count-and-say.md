---
title: 【LeetCode】38.count-and-say
date: 2019-01-18 13:24:16
tags: [LeetCode,C++,递归]
categories: 数据结构与算法
top:
---

## 题目描述
The count-and-say sequence is the sequence of integers with the first five terms as following:

    1.     1
    2.     11
    3.     21
    4.     1211
    5.     111221
1 is read off as `"one 1"` or 11.
11 is read off as `"two 1s"` or 21.
21 is read off as `"one 2, then one 1"` or 1211.

Given an integer n where 1 ≤ n ≤ 30, generate the nth term of the count-and-say sequence.

Note: Each term of the sequence of integers will be represented as a string.

## 解题思路

1：“1”
2：一个“1”->"11"
3: 两个“1”->"21"
4: 一个“2”，一个“1”->"1211"
5: 一个“1”，一个“2”，两个“1”->"111221"
6: 3个“1”，两个“2”，一个“1”->"312211"
。。。
思路就是每个数字把前一个数字的表达式数出来

##
因为Python对字符串的处理比较方便，这里先实现了Python的递归方法：
{% ghcode https://github.com/fuhailin/show-me-python-code/blob/master/leetcode/38.count-and-say.py %}

C++的实现：

{% ghcode https://github.com/fuhailin/show-me-cpp-code/blob/master/LeetCode/38.count-and-say.cpp %}
