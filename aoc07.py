########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

from queue import Queue

def solve_1(input_str):
    tree = parse_input(input_str)
    print_tree(tree['/'])
    limit_sizes = 0
    limit = 100000
    for dir_name in tree:
        size = tree[dir_name].get_size()
        if size <= limit:
            limit_sizes += size
    return limit_sizes

def solve_2(input_str):
    tree = parse_input(input_str)
    total_space = 70000000
    required_free_space = 30000000
    root = '/'
    used_space = tree[root].get_size()
    assert(used_space <= total_space)
    unused_space = total_space - used_space
    assert(unused_space < required_free_space)
    space_to_delete = required_free_space - unused_space
    dir_sizes = [d.get_size() for d in tree.values()]
    return min([d for d in dir_sizes if d >= space_to_delete])

def parse_input(input_str):
    '''
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
    '''
    tree = dict()
    stack = Queue()
    lines = input_str.strip().split('\n')
    assert(lines[0] == '$ cd /')
    current_path = '/'
    current_dir = '/'
    tree[current_path] = Directory(current_dir)
    for line in lines[1:]:
        words = line.split()
        discriminant = words[0]
        if discriminant == '$':
            command = words[1]
            if command == 'cd':
                dir_name = words[2]
                assert(dir_name != '/')
                if dir_name == '..':
                    current_path = '/'.join(current_path.split('/')[:-2])+'/'
                    current_dir = stack.get()
                else:
                    stack.put(current_dir)
                    path = current_path + dir_name + '/'
                    if not path in tree:
                        tree[path] = Directory(dir_name)
                    current_dir = dir_name
                    current_path += current_dir + '/'
            elif command == 'ls':
                pass
        elif discriminant == 'dir':
            assert(current_path in tree)
            dir_name = words[1]
            path = current_path + dir_name + '/'
            if not path in tree:
                tree[path] = Directory(dir_name)
            tree[current_path].add_child(tree[path])
        else:
            assert(current_path in tree)
            size = int(words[0])
            filename = words[1]
            tree[current_path].add_file(filename, size)
    return tree            

class Directory:

    def __init__(self, name):
        self.name = name
        self.children = list()
        self.files = dict()

    def get_size(self):
        return sum(self.files.values()) + sum([child.get_size() for child in self.children])

    def add_child(self, child):
        self.children.append(child)

    def add_file(self, filename, size):
        self.files[filename] = size

def print_tree(node, indent=0):
    '''
- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
    '''
    verboseprint(' '*indent + '- ' + node.name + " (dir)")
    for child in node.children:
        print_tree(child, indent+2)
    for filename in node.files:
        verboseprint(' '*(indent+2) + '- ' + filename + " (filename, size=%d)" % node.files[filename])
    
########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
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
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])

    def test_dir_size(self):
        t = self.tc_2[0][0]
        tree = parse_input(t)
        self.assertEqual(tree['/'].get_size(), 48381165)
