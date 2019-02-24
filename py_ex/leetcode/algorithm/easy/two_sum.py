#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
Given an array of integers, return indices of the two numbers such that
they add up to a specific target.

You may assume that each input would have exactly one solution,
and you may not use the same element twice.

Example:

Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].
"""


class Solution:
    def twoSum_0(self, nums: 'List[int]', target: 'int') -> 'List[int]':
        """ Brute-force search
        Loop through each element xx and find if there is another value
        that equals to target - x

        Time complexity : O(n^2)
        Space complexity : O(1)
        """
        i = 0
        while i < len(nums) - 1:
            j = i + 1
            target_j = target - nums[i]
            while j < len(nums):
                if nums[j] == target_j:
                    return [i, j]
                j += 1
            i += 1

    def twoSum_1(self, nums: 'List[int]', target: 'int') -> 'List[int]':
        """ Hash table
        Build a hash table (dictionary) for the list
        then search the dictionary is much faster than for the list

        corner cases:
        [3, 2, 4], 6: should return [1, 2] instead of [0, 0]
        [3, 3], 6: should return [0, 1] instead of [0, 0]

        Time complexity : O(n)
        Space complexity : O(n)
        """
        nums_dic = {}
        for i, v in enumerate(nums):
            if target - v in nums_dic:
                return [i, nums_dic[target - v]]
            nums_dic[v] = i


l = [3, 3]
t = 6
my_s = Solution()
rst = my_s.twoSum_1(l, t)
print(rst)
