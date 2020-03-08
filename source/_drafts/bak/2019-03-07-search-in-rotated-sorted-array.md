---
title: 【LeetCode】33. Search in Rotated Sorted Array
date: 2019-03-07 21:46:47
tags: [LeetCode,CPP]
categories: 数据结构与算法
top:
---
Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.

(i.e., `[0,1,2,4,5,6,7]` might become `[4,5,6,7,0,1,2]`).

You are given a target value to search. If found in the array return its index, otherwise return -1.

You may assume no duplicate exists in the array.

Your algorithm's runtime complexity must be in the order of O(log n).

Example 1:

> Input: nums = [4,5,6,7,0,1,2], target = 0
> Output: 4

Example 2:

> Input: nums = [4,5,6,7,0,1,2], target = 3
> Output: -1

<!-- more -->
# 思路一：寻找旋转点
找到旋转点之后，旋转点两边的数组就都是有序的，于是判断target在哪边，就可以直接用二分查找快速找到了。

怎么找到旋转点？

# 递归 + 二分查找

二分查找的好处在于可以减少一半的搜索空间，对旋转矩阵，二分查找将矩阵分为两部分，其中必然一部分有序，一部分**可能**无序。
例如对于旋转数组`[4, 5, 6, 7, 0, 1, 2, 3]`，以二分的方式将旋转数组分成两部分`[4, 5, 6, 7]` `[0, 1, 2, 3]`，这两部分都是有序的。
但是对于旋转数组`[5, 6, 7, 0, 1, 2, 3, 4]`，以二分的方式将旋转数组分成两部分`[5, 6, 7, 0]` `[1, 2, 3, 4]`,这两部分只有右边是有序的。
于是对于有序的那部分我们可以直接用二分查找快速搜索target，无序的那部分再以上面的方式划分，最终会分成右边都是有序的形式（哪怕只剩下一个值）

怎么判断划分出来的那一部分是不是有序呢？
观察到划分出来的那部分首元素肯定要小于划分点，而无序的那部分因为旋转过了，所以首元素要小于划分点；例如：划分点索引为3使，4<7, 左边肯定是有序；5>0，左边肯定是无序的，则右边为有序。于是我们可以归纳出判断数组是否有序的条件：`nums[left] <= nums[mid]`则左边有序，否则右边有序。

对于找出了有序的部分，我们首先要判断target在不在区间中：`nums[left]<=target && nums[mid]>=target`，在此区间范围内再二分搜索。

根据上面的思路，我们可以写出如下的代码：
```cpp
class Solution
{
  public:
    int search(vector<int> &nums, int target)
    {
        if (nums.empty())
            return -1;
        else
            return help(nums, target, 0, nums.size() - 1);
    }

  private:
    int help(vector<int> &vec, int target, int left, int right)
    {
        while (left <= right)
        {
            int left = -1, right = -1;
            int rot = (left + right) / 2;
            if (vec[left] <= vec[rot])
            {
                if (vec[rot] >= target && vec[left] <= target)
                    left = binary_search(vec, target, left, rot);
                else
                    right = help(vec, target, rot + 1, right);
            }
            else
            {
                if (vec[rot + 1] <= target && vec[right] >= target)
                    right = binary_search(vec, target, rot + 1, right);
                else
                    left = help(vec, target, left, rot);
            }

            if (left == -1 && right == -1)
                return -1;
            else
            {
                if (left == -1)
                    return right;
                else
                    return left;
            }
        }
        return -1;
    }

    int binary_search(vector<int> &vec, int target, int left, int right)
    {
        while (left <= right)
        {
            int mid = (left + right) / 2;
            if (vec[mid] == target)
                return mid;
            else if (vec[mid] < target)
                left = mid + 1;
            else
                right = mid - 1;
        }
        return -1;
    }
};
```
时间复杂度分析：最好的情况下O(1)，最坏的情况下O(n)，平均时间复杂度O(n/2).
空间复杂度分析：由于存在递归调用，会使用栈空间，空间复杂度O(n/2).
上述解决方案递交到LeetCode上面AC但是成绩并不高![](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/2019-03-08-004047.png)
而且写法也较为啰嗦，存在很大的优化空间。
