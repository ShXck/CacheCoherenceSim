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


class TransactionState(enum.Enum):
    UNRESOLVED = 0
    RESOLVED = 1


class TransactionType(enum.Enum):
    NO_TRANS = 0
    READ_MISS = 1
    INVALIDATE = 2
    WRITE_MISS = 3
