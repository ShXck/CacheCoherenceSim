import enum


class States(enum.Enum):
    MODIFIED = 0
    SHARED = 1
    INVALID = 2
    OWNER = 3
    EXCLUSIVE = 4
