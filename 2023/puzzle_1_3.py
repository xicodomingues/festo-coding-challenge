from decimal import Decimal, getcontext
from fractions import Fraction
import math
import re

def parse_line(str):
    matches = re.match("\s*(\d+): (.*)", str)
    return (int(matches.group(1)), matches.group(2))

def parse_trap(line):
    def parse_side(side):
        return [int(x) for x in side.split()]
    sides = tuple(parse_side(x) for x in line.split(" - "))
    return sides

def wierd_sum(side):
    base = math.prod(side)
    res = 0
    for x in side:
        res += base // x
    return res

def calc_gcd(side):
    if len(side[0]) == 2:
        p = math.prod(side[0])
        s = wierd_sum(side[0])
        print(f"For {str(side[0]):<20}: p: {p:<10} s: {s:<10} gcd: {math.gcd(p, s):<10}")
        print(side)

def same_sum(side):
    a = math.prod(side[1]) * wierd_sum(side[0])
    b = math.prod(side[0]) * wierd_sum(side[1])
    res = a == b
    if res:
        calc_gcd(side)
    return res


def other_test(trap):
    a = sum(Fraction(1, x) for x in trap[0])
    b = sum(Fraction(1, x) for x in trap[1])
    return a == b


def is_solution(trap):
    if len(trap[0]) != len(trap[1]):
        return False
    values = set(trap[0] + trap[1])
    if len(values) != len(trap[0]) * 2:
        return False
    a = same_sum(trap)
    b = other_test(trap)
    if (a != b):
        print("sasgsddsgsd WTF!!!!!!! ")
    return a

with open("13_trap_balance.txt") as file:
    result = 0
    for line in file.readlines():
        trap = parse_line(line)
        if is_solution(parse_trap(trap[1])):
            result += trap[0]
    print(result)