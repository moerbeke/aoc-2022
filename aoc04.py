########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    parsed_input = input_str.strip().split('\n')
    return parsed_input

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    n_overlap = 0
    for line in parsed_input:
        elf1, elf2 = line.split(',')
        e1_min, e1_max = elf1.split('-')
        e2_min, e2_max = elf2.split('-')
        s1 = set(range(int(e1_min), int(e1_max)+1))
        s2 = set(range(int(e2_min), int(e2_max)+1))
        if s1.issubset(s2) or s2.issubset(s1):
            n_overlap += 1
    return n_overlap

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    n_overlap = 0
    for line in parsed_input:
        elf1, elf2 = line.split(',')
        e1_min, e1_max = elf1.split('-')
        e2_min, e2_max = elf2.split('-')
        s1 = set(range(int(e1_min), int(e1_max)+1))
        s2 = set(range(int(e2_min), int(e2_max)+1))
        if len(s1.intersection(s2)) > 0:
            n_overlap += 1
    return n_overlap
