---
title: 三十六进制加法
date: 2019-03-05 23:57:24
tags: [CPP,LeetCode]
categories: 数据结构与算法
top:
---
**问题描述**
36进制由0-9，a-z，共36个字符表示，最小为’0’。 ‘0’、'9’对应十进制的0、9，‘a’、'z’对应十进制的10、35

例如：

 > '1b' 换算成10进制等于 1 * 36^1 + 11 * 36^0 = 36 + 11 = 47
 > 要求按照加法规则计算出任意两个36进制正整数的和
 > 如：按照加法规则，计算'1b' + '2x' = '48'
 >
要求：
不允许把36进制数字整体转为10进制数字，计算出10进制数字的相加结果再转回为36进制

<!-- more -->

**思路**
按照十进制的加法方法，满36向前进一位

C++实现代码：
{% ghcode https://github.com/fuhailin/show-me-cpp-code/blob/master/algorithm/36hex_calculation.cpp %}