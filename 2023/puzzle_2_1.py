rules = """1. A -> BC
2. A -> CB
3. B -> DD
4. B -> BD
5. C -> CD
6. C -> FE
7. D -> AF
8. D -> FA
"""

max_size = 15
    
    
def parse_rules(rules: str):
    def parse_rule(rule):
        entries = rule.split()
        return (entries[3], entries[1])
    return dict([parse_rule(x) for x in rules.splitlines()])


def apply_rule(rule, start: str):
    res = set()
    start_index = 0
    try:
        while True:
            pos = start.index(rule[0], start_index)
            guess = start[:pos] + rule[1] + start[pos + 2:]
            if not('AE' in guess or 'BE' in guess or 'CE' in guess or 'DE' in guess or 'EE' in guess):
                res.add(guess)
            start_index = pos + 1
    except ValueError:
        pass
    return res


def do_one_sub(rules, start: str):
    res = set()
    for rule in rules:
        res.update(apply_rule(rule, start))
    return res


def try_to_simplify_to_A(rules, entry):
    res = {entry}
    while True:
        temp = set()
        for option in res:
            temp.update(do_one_sub(rules, option))
        res = temp
        if len(temp) == 1 and 'A' in temp:
            return True
        if len(temp) == 0:
            return False
        

# rules = parse_rules(rules)
# with open("21_keymaker_forge.txt") as file:
#     result = 0
#     for line in file.readlines():
#         if try_to_simplify_to_A(rules, line.strip()):
#             print("key:", line.strip())
#             break


rules = parse_rules(rules)
all_chars = set('ABCDEF')


cache = {}


def reduce_to_letter(entry: str):
    if len(entry) == 1:
        return set(entry)
    
    cached = cache.get(entry)
    if cached is not None:
        return cached
    
    possible_chars = set()
    
    for i in range(1, len(entry)):
        for a in reduce_to_letter(entry[:i]):
            for b in reduce_to_letter(entry[i:]):
                possible_chars.update(rules.get(a + b, set()))
                
                if possible_chars == all_chars:
                    cache[entry] = all_chars
                    return all_chars
    
    cache[entry] = possible_chars
    return possible_chars


with open("21_keymaker_forge.txt") as file:
    result = 0
    for line in file.readlines():
        if res := reduce_to_letter(line.strip()):
            print("key:", line.strip(), "res:", res)
            if 'A' in res:
                print("found!!")
                break