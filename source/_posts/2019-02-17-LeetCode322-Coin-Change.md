---
title: 【LeetCode】Coin Change
date: 2019-02-17 19:13:21
tags: [LeetCode,CPP,Dynamic Programming]
categories: 数据结构与算法
top:
mathjax: true
---
# 322. Coin Change

给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。
<!-- more -->
示例 1:

    输入: coins = [1, 2, 5], amount = 11
    输出: 3
    解释: 11 = 5 + 5 + 1
示例 2:

    输入: coins = [2], amount = 3
    输出: -1
说明:
你可以认为每种硬币的数量是无限的。


## Approach #1 (Brute force) [Time Limit Exceeded]
上面的问题可以建模成如下的最优化问题：
$$
\min_{x}\sum_{i=0}^{n-1} {x_{i}} ,{ \text { subject to } \sum_{i=0}^{n-1} {x_{i}\ast c_{i}}}
$$
其中$S$是总额，$c_{i}$是第$i$种硬币，$x_{i}$是第$i$种硬币$c_{i}$在找零$S$的数量。很容易得出判断$x_{i} = [0,\frac{S}{c_{i}}]$.
贪心算法每次会选取可能的最大面值来实现硬币总数最少。（并不能保证找出最优解。）

## Approach #2 (Dynamic programming - Top down) [Accepted]
假设$F(S)$表示找零$S$元需要的最少硬币数

## Approach #3 (Dynamic programming - Bottom up) [Accepted]
```cpp
int coinChange(vector<int> &coins, int amount)
{
    if (amount == 0 || coins.size() == 0)
        return 0;
    vector<int> dp(amount + 1, MAX_Integer);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++)
    {
        for (auto coin : coins)
        {
            if ((i - coin) == 0)
                dp[i] = 1;
            else if ((i - coin) > 0)
            {
                dp[i] = min(dp[i], dp[i - coin] + 1);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```



https://forum.letstalkalgorithms.com/t/coin-change-leetcode/394
