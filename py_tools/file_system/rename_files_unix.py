#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Search all files in <work_dir>; for the files with a name matching <search_regex>,
rename to match <replace_regex>.

Created on Tue Nov 27 15:22:00 2018
@author: ZhiD
"""

import os
import fnmatch
import sys
import shutil
import re

def usage():
    print('Usage:\n\
%s <work_dir> <search_regex> <replace_regex> [-w|--write]\n\
\n\
By default no changes are made, add "-w" or "--write" as last argument\
to actually rename files after you have previewed the result.\n\
\n\
Example:\n\
python rename_files_regex.py . "([^\.]+?)-(m\\d+-\\d+)" "\\2_\\1" --write'
        %(os.path.basename(sys.argv[0])))


def rename_files(directory, search_pattern, replace_pattern,
                 write_changes=False):
    pattern_old = re.compile(search_pattern)

    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, "*.*"):
            if pattern_old.findall(filename):
                new_name = pattern_old.sub(replace_pattern, filename)

                filepath_old = os.path.join(path, filename)
                filepath_new = os.path.join(path, new_name)

                if not filepath_new:
                    print("Replacement regex {} returns empty value! Skipping"\
                          .format(replace_pattern))
                    continue

                print(new_name)

                if write_changes:
                    shutil.move(filepath_old, filepath_new)
            else:
                print("Name [{}] doesn't match search regex [{}]"\
                      .format(filename, search_pattern))


if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
        sys.exit(-1)

    work_dir = sys.argv[1]
    search_regex = sys.argv[2]
    replace_regex = sys.argv[3]
    write_changes = (len(sys.argv) > 4) and sys.argv[4].lower() in [
        '--write', '-w']
    rename_files(work_dir, search_regex, replace_regex, write_changes)
