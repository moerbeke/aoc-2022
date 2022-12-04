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
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""", 2),
                ]
        self.tc_2 = [
                (
"""
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""", 4),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])
