#!/usr/bin/env python3
# _*_ coding: utf-8 _*_


filename = 'file.dat'
rst = {}

with open(filename, 'r') as f:
    for i, l in enumerate(f):
        count = l.count('[') - 1
        if count in rst:
            rst[count] += 1
        else:
            rst[count] = 1
        print('length of list @line%d = %d' % (i + 1, count))

for k in sorted(rst):
    print('number of list with length %s = %d' % (k, rst[k]))
