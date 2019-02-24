#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
import pdb


def sorting(ori):
    for i, val in enumerate(ori):
        j = i + 1
        if j == len(ori):
            break
        # pdb.set_trace()
        while j < len(ori):
            if ori[i] > ori[j]:
                tmp = ori[i]
                ori[i] = ori[j]
                ori[j] = tmp
            j += 1
    return ori
