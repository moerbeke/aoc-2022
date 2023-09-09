########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from math import inf
from collections import namedtuple

P = namedtuple('Point',['x','y'])

z = None

def solve_1(input_str, y=2000000):
    """Solve part 1."""
    global z
    if z is None:
        z = Zone(input_str)
    return z.count_no_beacon_at_line(y)

def solve_2(input_str, b=4000000):
    """Solve part 2."""
    global z
    if z is None:
        z = Zone(input_str)
    return z.find_tunning_frequency(b)

class Zone:
    """Beacon Exclusion Zone"""

    def __init__(self, input_str):
        self._beacons = []
        self._d_to_closest_beacon = {}
        self._n_beacons_at_y = {}
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
            self._append_sensor_beacon(sensor_p, beacon_p)

    def _append_sensor_beacon(self, sensor_p, beacon_p):
        self._beacons.append(beacon_p)
        self._d_to_closest_beacon[sensor_p] = self._manhattan_distance(sensor_p, beacon_p)
        if beacon_p.y not in self._n_beacons_at_y.keys():
            self._n_beacons_at_y[beacon_p.y] = 0
        self._n_beacons_at_y[beacon_p.y] += 1

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
        min_x = inf 
        max_x = -inf
        no_beacon_positions = set()
        for sensor_p, d_to_closest_beacon in self._d_to_closest_beacon.items():
            x0 = sensor_p.x
            p = P(x0,y)
            while self._manhattan_distance(p, sensor_p) <= d_to_closest_beacon:
                if p not in self._beacons:
                    no_beacon_positions.add(p)
                p = P(p.x-1,y)
                if p.x-1 < min_x:
                    min_x = p.x-1
            p = P(x0+1,y)
            while self._manhattan_distance(p, sensor_p) <= d_to_closest_beacon:
                if p not in self._beacons:
                    no_beacon_positions.add(p)
                p = P(p.x+1,y)
                if p.x+1 > max_x:
                    max_x = p.x+1
        return len(no_beacon_positions)

    def find_tunning_frequency(self, b):
        a = 0
        no_beacon = {}
        f = None
        for sensor_p, d in self._d_to_closest_beacon.items():
            #print(sensor_p, d, "-----------------------------------------------------------")
            y1 = max(a, sensor_p.y - d)
            y2 = min(b, sensor_p.y + d)
            for y in range(y1, sensor_p.y):
                x1 = max(a, sensor_p.x - (y - sensor_p.y + d))
                x2 = min(b, sensor_p.x + (y - sensor_p.y + d))
                assert self._manhattan_distance(P(x1,y), sensor_p) <= d and self._manhattan_distance(P(x2,y), sensor_p) <= d
                self._add_no_beacon(no_beacon, y, x1, x2)
            for y in range(sensor_p.y, y2+1):
                x1 = max(a, sensor_p.x - (sensor_p.y + d - y))
                x2 = min(b, sensor_p.x + (sensor_p.y + d - y))
                assert self._manhattan_distance(P(x1,y), sensor_p) <= d and self._manhattan_distance(P(x2,y), sensor_p) <= d
                self._add_no_beacon(no_beacon, y, x1, x2)
        for y in range(a, b+1):
            if no_beacon[y][0][0] == a + 1:
                #print("1 FOUND", a, y)
                f = 4000000 * a + y
            elif no_beacon[y][-1][1] == b - 1:
                #print("2 FOUND", b, y)
                f = 4000000 * b + y
            else:
                max_x = no_beacon[y][0][1]
                #print(y, no_beacon[y])
                for i in range(1, len(no_beacon[y])):
                    assert no_beacon[y][i][0] >= no_beacon[y][i-1][0]
                    if no_beacon[y][i][1] <= max_x:
                        continue
                    elif no_beacon[y][i][0] <= max_x:
                        max_x = no_beacon[y][i][1]
                        continue
                    elif no_beacon[y][i][0] - no_beacon[y][i-1][1] == 2:
                        #print("3 FOUND", no_beacon[y][i-1][1] + 1, y)
                        f = 4000000 * (no_beacon[y][i-1][1] + 1) + y
                        break
                    else:
                        assert False
            if f is not None:
                return f

    def _add_no_beacon(self, intervals, y, x1, x2):
        append = False
        if y not in intervals.keys():
            intervals[y] = []
            intervals[y].append((x1, x2))
            append = False
        else:
            for i in range(len(intervals[y])):
                _x1, _x2 = intervals[y][i]
                if x2 < _x1 - 1:
                    self._insert_interval(intervals[y], i, x1, x2)
                    append = False
                elif _x1 - 1 <= x2 <= _x2 + 1:
                    self._update_interval(intervals[y], i, min(x1,_x1), max(x2,_x2))
                    append = False
                elif _x2 + 1 < x2:
                    if x1 - 1 <= _x2:
                        self._update_interval(intervals[y], i, min(x1, _x1), x2)
                        append = False
                    else:
                        append = True
                else:
                    assert False
        if append:
            self._append_interval(intervals[y], x1, x2)


    def _insert_interval(self, intervals, i, x1, x2):
        a, b = x1, x2
        if i > 0:
            a = max(x1, intervals[i-1][0])
        intervals.insert(i, (a, b))

    def _update_interval(self, intervals, i, x1, x2):
        a, b = x1, x2
        if i > 0:
            a = max(x1, intervals[i-1][0])
        intervals[i] = (a, b)

    def _append_interval(self, intervals, x1, x2):
        a, b = x1, x2
        intervals.append((a, b))

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
Sensor at x=20, y=1: closest beacon is at x=15, y=3""", 56000011),
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
            self.assertEqual(solve_2(t[0], 20), t[1])
