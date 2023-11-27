import re


disable = ["inactive", "disabled", "quiet", "standby", "idle"]
enable = ["live", "armed", "ready", "primed", "active"]
toggle = ["flipped", "toggled", "reversed", "inverted", "switched"]

def parse_line(str):
    matches = re.match("\s*(\d+): (.*)", str)
    return (int(matches.group(1)), matches.group(2).split())

def is_active(trap):
    is_active = None
    for state in trap[1]:
        if state in disable:
            is_active = False
        elif state in enable:
            is_active = True
        elif state in toggle:
            if (is_active == None):
                raise "WTF: is_active should not be None"
            is_active = not is_active
        else:
            raise Exception("WTF is this state: '{state}'")
    return is_active

with open("03_trap_logs.txt") as file:
    result = 0
    for line in file.readlines():
        trap = parse_line(line)
        if (not is_active(trap)):
            result += trap[0]
    print(result)