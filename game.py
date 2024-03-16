from dataclasses import dataclass
from enum import Enum, auto
from __future__ import annotations


@dataclass
class Player:
    pid: str


class Game:
    _players: list[Player]

    def __init__(self, player_ids: list[str]) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))

    @property
    def player_count(self) -> int:
        return len(self._players)


class CardKind(Enum):
    ROLE = auto()
    PANIC = auto()
    ACTION = auto()
    DEFENSE = auto()


@dataclass
class Card:
    name: str
    description: str
    kind: CardKind

    def play(self, game: Game) -> None:
        raise NotImplementedError()
