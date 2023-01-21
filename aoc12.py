########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022-2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple
from math import inf
import sys
#sys.setrecursionlimit(15000)

P = namedtuple('P', ['x', 'y'])

START = 'S'
END = 'E'
BOTTOM = 'a'
TOP = 'z'

def solve_1(input_str):
    heightmap = parse_input(input_str)
    verboseprint(dump_map(heightmap))
    start = get_start(heightmap)
    end = get_end(heightmap)
    return find_shortest_steps_to_end(start, end, heightmap)

def solve_2(input_str):
    heightmap = parse_input(input_str)
    verboseprint(dump_map(heightmap))
    end = get_end(heightmap)
    starts = [p for p in heightmap if heightmap[p] == BOTTOM]
    distances = list()
    for start in starts:
        verboseprint(start, "...")
        distances.append(find_shortest_steps_to_end(start, end, heightmap))
        verboseprint(start, len(distances), min(distances))
    return min(distances)

def parse_input(input_str):
    global max_x
    global max_y
    heightmap = dict()
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            heightmap[P(x,y)] = c
            x += 1
        y += 1
    max_x = x
    max_y = y
    return heightmap

def dump_map(heightmap):
    printable = ""
    for y in range(max_y):
        for x in range(max_x):
            printable += heightmap[P(x,y)]
        printable += "\n"
    return printable

def find_shortest_steps_to_end(start, end, heightmap):
    distance = comp_distance(start, end, heightmap)
    try:
        d = distance[end]
    except KeyError:
        d = inf
    return d

def get_extreme(heightmap, extreme_type):
    for p in heightmap:
        if heightmap[p] == extreme_type:
            return p
    return None

def get_start(heightmap):
    return get_extreme(heightmap, START)

def get_end(heightmap):
    return get_extreme(heightmap, END)

def comp_distance(start, end, heightmap):
    distance = dict()
    distance[start] = 0
    explore_next(end, heightmap, distance)
    return distance

def explore_next(end, heightmap, distance):
    assert(not end in distance)
    max_d = max(distance.values())
    edge = [p for p in distance if distance[p] == max_d]
    for e in edge:
        for p in get_adjacent_reachable_points(e, heightmap, distance):
            assert(not p in distance)
            distance[p] = max_d + 1
    if not end in distance and max(distance.values()) > max_d:
        explore_next(end, heightmap, distance)

def get_adjacent_reachable_points(p, heightmap, distance):
    points = list()
    ph = heightmap[p]
    if ph == START:
        ph = BOTTOM
    deltas = [P(0,-1), P(-1,0), P(1,0), P(0,1)]
    for delta in deltas:
        ap = P(p.x+delta.x,p.y+delta.y)
        if ap in distance:
            continue
        try:
            h = heightmap[ap]
        except KeyError:
            continue
        if h == END:
            if ord(TOP) - ord(ph) <= 1:
                points = [ap]
                break
        else:
            if ord(h) - ord(ph) <= 1:
                points.append(ap)
    return points

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""", 31),
                ]
        self.tc_2 = [
                (
"""
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""", 29),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_get_adjacent_reachable_points(self):
        heightmap = parse_input(self.tc_1[0][0])
        path = []
        self.assertEqual(get_adjacent_reachable_points(P(0,0), heightmap, path), [P(1,0), P(0,1)])
        self.assertEqual(get_adjacent_reachable_points(P(2,0), heightmap, path), [P(1,0), P(2,1)])
        path = [P(0,0), P(1,0), P(2,0), P(2,1)]
        self.assertEqual(get_adjacent_reachable_points(P(2,1), heightmap, path), [P(1,1), P(2,2)])
