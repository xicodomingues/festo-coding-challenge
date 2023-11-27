import string
import itertools
import hashlib

def is_valid_number(x):
    val = str(x)
    has_5 = '5' in val
    has_7 = '7' in val
    if (not has_5 and not has_7):
        return False
    elif (has_5 and has_7):
        return False
    else:
        return True

count = 0
i = 5
while True:
    if is_valid_number(i):
        count += 1
    if count == 1000:
        print(i)
        break
    i += 1