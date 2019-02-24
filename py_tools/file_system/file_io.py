#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:57:31 2018
basing on https://www.computerhope.com/issues/ch001721.htm
@author: ddengca@gmail.com
"""

'''
open(filename, mode)
mode: 
'r': Read (Default). Opens a file for reading; error if the file doesn't exist
'a': Append. Opens a file for appending; creates the file if it doesn't exist
'w': Write. Opens a file for writing; creates the file if it doesn't exist
'x': Create. Creates the specified file; returns an error if the file exist
'+': open a disk file for updating (reading and writing)

't': Text mode (Default)
'b': Binary mode (e.g. images)

For Python 3, encoding is added, like:
open(filename, mode, encoding='utf-8')
The similar command in Python 2 is io.open or codecs.open
'''


def read_text_file(filename):
    in_file = open(filename, 'rt')  # open file in read-text mode
    contents = in_file.read()   # read into a string variable
    in_file.close()
    print(contents)


def read_text_file_using_with(filename):
    with open(filename, 'rt') as in_file:
        contents = in_file.read()
    print(contents)


def read_text_file_using_with_line(filename):
    with open(filename, 'rt') as in_file:
        for line in in_file:
            print(line, end='') # to remove the newline of print()


def read_text_file_using_with_line_into_variable(filename):
    lines = []
    with open(filename, 'rt') as in_file:
        for line in in_file:
            lines.append(line)
    print(lines)
