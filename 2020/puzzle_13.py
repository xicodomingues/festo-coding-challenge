
def is_valid(number):
    nbr_str = str(number)
    try:
        first = nbr_str.index("2")
        #print(first)
        second = nbr_str[first + 1:].index("0") + first
        #print(second)
        third = nbr_str[second + 1:].index("2") + second
        #print(third)
        fouth = nbr_str[third + 1:].index("0") + third
        #print(fouth)
    except ValueError:
        return True
    return False
    
print(is_valid(120))

count = 0
i = 1
while True:
    if is_valid(i):
        count += 1
    if count == 1_000_000:
        break
    i += 1
print(i)
