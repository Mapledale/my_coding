# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 10:47:08 2018
to handle the files in order to make them an ebook
@author: ZhiD
"""

import os
import re
from pathlib import Path


def add_html_tag(filename):
    '''
    to add html tag at the begining and end of a file
    '''
    filename_ori = filename + '_ori'
    os.rename(filename, filename_ori)
    with open(filename_ori, encoding='utf-8') as f_ori:
        f = open(filename, 'a', encoding='utf-8')
        f.write('<!doctype html>\n<html>\n<head></head>\n<body>\n')
        for line in f_ori:
            f.write(line)
        f.write('\n</body>\n</html>\n')
        f.close()


def change_filename():
    '''
    this is to change the filename using
    os.rename()
    '''
    file_name = {}
    for i in range(3, 14):
        filename_bef = 'part00%02d.html' %int(i)
        filename_aft = 'ch%02d.html' %int(i - 1)
        file_name[filename_bef] = filename_aft

    for fn_bef in file_name:
        os.rename(fn_bef, file_name[fn_bef])


def filename_trimmer(folder, pat, repl):
    '''
    This function is to trimmer the filename in a folder:
        remove the ending digits after -: abc12-345.x --> abc12.x
        remove the starting part in [] or (): [ab]abc12.x --> abc12.x

    folder: the folder to workon
    pat: the regex to match and sub
    repl: the string to replace pat
    '''

    for file in os.listdir(folder):
        p = Path(file)
        fname = p.stem

        if pat.match(fname):
            fname_new = pat.sub(repl, fname)
            p.rename(Path(p.parent, fname_new + p.suffix))


def replace_text(filename_old, filename_new, text_old, text_new):
    with open(filename_old, encoding='utf-8') as f_old:
        f_new = open(filename_new, 'w+', encoding='utf-8')
        for line in f_old:
            line = line.replace(text_old, text_new)
            f_new.write(line)
        f_new.close()

if __name__ == '__main__':
#    change_filename()
#    text_old = 'https://www.safaribooksonline.com/library/view/creating-apps-in/9781491947333/'
#    replace_text('index.html', 'index_new.html', text_old, '')
#    add_html_tag('ch06.html')
    '''
    for i in range(7, 13):
        filename = 'ch%02d.html' %int(i)
        add_html_tag(filename)
    '''
    folder = os.path.dirname(os.path.realpath(__file__))
    print('Start to trimmer names of files in folder %s...' %folder)
    s0 = r'\(.*\)-*'  # for '(ab2)--de23'
    s1 = r'\[.*\]-*'  # for '[ab2]--de23'
    pat0 = re.compile(s0 + '|' + s1)

    pat10 = re.compile(r'乔治·奥威尔-')
    repl10 = r'George Orwell - '
    pat11 = re.compile(r'贾雷德·戴蒙德：')
    repl11 = r'Jared Diamond - '
    pat12 = re.compile(r'马特·海格-')
    repl12 = r'Matt Haig - '
    pat13 = re.compile(r'许倬云-')
    repl13 = r'许倬云 - '
    pat14 = re.compile(r'普里莫·莱维-')
    repl14 = r'Primo Levi - '
    pat15 = re.compile(r'雷·布拉德伯里-')
    repl15 = r'Ray Bradbury - '

    pat2 = re.compile(r'(.+)(-+[0-9]+)$')  # to match '(ab2)--23'
    repl2 = r'\1'
    filename_trimmer(folder, pat15, repl15)
