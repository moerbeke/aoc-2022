#!/usr/bin/env python3

########################################################################
# The Advent of Code 2022
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

import unittest

def suite(TestClass):
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestClass))
    return test_suite

def run_test(TestClass):
    aoc_test_suite = suite(TestClass)
    runner = unittest.TextTestRunner()
    runner.run(aoc_test_suite)
