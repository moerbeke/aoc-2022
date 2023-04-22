########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

import json

def solve_1(input_str):
    pairs = parse_input_as_pairs(input_str)
    return sum(compute_index_of_sorted_pairs(pairs))

def solve_2(input_str):
    received_packets = parse_input_as_packets(input_str)
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]
    received_packets.append(divider_packet_1)
    received_packets.append(divider_packet_2)
    sorted_packets = sort_packets(received_packets)
    i1 = sorted_packets.index(divider_packet_1)
    i2 = sorted_packets.index(divider_packet_2)
    return (i1+1) * (i2+1)

def compute_index_of_sorted_pairs(pairs):
    sorted_pairs = list()
    for i in range(len(pairs)):
        if is_sorted(pairs[i]):
            sorted_pairs.append(i+1)
            verboseprint(True)
        else:
            verboseprint(False)
    return sorted_pairs

def is_sorted(pair):
    left, right = pair
    verboseprint()
    verboseprint(left)
    verboseprint(right)
    return are_lists_sorted(left, right)

def are_lists_sorted(ll, rl):
    verboseprint("are_lists_sorted? ", ll, rl)
    for i in range(min(len(ll), len(rl))):
        left = ll[i]
        right = rl[i]
        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return True
            elif left > right:
                return False
            else:
                continue
        elif isinstance(left, list) and isinstance(right, list):
            sorted_lists = are_lists_sorted(left, right)
            if isinstance(sorted_lists, bool):
                return sorted_lists
            else:
                continue
        elif isinstance(left, int) and isinstance(right, list):
            sorted_lists = are_lists_sorted([left], right)
            if isinstance(sorted_lists, bool):
                return sorted_lists
            else:
                continue
        elif isinstance(left, list) and isinstance(right, int):
            sorted_lists = are_lists_sorted(left, [right])
            if isinstance(sorted_lists, bool):
                return sorted_lists
            else:
                continue
        else:
            assert(False)
    if len(ll) < len(rl):
        return True
    elif len(ll) > len(rl):
        return False
    else:
        return None

def sort_packets(packets):
    from functools import cmp_to_key
    return sorted(packets, key=cmp_to_key(compare_lists), reverse=False)

def compare_lists(l1, l2):
    r = are_lists_sorted(l1, l2)
    if r is None:
        return 0
    elif r:
        return -1
    else:
        return 1

def parse_input_as_pairs(input_str):
    pairs = list()
    left = None
    right = None
    for line in input_str.strip().split('\n\n'):
        left_line, right_line = line.split()
        left = json.loads(left_line)
        right = json.loads(right_line)
        pairs.append((left, right))
    return pairs

def parse_input_as_packets(input_str):
    packets = list()
    for line in input_str.strip().split('\n'):
        if line != '':
            packets.append(json.loads(line))
    return packets

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""", 13),
                ]
        self.tc_2 = [
                (
"""
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""", 140),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
