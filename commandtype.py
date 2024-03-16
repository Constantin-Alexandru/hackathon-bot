from enum import Enum


class CommandType(Enum):
    COMMAND_CREATE = 1
    COMMAND_JOIN = 2
    COMMAND_START = 3
    COMMAND_LEAVE = 4
