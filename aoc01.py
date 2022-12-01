#!/usr/bin/env python3

########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def parse_input(input_str):
    global _input_str
    _input_str = input_str.strip().split('\n')

def reset():
    return

def solve_1():
    calories = 0
    max_calories = 0
    for line in _input_str:
        try:
            c = int(line)
            calories += c
        except ValueError:
            if calories > max_calories:
                max_calories = calories
            calories = 0
    return max_calories

def solve_2():
    calories = 0
    elf_calories = []
    for line in _input_str:
        try:
            c = int(line)
            calories += c
        except ValueError:
            elf_calories.append(calories)
            calories = 0
    max_calories = sum(list(reversed(sorted(elf_calories)))[0:3])
    return max_calories


########################################################################
# main
########################################################################

if __name__ == '__main__':
    from os.path import basename
    import aocsolver
    scriptname = basename(__file__)
    aocsolver.AocSolver(scriptname, parse_input, solve_1, solve_2).run()
