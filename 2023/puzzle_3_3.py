from decimal import Decimal, getcontext
from fractions import Fraction
from functools import reduce
from itertools import product
import math
import re


def get_gcds(trap_side):
    if len(trap_side) == 3:
        res = sorted([
            math.gcd(trap_side[0], trap_side[1]),
            math.gcd(trap_side[0], trap_side[2]),
            math.gcd(trap_side[1], trap_side[2]),
        ])
    else:
        res = [math.gcd(trap_side[0], trap_side[1])]
    return res


def get_smallest(trap_side):
    if len(trap_side) == 3:
        gcds = get_gcds(trap_side)
        return Fraction(math.prod(gcds) // math.gcd(*gcds), math.prod(trap_side))
    else:
        return Fraction(math.gcd(*trap_side), math.prod(trap_side))



#solve()
# 74, 85
def test_differences():
    res = set()
    i = 0
    while True:
        temp = 74 * i % 85
        res.add(temp)
        print("i:", i, "res:", 74 * i % 85)
        i += 1
        if (len(res) == 85):
            break
    print(res)


def test_fractions(x, y):
    a = Fraction(1, x)
    b = Fraction(1, y)

    i = 1
    j = 1
    res = set()
    while True:
        temp = i * a - j * b
        j += 1
        if temp < 0:
            temp += a
            i += 1
            
        res.add(temp)
        #print(i, j, temp)
        # if temp == 2 * a * b:
        #     print(i, j)
        #     break
        if i > 1000:
            break
    
    res.difference_update([0])
    m = min(res)
    print(m)
    print("expected:", get_smallest([x, y]))

test_fractions(26, 292)

# 62, 172, 679
def test_fractions_3(x, y, z):
    res = set()
    a = Fraction(1, x)
    b = Fraction(1, y)
    c = Fraction(1, z)
    

    i = 1
    while True:
        j = 0
        k = 0
        while temp := (i * a - j * b - k * c) > 0:
            while (temp := (i * a - j * b - k * c)) > 0:
                #print(i, j, k, temp)
                res.add(temp)
                k += 1
            k = 0
            j += 1
        i += 1
        print(i)
        if (i > 70):
            break
    
    m = min(res)
    print(m)
    print("expected:", get_smallest([x, y, z]))
    print(x * y * z, m.denominator, x * y * z/m.denominator)
    
#test_fractions_3(62, 172, 679)
#test_fractions_3(58,138,568)
#test_fractions_3(122,464,1032)
#test_fractions_3(12,134,1988)

def parse_trap(line):
    matches = re.match("\s*(\d+): (.*)", line)
    entries = matches.group(2)
    sides = entries.split("-")
    res = ([int(x) for x in sides[0].split()], [int(x.replace("(", "").replace(")", "")) for x in sides[1].split()])
    return (int(matches.group(1)), res)



def solve():
    i = 0
    res = 0
    with open("2023/33_trap_water.txt") as file:
        for line in file.readlines():
            line_nbr, trap = parse_trap(line.strip())
            smallest = get_smallest(trap[1])
            target = sum(Fraction(1, x) for x in trap[0])
            # print(trap[1], smallest)
            if (smallest.numerator != 1):
                raise "WTF!!"
            solution = target * smallest.denominator
            if (solution.denominator == 1):
                res += line_nbr
            i += 1
    print(res)


solve()

#[15, 20, 42] [2, 3, 5] 30
#test_fractions_3(41, 73, 1113)
        