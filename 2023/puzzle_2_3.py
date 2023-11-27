import math
import re


def parse_line(str):
    matches = re.match("\s*(\d+): (.*)", str)
    return (int(matches.group(1)), matches.group(2))


def parse_trap(line):
    def parse_side(side):
        return [x for x in side.split()]
    sides = list(parse_side(x) for x in line.split(" - "))
    sides[0] = tuple(int(x) for x in sides[0])
    sides[1] = tuple(x for x in sides[1])  # add int(x) for test file
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
        print(
            f"For {str(side[0]):<20}: p: {p:<10} s: {s:<10} gcd: {math.gcd(p, s):<10}")
        print(side)


def same_sum(side):
    a = math.prod(side[1]) * wierd_sum(side[0])
    b = math.prod(side[0]) * wierd_sum(side[1])
    return a == b


def is_solution(trap):
    if len(trap[0]) != len(trap[1]):
        return False
    values = set(trap[0] + trap[1])
    if len(values) != len(trap[0]) * 2:
        return False
    return same_sum(trap)


def find_solution_2(entry):
    (a, b) = entry
    i = 2
    target = 1 / a + 1 / b
    while True:
        if i == a or i == b:
            i += 1
            continue

        close = 1 / (target - 1/i)
        # print(i,  close)
        if (close < 0):
            i += 1
            continue
        guess = round(close)
        if is_solution(((a, b), (i, guess))):
            return (i, guess)
        i += 1

        if close > 0 and close < i:
            break


def find_solution_3(entry):
    (a, b, c) = entry
    i = 2
    target = 1 / a + 1 / b + 1 / c
    while True:
        if i in [a, b, c]:
            i += 1
            continue
        j = i + 1
        close = 0
        while True:
            if j in [a, b, c]:
                j += 1
                continue
            prev_close = close
            close = 1 / (target - 1/i - 1/j)
            # print(i, j, close)
            if (close < 0 and abs(close - prev_close) < 0.1):
                break
            if (close < 0):
                j += 1
                continue
            guess = round(close)
            if is_solution(((a, b, c), (i, j, guess))):
                return (i, j, guess)
            j += 1

            if close > 0 and close < j:
                break
        prev_close = close
        close = 1 / (target - 1/i - 1/j)
        if (close > 0 and close < i):
            break
        i += 1


def find_solution(trap):
    if len(trap[0]) != len(trap[1]):
        print(trap)
        raise "WTF!!!"
    if len(trap[0]) == 2:
        return find_solution_2(trap[0])
    else:
        return find_solution_3(trap[0])

# print(find_solution_2(3, 54))
# None None ([29, 80, 97], [18, 576, 2700480])
# print(find_solution_3((2, 4, 20)))


def test():
    with open("13_trap_balance.txt") as file:
        result = 0
        for line in file.readlines():
            trap = parse_line(line)
            parsed_trap = parse_trap(trap[1])
            if is_solution(parsed_trap):
                a = find_solution(parsed_trap)
                b = find_solution([parsed_trap[1], parsed_trap[0]])
                if a is None or b is None:
                    raise "A solution should have been found!!"
                result += trap[0]

        print(result)


# test()


def solve():
    with open("2023/23_trap_right_side.txt") as file:
        result = 0
        for line in file.readlines():
            trap = parse_line(line)
            trap_stuct = parse_trap(trap[1])
            # print(f"testing: {trap}")
            if (find_solution(trap_stuct)):
                result += trap[0]
        print(result)


solve()
