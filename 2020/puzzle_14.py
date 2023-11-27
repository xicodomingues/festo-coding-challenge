import itertools

input = """ work  -   7  22  18  16  20  18  19  10  22   3   -
   s1  -   -   -  18  14  20  14  12   5  16   5  25
   s2  -   -   -  19  14  20  12   3  10   6  17  10
   p1  -  19  23   -   -   2   8  23  14  17  15  25
   p2  -  15  17   -   -   6   2  17   9  11  12  20
   h1  -  21  23   2   7   -   -  24  16  17  17  24
   h2  -  14  14   7   2   -   -  14   8   8  13  17
   d1  -  10   3  20  14  21  13   -   -   8  15  13
   d2  -   5  12  13   9  15   8   -   -  11   6  20
   t1  -  15   7  14   9  14   7   8  10   -   -   9
   t2  -   7  20  14  13  17  14  18   8   -   -  28
"""

def windows(sequence, limit=2):
    results = []
    iteration_length = len(sequence) - (limit - 1)
    max_window_indicies = range(iteration_length)
    for index in max_window_indicies:
        results.append(sequence[index:index + limit])
    return results

def parse_distances(input):
    distances = dict()
    keys = ["work", "s1", "s2", "p1", "p2", "h1", "h2", "d1", "d2", "t1", "t2", "home"]
    for line in input.splitlines():
        entries = line.split()
        key = entries[0]
        for i, d in enumerate(entries[1:]):
            if d == "-":
                continue
            vals = distances.get(key, {})
            vals[keys[i]] = int(d)
            distances[key] = vals
    return distances
    
def calculate_dist(seq, distances):
    paths = windows(seq)
    total = distances["work"][seq[0]]
    for path in paths:
        d = distances[path[0]][path[1]]
        total += d
    total += distances[seq[-1]]["home"]
    return total
    
def replace(entries, char):
    new = []
    for s in entries:
        new += [s.replace(char, char + "1"), s.replace(char, char + "2")]
    return new
    
def generate_sequences(entry):
    new = [entry]
    for char in "sphdt":
        new = replace(new, char)
    def chunk_it(bla):
        return [bla[i:i+2] for i in range(0, len(bla), 2)]
    return [chunk_it(x) for x in new]
    

print(generate_sequences("sphdt"))
    
ds = parse_distances(input)
print(calculate_dist(["s1", "p2", "h1", "d1", "t2"], ds))
min = [10000, ""]
for perm in itertools.permutations("sphdt"):
    for entry in generate_sequences("".join(perm)):
        new_d = calculate_dist(entry, ds)
        if new_d < min[0]:
            min = (new_d, entry)
print("".join(min[1]))