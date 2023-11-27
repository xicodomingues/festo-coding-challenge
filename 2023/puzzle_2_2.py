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
    else:
        raise "Unrecognized operation"
    res = res % 2**8
    as_str = '{0:b}'.format(res % 2**8)
    if entry[3] == "E":
        as_str = '{0}'.format(res % 2**8)
    return as_str

def check_theory_line(line, first_decoder, second_decoder):
    as_str = get_value_for_theory(line, first_decoder, second_decoder)
    expected = line.split()[6]
    if as_str != expected:
        print(f"problem: expected: {expected}, actual: {as_str}")
        return False
    return True
    
lines = """
input: XXXXXXXY; XXXXXXXY; W; Q; output: 1
input: XXXXXXYX; XXXXXXYX; W; Q; output: 100
input: XXXXXYYY; XXXXYYXX; W; Q; output: 1010100
input: XXXXXXYY; XXXXXXYX; W; E; output: 6
input: XXXXYYYY; XXXYXXXY; W; E; output: 255
input: XXYYXXXX; YYYYXXYX; W; E; output: 96
input: YYXXYXXY; XXXYXYYX; W; Q; output: 1000110
input: YXXXYXYY; XYYXXYXX; W; E; output: 76
input: XYXXXXXX; XXXXYYXX; W; Q; output: 0
"""

other_lines = """
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
    
    # for i in range(255):
    #     for j in range(255):
    #         if check_complete_theor1(lines, decoder_generator(i), decoder_generator(j)):
    #             return (decoder_generator(i), decoder_generator(j))
    print(check_complete_theory(lines, flip32_16, flip64_32))
    return (flip32_16, flip64_32)


decoder = formulate_theor1(other_lines.splitlines())

print(
    get_value_for_theory("bla: YXXYXXYY; YXYXXXYX; G; E; bla bla", decoder[0], decoder[1]),
    get_value_for_theory("bla: YXYXYXYX; YXYXXXYY; W; E; bla bla", decoder[0], decoder[1]), sep=""
    )

"""
0000 0000 : 0    +  0010 0000 : 32   =   0100 0000 : 64
0010 0000 : 32   -  0000 0000 : 0    =   0001 0000 : 16
0000 0000 : 0    +  0100 0000 : 64   =   0010 0000 : 32
0001 0000 : 16   -  0000 0000 : 0    =   0010 0000 : 32
0001 0101 : 21   *  0010 1010 : 42   =   1011 0010 : 178
1101 0001 : 209  +  1010 1010 : 170  =   1010 1011 : 171
0101 1100 : 92   *  0100 1111 : 79   =   1101 0100 : 212
0001 1110 : 30   -  1111 0001 : 241  =   0011 1101 : 61
1101 0101 : 213  -  1010 1010 : 170  =   0001 1011 : 27
0110 1111 : 111  *  1101 1111 : 223  =   1110 0001 : 225
"""

# flip 32 & 16       flip 64 & 32 
"""
0000 0000 : 0    +  0100 0000 : 32   =   0100 0000 : 64
0001 0000 : 32   -  0000 0000 : 0    =   0001 0000 : 16
0000 0000 : 0    +  0010 0000 : 64   =   0010 0000 : 32
0010 0000 : 16   -  0000 0000 : 0    =   0010 0000 : 32
0010 0101 : 21   *  0100 1010 : 42   =   1011 0010 : 178
1110 0001 : 209  +  1100 1010 : 170  =   1010 1011 : 171
0110 1100 : 92   *  0010 1111 : 79   =   1101 0100 : 212
0010 1110 : 30   -  1111 0001 : 241  =   0011 1101 : 61
1110 0101 : 213  -  1100 1010 : 170  =   0001 1011 : 27
0101 1111 : 111  *  1011 1111 : 223  =   1110 0001 : 225
"""