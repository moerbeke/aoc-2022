#!/usr/bin/env python3

########################################################################
# The Advent of Code 2022
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import importlib

########################################################################
# Test class
########################################################################

class TestAoc01(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
        self.tc_1 = [
                (
"""
""", None),
                ("", None),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ]

    def tearDown(self):
        pass

    @unittest.skip("not implemented yet")
    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    @unittest.skip("not implemented yet")
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    from os.path import basename
    scriptname = basename(__file__)
    day = scriptname.split('.')[0][-2:]
    aocname = 'aoc' + day
    aoc = importlib.import_module(aocname)
    testaocname = 'TestAoc' + day
    testaoc = globals()[testaocname]
    testbase.run_test(testaoc)
