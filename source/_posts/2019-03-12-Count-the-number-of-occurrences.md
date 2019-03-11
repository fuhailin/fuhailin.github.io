---
title: 统计数组中各元素出现次数
date: 2019-03-12 00:36:03
tags: [CPP,LeetCode]
categories: 数据结构与算法
top:
---
# 问题描述：

 * 给定一个整数数组a，长度为N，元素取值范围为[1,N]。
 * 统计各个元素出现的次数，要求时间复杂度为O(N)，空间复杂度为O(1)。
 * 可以改变原来数组结构。

<!-- more -->

思路：

 * 从第一个元素开始遍历，每遍历到一个元素，将（该元素值 - 1 记为index）作为一个下标值，令该下标对应的元素值为元素 index+1出现的次数。
 * 若下标index为负值，说明该元素已经处理过，跳过；
 * 判断，若a[index]为正，则赋初值-1；若为负，则执行减1操作。
 * 最后，数组中存储的元素即为统计次数，而该元素对应的下标+1即为元素值。
{% ghcode https://github.com/fuhailin/show-me-cpp-code/blob/master/algorithm/Count-the-number-of-occurrences.cpp %}
