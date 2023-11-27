import itertools

input = """work  -   6  10   4   1   9   2   9   7   -
   a  -   -   8   7   4   3   5   5  12   5
   b  -  11   -  16  12  11  10   5  20  15
   c  -   7  13   -   3  10   5  11   4   5
   d  -   4  10   3   -   8   2   8   7   5
   e  -   3   8  11   8   -   8   4  15   7
   f  -   5   8   6   2   8   -   7  10   7
   g  -   6   4  13  10   6   8   -  17  11
   h  -  10  16   3   6  14   8  15   -   8
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
    keys = ["work", "a", "b", "c", "d", "e", "f", "g", "h", "home"]
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
    
    
ds = parse_distances(input)
print(calculate_dist("abcdefgh", ds))
min = (81, "abcdefgh")
for perm in itertools.permutations("abcdefgh"):
    new_d = calculate_dist(perm, ds)
    if new_d < min[0]:
        min = (new_d, perm)
print("".join(min[1]))