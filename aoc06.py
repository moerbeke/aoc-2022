########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def solve_1(input_str):
    return find_marker(input_str, 4)

def solve_2(input_str):
    return find_marker(input_str, 14)

def find_marker(signal, marker_length):
    signal = signal.strip()
    for i in range(len(signal)-marker_length):
        piece = signal[i:i+marker_length]
        if len(set(piece)) == marker_length:
            return i+marker_length

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""", 7),
                ]
        self.tc_2 = [
                (
"""
mjqjpqmgbljsphdztnvjfqwrcgsmlb
""", 19),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
