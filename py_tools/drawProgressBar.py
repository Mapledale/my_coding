#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  drawProgressBar.py
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


import sys


def drawProgressBar(percent, barLen=20):
    '''
    *Example*
    drawProgressBar(0.5, 10)
    [=====     ] 50.00%
    '''
    sys.stdout.write('\r')
    progress = ''
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += '='
        else:
            progress += ' '
    sys.stdout.write('[%s] %.2f%%' % (progress, percent * 100))
    # alternative way:
    # num = int(percent * barLen)
    # sys.stdout.write('[%-{barLen}s] %.2f%%' %('='*num, percent * 100))
    sys.stdout.flush()


def main():
    from time import sleep

    barLen = int(input('Input the total length of the progress bar: '))
    for i in range(barLen + 1):
        percent = float(i) / barLen
        drawProgressBar(percent, barLen)
        sleep(0.2)
    print('\n')

if __name__ == '__main__':
    main()
