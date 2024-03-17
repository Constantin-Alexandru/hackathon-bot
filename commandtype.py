from enum import Enum, auto


class CommandType(Enum):
    CREATE = auto()
    JOIN = auto()
    START = auto()
    GAME = auto()
