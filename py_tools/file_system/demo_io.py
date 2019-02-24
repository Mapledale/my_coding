#!/usr/bin/env python
# _*_ coding: utf-8 _*_

'''
About I/O, file system
'''

import os
import json
import cPickle as pickle

# for <= Python 2.7
uni = u'string'
print(type(uni)) # <type 'unicode'>
# encode to utf-8
utf8 = uni.encode('utf-8')
print(type(utf8)) # <type 'str'>

pathname = os.getcwd()
filename = 'example.txt'
file = os.path.join(pathname, filename)

string = 'example string'
dic_ex = {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}

# write string to a file
with open(file, 'w+') as f:
    f.write(string)

# to write a dic to a file
with open(file, 'w+') as f:
    for k, v in dic_ex.items():
        f.write(k + ': ' + v + '\n')

    # or convert the dic into string
    f.write(json.dumps(dic_ex))
    
    # or serialize the dic
    f.write(pickle.dumps(dic_ex))
