########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

"""Rock types

####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
"""

# Initial position above chamber ceiling
ROCKS = [
        [(2,0), (3,0), (4,0), (5,0)],
        [(3,2), (2,1), (3,1), (4,1), (3,0)],
        [(4,2), (4,1), (2,0), (3,0), (4,0)],
        [(2,3), (2,2), (2,1), (2,0)],
        [(2,1), (3,1), (2,0), (3,0)]
        ]
N_ROCKS = len(ROCKS)
ROCK_HEIGHT = [1, 3, 3, 4, 2]

RIGHT = '>'
LEFT = '<'

ROCK_SPACE = '#'
EMPTY_SPACE = '.'
WALL_SPACE = '|'
FALLING_ROCK = '@'

CHAMBER_WIDTH = 7

g_chamber = {}
g_chamber_height = 0

"""Chamber coordinates

   (0,N) (1,N) (2,N) (3,N) (4,N) (5,N) (6,N)
   ...
   (0,2) (1,2) (2,2) (3,2) (4,2) (5,2) (6,2)
   (0,1) (1,1) (2,1) (3,1) (4,1) (5,1) (6,1)
   (0,0) (1,0) (2,0) (3,0) (4,0) (5,0) (6,0)
"""

g_jet_pattern_index = 0

def solve_1(input_str):
    jet_pattern = parse_input(input_str)
    n_rocks = 2022
    height = run(n_rocks, jet_pattern)
    return height

def solve_2(input_str):
    return None

def parse_input(input_str):
    return list(input_str.strip())

def run(n_rocks, jet_pattern):
    for i in range(n_rocks):
        fall_rock(i, jet_pattern)
        print_chamber()
        verboseprint(i, g_chamber_height)
    return g_chamber_height

def fall_rock(i, jet_pattern):
    global g_jet_pattern_index
    global g_chamber_height
    tmp_chamber_height = g_chamber_height
    # Add three empty lines
    for y in range(3):
        for x in range(CHAMBER_WIDTH):
            g_chamber[(x,tmp_chamber_height)] = EMPTY_SPACE
        tmp_chamber_height += 1
    # Add new rock
    rock_index = i % N_ROCKS
    falling_rock_shape = ROCKS[rock_index]
    falling_rock_height = ROCK_HEIGHT[rock_index]
    for y in range(falling_rock_height):
        for x in range(CHAMBER_WIDTH):
            if (x,y) in falling_rock_shape:
                g_chamber[(x,tmp_chamber_height+y)] = FALLING_ROCK
            else:
                g_chamber[(x,tmp_chamber_height+y)] = EMPTY_SPACE
    tmp_chamber_height += falling_rock_height
    falling_rock = []
    for p in falling_rock_shape:
        falling_rock.append((p[0], p[1] + tmp_chamber_height - falling_rock_height))
    # Fall
    jet_pattern_length = len(jet_pattern)
    still = False
    while not still:
        # Jet push
        jet_push_dir = jet_pattern[g_jet_pattern_index]
        g_jet_pattern_index = (g_jet_pattern_index + 1) % jet_pattern_length
        if jet_push_dir == RIGHT:
            falling_rock = move_right(falling_rock)
        elif jet_push_dir == LEFT:
            falling_rock = move_left(falling_rock)
        # Fall down
        falling_rock_after = move_down(falling_rock)
        if falling_rock_after == falling_rock:
            still = True
        falling_rock = falling_rock_after
    for (x,y) in falling_rock:
        g_chamber[(x,y)] = ROCK_SPACE
        g_chamber_height = max(g_chamber_height, y+1)

def move_right(rock):
    can_move = True
    for (x,y) in rock:
        if x == CHAMBER_WIDTH - 1 or g_chamber[(x+1,y)] == ROCK_SPACE:
            can_move = False
            break
    if can_move:
        verboseprint("Can move right", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x+1,y))
            g_chamber[(x+1,y)] = FALLING_ROCK
    else:
        verboseprint("Cannot move right", rock)
        rock_after = rock
    return rock_after

def move_left(rock):
    can_move = True
    for (x,y) in rock:
        if x == 0 or g_chamber[(x-1,y)] == ROCK_SPACE:
            can_move = False
            break
    if can_move:
        verboseprint("Can move left", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x-1,y))
            g_chamber[(x-1,y)] = FALLING_ROCK
    else:
        verboseprint("Cannot move left", rock)
        rock_after = rock
    return rock_after

def move_down(rock):
    can_move = True
    for (x,y) in rock:
        if y == 0 or g_chamber[(x,y-1)] == ROCK_SPACE:
            can_move = False
            break
    if can_move:
        verboseprint("Can move down", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x,y-1))
            g_chamber[(x,y-1)] = FALLING_ROCK
    else:
        verboseprint("Cannot move down", rock)
        rock_after = rock
    return rock_after

def print_chamber(height=None):
    if height is None:
        height = g_chamber_height
    verboseprint()
    for y in range(height):
        line = ""
        for x in range(CHAMBER_WIDTH):
            line += g_chamber[(x,height-1-y)]
        verboseprint(WALL_SPACE+line+WALL_SPACE)
    verboseprint("+" + "-"*CHAMBER_WIDTH + "+")

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""", 3068),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
