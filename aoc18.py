########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################


import sys
sys.setrecursionlimit(6000)

def solve_1(input_str):
    cubes = parse_input(input_str)
    n_surface_sides = count_sides(cubes)
    return n_surface_sides

def solve_2(input_str):
    """
    Count surface sides
    Count air pockets
    Count sides of air pockets
    Exterior sides = surface sides - sides of air pockets
    """
    cubes = parse_input(input_str)
    n_surface_sides = count_sides(cubes)
    air_pockets = compute_air_pockets([cube.centre for cube in cubes])
    n_air_pocket_sides = count_sides(air_pockets)
    return n_surface_sides - n_air_pocket_sides

def parse_input(input_str):
    cubes = []
    for line in input_str.strip().split('\n'):
        x,y,z = [int(n) for n in line.split(',')]
        cubes.append(Cube((x,y,z)))
    return(cubes)

def count_sides(cubes):
    all_sides = []
    common_sides = []
    for cube in cubes:
        for side in cube.sides:
            if side in all_sides:
                if side not in common_sides:
                    common_sides.append(side)
            else:
                all_sides.append(side)
    return len(all_sides) - len(common_sides)

AIR = '.'
AIR = '.'
STEAM = '~'
LAVA = '#'

cells = {}

def compute_air_pockets(cube_centres):
    global min_x
    global max_x
    global min_y
    global max_y
    global min_z
    global max_z
    min_x = min([x for (x,y,z) in cube_centres]) - 1
    max_x = max([x for (x,y,z) in cube_centres]) + 1
    min_y = min([y for (x,y,z) in cube_centres]) - 1
    max_y = max([y for (x,y,z) in cube_centres]) + 1
    min_z = min([z for (x,y,z) in cube_centres]) - 1
    max_z = max([z for (x,y,z) in cube_centres]) + 1
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                if (x,y,z) in cube_centres:
                    cells[(x,y,z)] = LAVA
                else:
                    cells[(x,y,z)] = AIR
    propagate_steam(0, 0, 0)
    air_pockets = []
    printable = ""
    for p in cells:
        if cells[p] == AIR:
            printable += " " + str(p)
            air_pockets.append(Cube(p))
    verboseprint(printable)
    verboseprint(cells)
    return air_pockets

def propagate_steam(x0, y0, z0):
    verboseprint("Propagate from %s" % str((x0,y0,z0)))
    if cells[(x0,y0,z0)] == AIR:
        cells[(x0,y0,z0)] = STEAM
    else: 
        return
    ps = []
    ps += [(x0+i,y0,z0) for i in [-1,+1]]
    ps += [(x0,y0+i,z0) for i in [-1,+1]]
    ps += [(x0,y0,z0+i) for i in [-1,+1]]
    verboseprint("Propagate:", ps)
    for (x,y,z) in ps:
        if min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z:
            if  cells[(x,y,z)] == AIR:
                verboseprint("Steam to %s" % str((x,y,z)))
                propagate_steam(x, y, z)

class Cube:
    """
                   * z
                   *
                   B * * * D        -
                 * *     * *        |
               F * * * H   *        | L=1
               *   *   *   *        |
               *   A * * * C * * y  -
               * *     * *
               E * * * G
             *
           * x

  Cube center at (x,y,z) = (0,0,0)
  Edge length = 1

  Corners:
  A(-0.5,-0.5,-0.5)
  B(-0.5,-0.5,+0.5)
  C(-0.5,+0.5,-0.5)
  D(-0.5,+0.5,+0.5)
  E(+0.5,-0.5,-0.5)
  F(+0.5,-0.5,+0.5)
  G(+0.5,+0.5,-0.5)
  H(+0.5,+0.5,-0.5)
    
  Sides:
  ABCD
  EFGH
  CDHG
  ABEF
  ACEG
  BDFH
    """

    def __init__(self, centre):
        L = 1/2
        self._centre = centre
        x0,y0,z0 = centre
        A = (x0-L, y0-L, z0-L)
        B = (x0-L, y0-L, z0+L)
        C = (x0-L, y0+L, z0-L)
        D = (x0-L, y0+L, z0+L)
        E = (x0+L, y0-L, z0-L)
        F = (x0+L, y0-L, z0+L)
        G = (x0+L, y0+L, z0-L)
        H = (x0+L, y0+L, z0+L)
        self._corners = [A, B, C, D, E, F, G, H]
        self._sides = [
                set([A, B, C, D]),
                set([E, F, G, H]),
                set([C, D, H, G]),
                set([A, B, E, F]),
                set([A, C, E, G]),
                set([B, D, F, H])
                ]

    def __str__(self):
        printable = str(self._centre)
        return printable

    def has_side(self, side):
        return side in self._sides

    @property
    def centre(self):
        return self._centre

    @property
    def sides(self):
        return self._sides

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
1,1,1
2,1,1
""", 10),
                (
"""
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""", 64),
                ]
        self.tc_2 = [
                (
"""
1,1,1
1,1,2
1,1,3
1,2,1
1,2,2
1,2,3
1,3,1
1,3,2
1,3,3
2,1,1
2,1,2
2,1,3
2,2,1
2,2,3
2,3,1
2,3,2
2,3,3
3,1,1
3,1,2
3,1,3
3,2,1
3,2,2
3,2,3
3,3,1
3,3,2
3,3,3
""", 54),
                (
"""
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""", 58),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
