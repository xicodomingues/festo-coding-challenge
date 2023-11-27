from __future__ import annotations

import os
from pathlib import Path
import re
import numpy as np


def get_local_path(filename: str):
    return Path(os.path.dirname(os.path.realpath(__file__)), filename)


class BloodSample:

    def __init__(self, sample: str) -> None:
        self.sample = sample

    @classmethod
    def parse(cls, input: str) -> BloodSample:
        res = []
        for line in input.splitlines():
            if '|' not in line:
                continue
            res.append(line.split("|")[1])
        return BloodSample([list(x) for x in res])

    def has_pico(self) -> bool:
        def check(lines):
            for line in lines:
                s = "".join(line)
                if "pico" in s:
                    return True
                if "ocip" in s:
                    return True
            return False

        return check(self.sample) or check(np.transpose(self.sample))

    def __repr__(self) -> str:
        header = "+" + "-" * len(self.sample[0]) + "+\n"
        res = header
        for line in self.sample:
            res += '|' + "".join(line) + '|\n'
        res += header
        return res


class Person:

    PERSON_RE = re.compile(
        r"Name: ([\w ]+)\nID: (\d+)\nHome Planet: ([\w ]+)\n(.*)", re.MULTILINE | re.DOTALL)

    def __init__(self, name, id, planet, blood_sample) -> None:
        self.name = name
        self.id = id
        self.planet = planet
        self.blood_sample: BloodSample = blood_sample

    @classmethod
    def parse(cls, input: str) -> Person:
        m = cls.PERSON_RE.match(input.strip())
        if not m or len(m.groups()) != 4:
            print(input)
            raise "WTF wrong regex"
        bs = BloodSample.parse(m.group(4))
        return Person(m.group(1), int(m.group(2)), m.group(3), bs)

    def has_pico(self) -> bool:
        return self.blood_sample.has_pico()

    def __repr__(self) -> str:
        return str(self.__dict__)


def test_1():
    with open(get_local_path("lab_blood_clean.txt")) as f:
        entries = f.read().split("\n\n")
        for entry in entries:
            if BloodSample.parse(entry).has_pico():
                raise "WTF: Should not have pico"

    with open(get_local_path("lab_blood_gen1.txt")) as f:
        entries = f.read().split("\n\n")
        for entry in entries:
            if entry == "\n":
                continue
            if not BloodSample.parse(entry).has_pico():
                raise "WTF: Should have pico"


test_1()


def solve_1():
    with open(get_local_path("population.txt")) as f:
        entries = f.read().split("\n\n")

    ids = 0
    for entry in entries:
        if entry == "\n":
            continue
        person = Person.parse(entry)
        if person.has_pico():
            ids += person.id
    print(ids)


# solve_1()
import matplotlib.pyplot as plt

# These constants are to create random data for the sake of this example
N_POINTS = 100
TARGET_X_SLOPE = 2
TARGET_y_SLOPE = 3
TARGET_OFFSET = 5
EXTENTS = 5
NOISE = 5

# Create random data.
# In your solution, you would provide your own xs, ys, and zs data.
xs = [np.random.uniform(2*EXTENTS)-EXTENTS for i in range(N_POINTS)]
ys = [np.random.uniform(2*EXTENTS)-EXTENTS for i in range(N_POINTS)]
zs = []
for i in range(N_POINTS):
    zs.append(xs[i]*TARGET_X_SLOPE +
              ys[i]*TARGET_y_SLOPE +
              TARGET_OFFSET + np.random.normal(scale=NOISE))

# plot raw data
plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(xs, ys, zs, color='b')

# do fit
tmp_A = []
tmp_b = []
for i in range(len(xs)):
    tmp_A.append([xs[i], ys[i], 1])
    tmp_b.append(zs[i])
b = np.matrix(tmp_b).T
A = np.matrix(tmp_A)

# Manual solution
fit = (A.T * A).I * A.T * b
errors = b - A * fit
residual = np.linalg.norm(errors)

# Or use Scipy
# from scipy.linalg import lstsq
# fit, residual, rnk, s = lstsq(A, b)

print("solution: %f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
#print("errors: \n", errors)
print("residual:", residual)

# plot plane
xlim = ax.get_xlim()
ylim = ax.get_ylim()
X, Y = np.meshgrid(np.arange(xlim[0], xlim[1]),
                   np.arange(ylim[0], ylim[1]))
Z = np.zeros(X.shape)
for r in range(X.shape[0]):
    for c in range(X.shape[1]):
        Z[r, c] = fit[0] * X[r, c] + fit[1] * Y[r, c] + fit[2]
ax.plot_wireframe(X, Y, Z, color='k')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
