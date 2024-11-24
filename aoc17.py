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

RIGHT_PUSH = '>'
LEFT_PUSH = '<'

ROCK_SPACE = '#'
EMPTY_SPACE = '.'
WALL_SPACE = '|'
FALLING_ROCK = '@'

CHAMBER_WIDTH = 7

UP, DOWN, LEFT, RIGHT = 'U', 'D', 'L', 'R'
UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT

"""Chamber coordinates

   (0,N) (1,N) (2,N) (3,N) (4,N) (5,N) (6,N)
   ...
   (0,2) (1,2) (2,2) (3,2) (4,2) (5,2) (6,2)
   (0,1) (1,1) (2,1) (3,1) (4,1) (5,1) (6,1)
   (0,0) (1,0) (2,0) (3,0) (4,0) (5,0) (6,0)
"""

def init():
    global g_chamber
    global g_chamber_height
    global g_jet_pattern_index
    global g_skylines
    global g_chamber_heights
    g_chamber = {}
    g_chamber_height = 0
    g_jet_pattern_index = 0
    g_skylines = []
    g_chamber_heights = []

def solve_1(input_str):
    init()
    jet_pattern = parse_input(input_str)
    n_rocks = 2022
    height = run(n_rocks, jet_pattern)
    return height

def solve_2(input_str):
    init()
    jet_pattern = parse_input(input_str)
    n_rocks = 1000000000000
    height = run(n_rocks, jet_pattern)
    return height

def parse_input(input_str):
    return list(input_str.strip())

def run(n_rocks, jet_pattern):
    global g_chamber_height
    for i in range(n_rocks):
        verboseprint(g_jet_pattern_index, i, g_chamber_height)
        fall_rock(i, jet_pattern)
        """
        x = 5
        y = 7
        z = 11
        w = 13
        b = +1
        c = +2
        d = +3
        e = +4

        g_chamber_height = (x+y+z) + (b+c+d+e) + b = 23 + 10 + 1 = 34
        len(g_skylines) = 7
        total_height = (x+y+z) + (b+c+d+e)*4 + (b+c+d) = 23 + 10*4 + 6 = 69
               v         
        0123456789012345678901
        xyzbcdebcdebcdebcdebcd
        n_rocks = 22
        skyline_offset = 3
        skyline_period = 7 - 3 = 4
        n_periods = (22-3)//4 = 4
        initial_offset_height = h[3-1] = h[2] = 5+7+11 = 23
        period_height = g_chamber_height - h[3] = 34 - (5+7+11+1) = 34 - 24 = 10
        trailing_offset = (22-3)%4 = 3
        trailing_offset_height = h[3+3-1] - h[2] = h[5] - h[2] = (x+y+z+b+c+d) - (x+y+z) = 29 - 23 = 6
        total_height = 23 + 10*4 + 6 = 69

        g_chamber_height = (x+y+z) + (b+c+d+e) + b = 23 + 10 + 1 = 34
        len(g_skylines) = 7
        total_height = (x+y+z) + (b+c+d+e)*4 + (b) = 23 + 10*4 + 1 = 64
               v         
        01234567890123456789
        xyzbcdebcdebcdebcdeb
        n_rocks = 20
        skyline_offset = 3
        skyline_period = 7 - 3 = 4
        n_periods = (20-3)//4 = 4
        initial_offset_height = h[3-1] = h[2] = 5+7+11 = 23
        period_height = g_chamber_height - h[3] = 34 - (5+7+11+1) = 34 - 24 = 10
        trailing_offset = (20-3)%4 = 1
        trailing_offset_height = h[3+1-1] - h[2] = h[3] - h[2] = (x+y+z+b) - (x+y+z) = 24 - 23 = 1
        total_height = 23 + 10*4 + 1 = 64

        g_chamber_height = (x+y+z+w) + (b+c+d) + b = 36 + 6 + 1 = 43
        len(g_skylines) = 7
        total_height = (x+y+z+w) + (b+c+d)*4 + (b) = 36 + 10*4 + 1 = 77
               v         
        01234567890123456
        xyzwbcdbcdbcdbcdb
        n_rocks = 17
        skyline_offset = 4
        skyline_period = 7 - 4 = 3
        n_periods = (17-4)//3 = 4
        initial_offset_height = h[4-1] = h[3] = 5+7+11+13 = 36
        period_height = g_chamber_height - h[4] = 43 - h[4] = 43 - (36+1) = 43 - 37 = 6
        trailing_offset = (17-4)%3 = 1
        trailing_offset_height = h[4+1-1] - h[3] = h[4] - h[3] = (x+y+z+w+b) - (x+y+z+w) = 37 - 36 = 1
        total_height = 36 + 6*4 + 1 = 77
        """
        skyline = get_skyline(i%N_ROCKS)
        try:
            skyline_offset = g_skylines.index(skyline)
            skyline_period = len(g_skylines) - skyline_offset
            n_periods = (n_rocks - skyline_offset) // skyline_period
            initial_offset_height = g_chamber_heights[skyline_offset-1]
            period_height = g_chamber_height - g_chamber_heights[skyline_offset]
            trailing_offset = (n_rocks - skyline_offset) % skyline_period
            trailing_offset_height = g_chamber_heights[skyline_offset+trailing_offset-1] - initial_offset_height
            total_height = initial_offset_height + period_height * n_periods + trailing_offset_height
            verboseprint("g_chamber_height=%d, len(g_skylines)=%d" % (g_chamber_height, len(g_skylines)))
            verboseprint("skyline_offset=%d, skyline_period=%d, n_periods=%d, trailing_offset=%d" % (skyline_offset, skyline_period, n_periods, trailing_offset))
            verboseprint("initial_offset_height=%d, period_height=%d, trailing_offset_height=%d" % (initial_offset_height, period_height, trailing_offset_height))
            verboseprint("g_chamber_heights", g_chamber_heights)
            verboseprint("skyline", skyline)
            print_chamber()
            break
        except ValueError:
            g_skylines.append(skyline)
            g_chamber_heights.append(g_chamber_height)
    try:
        g_chamber_height = total_height
    except NameError:
        pass
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
        if jet_push_dir == RIGHT_PUSH:
            falling_rock = move_right(falling_rock)
        elif jet_push_dir == LEFT_PUSH:
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
        #verboseprint("Can move right", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x+1,y))
            g_chamber[(x+1,y)] = FALLING_ROCK
    else:
        #verboseprint("Cannot move right", rock)
        rock_after = rock
    return rock_after

def move_left(rock):
    can_move = True
    for (x,y) in rock:
        if x == 0 or g_chamber[(x-1,y)] == ROCK_SPACE:
            can_move = False
            break
    if can_move:
        #verboseprint("Can move left", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x-1,y))
            g_chamber[(x-1,y)] = FALLING_ROCK
    else:
        #verboseprint("Cannot move left", rock)
        rock_after = rock
    return rock_after

def move_down(rock):
    can_move = True
    for (x,y) in rock:
        if y == 0 or g_chamber[(x,y-1)] == ROCK_SPACE:
            can_move = False
            break
    if can_move:
        #verboseprint("Can move down", rock)
        rock_after = []
        for (x,y) in rock:
            g_chamber[(x,y)] = EMPTY_SPACE
        for (x,y) in rock:
            rock_after.append((x,y-1))
            g_chamber[(x,y-1)] = FALLING_ROCK
    else:
        #verboseprint("Cannot move down", rock)
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

def get_skyline(rock_index):
    """Example
|...@...|
|..@@@..|
|...@...|
|.......|
|.......|
|.......|
|..####.|
+-------+

|.......| y=0
|...#...| y=1
|..###..| y=2
|...#...| y=3
|..####.| y=4
+-------+
 |
 x=0
  |
  x=1
       |
       x=6
Skyline: j0  r1  0,0  0,1  0,2  0,3  0,4  1,4  2,3  1,2  2,1  4,1  5,2  4,3  5,3  6,4  6,3  6,2  6,1  6,0

|.......| y=0
|.#...#.| y=1
|###.###| y=2
|.#...##| y=3
|####..#| y=4
|...##.#| y=5
|...##.#| y=6
+-------+

Skyline: j0  r1  0,0  0,1  1,0  2,1  3,2  2,3  3,3  4,4  5,5  5,6  5,5  5,4  4,3  3,2  4,1  5,0  6,1  6,0

Directions:
               U
              L R
               D

Current pos   Current dir  Pos to scan           Scan dir  Pos to check    Next pos  Next dir  Assert
 0,0           D            DL,L,UL D,DR,R,UR,U   CW        DL:-1,1 OUT
 0,0           D            DL,L,UL D,DR,R,UR,U   CCW       D:0,1 EMPTY     0,1       D
 0,1           D            DL,L,UL D,DR,R,UR,U   CW        DL:-1,2 OUT
 0,1           D            DL,L,UL D,DR,R,UR,U   CCW       D:0,2 ROCK
 0,1           D            DL,L,UL D,DR,R,UR,U   CCW       DR:1,2 ROCK
 0,1           D            DL,L,UL D,DR,R,UR,U   CCW       R:1,1 ROCK
 0,1           D            DL,L,UL D,DR,R,UR,U   CCW       UR:1,0 EMPTY    1,0       UR
 1,0           UR           R,DR,D UR,U,UL,L,DL   CW        R:2,0 EMPTY
 1,0           UR           R,DR,D UR,U,UL,L,DL   CW        DR:2,1 EMPTY
 1,0           UR           R,DR,D UR,U,UL,L,DL   CW        D:1,1 ROCK      2,1       DR
 2,1           DR           D,DL,L DR,R,UR,U,DL   CW        D:2,2 ROCK
 2,1           DR           D,DL,L DR,R,UR,U,DL   CCW       DR:3,2 EMPTY    3,2       DR
 3,2           DR           D,DL,L DR,R,UR,U,DL   CW        D:3,3 EMPTY
 3,2           DR           D,DL,L DR,R,UR,U,DL   CW        DL:2,3 EMPTY
 3,2           DR           D,DL,L DR,R,UR,U,DL   CW        L:2,2 ROCK      2,3       DL
 2,3           DL           L,UL,U DL,D,DR,R,UR   CW        L:1,3 ROCK
 2,3           DL           L,UL,U DL,D,DR,R,UR   CCW       DL:1,4 ROCK
 2,3           DL           L,UL,U DL,D,DR,R,UR   CCW       D:2,4 ROCK
 2,3           DL           L,UL,U DL,D,DR,R,UR   CCW       DR:3,4 ROCK
 2,3           DL           L,UL,U DL,D,DR,R,UR   CCW       R:3,3 EMPTY     3,3       R
 3,3           R            DR,D,DL R,UR,U,UL,L   CW        DR:4,4 EMPTY
 3,3           R            DR,D,DL R,UR,U,UL,L   CW        D:3,4 ROCK      4,4       DR
 4,4           DR           D,DL,L DR,R,UR,U,UL   CW        D:4,5 ROCK
 4,4           DR           D,DL,L DR,R,UR,U,UL   CCW       DR:5,5 EMPTY    5,5       DR
 5,5           DR           D,DL,L DR,R,UR,U,UL   CW        D:5,6 EMPTY
 5,5           DR           D,DL,L DR,R,UR,U,UL   CW        DL:4,6 ROCK     5,6       D
 5,6           D            DL,L,UL D,DR,R,UR,U   CW        DL:4,7 OUT
 5,6           D            DL,L,UL D,DR,R,UR,U   CCW       D:5,7 OUT
 5,6           D            DL,L,UL D,DR,R,UR,U   CCW       DR:6,7 OUT
 5,6           D            DL,L,UL D,DR,R,UR,U   CCW       R:6,6 ROCK
 5,6           D            DL,L,UL D,DR,R,UR,U   CCW       UR:6,5 ROCK
 5,6           D            DL,L,UL D,DR,R,UR,U   CCW       U:5,5 EMPTY     5,5       U
 5,5           U            UR,R,DR U,UL,L,DL,D   CW        UR:6,4 ROCK
 5,5           U            UR,R,DR U,UL,L,DL,D   CCW       U:5,4 EMPTY     5,4       U
 5,4           U            UR,R,DR U,UL,L,DL,D   CW        UR:6,3 ROCK
 5,4           U            UR,R,DR U,UL,L,DL,D   CCW       U:5,3 ROCK
 5,4           U            UR,R,DR U,UL,L,DL,D   CCW       UL:4,3 EMPTY    4,3       UL
 4,3           UL           U,UR,R UL,L,DL,D,DR   CW        U:4,2 ROCK
 4,3           UL           U,UR,R UL,L,DL,D,DR   CCW       UL:3,2 EMPTY    3,2       UL
 3,2           UL           U,UR,R UL,L,DL,D,DR   CW        U:3,1 EMPTY
 3,2           UL           U,UR,R UL,L,DL,D,DR   CW        UR:4,1 EMPTY
 3,2           UL           U,UR,R UL,L,DL,D,DR   CW        R:4,2 ROCK      4,1       UR
 4,1           UR           R,DR,D UR,U,UL,L,DL   CW        R:5,1 ROCK
 4,1           UR           R,DR,D UR,U,UL,L,DL   CCW       UR:5,0 EMPTY    5,0       UR
 5,0           UR           R,DR,D UR,U,UL,L,DL   CW        R:6,0 EMPTY
 5,0           UR           R,DR,D UR,U,UL,L,DL   CW        DR:6,1 EMPTY
 5,0           UR           R,DR,D UR,U,UL,L,DL   CW        D:5,1 ROCK      6,1       DR
 6,1           DR           D,DL,L DR,R,UR,U,UL   CW        D:6,2 ROCK
 6,1           DR           D,DL,L DR,R,UR,U,UL   CCW       DR:7,2 OUT
 6,1           DR           D,DL,L DR,R,UR,U,UL   CCW       R:7,1 OUT
 6,1           DR           D,DL,L DR,R,UR,U,UL   CCW       UR:7,0 OUT
 6,1           DR           D,DL,L DR,R,UR,U,UL   CCW       U:6,0 EMPTY     6,0       U

|.......| y=0
|.#...#.| y=1
|###.###| y=2
|.#...##| y=3
|####..#| y=4
|...##.#| y=5
|...##.#| y=6
+-------+
Skyline: j0  r1  0,0  0,1  1,0  2,1  3,2  2,3  3,3  4,4  5,5  5,6  5,5  5,4  4,3  3,2  4,1  5,0  6,1  6,0

scanned_pos = None
next_pos_candidate = None
while scanned_pos is EMPTY or None
    scanned_pos = scan clock wise
    if scanned_pos is EMPTY:
        next_pos_candidate = scanned_pos
if next_pos_candidate is None:
    scanned_pos = None
    next_pos_candidate = None
    while scanned_pos is not EMPTY or None
        scanned_pos = scan counter clock wise
        if scanned_pos is EMPTY:
            next_pos_candidate = scanned_pos
next_pos = next_pos_candidate
    """
    skyline = 'j'+str(g_jet_pattern_index) + '  r'+str(rock_index)
    cur_pos = (0,0)
    cur_dir = DOWN
    skyline += '  ' + get_pos_str(cur_pos)
    next_pos = cur_pos
    last_pos = (CHAMBER_WIDTH-1,0)
    while next_pos != last_pos:
        scanned_pos = None
        next_pos_candidate = None
        next_dir_candidate = None
        scanned_pos_empty = False
        for d in get_dir_to_scan_cw(cur_dir):
            scanned_pos = get_next_pos(cur_pos, d)
            x, y = scanned_pos
            if y < 0:
                scanned_pos_empty = False
                break
            elif 0 <= x < CHAMBER_WIDTH:
                if not is_corner_empty(cur_pos, scanned_pos, d):
                    scanned_pos_empty = False
                    break
                elif y == 0:
                    scanned_pos_empty = True
                    next_pos_candidate = scanned_pos
                    next_dir_candidate = d
                elif y > 0:
                    cy = g_chamber_height - y
                    if cy < 0 or g_chamber[(x,cy)] != EMPTY_SPACE:
                        scanned_pos_empty = False
                        break
                    else:
                        scanned_pos_empty = True
                        next_pos_candidate = scanned_pos
                        next_dir_candidate = d
            else:
                scanned_pos_empty = False
                break
        if next_pos_candidate is None:
            scanned_pos = None
            next_pos_candidate = None
            next_dir_candidate = None
            scanned_pos_empty = False
            for d in get_dir_to_scan_ccw(cur_dir):
                scanned_pos = get_next_pos(cur_pos, d)
                x, y = scanned_pos
                if y < 0:
                    scanned_pos_empty = False
                elif 0 <= x < CHAMBER_WIDTH:
                    if not is_corner_empty(cur_pos, scanned_pos, d):
                        scanned_pos_empty = False
                    elif y == 0:
                        scanned_pos_empty = True
                        next_pos_candidate = scanned_pos
                        next_dir_candidate = d
                        break
                    elif y > 0:
                        cy = g_chamber_height - y
                        if cy < 0 or g_chamber[(x,cy)] != EMPTY_SPACE:
                            scanned_pos_empty = False
                        else:
                            scanned_pos_empty = True
                            next_pos_candidate = scanned_pos
                            next_dir_candidate = d
                            break
                else:
                    scanned_pos_empty = False
            assert(next_pos_candidate is not None)
        next_pos = next_pos_candidate
        next_dir = next_dir_candidate
        skyline += '  ' + get_pos_str(next_pos)
        cur_pos = next_pos
        cur_dir = next_dir
    return skyline

def get_pos_str(p):
    x, y = p
    return str(x) + ',' + str(y)

def get_dir_to_scan_cw(d):
    dirs_cw = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT]
    i = dirs_cw.index(d)
    return (dirs_cw+dirs_cw)[i+1:i+4]

def get_dir_to_scan_ccw(d):
    dirs_ccw = [UP, UP_LEFT, LEFT, DOWN_LEFT, DOWN, DOWN_RIGHT, RIGHT, UP_RIGHT]
    i = dirs_ccw.index(d)
    return (dirs_ccw+dirs_ccw)[i:i+5]

def get_next_pos(pos, d):
    x, y = pos
    if UP in d:
        y -= 1
    elif DOWN in d:
        y += 1
    if LEFT in d:
        x -= 1
    elif RIGHT in d:
        x += 1
    return x,y

def is_corner_empty(p1, p2, d):
    x1, y1 = p1
    x2, y2 = p2
    cy1 = g_chamber_height - y1
    cy2 = g_chamber_height - y2
    if d == UP_LEFT:
        assert(x2 == x1-1 and y2 == y1-1)
        if y2 == 0:
            corner_empty = True
        else:
            corner_empty = (g_chamber[(x2,cy1)] == EMPTY_SPACE)
    elif d == DOWN_LEFT:
        assert(x2 == x1-1 and y2 == y1+1)
        corner_empty = (g_chamber[(x1,cy2)] == EMPTY_SPACE)
    elif d == DOWN_RIGHT:
        assert(x2 == x1+1 and y2 == y1+1)
        if y1 == 0:
            corner_empty = True
        else:
            cy1 = g_chamber_height - y1
            corner_empty = (g_chamber[(x2,cy1)] == EMPTY_SPACE)
    elif d == UP_RIGHT:
        assert(x2 == x1+1 and y2 == y1-1)
        corner_empty = (g_chamber[(x1,cy2)] == EMPTY_SPACE)
    else:
        corner_empty = True
    #corner_empty = (g_chamber[(x2,y1)] == EMPTY_SPACE) or (g_chamber[(x1,y2)] == EMPTY_SPACE)
    return corner_empty

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
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
""", 1514285714288),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
