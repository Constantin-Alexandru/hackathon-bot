from __future__ import annotations
from enum import Enum, auto
from deck import Card, CardType


class Player:
    pid: str
    hand: list[Card]
    role: Role

    def __init__(self, pid: str) -> None:
        self.pid = pid
        self.hand = list()
        self.role = Role.HUMAN

    def deal_card(self, card: Card) -> None:
        if card.card_type == CardType.THE_THING:
            self.role = Role.THE_THING
        self.hand.append(card)


class Role(Enum):
    HUMAN = auto()
    INFECTED = auto()
    THE_THING = auto()


class Game:
    _players: list[Player]

    def __init__(self, player_ids: list[str]) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))

    @property
    def player_count(self) -> int:
        return len(self._players)
