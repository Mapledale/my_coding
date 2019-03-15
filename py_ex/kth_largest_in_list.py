#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
for a given list of integers, find out the kth largest integer
here k <= n where n is the length of the given list

example:
list = [5, 2, -1, 4, 9, 3], k = 3
return: 4
"""


def kth_largest(l: 'List[int]', k: int) -> int:
    l_sorted = sorted(l)
    return l_sorted[-k]

my_list = [5, 2, -1, 4, 9, 3]
k = 3
print('kth largest is: %d' % kth_largest(my_list, k))
