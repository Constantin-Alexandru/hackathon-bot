from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


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


@dataclass(eq=True, frozen=True)
class Card:
    name: str
    description: str
    kind: CardKind

    def play(self, game: Game) -> None:
        raise NotImplementedError()


class Deck:
    _cards: list[Card]

    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards

    @property
    def size(self) -> int:
        return len(self._cards)

    def draw(self) -> Card:
        """Draw a card from the deck"""
        raise NotImplementedError()

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        raise NotImplementedError()

    def shuffle(self) -> None:
        """Shuffle the deck"""
        raise NotImplementedError()
