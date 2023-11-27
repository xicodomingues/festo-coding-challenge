import string
import itertools
import hashlib


valid_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

possibilities = map(lambda x: "".join(x).encode(), itertools.product(valid_chars, valid_chars, valid_chars))

for x in possibilities:
    if hashlib.md5(x).hexdigest().startswith("19acf8371f"):
        print(x)
        break
    