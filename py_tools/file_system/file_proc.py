#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  file_proc.py
#  
#  Copyright 2017 David Deng <ddengca@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import re

def main():
    test_patt = {}
    file_in = 'test_monali.txt'
    f_in = open(file_in, 'r')    
    content = f_in.readlines()
    f_in.close()
    
    for line in content:        
        ch_id = re.search(r'\d{5}', line)
        if ch_id:
            ch_id = int(ch_id.group())
        else:
            continue
        bw = re.search(r'\d+G', line).group()
        bw = int(bw[:-1])
        test_patt[ch_id] = bw
    
    file_out = 'flex_grid.py'
    f_out = open(file_out, 'a+')
    f_out.write('\npattern01 = {\n')
    keys = test_patt.keys()
    keys.sort()
    for key in keys[:-1]:
        f_out.write('  {}: {},\n'.format(key, test_patt[key]))
    f_out.write('  {}: {}\n'.format(keys[-1], test_patt[keys[-1]]))
    f_out.write('}\n')
    f_out.close()

if __name__ == '__main__':
    main()
