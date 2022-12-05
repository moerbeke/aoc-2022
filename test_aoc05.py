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
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", 'CMZ'),
                ]
        self.tc_2 = [
                (
"""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", 'MCD'),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])
