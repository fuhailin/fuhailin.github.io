---
title: 【LeetCode】53. 最大子序和
date: 2018-12-27 10:26:50
tags: [LeetCode,CPP,Dynamic Programming,分治法]
categories: 数据结构与算法
top:
mathjax: true
---

题目描述：
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

示例:
> 输入: [-2,1,-3,4,-1,2,1,-5,4],
> 输出: 6
> 解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

<!--more-->

# 暴力破解法
思路：遍历所有可能的子序列组合，得到最大的子序列和`max(nums[i:j])`

```cpp
int maxSubArray(vector<int> &nums)
{
    int maxsum = 0x80000000;
    for (int i = 0; i < nums.size(); i++)
    {
        for (int j = i; j < nums.size(); j++)
        {
            int tempsum = 0;
            for (int k = i; k <= j; k++)
            {
                tempsum = tempsum + nums[k];
            }
            if (tempsum > maxsum)
                maxsum = tempsum;
        }
    }
    return maxsum;
}
```
时间复杂度：$O(N3)$

# 优化的暴力破解法
观察到上面的计算过程中，`nums[0:i]`和的计算过程与`nums[0:i+1]`和的计算过程只相差一个数`nums[i+1]`，因此`sum(nums[0:i+1])`可以简化为`sum(nums[0:i])+nums[i+1]`

```cpp
int maxSubArray(vector<int> &nums)
{
    int maxsum = 0x80000000;
    for (int i = 0; i < nums.size(); i++)
    {
        int tempsum = 0;
        for (int j = i; j < nums.size(); j++)
        {
            tempsum = tempsum + nums[j];
            if (tempsum > maxsum)
                maxsum = tempsum;
        }
    }
    return maxsum;
}
```
时间复杂度：$O(N2)$

# 分治法

该方法采用一种“分治”策略。其想法就是把问题分成两个大致相等的子问题，然后递归地对它们求解，这是“分”的阶段。“治”阶段就是将两个子问题的解修补到一起并可能再做些少量的附加工作，最后得到整个问题的解。

在我们的例子中，最大子序列的和只可能出现在3个地方：

 1. 出现在输入数据的左半部分
 2. 出现在输入数据的右半部分
 3. 跨越输入数据的中部而位于左右两个部分

前两种情况可以递归求解，第三种情况的最大和可以通过求出前半部分（包含前半部分的最后一个元素）的最大和以及后半部分（包括后半部分的第一个元素）的最大和，再将二者相加得到。作为例子，考虑以下输入：

```
-----------------------------------------
    前半部分           后半部分
-----------------------------------------
-2, 11, 8, -4,    -1, 16, 5, 0
-----------------------------------------

```
其中，前半部分的最大子序列和为19（A2~A3），而后半部分的最大子序列和为21（A6～A7）。前半部分包含其最后一个元素的最大和是15（A2～A4），后半部分包含第一个元素的最大和是20（A5～A7）。因此，跨越这两部分的这个子序列才是拥有最大和的子序列，和为15+20=35（A2～A7）。于是出现了下面这种算法：

```cpp
#include <algorithm>
int divide(vector<int> &nums, int left, int right)
{
    if (left == right)
        return nums[left];
    int center = (left + right) / 2;
    int maxLeftSum = divide(nums, left, center);
    int maxRightSum = divide(nums, center + 1, right);

    int leftBorderSum = 0x80000000, tmpleft = 0;
    for (int i = center; i >= left; i--)
    {
        tmpleft = tmpleft + nums[i];
        if (tmpleft > leftBorderSum)
            leftBorderSum = tmpleft;
    }

    int rightBorderSum = 0x80000000, tmpright = 0;
    for (int i = center + 1; i <= right; i++)
    {
        tmpright = tmpright + nums[i];
        if (tmpright > rightBorderSum)
            rightBorderSum = tmpright;
    }
    return max({maxLeftSum, maxRightSum, leftBorderSum + rightBorderSum});
}
```
分治法算法复杂度分析：

算法的递推关系：$T(n)=2*T(n/2) + cn$，c为常数

若$n = 2 ^ { k }$ ，则有
$$
\begin{array} { l } { T ( n ) = 2 \cdot T \left( \frac { n } { 2 } \right) + c \cdot n } \\
{ = 2 \cdot \left( 2 \cdot T \left( \frac { n } { 4 } \right) + c \cdot \frac { n } { 2 } \right) + c \cdot n = 4 T \left( \frac { n } { 4 } \right) + 2 c \cdot n } \\
{ = 4 \left( 2 \cdot T \left( \frac { n } { 8 } \right) + c \cdot \frac { n } { 4 } \right) + 2 c \cdot n = 8 T \left( \frac { n } { 8 } \right) + 3 c \cdot n } \\
{ = 8 \left( 2 \cdot T \left( \frac { n } { 16 } \right) + c \cdot \frac { n } { 8 } \right) + 3 c \cdot n = 16 T \left( \frac { n } { 8 } \right) + 4 c \cdot n } \\
{ = \cdots \ldots } \\ { = 2 ^ { k } T ( 1 ) + k c \cdot n = a n + c n \log _ { 2 } n } \end{array}
$$

时间复杂度：$O(NlogN)$

# 动态规划

-具有最优子结构，和重叠子问题， 动态规划的算法思路：

最大连续子序列和只可能是以位置0～n-1中某个位置结尾。当遍历到第i个元素时，判断在它前面的连续子序列和是否大于0，如果大于0，则以位置i结尾的最大连续子序列和为元素i和前门的连续子序列和相加；否则，则以位置i结尾的最大连续子序列和为元素i。

状态转移方程： sum[i]=max(sum[i-1]+a[i],a[i])

```cpp
int maxSubArray_DP(vector<int> &nums)
{
   int curMax = nums[0], allMax = nums[0];
   for (int i = 1; i < nums.size(); i++)
   {
      curMax = max(nums[i], curMax + nums[i]);
      allMax = max(allMax, curMax);
   }
   return allMax;
}
```

# 另一种解法

```cpp
int maxSubArray(vector<int> &nums)
{
    int res = nums[0];
    int sum = 0;
    for (int num : nums)
    {
        if (sum > 0)
            sum += num;
        else
            sum = num;
        res = max(res, sum);
    }
    return res;
}
```
