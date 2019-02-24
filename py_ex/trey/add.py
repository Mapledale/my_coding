# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 13:59:29 2019

@author: ZhiD
"""


def add_list(l1, l2):
    ret = []
    for n in range(len(l1)):
        num = l1[n] + l2[n]
        ret.append(num)
    return ret


def add(m1, m2):
    ret = []
    for n in range(len(m1)):
        l = add_list(m1[n], m2[n])
        ret.append(l)
    return ret
