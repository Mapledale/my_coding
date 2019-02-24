#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
Given an integer array nums, find the sum of the elements
between indices i and j (i ≤ j), inclusive.

Example:
Given nums = [-2, 0, 3, -5, 2, -1]
sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3

Note:
You may assume that the array does not change.
There are many calls to sumRange function.
"""


class NumArray:

    """ brute-force
    it could take very long time when calculate many times
    """
    def __init__(self, nums: List[int]):
        self.nums = nums

    def sumRange_0(self, i: int, j: int) -> int:
        sum = 0
        for idx in range(i, j + 1):
            sum += self.nums[idx]
        return sum

    """ cashing approach
        as the range sum will be calculated many times for a same list,
        it's better to save sum for each index in a dictionary
        then do a subtractoin each time
    """
    def __init__(self, nums: List[int]):
        self.sums = {}
        sum = 0
        for idx, val in enumerate(nums):
            sum += val
            self.sums[idx] = sum

    def sumRange_1(self, i: int, j: int) -> int:
        if i == 0:
            return self.sums[j]
        else:
            return self.sums[j] - self.sums[i - 1]

    """ optimized further
    the if statement can be remved by adding a psudo-index (-1)
    """
    def __init__(self, nums: List[int]):
        self.sums = {-1: 0}
        for idx, val in enumerate(nums):
            self.sums[idx] = self.sums[idx - 1] + val

    def sumRange(self, i: int, j: int) -> int:
        return self.sums[j] - self.sums[i - 1]
