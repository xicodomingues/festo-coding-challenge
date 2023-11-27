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


forbidden = {'AE', 'BE', 'CE', 'DE', 'EE', 'BAA', 'BAB', 'BAC', 'BAD', 'CAA', 'CAB', 'CAC', 'CAD', 'DAA', 'DAB', 'DAC', 'DAD', 'EAA', 'EAB', 'EAC', 'EAD'}
forbidden_starts = {'E', 'AA', 'AB', 'AC', 'AD', 'AFE'}
forbidden_ends = {'AA', 'BA', 'CA', 'DA', 'EA'}

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
        #print(temp)
        if len(temp) == 1 and 'A' in temp:
            return True
        if len(temp) == 0:
            return False



def solve(rules):
    with open("31_keymaker_forge_2.txt") as file:
        result = 0
        for line in file.readlines():
            print(line)
            if try_to_simplify_to_A(rules, line.strip()):
                print("key:", line.strip())
                break
            
            
#solve(rules)





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


#print(rules)

print(reduce_to_letter("FFCDFADFCB"))
#print(cache)
#try_to_simplify_to_A(rules, "BFCAFCBFCDDDFADCDFAFDDFEFCBDCF")

#print('AB' in "ABFCD")


def solve_mem():
    with open("2023/31_keymaker_forge_2.txt") as file:
        result = 0
        for line in file.readlines():
            if res := reduce_to_letter(line.strip()):
                print("key:", line.strip(), "res:", res)
                if 'A' in res:
                    print("found!!")
                    break
            
            
solve_mem()



##############################
# GENERATE ALL POSSIBILITIES #
##############################

def apply_rule_combo(rule, start: str):
    res = set()
    start_index = 0
    try:
        while True:
            pos = start.index(rule[1], start_index)
            guess = start[:pos] + rule[0] + start[pos + 1:]
            res.add(guess)
            start_index = pos + 1
    except ValueError:
        pass
    return res


def do_one_sub_combo(rules, start: str):
    res = set()
    for rule in rules:
        res.update(apply_rule_combo(rule, start))
    return res


def generate_all_combos(rules):
    res = {'A'}
    all = {'A'}
    times = 0
    while times < 10:
        temp = set()
        for option in res:
            temp.update(do_one_sub_combo(rules, option))
        res = temp
        all.update(res)
        times += 1
    for x in all:
        print(x)

#generate_all_combos(rules)