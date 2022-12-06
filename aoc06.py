########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

def solve_1(input_str):
    return find_marker(input_str, 4)

def solve_2(input_str):
    return find_marker(input_str, 14)

def find_marker(signal, marker_length):
    signal = signal.strip()
    for i in range(len(signal)-marker_length):
        piece = signal[i:i+marker_length]
        if len(set(piece)) == marker_length:
            return i+marker_length
