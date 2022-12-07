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

OPP_ROCK = 'A'
OPP_PAPER = 'B'
OPP_SCISSORS = 'C'

MY_ROCK = 'X'
MY_PAPER = 'Y'
MY_SCISSORS = 'Z'

MY_LOSS = 'X'
MY_DRAW = 'Y'
MY_WIN = 'Z'

SHAPE = {
        OPP_ROCK: 1,
        OPP_PAPER: 2,
        OPP_SCISSORS: 3,
        MY_ROCK: 1,
        MY_PAPER: 2,
        MY_SCISSORS: 3,
        }

WIN = 6
DRAW = 3
LOSS = 0

def compute_1_round(opponent_play, my_play):
    if (my_play == MY_ROCK and opponent_play == OPP_SCISSORS or
        my_play == MY_SCISSORS and opponent_play == OPP_PAPER or
        my_play == MY_PAPER and opponent_play == OPP_ROCK):
        points = WIN
    elif (my_play == MY_ROCK and opponent_play == OPP_PAPER or
        my_play == MY_SCISSORS and opponent_play == OPP_ROCK or
        my_play == MY_PAPER and opponent_play == OPP_SCISSORS):
        points = LOSS
    else:
        points = DRAW
    points += SHAPE[my_play]
    return points

def compute_2_round(opponent_play, my_play):
    if my_play == MY_WIN:
        points = WIN
        if opponent_play == OPP_ROCK:
            my_shape = MY_PAPER
        elif opponent_play == OPP_SCISSORS:
            my_shape = MY_ROCK
        elif opponent_play == OPP_PAPER:
            my_shape = MY_SCISSORS
        else:
            assert(False)
    elif my_play == MY_DRAW:
        points = DRAW
        if opponent_play == OPP_ROCK:
            my_shape = MY_ROCK
        elif opponent_play == OPP_SCISSORS:
            my_shape = MY_SCISSORS
        elif opponent_play == OPP_PAPER:
            my_shape = MY_PAPER
        else:
            assert(False)
    elif my_play == MY_LOSS:
        points = LOSS
        if opponent_play == OPP_ROCK:
            my_shape = MY_SCISSORS
        elif opponent_play == OPP_SCISSORS:
            my_shape = MY_PAPER
        elif opponent_play == OPP_PAPER:
            my_shape = MY_ROCK
        else:
            assert(False)
    points += SHAPE[my_shape]
    return points

def solve_1(input_str):
    parsed_input = parse_input(input_str)
    my_score = 0
    for game_round in parsed_input:
        opponent_play, my_play = game_round.split(' ')
        round_my_score = compute_1_round(opponent_play, my_play)
        my_score += round_my_score
    return my_score

def solve_2(input_str):
    parsed_input = parse_input(input_str)
    my_score = 0
    for game_round in parsed_input:
        opponent_play, my_play = game_round.split(' ')
        round_my_score = compute_2_round(opponent_play, my_play)
        my_score += round_my_score
    return my_score

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
A Y
B X
C Z
""", 15),
                ]
        self.tc_2 = [
                (
"""
A Y
B X
C Z
""", 12),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
