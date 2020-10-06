import enum


class BlockStates(enum.Enum):
    MODIFIED = 0
    SHARED = 1
    INVALID = 2
    OWNER = 3
    EXCLUSIVE = 4


class Instructions(enum.Enum):
    CALC = "CALC"
    READ = "READ"
    WRITE = "WRITE"
