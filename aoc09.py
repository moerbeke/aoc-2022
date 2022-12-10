########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

Move = namedtuple('Move', ['d', 'n'])
P = namedtuple('P',['x', 'y'])

R = 'R'
L = 'L'
U = 'U'
D = 'D'

def solve_1(input_str):
    h = P(0,0)
    t = P(0,0)
    moves = parse_input(input_str)
    t_grid = set()
    t_grid.add(t)
    for move in moves:
        h, t, t_grid = process_move(move, h, t, t_grid)
    print_tail_grid(t_grid)
    return len(t_grid)

def solve_2(input_str):
    h = P(0,0)
    t = P(0,0)
    knots = [P(0,0)] * 10
    moves = parse_input(input_str)
    t_grid = set()
    t_grid.add(t)
    for move in moves:
        knots, t_grid = process_move_knots(move, knots, t_grid)
    print_tail_grid(t_grid)
    return len(t_grid)

def print_tail_grid(t_grid):
    printable = '\n'
    x1 = min([p.x for p in t_grid])
    x2 = max([p.x for p in t_grid])
    y1 = min([p.y for p in t_grid])
    y2 = max([p.y for p in t_grid])
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            if P(x,y) in t_grid:
                if x == 0 and y == 0:
                    printable += 's'
                else:
                    printable += '#'
            else:
                printable += '.'
        printable += '\n'
    print(printable)

def process_move(move, h, t, t_grid):
    for i in range(move.n):
        h, t, t_grid = move_knot(move.d, h, t, t_grid)
    return h, t, t_grid

def process_move_knots(move, knots, t_grid):
    for i in range(move.n):
        knots, t_grid = move_knots(move.d, knots, t_grid)
        draw(move, knots)
    return knots, t_grid

def draw(move, knots):
    print("== %s %d ==" % (move.d, move.n))
    x1 = min([p.x for p in knots])
    x2 = max([p.x for p in knots])
    y1 = min([p.y for p in knots])
    y2 = max([p.y for p in knots])
    printable = '\n'
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            try:
                k = knots.index(P(x,y))
                if k == 0:
                    printable += "H"
                else:
                    printable += str(k)
            except ValueError:
                printable += "."
        printable += '\n'
    print(printable)

def move_knot(direction, h, t, t_grid):
    h = move_head(direction, h)
    if not adjacent(h, t):
        delta_x = sign(h.x - t.x)
        delta_y = sign(h.y - t.y)
        t = P(t.x + delta_x, t.y + delta_y)
        t_grid.add(t)
    return h, t, t_grid

def move_knots(direction, knots, t_grid):
    h = knots[0]
    h = move_head(direction, h)
    knots[0] = h
    for i in range(1, len(knots[1:])+1):
        t = knots[i]
        if not adjacent(h, t):
            delta_x = sign(h.x - t.x)
            delta_y = sign(h.y - t.y)
            t = P(t.x + delta_x, t.y + delta_y)
            knots[i] = t
        h = knots[i]
    t_grid.add(t)
    return knots, t_grid

def move_head(direction, h):
    if direction == R:
        delta_x = 1
        delta_y = 0
    elif direction == L:
        delta_x = -1
        delta_y = 0
    elif direction == U:
        delta_x = 0
        delta_y = -1
    elif direction == D:
        delta_x = 0
        delta_y = 1
    else:
        assert(False)
    return P(h.x + delta_x, h.y + delta_y)

def adjacent(h, t):
    return (abs(h.x-t.x) <= 1 and abs(h.y-t.y) <= 1)

def sign(x):
    if x > 0:
        s = 1
    elif x < 0:
        s = -1
    else:
        s = 0
    return s

def parse_input(input_str):
    moves = list()
    for line in input_str.strip().split('\n'):
        words = line.split(' ')
        direction = words[0]
        n = int(words[1])
        moves.append(Move(direction, n))
    return moves

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""", 13),
                ]
        self.tc_2 = [
                (
"""
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
""", 1),
                (
"""
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
""", 36),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
