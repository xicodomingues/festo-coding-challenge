import string
import itertools
import hashlib


valid_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

possibilities = map(lambda x: "".join(x), itertools.product(valid_chars, valid_chars))

for x in possibilities:
    to_try = f"sQyW{x}3w".encode()
    if hashlib.md5(to_try).hexdigest().startswith("002a8a8b23d03e70"):
        print(to_try)
        break
    