import itertools

input = """ work  -   6   3  22  20  10   -   -   -   -   -   -
  r1  -   -   5  28  18   4  22  17   8  23  26   -
  r2  -   4   -  23  18   7  17  12   8  19  21   -
  r3  -  25  21   -  21  27   5  17  22   6   4   -
  r4  -  20  20  25   -  16  19  28  10  17  26   -
  r5  -   5   9  30  16   -  23  21   6  24  28   -
  c1  -   -  16   6  16  21   -  14  16   3   6  16
  c2  -  14   -  17  24  17  14   -  17  17  14  15
  c3  -   9  10   -  10   6  19  21   -  18  24   3
  c4  -  22  18   8   -  22   4  19  16   -  10  17
  c5  -  23  18   4  22   -   5  13  21   8   -  20
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
    keys = ["work", "r1", "r2", "r3", "r4", "r5", "c1", "c2", "c3", "c4", "c5", "home"]
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
    
    
def chunk_it(bla):
    return [bla[i:i+2] for i in range(0, len(bla), 2)]
    
    
def generate_sequences(entry):
    new = [entry]
    for char in "sphdt":
        new = replace(new, char)
    return [chunk_it(x) for x in new]
    
    
def is_delivery_order_correct(entry):
    for i in range(1, 6):
        if entry.index(f"r{i}") > entry.index(f"c{i}"):
            return False
    return True
        
    
def less_three_meals(entry):
    meals = set()
    for place in entry:
        if place.startswith("r"):
            meals.add(place)
        if place.startswith("c"):
            meals.remove(f"r{place[1]}")
        if len(meals) > 3:
            return False
    return True
    
def is_valid_route(entry):
    return is_delivery_order_correct(entry) and less_three_meals(entry)
    
    
print(is_valid_route(["r1", "r2", "r3", "c1", "r5", "c2", "r4", "c3", "c4", "c5"]))
    
ds = parse_distances(input)
min = [10000, ""]
for perm in itertools.permutations(["r1", "r2", "r3", "r4", "r5", "c1", "c2", "c3", "c4", "c5"]):
    if not is_valid_route(perm):
        continue
    new_d = calculate_dist(perm, ds)
    if new_d < min[0]:
        min = (new_d, perm)
print("".join(min[1]))