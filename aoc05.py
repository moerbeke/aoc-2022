########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    global stacks
    global instructions
    parsed_input = input_str.split('\n')
    stacks = dict()
    instructions = list()
    stack_lines = list()
    for line in parsed_input:
        if line.split(' ')[0] == 'move':
            instructions.append(line)
        elif line.strip() != '':
            stack_lines.append(line)
    parse_stack(stack_lines)

def parse_stack(lines):
    '''
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    0123456789

    Stack positions starting at 4n-3, n = 0, 1, ..., 8
    '''
    n_stacks = int(lines[-1].split()[-1])
    for n in range(1, n_stacks+1):
        stacks[n] = list()
    for line in reversed(lines[0:-1]):
        for n in range(1, n_stacks+1):
            try:
                crate = line[4*n-3]
                if crate != ' ':
                    stacks[n].append(crate)
            except IndexError:
                break

########################################################################
# Algorithms
########################################################################

def process(instruction, crate_mover):
    '''
    Instruction:
    move 1 from 2 to 1
    move <n> from <source> to target>
    '''
    tokens = instruction.split()
    n = int(tokens[1])
    source = int(tokens[3])
    target = int(tokens[5])
    crate_mover(n, source, target)

def crate_mover_9000(n, source, target):
    for i in range(n):
        crate = pop(stacks[source])
        push(stacks[target], crate)

def crate_mover_9001(n, source, target):
    heap = list()
    for i in range(n):
        crate = pop(stacks[source])
        heap.append(crate)
    for crate in reversed(heap):
        push(stacks[target], crate)

def pop(stack):
    crate = stack[-1]
    del stack[-1]
    return crate

def push(stack, crate):
    stack.append(crate)

def solve_1(input_str):
    parse_input(input_str)
    for instruction in instructions:
        process(instruction, crate_mover_9000)
    tops = ''.join([stack[-1] for stack in stacks.values()])
    return tops

def solve_2(input_str):
    parse_input(input_str)
    for instruction in instructions:
        process(instruction, crate_mover_9001)
    tops = ''.join([stack[-1] for stack in stacks.values()])
    return tops

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", 'CMZ'),
                ]
        self.tc_2 = [
                (
"""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""", 'MCD'),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
