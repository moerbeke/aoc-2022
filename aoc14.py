########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    c = Cave(input_str)
    while c.can_accept_sand():
        print(c)
        c.step()
    print(c)
    return c.sand_units_count()

def solve_2(input_str):
    c = ExtendedCave(input_str)
    while c.can_accept_sand():
        #print(c)
        c.step()
    print(c)
    return c.sand_units_count()

def parse_input(input_str):
    pass

ROCK = '#'
AIR = '.'
SAND = 'o'
SOURCE = '+'

SOURCE_X_Y = 500, 0

class Cave:

    def __init__(self, input_str):
        self._map = {}
        for line in input_str.strip().split('\n'):
            segments = []
            p1 = None
            p2 = None
            for p in line.split(' -> '):
                x, y = (int(i) for i in p.split(','))
                assert y > 0
                if p1 == None:
                    p1 = (x, y)
                else:
                    p2 = (x, y)
                    x1 = min(p1[0], p2[0])
                    x2 = max(p1[0], p2[0])
                    y1 = min(p1[1], p2[1])
                    y2 = max(p1[1], p2[1])
                    for i in range(x1,x2+1):
                        for j in range(y1,y2+1):
                            self._map[i,j] = ROCK
                    p1 = p2
        xs = [x for x,y in self._map.keys()]
        ys = [y for x,y in self._map.keys()]
        self._min_x = min(xs)
        self._max_x = max(xs)
        self._min_y = 0
        self._max_y = max(ys)
        for x in range(self._min_x, self._max_x+1):
            for y in range(self._min_y, self._max_y+1):
                if (x, y) not in self._map.keys():
                    self._map[x,y] = AIR
        self._map[SOURCE_X_Y] = SOURCE
        self._abyss_found = False
        self._sand_unit_p = None

    def __str__(self):
        s = ''
        for y in range(self._min_y, self._max_y+1):
            for x in range(self._min_x, self._max_x+1):
                s += self._map[x,y]
            s += "\n"
        return s

    def can_accept_sand(self):
        return not self._abyss_found

    def step(self):
        self._sand_unit_p = SOURCE_X_Y
        while not self._abyss_found and self._try_move():
            x, y = self._sand_unit_p
            if x not in range(self._min_x, self._max_x+1) or y not in range(self._min_y, self._max_y):
                self._abyss_found = True
        if not self._abyss_found:
            self._map[self._sand_unit_p] = SAND

    def sand_units_count(self):
        return sum([1 for k,v in self._map.items() if v == SAND])

    def _try_move(self):
        can_move = False
        if self._try_down() or self._try_left() or self._try_right():
            can_move = True
        return can_move

    def _try_down(self):
        x0, y0 = self._sand_unit_p
        target_p = x0, y0+1
        return self._try_p(target_p)

    def _try_left(self):
        x0, y0 = self._sand_unit_p
        target_p = x0-1, y0+1
        return self._try_p(target_p)

    def _try_right(self):
        x0, y0 = self._sand_unit_p
        target_p = x0+1, y0+1
        return self._try_p(target_p)

    def _try_p(self, p):
        can_move = False
        if p not in self._map.keys() or self._map[p] == AIR:
            self._sand_unit_p = p
            can_move = True
        return can_move

class ExtendedCave:

    def __init__(self, input_str):
        self._map = {}
        for line in input_str.strip().split('\n'):
            segments = []
            p1 = None
            p2 = None
            for p in line.split(' -> '):
                x, y = (int(i) for i in p.split(','))
                assert y > 0
                if p1 == None:
                    p1 = (x, y)
                else:
                    p2 = (x, y)
                    x1 = min(p1[0], p2[0])
                    x2 = max(p1[0], p2[0])
                    y1 = min(p1[1], p2[1])
                    y2 = max(p1[1], p2[1])
                    for i in range(x1,x2+1):
                        for j in range(y1,y2+1):
                            self._map[i,j] = ROCK
                    p1 = p2
        xs = [x for x,y in self._map.keys()]
        ys = [y for x,y in self._map.keys()]
        self._min_x = min(xs)
        self._max_x = max(xs)
        self._min_y = 0
        self._max_y = max(ys)
        for x in range(self._min_x, self._max_x+1):
            for y in range(self._min_y, self._max_y+1):
                if (x, y) not in self._map.keys():
                    self._map[x,y] = AIR
            self._map[x,self._max_y+1] = AIR
            self._map[x,self._max_y+2] = ROCK
        self._max_y += 2
        self._map[SOURCE_X_Y] = SOURCE
        self._sand_unit_p = None

    def __str__(self):
        s = ''
        for y in range(self._min_y, self._max_y+1):
            for x in range(self._min_x, self._max_x+1):
                if (x,y) not in self._map.keys():
                    s += AIR
                else:
                    s += self._map[x,y]
            s += "\n"
        return s

    def can_accept_sand(self):
        return not self._map[SOURCE_X_Y] == SAND

    def step(self):
        self._sand_unit_p = SOURCE_X_Y
        while self._try_move():
            pass
        self._map[self._sand_unit_p] = SAND

    def sand_units_count(self):
        return sum([1 for k,v in self._map.items() if v == SAND])

    def _try_move(self):
        can_move = False
        if self._try_down() or self._try_left() or self._try_right():
            can_move = True
        return can_move

    def _try_down(self):
        x0, y0 = self._sand_unit_p
        target_p = x0, y0+1
        return self._try_p(target_p)

    def _try_left(self):
        x0, y0 = self._sand_unit_p
        target_p = x0-1, y0+1
        return self._try_p(target_p)

    def _try_right(self):
        x0, y0 = self._sand_unit_p
        target_p = x0+1, y0+1
        return self._try_p(target_p)

    def _try_p(self, p):
        can_move = False
        self._explore(p)
        if self._map[p] == AIR:
            self._sand_unit_p = p
            can_move = True
        return can_move

    def _explore(self, p):
        x, y = p
        if p not in self._map.keys():
            assert y <= self._max_y
            if y == self._max_y:
                self._map[p] = ROCK
            else:
                self._map[p] = AIR
        if x < self._min_x:
            assert x == self._min_x - 1
            self._min_x -= 1
        elif x > self._max_x:
            assert x == self._max_x + 1
            self._max_x += 1


########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""", 24),
                ]
        self.tc_2 = [
                (
"""
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""", 93),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
