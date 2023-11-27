print("10010110")
# define the rules as a dictionary
rules = {
    ('X', 'X', 'R', 'Q'): '0',
    ('X', 'Y', 'R', 'Q'): '1',
    ('Y', 'X', 'R', 'Q'): '1',
    ('Y', 'Y', 'R', 'Q'): '1',
    ('X', 'X', 'N', 'Q'): '0',
    ('Y', 'X', 'N', 'Q'): '0',
    ('X', 'Y', 'N', 'Q'): '0',
    ('Y', 'Y', 'N', 'Q'): '1'
}

# define the task for the lock code
task = "YXYY; YYXY; N; Q;\nXYXX; XYYX; R; Q;"

# split the task into input sequences
input_sequences = [line.strip().split(';') for line in task.split('\n') if line.strip()]

# create formatted input tuples
formatted_inputs = []
for seq in input_sequences:
    formatted_seq = []
    for el in seq:
        if el == 'N' or el == 'Q':
            formatted_seq.append(el)
        else:
            formatted_seq += [c for c in el]
    formatted_inputs.append(tuple(formatted_seq))

# generate the code using the input sequences and rules
solutions = []
for inputs in formatted_inputs:
    try:
        output = rules[inputs]
        solutions.append(output)
    except KeyError:
        print('No solution found for inputs:', ' '.join(inputs))

code = ''.join(solutions)

print('The code is:', code)