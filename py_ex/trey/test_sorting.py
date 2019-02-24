#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import unittest
from sorting import sorting


class TestSorting(unittest.TestCase):
    def testcase01(self):
        ori = [3, 1, 0, 7, 9, 12, 11]
        sorted = [0, 1, 3, 7, 9, 11, 12]
        self.assertEqual(sorting(ori), sorted)

    @unittest.expectedFailure
    def testcase02(self):
        ori = [3, 1, 0, 7, 9, 12, 11]
        sorted = [1, 3, 7, 9, 11, 12]
        self.assertEqual(sorting(ori), sorted)

if __name__ == '__main__':
    unittest.main()
