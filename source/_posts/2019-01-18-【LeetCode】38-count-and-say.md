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
```py
class Solution:
    def countAndSay(self, n):
        """
        :type n: int
        :rtype: str
        """
        result = "1"
        for i in range(1, n):
            result = self.getNext(result)
        return result

    def getNext(self, last):
        result = str()
        count = 1
        i = 0
        while i < len(last):
            # for i in range(len(last), 1):
            if i == (len(last)-1):
                result = result+str(count)+last[i]
                break
            while last[i] == last[i+1]:
                count += 1
                i += 1
                if(i+1 == len(last)):
                    break
            result = result+str(count)+last[i]
            count = 1
            i += 1
        return result


test = Solution().countAndSay(2)
print(test)
```
