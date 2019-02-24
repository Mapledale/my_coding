#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  try_multiprocessing.py
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

from multiprocessing import Pool, TimeoutError
from time import sleep
import os

def main():
    my_pool = Pool(processes = 4)
    res = my_pool.apply_async(sleep, (5,))
    try:
        print(res.get(timeout = 1))
    except TimeoutError:
        print('We lacked patience and got a multiprocessing.TimeoutError')

if __name__ == '__main__':
	main()

