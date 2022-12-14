########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    parsed_input = input_str.strip().split('\n')
    return parsed_input

########################################################################
# Algorithms
########################################################################

def get_sections(line):
    elf1, elf2 = line.split(',')
    e1_min, e1_max = elf1.split('-')
    e2_min, e2_max = elf2.split('-')
    s1 = set(range(int(e1_min), int(e1_max)+1))
    s2 = set(range(int(e2_min), int(e2_max)+1))
    return s1, s2

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    n_overlap = 0
    for line in parsed_input:
        s1, s2 = get_sections(line)
        if s1.issubset(s2) or s2.issubset(s1):
            n_overlap += 1
    return n_overlap

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    n_overlap = 0
    for line in parsed_input:
        s1, s2 = get_sections(line)
        if len(s1.intersection(s2)) > 0:
            n_overlap += 1
    return n_overlap

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
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
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
