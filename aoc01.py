########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    parsed_input = input_str.strip().split('\n')
    parsed_input.append('')
    return parsed_input

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    calories = 0
    max_calories = 0
    for line in parsed_input:
        try:
            c = int(line)
            calories += c
        except ValueError:
            if calories > max_calories:
                max_calories = calories
            calories = 0
    return max_calories

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    calories = 0
    elf_calories = []
    for line in parsed_input:
        try:
            c = int(line)
            calories += c
        except ValueError:
            elf_calories.append(calories)
            calories = 0
    max_calories = sum(list(reversed(sorted(elf_calories)))[0:3])
    return max_calories

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
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
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
