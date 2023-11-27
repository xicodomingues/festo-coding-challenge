def replace_binary(string):
    return string.replace(";", "").replace("X", "0").replace("Y", "1")

def parse_line(line):
    entry = line.split()
    return (replace_binary(entry[1]), replace_binary(entry[2]), replace_binary(entry[3]), entry[6])

def check_theory(entry):
    a = int(entry[0], 2)
    b = int(entry[1], 2)
    if entry[2] == "G":
        res = a + b
    else:
        res = a - b
    print('{0:b}'.format(res % 2**8), entry[3])
    
lines = """input: XXXXXXXX; XXXXXXXX; G; Q; output: 0
input: XXXXXXXY; XXXXXXXX; G; Q; output: 1
input: XXXXXXXY; XXXXXXXY; G; Q; output: 10
input: XXXXXXXX; XXXXXXXX; L; Q; output: 0
input: XXXXXXXY; XXXXXXXY; L; Q; output: 0
input: XXXXXXYX; XXXXXXXY; L; Q; output: 1
input: XXXXXXYX; XXXXXXXY; G; Q; output: 11
input: XXXXXXYY; XXXXXXXY; L; Q; output: 10
input: XXXXXYXY; XXXXXXYY; G; Q; output: 1000
input: XXXXYXXX; XXXXXXXY; L; Q; output: 111
bla: XXXXXYXY; XXXXYXXY; G; Q; bla: --
bla: XXXXYYXY; XXXXXXYY; L; Q; bla: --
input: YXXXXXXX; YXXXXXXX; G; Q; output: 0
input: YXXXXXXY; YXXXXXXX; G; Q; output: 1
input: YYXXXXXX; YYYXXXXY; G; Q; output: 10100001
input: XXXXXXXX; XXXXXXXY; L; Q; output: 11111111
input: XXXXYYXY; XXXXYYYY; L; Q; output: 11111110
input: XYYYXXXX; YYYYXXXX; L; Q; output: 10000000
input: YXXXYXYX; YXXXYXXY; G; Q; output: 10011
input: YYXXXXYY; YYYXYXXY; L; Q; output: 11011010
input: YYXXXXXX; YYYXXYYY; G; Q; output: 10100111
input: XYXXXXXX; YXXYYYYY; L; Q; output: 10100001
bla: YXXXXYXY; XXXXXYXY; G; Q; bla: --
bla: YXXXYXYX; YYYXXXXX; L; Q; bla: --
"""
for line in lines.splitlines():
    check_theory(parse_line(line))