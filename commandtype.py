from enum import Enum, auto


class CommandType(Enum):
    CREATE = auto()
    COMMAND_JOIN = auto()
    COMMAND_START = auto()
