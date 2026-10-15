import re
from dataclasses import dataclass

@dataclass
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, s):
        m = re.match(r"(\d+)\.(\d+)\.(\d+)", s)
        if not m:
            raise ValueError(f"Invalid version: {s}")
        return cls(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

def bump_major(v: str):
    p = Version.parse(v)
    return f"{p.major+1}.0.0"

def bump_minor(v: str):
    p = Version.parse(v)
    return f"{p.major}.{p.minor+1}.0"

def bump_patch(v: str):
    p = Version.parse(v)
    return f"{p.major}.{p.minor}.{p.patch+1}"
