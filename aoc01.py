#!/usr/bin/env python3

########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def parse_input(input_str):
    parsed_input = input_str.strip().split('\n')
    parsed_input.append('')
    return parsed_input

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    calories = 0
    max_calories = 0
    for line in parsed_input:
        try:
            c = int(line)
            calories += c
        except ValueError:
            if calories > max_calories:
                max_calories = calories
            calories = 0
    return max_calories

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    calories = 0
    elf_calories = []
    for line in parsed_input:
        try:
            c = int(line)
            calories += c
        except ValueError:
            elf_calories.append(calories)
            calories = 0
    max_calories = sum(list(reversed(sorted(elf_calories)))[0:3])
    return max_calories
