---
title: 【剑指Offer】24. 二叉搜索树的后序遍历
date: 2018-11-09 23:32:06
tags: C++
categories: 编程
---

题目描述：
输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历的结果。如果是则输出Yes,否则输出No。假设输入的数组的任意两个数字都互不相同。

思路：
1、序列的的最后一个数字是根节点
2、二叉搜索树左子树的节点都比根节点小，右子树的节点都比根节点大。
![在这里插入图片描述](/uploads/20181020211958624.png)

<!--more-->

C++递归与非递归实现代码：

```cpp
#include <iostream>
#include <vector>
#include <set>

using namespace std;

class Solution
{
  private:
	//参数为引用，不为值传递是为了防止拷贝构造函数的无限递归，最终导致栈溢出。
	bool judge(vector<int> &sequence, int left, int right)
	{
		if (left == right)
			return true;
		int mid = left;
		while (sequence[mid] < sequence[right] && mid < right)
		{
			mid++;
		}
		int tmp = mid;
		while (sequence[tmp] > sequence[right] && tmp < right)
		{
			tmp++;
		}
		if (tmp < right)
		{
			return false;
		}
		if (mid == left || mid == right)
		{
			return judge(sequence, left, right - 1);
		}
		else
		{
			return judge(sequence, left, mid - 1) && judge(sequence, mid, right - 1);
		}
	}

  public:
	bool VerifySquenceOfBST(vector<int> sequence)
	{
		int size = sequence.size();
		if (0 == size)
			return false;

		int i = 0;
		while (--size)
		{
			while (sequence[i] < sequence[size])
			{
				i++;
			}
			//while (sequence[i++] < sequence[size]);
			//while (sequence[i++] > sequence[size]);
			while (sequence[i] > sequence[size])
			{
				i++;
			}

			if (i < size)
				return false;
			i = 0;
		}
		return true;
	}

	bool VerifySquenceOfBSTRecursize(vector<int> sequence)
	{
		int length = sequence.size();
		if (length == 0)
			return false;
		return judge(sequence, 0, length - 1);
	}
};

int main()
{
	vector<int> tree1{5, 7, 6, 9, 11, 10, 8};
	vector<int> tree2{4, 8, 6, 12, 16, 14, 10};
	vector<int> tree3{2, 1, 7, 4, 6, 5, 3};
	Solution solution = Solution();
	bool tmp = solution.VerifySquenceOfBST(tree3);
	cout << boolalpha << tmp << endl;
	return 0;
}

```

