#!/usr/bin/env python3

########################################################################
# The Advent of Code 2022
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

import unittest

########################################################################
# Test class
########################################################################

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.aocsolver = daysolver
        self.tc_1 = [
                (
"""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

""", 24000),
                ]
        self.tc_2 = [
                (
"""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

""", 45000),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])
