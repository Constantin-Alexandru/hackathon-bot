from __future__ import annotations
from enum import Enum, auto
import string
from typing import Optional

from async_handler import AsyncHandler
from utils import random_string


class Lobby:
    class State(Enum):
        WAITING = auto()
        CLOSED = auto()

    __host: int
    __players: list[int]
    __game: Optional[int] # TODO: add game class here

    def __init__(self, host: int):
        self.__host = host
        self.__players = {host}
        self.__game = None

    def add_player(self, player: int) -> None:
        if self.__game == None:
            self.__players.append(player)
        else:
            raise Exception("Cannot join closed lobby")

    def get_host_uid(self) -> int:
        return self.__host

    def get_player_count(self) -> int:
        return self.__players.count()
    
    def close_lobby(self) -> None:
        if (self.__players.count() < 4):
            raise Exception("Lobby too small to close")
        
        self.__game = 1 # TODO ctor game here
        
