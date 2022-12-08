########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

P = namedtuple('P', ['x', 'y'])

def solve_1(input_str):
    trees, nx, ny = parse_input(input_str)
    return count_visible(trees, nx, ny)

def solve_2(input_str):
    trees, nx, ny = parse_input(input_str)
    return max(highest_scenic_score(trees, nx, ny))

def parse_input(input_str):
    trees = dict()
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            trees[P(x,y)] = c
            x += 1
        y += 1
    return trees, x, y

def count_visible(trees, nx, ny):
    nl = visible_from_left(trees, nx, ny)
    nr = visible_from_right(trees, nx, ny)
    nu = visible_from_up(trees, nx, ny)
    nd = visible_from_down(trees, nx, ny)
    return len(nl.union(nr).union(nu).union(nd))

def visible_from_left(trees, nx, ny):
    visible_trees = set()
    for y in range(ny):
        heights_in_this_raw = list()
        p = P(0,y)
        heights_in_this_raw.append(trees[p])
        visible_trees.add(p)
        for x in range(1, nx):
            p = P(x,y)
            if trees[p] > max(heights_in_this_raw):
                heights_in_this_raw.append(trees[p])
                visible_trees.add(p)
    return visible_trees

def visible_from_right(trees, nx, ny):
    visible_trees = set()
    for y in range(ny):
        heights_in_this_raw = list()
        p = P(nx-1,y)
        heights_in_this_raw.append(trees[p])
        visible_trees.add(p)
        for x in range(nx-1, -1, -1):
            p = P(x,y)
            if trees[p] > max(heights_in_this_raw):
                heights_in_this_raw.append(trees[p])
                visible_trees.add(p)
    return visible_trees

def visible_from_up(trees, nx, ny):
    visible_trees = set()
    for x in range(nx):
        heights_in_this_raw = list()
        p = P(x,0)
        heights_in_this_raw.append(trees[p])
        visible_trees.add(p)
        for y in range(1, ny):
            p = P(x,y)
            if trees[p] > max(heights_in_this_raw):
                heights_in_this_raw.append(trees[p])
                visible_trees.add(p)
    return visible_trees

def visible_from_down(trees, nx, ny):
    visible_trees = set()
    for x in range(nx):
        heights_in_this_raw = list()
        p = P(x,nx-1)
        heights_in_this_raw.append(trees[p])
        visible_trees.add(p)
        for y in range(ny-1, -1, -1):
            p = P(x,y)
            if trees[p] > max(heights_in_this_raw):
                heights_in_this_raw.append(trees[p])
                visible_trees.add(p)
    return visible_trees

def highest_scenic_score(trees, nx, ny):
    scenic_scores = list()
    for x in range(1,nx-1):
        for y in range(1,ny-1):
            scenic_scores.append(scenic_score(trees, nx, ny, P(x,y)))
    return scenic_scores

def scenic_score(trees, nx, ny, p):
    return (
            count_visible_trees(trees, nx, ny, p, P(p.x+1,p.y), P(nx,p.y+1)) *
            count_visible_trees(trees, nx, ny, p, P(p.x-1,p.y), P(-1,p.y+1)) *
            count_visible_trees(trees, nx, ny, p, P(p.x,p.y+1), P(p.x+1,ny)) *
            count_visible_trees(trees, nx, ny, p, P(p.x,p.y-1), P(p.x+1,-1))
            )

def count_visible_trees(trees, nx, ny, p, p1, p2):
    sh = trees[p]
    count = 0
    tall_found = False
    for x in range(p1.x, p2.x, sign(p2.x-p1.x)):
        for y in range(p1.y, p2.y, sign(p2.y-p1.y)):
            h = trees[P(x,y)]
            count += 1
            if h >= sh:
                tall_found = True
                break
        if tall_found:
            break
    return count

def sign(x):
    if x > 0:
        s = 1
    elif x < 0:
        s = -1
    else:
        s = 0
    return s

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
30373
25512
65332
33549
35390
""", 21),
                ]
        self.tc_2 = [
                (
"""
30373
25512
65332
33549
35390
""", 8),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
