#! /usr/bin/env python
# _*_ coding: utf-8 _*_
'''
demo for drawing with package Turtle
'''

import turtle
import math


def polygon(tur, n, length):
    ang = 360 / n
    for i in range(n):
        tur.fd(length)
        tur.lt(ang)


def circle(tur, r):
    polygon(tur, 360, 2.0 * math.pi * r / 360)


def arc(tur, r, ang):
    length = 2.0 * math.pi * r / 360
    for i in range(ang):
        tur.fd(length)
        tur.lt(1)


my_tt = turtle.Turtle()
leng = 2
polygon(my_tt, 7, 100)
# arc(my_tt, 200, 90)

# my_tt.mainloop()
