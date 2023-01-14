########################################################################
# Advent of Code 2022 - solver
#
# Copyright (C) 2022-2023 Antonio Ceballos Roa
########################################################################

########################################################################
# Algorithms
########################################################################

def solve_1(input_str):
    monkeys = parse_input(input_str)
    return compute_monkey_business(monkeys, n_turns=20)

def solve_2(input_str):
    Monkey.reset()
    monkeys = parse_input(input_str)
    return compute_monkey_business(monkeys, n_turns=10000, relief=False)

def parse_input(input_str):
    '''
    Monkey attributes:

    Monkey 0:
      Starting items: 79, 98
      Operation: new = old * 19
      Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3
    '''
    monkeys = list()
    monkeys_attrs = input_str.strip().split('\n\n')
    pn = None
    for monkey_attrs in monkeys_attrs:
        attrs = monkey_attrs.split('\n')
        n = int(attrs[0].split(' ')[1].split(':')[0])
        starting_items = [int(item.strip()) for item in attrs[1].split(':')[1].strip().split(',')]
        op_arg = attrs[2].split('= old')[1].strip().split(' ')
        test_divisor = int(attrs[3].split(' ')[-1])
        test_true = int(attrs[4].split(' ')[-1])
        test_false = int(attrs[5].split(' ')[-1])
        if pn is not None:
            assert(n == pn + 1)
        pn = n
        monkeys.append(Monkey(n, starting_items, op_arg, test_divisor, test_true, test_false))
    return monkeys

def compute_monkey_business(monkeys, n_turns, relief=True):
    play_keep_away(monkeys, n_turns, relief)
    most_active_monkeys = list(reversed(sorted([m.inspected_times for m in monkeys])))[:2]
    return most_active_monkeys[0] * most_active_monkeys[1]

def play_keep_away(monkeys, turns, relief):
    for i in range(turns):
        #verboseprint(i)
        verboseprint(i, get_printable_monkeys(monkeys))
        play_keep_away_turn(monkeys, relief)

def play_keep_away_turn(monkeys, relief):
    for monkey in monkeys:
        throws = monkey.play(relief)
        for throw in throws:
            monkeys[throw[0]].recv(throw[1])

def get_printable_monkeys(monkeys):
    printable = ""
    for monkey in monkeys:
        printable += str(monkey.inspected_times) + ";"
    return printable

class Monkey:

    SUM = '+'
    PROD = '*'
    ops = [SUM, PROD]
    OLD = 'old'
    mcm = 1

    def reset():
        Monkey.mcm = 1

    def __init__(self, n, starting_items, op_arg, test_divisor, test_true, test_false):
        self.id = n
        self.items = starting_items
        self.op = op_arg[0]
        assert(self.op in Monkey.ops)
        try:
            self.arg = int(op_arg[1])
        except ValueError:
            self.arg = op_arg[1]
        self.test_divisor = test_divisor
        self.test_true = test_true
        self.test_false = test_false
        self.inspected_times = 0
        Monkey.mcm *= self.test_divisor
        print(Monkey.mcm)

    def play(self, relief=True):
        throws = list()
        for item in self.items:
            worry_level = self.compute_worry_level(item)
            self.inspected_times += 1
            if relief:
                worry_level //= 3
            if self.test_worry_level(worry_level):
                throw_to = self.test_true
            else:
                throw_to = self.test_false
            throws.append((throw_to, worry_level))
        self.items = []
        return throws

    def compute_worry_level(self, item):
        if self.op == Monkey.SUM:
            if self.arg == Monkey.OLD:
                worry_level = item + item
            else:
                worry_level = item + self.arg
        elif self.op == Monkey.PROD:
            if self.arg == Monkey.OLD:
                worry_level = item * item
            else:
                worry_level = item * self.arg
        return worry_level

    def test_worry_level(self, worry_level):
        return worry_level % self.test_divisor == 0

    def recv(self, item):
        self.items.append(item % Monkey.mcm)

########################################################################
# Test class
########################################################################

import unittest

class TestAoc(unittest.TestCase):

    def setUp(self):
        self.tc_1 = [
                (
"""
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""", 10605),
                ]
        self.tc_2 = [
                (self.tc_1[0][0], 2713310158),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(solve_2(t[0]), t[1])
