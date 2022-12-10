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
    program = parse_input(input_str)
    return draw_crt(program)

def parse_input(input_str):
    return input_str.strip().split('\n')

def compute_signal_strength(program, cycles):
    cpu = Cpu()
    cpu.run_strength(program, cycles)
    return cpu.get_signal_strength()

def draw_crt(program):
    cpu = Cpu()
    cpu.run_crt(program)
    return cpu.draw_crt()

class Cpu:

    def __init__(self):
        self.clock = 0
        self.strength = dict()
        self.x = 1
        self.signal_strength = 0
        self.instruction_in_cpu = None
        self.instruction_time_in_cpu = 0

    def run_strength(self, program, cycles):
        self.program = program
        t = 1
        while t <= cycles[-1]:
            if t in cycles:
                self.signal_strength += t * self.x
            if self.instruction_in_cpu is None:
                self.load_next_instruction()
            self.instruction_time_in_cpu += 1
            self.run_instruction()
            t += 1

    def run_instruction(self):
        assert(self.instruction_in_cpu is not None)
        complete = False
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
        self.instruction_in_cpu = instruction_line.split(' ')
        self.instruction_time_in_cpu = 0

    def get_signal_strength(self):
        return self.signal_strength

    def run_crt(self, program):
        self.program = program
        self.crt_x = 40
        self.crt_y = 6
        self.crt = ''
        for t in range(1, self.crt_x * self.crt_y+1):
            if self.instruction_in_cpu is None:
                self.load_next_instruction()
            self.instruction_time_in_cpu += 1
            self.update_crt(t)
            self.run_instruction()

    def update_crt(self, t):
        x = (t - 1) % self.crt_x
        if x in [self.x-1, self.x, self.x+1]:
            self.crt += '#'
        else:
            self.crt += "."

    def draw_crt(self):
        printable = "\n"
        i = 0
        for y in range(self.crt_y):
            for x in range(self.crt_x):
                printable += self.crt[i]
                i += 1
            printable += "\n"
        return printable

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
                (self.tc_1[0][0],
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
