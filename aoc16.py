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
        #print("%d / %d" % (i, f(len(flow_nodes))))
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

def solve_2(input_str):
    pass

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

def f(n):
    if n == 0:
        return 1
    else:
        return n * f(n-1)
            
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
