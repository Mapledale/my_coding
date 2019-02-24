#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-08 14:46:54
# @Author  : David Deng (ddengca@gmail.com)
# @Version :
'''
This script reads the content of file_r, readlines().
For each line starts with a specific string,
(leading white space stripped), write to another file.
'''
import sys

file_r = '/home/user/.virtualenvs/rfw/lib/python2.7/' + \
    'site-packages/NEDdriver/__init__.py'
file_w = '/home/user/Documents/all_methods.txt'


def input_file_r():
    file_r = str(input('Please input the file name (with path) to read: '))
    return file_r


def input_file_w():
    file_w = str(input('Please input the file name (with path) to write: '))
    return file_w


def input_target():
    tgt = str(input('Please input the string to search: '))
    return tgt


def get_all_methods(file_r, file_w, tgt):
    with open(file_r, 'r') as f_r:
        cont = f_r.readlines()

    with open(file_w, 'w') as f_w:
        for line in cont:
            line_new = line.lstrip()
            if line_new.startswith(tgt):
                f_w.write(line_new)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        file_r = input_file_r()
        file_w = input_file_w()
        tgt = input_target()
    elif len(sys.argv) == 2:
        file_r = sys.argv[1]
        file_w = input_file_w()
        tgt = input_target()
    elif len(sys.argv) == 3:
        file_r = sys.argv[1]
        file_w = sys.argv[2]
        tgt = input_target()
    elif len(sys.argv) == 4:
        file_r = sys.argv[1]
        file_w = sys.argv[2]
        tgt = sys.argv[3]
    else:
        sys.exit('Too many arguments!')

    get_all_methods(file_r, file_w, tgt)
