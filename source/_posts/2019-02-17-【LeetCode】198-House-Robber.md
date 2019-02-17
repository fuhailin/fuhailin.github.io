---
title: 【LeetCode】House Robber
date: 2019-02-17 14:40:31
tags: [CPP,LeetCode,Dynamic Programming]
categories: 数据结构与算法
top:
---
# 198. House Robber
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。

<!-- more -->

示例 1:

    输入: [1,2,3,1]
    输出: 4
    解释: 偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
         偷窃到的最高金额 = 1 + 3 = 4 。
示例 2:

    输入: [2,7,9,3,1]
    输出: 12
    解释: 偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
         偷窃到的最高金额 = 2 + 9 + 1 = 12 。

这是一题典型的动态规划问题，有点类似于背包问题。动态规划问题大多数可以按照以下的步骤来一步步优化：
 1. Find recursive relation
 2. Recursive (top-down)
 3. Recursive + memo (top-down)
 4. Iterative + memo (bottom-up)
 5. Iterative + N variables (bottom-up)

## Step 1. 找出 recursive 关系.

以上面的题为例，Robber有两个选项：a)要么打劫当前的房屋`i`，b)要么不打劫`i`。
如果选择a)那意味着他不能打劫邻居`i-1`但是可以选择`i-2`；
如果选择b)，Robber可以选择打劫邻居`i-1`和接下来的所有房屋。
所以劫匪为了所得最大化可以归结为考虑比较以下两种形式：
 - 当前的房屋`i`的所得 + 之前所得
 - 之前所得

`rob(i) = max( rob(i - 2) + currentHouseValue, rob(i - 1) )`
## Step 2. Recursive (top-down)
将上面的关系转换为下面的C++代码：
```cpp
public:
  int rob(vector<int> &nums)
  {
      return rob_brute_force(nums, nums.size() - 1);
  }

private:
  int rob_brute_force(vector<int> &nums, int i)
  {
      if (i < 0)
          return 0;
      return max(rob_brute_force(nums, i - 2) + nums[i], rob_brute_force(nums, i - 1));
  }
```
但是这个算法将处理同一个`i`多次，具有重叠子问题，可以被优化。

## Step 3. Recursive + memo (top-down).
用空间换时间的方法来优化重叠子问题，就是用一个“备忘录”将子问题`i`的结果记录下来。
```cpp
public:
  vector<int> memo;
  int rob(vector<int>& nums) {
      memo = vector<int>(nums.size() + 1, -1);
      return rob(nums, nums.size() - 1);
  }
private:
  int rob(vector<int> &nums, int i)
  {
      if (i < 0)
          return 0;
      if (memo[i] >= 0)
          return memo[i];
      int result = max(rob(nums, i - 2) + nums[i], rob(nums, i - 1));
      memo[i] = result;
      return result;
  }
```

## Step 4. Iterative + memo (bottom-up)

```cpp
int rob(vector<int> &nums)
{
    if (nums.size() == 0)
        return 0;
    vector<int> memo = vector<int>(nums.size() + 1);
    memo[0] = 0;
    memo[1] = nums[0];
    for (int i = 1; i < nums.size(); i++)
    {
        int val = nums[i];
        memo[i + 1] = max(memo[i], memo[i - 1] + val);
    }
    return memo[nums.size()];
}
```

## Step 5. Iterative + 2 variables (bottom-up)

```cpp
int rob(vector<int> &nums)
{
    if (nums.size() == 0)
        return 0;
    int prev1 = 0;
    int prev2 = 0;
    for (auto num : nums)
    {
        int tmp = prev1;
        prev1 = max(prev2 + num, prev1);
        prev2 = tmp;
    }
    return prev1;
}
```
# 213.House Robber II
你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都围成一圈，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你在不触动警报装置的情况下，能够偷窃到的最高金额。

这个题唯一变化的一点就是房子不再是一排，而是一圈。

House Robber II可以被分解成两个简单的House Robber问题：
 1. Rob houses 0 to n - 2;
 2. Rob houses 1 to n - 1.
