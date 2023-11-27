import string
import itertools
import hashlib


valid_chars = list(string.ascii_lowercase) #+ string.ascii_uppercase + string.digits)

random2 = map(lambda x: "".join(x), itertools.product(valid_chars, valid_chars))

first = ["0b", "Ob", "06", "O6"] # maybe even lowercase o
second = ["nO", "n0"]
third = ["6u", "bu"]


for x in itertools.product(first, second, third, random2):
    for y in itertools.permutations(x):
        to_try = "".join(y).encode()
        if hashlib.md5(to_try).hexdigest().startswith("a84ba651fd122ef5"):
            print(to_try)
            break
    