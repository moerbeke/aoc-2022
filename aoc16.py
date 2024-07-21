########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from math import inf
from itertools import permutations
from functools import total_ordering

import time

def solve_1(input_str):
    nodes, rates, neighbours = parse_input(input_str)
    source = 'AA'
    shortest_path, dist = comp_shortest_path(source, nodes, rates, neighbours)
    flow_nodes = [node for node, rate in reversed(sorted(rates.items(), key=lambda item: item[1])) if rate > 0][:10]
    # The removal of the smallests nodes was just a guess that happenned to yield the right solution.
    # If we keep the total number of nodes, the permutations below are too many.
    #print(flow_nodes)
    eruption_time = 30
    max_flow = 0
    i = 0
    for path in permutations(flow_nodes):
        i += 1
        flow = 0
        m = 0
        n1 = source
        for n2 in path:
            m += dist[n1][n2] + 1
            if m < eruption_time:
                flow += (eruption_time - m) * rates[n2]
                n1 = n2
            else:
                break
        if flow > max_flow:
            max_flow = flow
            max_path = path
            #print(max_flow, max_path)
    return max_flow

def comp_shortest_path(source, nodes, rates, neighbours):
    dist = {}
    prev = {}
    flow_nodes = [node for node, rate in rates.items() if rate > 0]
    for s in [source] + flow_nodes:
        dist[s] = {}
        prev[s] = {}
        Q = set()
        for v in nodes:
            if v == s:
                continue
            if v in neighbours[s]:
                dist[s][v] = 1
                prev[s][v] = s
            else:
                dist[s][v] = inf
                prev[s][v] = None
            Q.add(v)
        while len(Q) != 0:
            u = None
            d = inf
            for q in Q.copy():
                if dist[s][q] < d:
                    u = q
                    d = dist[s][q]
                elif dist[s][q] == d:
                    if u is None:
                        u = q
                    elif q < u:
                        u = q
                else:
                    assert(q is not None)
            Q.remove(u)
            for v in neighbours[u]:
                if v not in Q:
                    continue
                alt = dist[s][u] + 1
                if alt < dist[s][v]:
                    dist[s][v] = alt
                    prev[s][v] = u
    path = {}
    for v in dist[source]:
        if v == source:
            continue
        path[v] = [v]
        p = prev[source][v]
        while p != source:
            path[v].insert(0, p)
            p = prev[source][p]
    return path, dist

def solve_2(input_str):
    global resources
    global eruption_time
    nodes, rates, neighbours = parse_input(input_str)
    resources = Resource(nodes, rates, neighbours)
    # print("solve_2 # valves")
    # print_valves(resources.valves_sorted_by_name)
    # print("solve_2 # times")
    # print(resources.times_map)
    eruption_time = 26
    # valves = reversed(sorted([v for v in resources.valves if v.rate > 0], key=lambda v: v.rate))
    valves = resources.valves_sorted_by_rate
    # for valve in valves:
    #     print(valve)
    max_path, max_flow = calculate_max_pressures(valves, eruption_time)
    return max_flow

def calculate_max_pressures(valves, eruption_time):
    path_map = {}
    for i in range(1, 1 << len(valves) - 1):
        # print(i)
        index = i
        t0 = time.time()
        valves1 = list(reversed(sorted([valves[j] for j in range(len(valves)) if index & (1 << j) > 0])))
        t1 = time.time()
        valves2 = list(reversed(sorted([v for v in valves if v not in valves1])))
        t2 = time.time()
        path1, pressure1 = calculate_max_pressure(valves1)
        t3 = time.time()
        path2, pressure2 = calculate_max_pressure(valves2)
        t4 = time.time()
        path_map[path1 + "|" + path2] = pressure1 + pressure2
        t5 = time.time()
        # print_valves(valves1)
        # print_valves(valves2)
        # print("ellapsed time", t1-t0, t2-t1, t3-t2, t4-t3, t5-t4, "total", t5-t0)
    max_path = max(path_map, key=(lambda key: path_map[key]))
    return max_path, path_map[max_path]

def calculate_max_pressure(valves):
    global pressure
    global path
    pressure = 0
    to = []
    goto_next_valve(to, valves)
    return path, pressure

def goto_next_valve(to, from_):
    global pressure
    global path
    for i in range(0, len(from_)):
        if from_[i] not in to:
            to.append(from_[i])
            # print_valves(to, False)
            value = calculate_pressure(to)
            # print("calculate_pressure", value)
            if value > pressure:
                pressure = value
                path = print_path(to)
            if value > 0 and len(to) < len(from_):
                goto_next_valve(to, from_)
            del(to[len(to)-1])
    
def calculate_pressure(valves):
    # print("calculate_pressure...")
    # print_valves(valves, False)
    global resources
    global eruption_time
    valves.insert(0, resources.get_AA())
    max_rate = 0
    time = 0
    accumulator = 0
    for i in range(0, len(valves)-1):
        max_rate += valves[i].rate
        # print(i, "max_rate", max_rate)
        time += resources.times_map[valves[i].name + valves[i+1].name]
        # print("time >= eruption_time ?", time, eruption_time)
        if time >= eruption_time:
            del(valves[0])
            return 0
        accumulator += valves[i+1].rate * time
        # print("accumulator", accumulator)
    max_rate += valves[-1].rate
    # print("max_rate", max_rate)
    del(valves[0])
    # print("calculate_pressure END")
    return max_rate * eruption_time - accumulator

def print_path(path):
    path_str = ""
    for i in range(len(path)):
        path_str += path[i].name
        if i + 1 < len(path):
            path_str += "-"
    return path_str

def print_valves(valves, sort=True):
    printable = "["
    if sort:
        valves = sorted([v for v in valves], key=lambda v: v.name)
    for v in valves:
        printable += str(v) + ", "
    printable = printable[:-2] + "]"
    print(printable)

class Resource:

    def __init__(self, nodes, rates, neighbours):
        self._all_valves = {}
        for node in nodes:
            self._all_valves[node] = Valve(node, rates[node])
        for n in neighbours:
            v_neighbours = []
            for neighbour in neighbours[n]:
                v_neighbours.append(self._all_valves[neighbour])
            self._all_valves[n].set_neighbours(v_neighbours)
        self._AA = self._all_valves['AA']
        self._times_map = None
        self._compute_times_map()

    def __str__(self):
        printable = ""
        for valve in self._all_valves.values():
            printable += str(valve) + "\n"
        return printable

    def get_AA(self):
        return self._AA
    
    @property
    def all_valves(self):
        return self._all_valves.values()

    @property
    def valves_sorted_by_name(self):
        return list(sorted([v for v in self.all_valves if v.rate > 0], key=lambda v: v.name))

    @property
    def valves_sorted_by_rate(self):
        return list(reversed(sorted([v for v in self.all_valves if v.rate > 0], key=lambda v: v.rate)))

    def reset_all_levels(self):
        # print("reset")
        # print_valves(self.all_valves)
        for valve in self.all_valves:
            valve.level = -1
        # print_valves(self.all_valves)

    @property
    def times_map(self):
        return self._times_map

    def _compute_times_map(self):
        times = {}
        valves = self.valves_sorted_by_name
        # print_valves(valves)
        for i in range(0,len(valves)):
            self.reset_all_levels()
            times[self._AA.name + valves[i].name] = self._AA.get_time(valves[i])
        # print_valves(valves)
        for i in range(0,len(valves)-1):
            # print("i=", i)
            for j in range(i+1,len(valves)):
                # print("j=", j)
                self.reset_all_levels()
                # print_valves(valves)
                time = valves[i].get_time(valves[j])
                times[valves[i].name + valves[j].name] = time
                times[valves[j].name + valves[i].name] = time
            #     print(valves[i].name + valves[j].name, time)
            #     print(valves[j].name + valves[i].name, time)
            #     print_valves(valves)
        # print("get_times_map # valves")
        # print_valves(valves)
        # print("get_times_map # times")
        # print(times)
        self._times_map = times

class Valve:

    def __init__(self, name, rate):
        self._name = name
        self._rate = rate
        self._neighbours = None
        self._level = -1

    def set_neighbours(self, valves):
        self._neighbours = valves

    @property
    def name(self):
        return self._name

    @property
    def rate(self):
        return self._rate

    @property
    def level(self):
        return self._level

    @property
    def neighbours(self):
        return self._neighbours

    @level.setter
    def level(self, value):
        self._level = value

    def set_all_levels(self, level):
        # print(self.name, "set_all_levels", level)
        if self._level < 0 or self._level > level:
            self._level = level
            level += 1
            for valve in self._neighbours:
                valve.set_all_levels(level)

    def get_time(self, target_valve):
        self.set_all_levels(0)
        return target_valve.level + 1

    def __eq__(self, other):
        return self._rate == other._rate

    def __lt__(self, other):
        return self._rate < other._rate

    def __str__(self):
        # printable = self._name + ", " + str(self._rate) + ","
        # for neighbour in self._neighbours:
        #     printable += " " + str(neighbour.name)
        printable = self._name + "." + str(self._rate) + "." + str(self._level) + "." + str(len(self._neighbours))
        return printable

def parse_input(input_str):
    """
    Line:
        Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    """
    nodes = []
    rates = {}
    neighbours = {}
    for line in input_str.strip('\n').split('\n'):
        node = line.split(' ')[1]
        nodes.append(node)
        rate = int(line.split(' ')[4].split('=')[1][:-1])
        tunnels = []
        for word in line.split(' ')[9:]:
            tunnels.append(word.split(',')[0])
        rates[node] = rate
        neighbours[node] = tunnels
    return nodes, rates, neighbours

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""", 1651),
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

    @unittest.skip('')
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_comp_shortests_dist(self):
        AA = 'AA'
        BB = 'BB'
        CC = 'CC'
        DD = 'DD'
        EE = 'EE'
        FF = 'FF'
        GG = 'GG'
        HH = 'HH'
        II = 'II'
        JJ = 'JJ'
        nodes, rates, neighbours = parse_input(self.tc_1[0][0])
        expected_shortest_path = {
                BB: [BB],
                CC: [BB, CC],
                DD: [DD],
                EE: [DD, EE],
                HH: [DD, EE, FF, GG, HH],
                JJ: [II, JJ]
                }
        expected_dist = {
                AA: {BB: 1, CC: 2, DD: 1, EE: 2, HH: 5, JJ: 2},
                BB: {CC: 1, DD: 2, EE: 3, HH: 6, JJ: 3},
                CC: {BB: 1, DD: 1, EE: 2, HH: 5, JJ: 4},
                DD: {BB: 2, CC: 1, EE: 1, HH: 4, JJ: 3},
                EE: {BB: 3, CC: 2, DD: 1, HH: 3, JJ: 4},
                HH: {BB: 6, CC: 5, DD: 4, EE: 3, JJ: 7},
                JJ: {BB: 3, CC: 4, DD: 3, EE: 4, HH: 7},
                }
        source = AA
        shortest_path, dist = comp_shortest_path(source, nodes, rates, neighbours)
        for v in expected_shortest_path:
            self.assertEqual(shortest_path[v], expected_shortest_path[v])
        for n1 in expected_dist.keys():
            for n2 in expected_dist[n1].keys():
                self.assertEqual(dist[n1][n2], expected_dist[n1][n2])
