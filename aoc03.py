########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    parsed_input = input_str.strip().split('\n')
    return parsed_input

priority = {}
for i in range(0,26):
    priority[chr(ord('a')+i)] = i + 1
    priority[chr(ord('A')+i)] = i + 1 + 26

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    priosum = 0
    for rucksack in parsed_input:
        l = len(rucksack)
        assert(l % 2 == 0)
        compartment_1 = set(rucksack[:l//2])
        compartment_2 = set(rucksack[l//2:])
        items_share = compartment_1.intersection(compartment_2)
        assert(len(items_share) == 1)
        for item in items_share:
            break
        priosum += priority[item]
    return priosum

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    parsed_input = parse_input(input_str)
    priosum = 0
    n_rucksacks = len(parsed_input)
    assert(n_rucksacks % 3 == 0)
    n_group_rucksacks = n_rucksacks // 3
    for i in range(n_group_rucksacks):
        rucksack_1 = set(parsed_input[3*i])
        rucksack_2 = set(parsed_input[3*i+1])
        rucksack_3 = set(parsed_input[3*i+2])
        items_share = rucksack_1.intersection(rucksack_2).intersection(rucksack_3)
        assert(len(items_share) == 1)
        for item in items_share:
            break
        priosum += priority[item]
    return priosum

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""", 157),
                ]
        self.tc_2 = [
                (
"""
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
""", 70),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
