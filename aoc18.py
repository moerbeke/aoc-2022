########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2024 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################


def solve_1(input_str):
    cubes = parse_input(input_str)
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

def solve_2(input_str):
    return None

def parse_input(input_str):
    cubes = []
    for line in input_str.strip().split('\n'):
        x,y,z = [int(n) for n in line.split(',')]
        cubes.append(Cube((x,y,z)))
    return(cubes)

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
