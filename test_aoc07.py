########################################################################
# The Advent of Code 2022
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

import unittest

########################################################################
# Test class
########################################################################

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.aocsolver = daysolver
        self.tc_1 = [
                (
"""
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""", 95437),
                ]
        self.tc_2 = [
                (
"""
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
""", 24933642),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])

    def test_dir_size(self):
        t = self.tc_2[0][0]
        tree = self.aocsolver.parse_input(t)
        self.assertEqual(tree['/'].get_size(), 48381165)
