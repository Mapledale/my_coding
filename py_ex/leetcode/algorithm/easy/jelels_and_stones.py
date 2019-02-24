#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

""" You're given strings J representing the types of stones that are jewels,
and S representing the stones you have.
Each character in S is a type of stone you have.
You want to know how many of the stones you have are also jewels.

The letters in J are guaranteed distinct,
and all characters in J and S are letters.
Letters are case sensitive,
so "a" is considered a different type of stone from "A".

Example 1:
Input: J = "aA", S = "aAAbbbb"
Output: 3

Example 2:
Input: J = "z", S = "ZZ"
Output: 0

Note:
S and J will consist of letters and have length at most 50.
The characters in J are distinct.
"""


class Solution:
    def numJewelsInStones_0(self, J: 'str', S: 'str') -> 'int':
        """ loop in S
        this is the normal solution, but S could be long
        """
        n = 0
        for lt in S:
            if lt in J:
                n += 1
        return n

    def numJewelsInStones_1(self, J: 'str', S: 'str') -> 'int':
        """ loop in J
        which is less than S
        """
        n = 0
        for lt in J:
            n += S.count(lt)
        return n
