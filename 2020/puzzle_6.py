import string
import itertools
import hashlib


valid_chars = string.digits

possibilities = map(lambda x: "".join(x).encode(), itertools.product(valid_chars, valid_chars, valid_chars, valid_chars, valid_chars, valid_chars, valid_chars, valid_chars, valid_chars))

for x in possibilities:
    if hashlib.md5(x).hexdigest().startswith("351635d71448baca"):
        print(x)
        break