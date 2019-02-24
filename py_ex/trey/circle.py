# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 10:39:05 2019

@author: ZhiD
"""


import math


class Circle(object):
    '''circle with radius, diameter, and area
    '''
    def __init__(self, radius=1):
        # by the time __init__ is called,
        # a Circle instance has been constructed.
        # so assigning to self.radius will call @radius.setter
        self.radius = radius

    def __repr__(self):
        # for Python 3.6+, using f-string
        # return f'Circle({self.radius})'

        # traditional way
        return 'Circle(%d)' %self.radius
        # traditional way, for Python 3.x:
        # %d: truncate to integer
        # %s: maintain formatting
        # %f: float
        # %g: generic number

    # in order to change the diameter and area automatically
    # when the radius is changed,
    # using the property decorator,
    # (which is Python's preferred equivalent to getter and setter methods)
    # and make the diameter and area attributes into properties
    @property
    def area(self):
        return math.pi * self.radius * self.radius

    @property
    def diameter(self):
        return 2 * self.radius

    # in order to change the radius automatically
    # when the diameter is changed,
    # using a setter for the diameter property
    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    # in order to prohibit setting radius to a negative number
    @property
    def radius(self):
        return self._radius

    # this setter will be called whenever radius is set
    # including in direct assignment like c.radius = 7,
    # and in __init__ method or diameter setter
    @radius.setter
    def radius(self, radius):
        if radius < 0:
            raise ValueError('Radius cannot be negative!')
        self._radius = radius
