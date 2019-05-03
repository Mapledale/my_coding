#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""
Given two integers n and k,
return all possible combinations of k numbers out of 1 ... n.

Example:
Input: n = 4, k = 2
Output:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        assert n >= k, 'wrong input: n should not be less than k'

        ret = []
        while True:
            ele = []
            for i in range(k):
                
