def remove_semicolon(string):
    return string.replace(";", "")

def replace_binary(string):
    return string.replace("X", "0").replace("Y", "1")

def parse_line(line, first_decoder, second_decoder):
    entry = [remove_semicolon(x) for x in line.split()]
    return (first_decoder(entry[1]), second_decoder(entry[2]),  entry[3], entry[4], entry[6])

def get_value_for_theory(line, first_decoder, second_decoder):
    entry = parse_line(line, first_decoder, second_decoder)
    a = int(entry[0], 2)
    b = int(entry[1], 2)
    if entry[2] == "G":
        res = a + b
    elif entry[2] == "L":
        res = a - b
    elif entry[2] == "W":
        res = a * b
    elif entry[2] == "P":
        res = round(a / b)
    elif entry[2] == "M":
        if b == 1:
            res = a >> 1
            if a % 2 == 1:
                res += 128
        else:
            res = a << 1
            if a >= 128:
                res += 1
    else:
        raise "Unrecognized operation"
    res = res % 2**8
    
    if entry[3] == "Q":
        as_str = '{0:b}'.format(res % 2**8)
    elif entry[3] == "E":
        as_str = '{0}'.format(res % 2**8)
    elif entry[3] == "F":
        as_str = '{0:x}'.format(res % 2**8)
    else:
        print(entry[3])
        raise "unrecognized output format"
    return as_str

def check_theory_line(line, first_decoder, second_decoder):
    as_str = get_value_for_theory(line, first_decoder, second_decoder)
    expected = line.split()[6]
    if as_str != expected:
        print(f"problem: expected: {expected}, actual: {as_str} for: {line}")
        return False
    return True
    
tests = """
input: XXXXXXXX; XXXXXXXX; G; Q; output: 0
input: XXXXXXXY; XXXXXXXX; G; Q; output: 1
input: XXXXXXXY; XXXXXXXY; G; Q; output: 10
input: XXXXXXXX; XXXXXXXX; L; Q; output: 0
input: XXXXXXXY; XXXXXXXY; L; Q; output: 0
input: XXXXXXYX; XXXXXXXY; L; Q; output: 1
input: XXXXXXYX; XXXXXXXY; G; Q; output: 11
input: XXXXXXYY; XXXXXXXY; L; Q; output: 10
input: XXXXXYXY; XXXXXXYY; G; Q; output: 1000
input: XXXXYXXX; XXXXXXXY; L; Q; output: 111
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
input: XXXXXXXY; XXXXXXXY; W; Q; output: 1
input: XXXXXXYX; XXXXXXYX; W; Q; output: 100
input: XXXXXYYY; XXXXYYXX; W; Q; output: 1010100
input: XXXXXXYY; XXXXXXYX; W; E; output: 6
input: XXXXYYYY; XXXYXXXY; W; E; output: 255
input: XXYYXXXX; YYYYXXYX; W; E; output: 96
input: YYXXYXXY; XXXYXYYX; W; Q; output: 1000110
input: YXXXYXYY; XYYXXYXX; W; E; output: 76
input: XYXXXXXX; XXXXYYXX; W; Q; output: 0
input: XXXXXXXX; XXYXXXXX; G; E; output: 64
input: XXYXXXXX; XXXXXXXX; L; E; output: 16
input: XXXXXXXX; XYXXXXXX; G; E; output: 32
input: XXXYXXXX; XXXXXXXX; L; E; output: 32
input: XXXYXYXY; XXYXYXYX; W; Q; output: 10110010
input: YYXYXXXY; YXYXYXYX; G; E; output: 171
input: XYXYYYXX; XYXXYYYY; W; Q; output: 11010100
input: XXXYYYYX; YYYYXXXY; L; E; output: 61
input: YYXYXYXY; YXYXYXYX; L; Q; output: 11011
input: XYYXYYYY; YYXYYYYY; W; E; output: 225
input: XXXXXXYY; XXXXXXYY; P; Q; output: 1
input: YXXXXXXX; XXXXYXXX; P; E; output: 16
input: XXXXYXYX; XXXXXXXY; P; F; output: a
input: XXXXXYYX; XXXXXYXY; P; F; output: 1
input: XXXXYXXX; XXXXXYXY; P; F; output: 2
input: XXXXXXYY; XXXXXXYX; P; F; output: 2
input: XYXYXXYY; XXXXXXYY; P; E; output: 33
input: YXYXXXXX; XXXXYYXX; P; E; output: 12
input: XYXYYXYY; XXXXYXYX; P; F; output: b
input: YYXXXXXX; XXXXXXYY; P; F; output: 40
input: XXXXXXYX; XXXXXXXY; M; Q; output: 1
input: XXXXXXYX; YXXXXXXX; M; E; output: 4
input: XXXXXYYX; YXXXXXXX; M; F; output: c
input: XXXYXXXX; YXXXXXXX; M; E; output: 64
input: YXXXXXYX; YXXXXXXX; M; Q; output: 101
input: YXXYYXYY; XXXXXXXY; M; F; output: d5
input: YXXXYYYY; YXXXXXXX; M; Q; output: 11111
input: XXXXXXYY; XXXXXXXY; M; E; output: 129
input: YYYXXXXX; YXXXXXXX; M; Q; output: 10100001
input: XYXYYXYY; XXXXXXXY; M; F; output: b5
"""

def check_complete_theory(lines, first_decoder, second_decoder):
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if not check_theory_line(line, first_decoder, second_decoder):
            return False
    return True


def decoder_generator(base):
    def decode_pos(entry, value):
        if entry == 'X':
            return '0' if value == '0' else '1'
        elif entry == 'Y':
            return '1' if value == '0' else '0'
        else:
            print(f"unexpected character: {entry}")
            raise "WTF"
    base_b = '{0:08b}'.format(base)
    return lambda string: "".join(decode_pos(x, base_b[i]) for i, x in enumerate(string))

def flip32_16(string):
    string = [x for x in string]
    orig = string[2]
    string[2] = string[3]
    string[3] = orig
    return replace_binary("".join(string))


def flip64_32(string):
    string = [x for x in string]
    orig = string[2]
    string[2] = string[1]
    string[1] = orig
    return replace_binary("".join(string))

def formulate_theor1(lines):
    print(check_complete_theory(lines, flip32_16, flip64_32))
    return (flip32_16, flip64_32)



to_decode = """XYYYYYYY; YXXXXXXX; M; F;
XYXYXYXX; XXXYXXYY; P; E;
YXXYXXYX; XXXXXXXY; M; E;
YYXYXXYX; XXXYXYXY; P; F;
"""

def solve(to_decode: str):
    decoder = formulate_theor1(tests.splitlines())
    for line in to_decode.splitlines():
        print(get_value_for_theory(f"-: {line} - -", decoder[0], decoder[1]), end="")
    print()

solve(to_decode)