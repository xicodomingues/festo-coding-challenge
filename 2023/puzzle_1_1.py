rules = """1. A -> BC
2. A -> CB
3. B -> DD
4. B -> BD
5. C -> CD
6. C -> FE
7. D -> AF
8. D -> FA
"""

step = "(1, 1) - (3, 1) - (7, 2)"

def parse_entry(entry):
    temp = entry.replace("(", "").replace(")", "").replace(",", "").split()
    return (int(temp[0]), int(temp[1]))

def parse_steps(step):
    entries = step.split(" - ")
    entries = [parse_entry(x) for x in entries]
    return entries
    
def parse_rules(rules: str):
    def parse_rule(rule):
        entries = rule.split()
        return (entries[1], entries[3])
    return [parse_rule(x) for x in rules.splitlines()]

def change_str(rule, pos, start):
    return start[:pos] + rule[1] + start[pos + 1:]

def apply_step(rules, start, step):
    if step[0] > len(rules):
        return False
    to_apply = rules[step[0] - 1]
    pos = step[1] - 1
    # print(pos, len(start), start, to_apply)
    if pos >= len(start) or start[pos] != to_apply[0]:
        return False
    else:
        return change_str(to_apply, pos, start)

# parse_steps(step)
# print(parse_rules(rules))
# print(apply_step(parse_rules(rules), "BC", (3, 2)))

initial = "A"

def apply_steps(rules, steps):
    res = "A"
    for step in steps:
        res = apply_step(rules, res, step)
        if res == False:
            return False
    return res

rules = parse_rules(rules)
with open("11_keymaker_recipe.txt") as file:
    result = 0
    for line in file.readlines():
        steps = parse_steps(line)
        if res := apply_steps(rules, steps):
            print(res)
            break