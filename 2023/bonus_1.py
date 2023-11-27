from itertools import islice
from enum import Enum


def batched(iterable, chunk_size):
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, chunk_size)):
        yield chunk


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def get_char(self):
        if self == Direction.UP:
            return "A"
        if self == Direction.DOWN:
            return "v"
        if self == Direction.LEFT:
            return "<"
        if self == Direction.RIGHT:
            return ">"

    def clockwise(self):
        if self == Direction.UP:
            return Direction.RIGHT
        if self == Direction.DOWN:
            return Direction.LEFT
        if self == Direction.LEFT:
            return Direction.UP
        if self == Direction.RIGHT:
            return Direction.DOWN

    def as_coord(self):
        if self == Direction.UP:
            return Coord(-1, 0)
        if self == Direction.DOWN:
            return Coord(1, 0)
        if self == Direction.LEFT:
            return Coord(0, -1)
        if self == Direction.RIGHT:
            return Coord(0, 1)


class Coord:

    def __init__(self, row, col) -> None:
        self.r = row
        self.c = col

    def __add__(self, other):
        r = self.r + other.r
        c = self.c + other.c
        return Coord(r, c)

    def __eq__(self, obj):
        if isinstance(obj, Coord):
            return self.r == obj.r and self.c == obj.c
        elif isinstance(obj, tuple):
            return self.r == obj[0] and self.c == obj[1]
        else:
            return False

    def at(self, direction: Direction):
        return self + direction.as_coord()

    def __hash__(self):
        return hash((self.r, self.c))

    def __repr__(self) -> str:
        return f"<{self.r}, {self.c}>"


class Battery:

    def __init__(self, lines) -> None:
        self.id = int(lines[0].replace("(", "").replace(")", "").strip())

        self.rows = len(lines) - 2
        self.columns = len(lines[1].strip())
        self.map = Battery.parse_map(lines[1:], self.rows, self.columns)

        self.sensor_active = True
        self.visited_positions = []
        self.position = Coord(1, 1)
        self.orientation = Direction.RIGHT

    @staticmethod
    def parse_map(lines, rows, columns):
        res = [['X' for i in range(columns + 2)] for j in range(rows + 2)]
        for r, line in enumerate(lines[:rows]):
            for c, char in enumerate(line[:columns]):
                if char == '>':
                    char = '.'
                res[r + 1][c + 1] = char
        return res

    def in_map(self, position: Coord):
        return position.r >= 0 and position.r < self.rows and position.c >= 0 and position.c < self.columns

    def has_charge(self, direction: Direction):
        dir_offset = direction.as_coord()
        pos = self.position + dir_offset
        while self.map[pos.r][pos.c] == '.':
            pos = pos + dir_offset

        if self.map[pos.r][pos.c] == 'O':
            return True
        return False

    def detects_charge(self):
        if not self.sensor_active:
            return False
        sensor_dir = self.orientation.clockwise()
        return self.has_charge(sensor_dir)

    def can_move(self):
        pos = self.position.at(self.orientation)
        return self.map[pos.r][pos.c] in ".O"

    def move(self):
        pos = self.position.at(self.orientation)
        if self.map[pos.r][pos.c] == '.':
            self.position = pos
            return

        if self.map[pos.r][pos.c] == 'O':
            if self.push_electron(pos) == '.':
                self.position = pos
            else:
                self.sensor_active = True

    def push_electron(self, pos: Coord):
        if self.map[pos.r][pos.c] == 'X':
            return 'X'
        if self.map[pos.r][pos.c] == '.':
            return '.'
        next_pos = pos.at(self.orientation)
        res_next = self.push_electron(next_pos)
        if res_next == '.':
            self.map[next_pos.r][next_pos.c] = 'O'
            self.map[pos.r][pos.c] = '.'
            return '.'
        else:
            self.map[pos.r][pos.c] = 'X'
            return 'X'

    def do_step(self):
        if self.sensor_active:
            self.visited_positions.append((self.position, self.orientation))
        if self.detects_charge():
            self.orientation = self.orientation.clockwise()
            self.sensor_active = False
            self.visited_positions = []
        else:
            if not self.can_move():
                self.orientation = self.orientation.clockwise()
            else:
                self.move()
                if self.position.at(self.orientation) == 'X':
                    self.sensor_active = True
                    self.visited_positions = []

    def has_visited(self):
        try:
            index = self.visited_positions.index(
                (self.position, self.orientation))
            return index != len(self.visited_positions) - 1
        except Exception:
            return False

    def get_uncharged(self):
        res = 0
        for row in self.map[1:-1]:
            for char in row[1:-1]:
                if char == 'O':
                    res += 1
        return res

    def solve(self):
        # print(self)
        while not self.has_visited():
            self.do_step()
            # print(self)
        return self.get_uncharged()

    def __repr__(self) -> str:
        res = ""
        for r, row in enumerate(self.map[1:-1]):
            for c, char in enumerate(row[1:-1]):
                if self.position == (r+1, c+1):
                    res += self.orientation.get_char()
                else:
                    res += char
            if r != len(self.map) - 3:
                res += '\n'
        res += f"    sensor: {'on' if self.sensor_active else 'off'}\n"
        return res


def test():
    test_bat = """(1)
    >.......
    .OO.O.O.
    .O....O.
    ..O..OO.
    ..O.OO..
    ........    sensor: on

    """
    bat = Battery(test_bat.splitlines(keepends=True))
    print(bat.solve())


def solve_all():
    with open("batteries.txt") as file:
        batteries = batched(file.readlines(), 22)
        for battery_lines in batteries:
            bat = Battery(battery_lines)
            if bat.solve() == 0:
                print(bat.id)


solve_all()
