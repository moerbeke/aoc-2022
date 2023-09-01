########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

P = namedtuple('Point',['x','y'])

SENSOR = 'S'
BACON = 'B'
NIL = '.'

def solve_1(input_str, y=2000000):
    """Solve part 1."""
    z = Zone(input_str)
    return z.count_no_beacon_at_line(y)

def solve_2(input_str):
    """Solve part 2."""
    return None

class Zone:
    """Beacon Exclusion Zone"""

    def __init__(self, input_str):
        self._beacons = []
        self._d_to_closest_beacon = {}
        for line in input_str.strip().split('\n'):
            # line:
            # Sensor at x=2, y=18: closest beacon is at x=-2, y=15
            sensor_info_from = line.find('x=')
            sensor_info_to = line.find(':')
            sensor_info = line[sensor_info_from:sensor_info_to]
            beacon_info_from = line.rfind('x=')
            beacon_info = line[beacon_info_from:]
            sensor_x_info, sensor_y_info = sensor_info.split(', ')
            sensor_x = int(sensor_x_info.split('=')[1])
            sensor_y = int(sensor_y_info.split('=')[1])
            sensor_p = P(sensor_x, sensor_y)
            beacon_x_info, beacon_y_info = beacon_info.split(', ')
            beacon_x = int(beacon_x_info.split('=')[1])
            beacon_y = int(beacon_y_info.split('=')[1])
            beacon_p = P(beacon_x, beacon_y)
            self._beacons.append(beacon_p)
            self._d_to_closest_beacon[sensor_p] = self._manhattan_distance(sensor_p, beacon_p)

    def _manhattan_distance(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def count_no_beacon_at_line(self, y):
        """Count number of positions where a beacon bannot possible be.
        
        Loop over all sensors - for each sensor:
            Compute the distance to the closest beacon: min_bd
            Loop over all x at the given y starting at sensor_x going to the left - for each p(x,y):
                if distance(p, sensor) <= min_bd:
                    if no beacon at p:
                        No beacon can be at p
                else:
                    break
            Idem going to the right
        """
        no_beacon_positions = set()
        for sensor_p, d_to_closest_beacon in self._d_to_closest_beacon.items():
            x0 = sensor_p.x
            p = P(x0,y)
            while self._manhattan_distance(p, sensor_p) <= d_to_closest_beacon:
                if p not in self._beacons:
                    no_beacon_positions.add(p)
                p = P(p.x-1,y)
            p = P(x0+1,y)
            while self._manhattan_distance(p, sensor_p) <= d_to_closest_beacon:
                if p not in self._beacons:
                    no_beacon_positions.add(p)
                p = P(p.x+1,y)
        return len(no_beacon_positions)

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):
    """Test class for the solver."""

    def setUp(self):
        self.tc_1 = [
                (
"""
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""", 26),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        """Test cases for part1."""
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0], 10), t[1])

    def test_solve_2(self):
        """Test cases for part2."""
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
