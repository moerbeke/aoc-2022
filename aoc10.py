########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    program = parse_input(input_str)
    cycles = [20 + i*40 for i in range(6)]
    return compute_signal_strength(program, cycles)

def solve_2(input_str):
    return None

def parse_input(input_str):
    return input_str.strip().split('\n')

def compute_signal_strength(program, cycles):
    cpu = Cpu()
    cpu.run(program, cycles)
    return cpu.get_signal_strength()

class Cpu:

    def __init__(self):
        self.clock = 0
        self.strength = dict()
        self.x = 1
        self.signal_strength = 0
        self.instruction_in_cpu = None
        self.instruction_time_in_cpu = 0

    def run(self, program, cycles):
        self.program = program
        t = 1
        while t <= cycles[-1]:
            print(t,self.x)
            if t in cycles:
                print("--->",t,self.x,t*self.x)
                self.signal_strength += t * self.x
            if self.instruction_in_cpu is None:
                self.load_next_instruction()
            self.instruction_time_in_cpu += 1
            self.run_instruction()
            t += 1

    def run_instruction(self):
        assert(self.instruction_in_cpu is not None)
        complete = False
        print("  run instruction", self.instruction_in_cpu)
        if self.instruction_in_cpu[0] == 'noop':
            if self.instruction_time_in_cpu == 1:
                complete = True
        elif self.instruction_in_cpu[0] == 'addx':
            if self.instruction_time_in_cpu == 2:
                self.x += int(self.instruction_in_cpu[1])
                complete = True
        else:
            assert(False)
        if complete:
            self.instruction_in_cpu = None

    def load_next_instruction(self):
        assert(len(self.program) >= 1)
        instruction_line = self.program[0].strip()
        del self.program[0]
        #print(instruction_line)
        self.instruction_in_cpu = instruction_line.split(' ')
        print("  load instruction", self.instruction_in_cpu)
        self.instruction_time_in_cpu = 0

    def get_signal_strength(self):
        return self.signal_strength

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""", 13140),
                ]
        self.tc_2 = [
                (
"""
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""",
"""
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]).strip(), t[1].strip())
