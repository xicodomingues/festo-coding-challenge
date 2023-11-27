import re
from datetime import timedelta


def timedelta_str(td: timedelta):
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    if seconds:
        raise "WTF there are seconds"
    return f"{int(hours):02}:{int(minutes):02}"


class Entry:

    ENTRY_RE = re.compile(r"^(.+),\s+(\d+),\s+(\d+),\s+(\d{2}):(\d{2})$")

    def __init__(self, username, id, accessKey, login) -> None:
        self.username = username
        self.id = id
        self.accessKey = accessKey
        self.login = login

    @classmethod
    def parse(cls, input: str):
        m = cls.ENTRY_RE.match(input)
        if not m or len(m.groups()) != 5:
            raise "Regex not correct, check it"
        td = timedelta(hours=int(m.group(4)), minutes=int(m.group(5)))
        return Entry(m.group(1).strip(), int(m.group(2)), int(m.group(3)), td)

    def id_contains(self, sub_str: str):
        return sub_str in str(self.id)

    def has_access(self, module: int):
        return bool(self.accessKey & (1 << (8 - module)))

    def login_before(self, td: timedelta):
        return self.login < td

    def __repr__(self):
        return f"{{'{self.username}': id: {self.id}, key: {self.accessKey}, login: {timedelta_str(self.login)}}}"


def test():
    entry = Entry.parse("immenseResearch               , 500025, 8, 07:04")
    print(entry.has_access(5))
    print(entry.login_before(timedelta(hours=7, minutes=14)))


test()


def solve():
    with open("office_database.txt") as f:
        ids = 0
        access = 0
        logins = 0
        thief = []
        for line in f.readlines():
            entry = Entry.parse(line)
            is_thief = True
            if entry.id_contains("814"):
                ids += entry.id
            else:
                is_thief = False
            if entry.has_access(5):
                access += entry.id
            else:
                is_thief = False
            if entry.login_before(timedelta(hours=7, minutes=14)):
                logins += entry.id
            else:
                is_thief = False
            if is_thief:
                thief.append(entry.username)
    print(f"ids: {ids}, accesses: {access}, logins: {logins}, thief: {thief}")


solve()
