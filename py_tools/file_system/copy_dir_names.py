#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 17:21:25 2019
@author: ddengca@gmail.com
"""

import os
import shutil
import tempfile


def copy_dir_names(directory, out_filename):
    '''
    copy names of all sub-dir of directory,
    append to out_filename
    '''
    # use utf-8 when open the file, as the name including utf charactors
    out_file = open(out_filename, 'at', encoding="utf-8")
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            out_file.write(item + '\n')
    out_file.close()


def rename_dir(directory):
    '''
    if a sub-dir of directory is like "【7】*",
    rename it to "【07】*"
    '''
    os.chdir(directory)
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)) and '】' in item:
            h, t = item.split('】')
            if len(h) == 2 and h[0] == '【':
                item_new = '【0' + h[1] + '】' + t
                os.rename(item, item_new)


def del_dir(directory):
    '''
    to delete all sub-directories in directory

    os.remove(): delete a file
    os.rmdir(): delete an empty directory
    shutil.rmtree(): deletes a directory and all its contents
    '''
    os.chdir(directory)
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            shutil.rmtree(item)


def rename_file(directory):
    '''
    rename all files in directory, to remove the "【*】" part
    Note that os.rename() a file to a name under another directory
    actually moves it
    '''
    os.chdir(directory)
    for item in os.listdir():
        if os.path.isfile(item) and '】' in item:
            h, item_new = item.split('】')
            os.rename(item, item_new)


def move_files_from_subdir(directory, type):
    '''
    move files with a certain type from all sub-dir to current directory
    '''
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            os.chdir(os.path.join(directory, item))
            for file in os.listdir():
                if os.path.isfile(file) and file.endswith(type):
                    os.rename(file, os.path.join(directory, file))


def treat_png():
    # to move and rename *.png files from all sub-dirs
    for item in os.listdir(dir_working):
        if os.path.isdir(os.path.join(dir_working, item)):
            os.chdir(os.path.join(dir_working, item))
            for file in os.listdir():
                if os.path.isfile(file) and file.endswith('png'):
                    file_new = os.path.join(dir_working, item + '.png')
                    os.rename(file, file_new)


def copy_book_name(dir_base, o_filename):
    # to copy book names to o_filename
    # insert under each corresponding categories
    # open an tempfile.NamedTemporaryFile()
    # then replace o_filename when finish inserting book names
    with open(o_filename, encoding='utf-8') as o_file, \
        tempfile.NamedTemporaryFile(
            'w+t', encoding='utf-8', delete=False) as o_tmp:
        for line in o_file:
            o_tmp.write(line)
            dir_cat = line[:-1]  # remove EOL in line
            os.chdir(os.path.join(dir_base, dir_cat))
            for book in os.listdir():
                # remove the starting 【*】 part in the dir name
                if '】' in book:
                    book_new = book.split('】')[1]
                    os.rename(book, book_new)
                    book = book_new
                os.chdir(os.path.join(dir_base, dir_cat, book))
                w_bookname = False
                for file in os.listdir():
                    if os.path.isdir(file):
                        continue
                    # remove the starting 【*】 part in the filename
                    if '】' in file:
                        file_new = file.split('】')[1]
                        os.rename(file, file_new)
                        file = file_new
                    # copy filename to o_tmp under corresponding category
                    if not w_bookname:
                        # remove extension from filename using os.path.splitext
                        bookname2write = os.path.splitext(file)[0]
                        o_tmp.write(bookname2write + '\n')
                        w_bookname = True
                        continue
                    # move azw3 or epub files to dir_base
                    # if file.endswith('azw3') or file.endswith('epub'):
                    #     os.rename(file, os.path.join(dir_base, file))
            o_tmp.write('\n')
    os.replace(o_tmp.name, o_filename)


def copy_all_books(dir_base, o_filename, types):
    """ Copy books from all sub-folders to dir_base
    Only copy books whose extension is in types
    """
    with open(o_filename, encoding='utf-8') as f:
        booknames = f.readlines()
    os.chdir(dir_base)
    for cat in os.listdir():  # category names like '【01】2018年度高分图书'
        if os.path.isdir(os.path.join(dir_base, cat)):
            os.chdir(os.path.join(dir_base, cat))
            for book in os.listdir():
                os.chdir(os.path.join(dir_base, cat, book))
                for file in os.listdir():
                    if os.path.isdir(file):
                        continue
                    file_name, file_ext = os.path.splitext(file)
                    if file_ext[1:] in types:
                        for line in booknames:
                            if file_name in line and ',' in line:
                                file_name = line.rpartition(', ')[2][:-1]
                                break
                        try:
                            os.rename(file, os.path.join(
                                dir_base, file_name + file_ext))
                        except FileExistsError:
                            print('%s already moved!' % file)


def rename_file(dir_base, o_filename):
    """ For books in all sub-folders of dir_base,
    change files name according to lines in o_filename
    """
    with open(o_filename, encoding='utf-8') as f:
        booknames = f.readlines()
    os.chdir(dir_base)
    for cat in os.listdir():  # category names like '【01】2018年度高分图书'
        if os.path.isdir(os.path.join(dir_base, cat)):
            os.chdir(os.path.join(dir_base, cat))
            for book in os.listdir():
                os.chdir(os.path.join(dir_base, cat, book))
                for file in os.listdir():
                    if os.path.isdir(file):
                        continue
                    file_name, file_ext = os.path.splitext(file)
                    for line in booknames:
                        if file_name in line and ',' in line:
                            # new name: the part after ', ' and removing EOL
                            file_name = line.rpartition(', ')[2][:-1]
                            break
                    try:
                        file_new = file_name + file_ext
                        os.rename(file, file_new)
                        print('Renamed %s to %s' % (file, file_new))
                    except FileExistsError:
                        print('%s already moved!' % file)


def clean_file(o_filename):
    ''' remove the old book names in o_filename
    '''
    with open(o_filename, encoding='utf-8') as o_file, \
        tempfile.NamedTemporaryFile(
            'w+t', encoding='utf-8', delete=False) as o_tmp:
        for line in o_file:
            if ', ' in line:
                line = line.rpartition(', ')[2]
            o_tmp.write(line)
    os.replace(o_tmp.name, o_filename)


def clean_up_dir(dir_base):
    ''' Walk through all sub-folders in dir_base,
    delete files duplicate with one in dir_base,
    delete empty sub-folders
    '''
    # get a list of all files at dir_base
    files_at_base = os.listdir(dir_base)
    files_at_base_loop = files_at_base.copy()
    for f in files_at_base_loop:
        if os.path.isdir(os.path.join(dir_base, f)):
            files_at_base.remove(f)

    for root, dirs, files in os.walk(dir_base):
        # skip scanning dir_base
        if root == dir_base:
            continue

        # delete empty dir
        if not dirs and not files:
            os.rmdir(root)
            continue

        # delete duplicate files
        for f in files:
            file_name, file_ext = os.path.splitext(f)
            if file_name + '.azw3' in files_at_base or \
                    file_name + '.epub' in files_at_base:
                print('DEL %s at %s...' % (f, root))
                os.remove(os.path.join(root, f))


def write_monthly_list(dir_month, o_file):
    ''' walk dir_month, copy book names of each month and
    append to o_file under each month
    '''
    with open(o_file, 'at', encoding='utf-8') as o_f:
        o_f.write('\n【19】2018月度热门图书\n')
        for root, dirs, files in os.walk(dir_month):
            if files:
                month = root.rpartition('\\')[2]
                o_f.write(month + ':\n')
                # trim extension from each filename
                files_name = []
                for f in files:
                    files_name.append(os.path.splitext(f)[0])
                # to remove duplicate filenames
                files_name = set(files_name)
                for f in files_name:
                    o_f.write('    ' + f + '\n')


def move_extra(dir_base, dir_copy):
    ''' walk all sub-dir of dir_copy;
    for each book files found, check if it's in dir_base
    if not, copy it to dir_base
    '''
    i = j = k = 0
    for root, dirs, files in os.walk(dir_copy):
        if not dirs and not files:
            os.rmdir(root)
            k += 1
            print('DEL: %s is empty!' % root)
            continue
        for f in files:
            try:
                os.rename(os.path.join(root, f),
                          os.path.join(dir_base, f))
                print('Moved: %s.' % f)
                i += 1
            except FileExistsError:
                j += 1
                os.remove(os.path.join(root, f))
                print('Deleted: %s at %s already exists!' % (f, root))
    print('Totally moved %i books.' % i)
    print('There are total %i duplicates deleted.' % j)
    print('Totally deleted %i empty folders.' % k)


def find_missing(dir_base, o_file):
    ''' go through each books listed in o_file,
    find out anyone not in dir_base, then marked as (missing)
    '''


def treat_monthly():
    # to handle top books for each months
    i = 1
    while i < 13:
        dir = dir_working + '\\' + str(i) + '月'
        move_files_from_subdir(dir, 'epub')
        rename_file(dir)
        del_dir(dir)
        i += 1


dir_working = \
    'C:\\Users\\zhid\\Documents\\private\\myebooks\\豆瓣2018年度读书榜单'
dir_clancy = \
    'C:\\Users\\zhid\\Documents\\private\\myebooks\\Tom Clancy'
dir_copy = \
    'C:\\Users\\zhid\\Documents\\private\\myebooks\\豆瓣2018年度读书榜单 - Copy'
dir_month = os.path.join(dir_copy, '【19】2018月度热门图书')
out_filename = os.path.join(dir_working, '_豆瓣2018年度读书榜单.txt')
# copy_dir_names(dir_working, out_filename)
# rename_dir(dir_working)


def main():
    # copy_book_name(dir_working, out_filename)
    # copy_all_books(dir_working, out_filename, ['azw3', 'epub'])
    # rename_file(dir_working, out_filename)
    # clean_up_dir(dir_working)
    # clean_file(out_filename)
    # write_monthly_list(dir_month, out_filename)
    # move_extra(dir_working, dir_copy)
    move_files_from_subdir(dir_clancy, 'mobi')


if __name__ == "__main__":
    main()
