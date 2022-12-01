########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

import argparse

########################################################################
# Generic input parser and solver invoker for daily puzzle
########################################################################

class AocSolver:

    def __init__(self, scriptname, day_parse_input, day_solve_1, day_solve_2):
        self._day = scriptname.split('.')[0][-2:]
        self._day_parse_input = day_parse_input
        self._day_solve_1 = day_solve_1
        self._day_solve_2 = day_solve_2
        self._year = 2022

    def run(self):
        args = self._parse_cmd_line_args()
        day = self._day
        if day[0] == '0':
            day = day[1:]
        print("\n===== AoC-%d day #%s =====\n" % (self._year, day))
        input_filename = self._day + '.in'
        input_str = self._read_file(input_filename)
        self._day_parse_input(input_str)
        if args.part_2_only:
            output_1 = None
        else:
            # Part 1
            output_1 = self._day_solve_1()
            print("Answer 1:", output_1)
        if args.part_1_only:
            output_2 = None
        else:
            # Part 2
            output_2 = self._day_solve_2()
            print("Answer 2:", output_2)
        return output_1, output_2

    def solve_1(self, input_str):
        self._day_parse_input(input_str)
        return self._day_solve_1()

    def solve_2(self, input_str):
        self._day_parse_input(input_str)
        return self._day_solve_2()

    # TODO Refactor: extract as a global method of the module
    def _parse_cmd_line_args(self):
        parser = argparse.ArgumentParser()
        part_group = parser.add_mutually_exclusive_group()
        part_group.add_argument("-p1", "--part-1-only", help="solve part 1 only", action="store_true")
        part_group.add_argument("-p2", "--part-2-only", help="solve part 2 only", action="store_true")
        args = parser.parse_args()
        return args

    def _read_file(self, filename):
        """Read a file and return its contents as a multiline string.
        """
        with open(filename, 'r') as f:
            contents = f.read()
        return contents.strip()
