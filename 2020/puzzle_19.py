
import itertools

def get_number(powers):
    return (7**powers[0])*(11**powers[1])*(13**powers[2])

numbers = []
for x in itertools.product(list(range(0, 20)), list(range(0, 20)), list(range(0, 20))):
    numbers.append(get_number(x))
numbers.sort()
print(numbers[199])