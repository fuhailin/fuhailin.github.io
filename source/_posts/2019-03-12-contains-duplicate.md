---
title: 【LeetCode】Contains Duplicate
date: 2019-03-12 00:07:36
tags: [CPP,LeetCode]
categories: 数据结构与算法
top:
description: 【LeetCode】Contains Duplicate：217. Contains Duplicate、219. Contains Duplicate II、220. Contains Duplicate III
---
# 217. Contains Duplicate

## 解法一、基于排序

对于给定的数组先排序然后再顺序查找有无重复，时间复杂度O(nlogn)。
{% ghcode https://github.com/fuhailin/show-me-cpp-code/blob/master/LeetCode/217.contains-duplicate.cpp 13 22 %}
这里直接使用了STL<algorithm>库中sort()函数，其STL的sort()底层算法，**数据量大时采用Quick Sort**，分段递归排序，一旦分段后的数据量小于某个门槛，为避免Quick Sort的递归调用带来过大的额外负荷，就改用**Insertion Sort**。如果**递归层次过深，还会改用Heap Sort**。
参考[详细解说 STL 排序(Sort)](http://www.cppblog.com/mzty/archive/2005/12/15/1770.html)

## 解法二、基于Hash表
将数组中的元素转换到Hash表当中时间复杂度O(n).
{% ghcode https://github.com/fuhailin/show-me-cpp-code/blob/master/LeetCode/217.contains-duplicate.cpp 24 28 %}
C++ STL中Hash Table对应的数据结构是<unordered_set>，查找某元素是否在unordered_set当中的方法是`const bool is_in = container.find(element) != container.end();`。**<unordered_set>底层对应的数据结构是红黑树**。

# 219. Contains Duplicate II

# 220. Contains Duplicate III
