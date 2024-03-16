from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from random import shuffle
import json


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

    @property
    def top_card_kind(self) -> Optional[CardKind]:
        return None if self.size == 0 else self._cards[0].kind

    def draw(self) -> Optional[Card]:
        """Draw a card from the deck"""
        if self.size == 0:
            return None
        return self._cards.pop(0)

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self._cards.append(card)

    def shuffle(self) -> None:
        """Shuffle the deck"""
        shuffle(self._cards)


class DeckFactory:
    _config: Optional[dict[str, dict[str, int]]] = None
    CONFIG_FILE = "card_counts.json"

    @staticmethod
    def create_deck(player_count: int) -> Deck:
        """Creates a deck based on the player count"""
        assert 4 <= player_count <= 12

        if DeckFactory._config is None:
            DeckFactory.load_config()

        deck_description = DeckFactory._config.get(str(player_count))
        cards: list[Card] = []

        for card_name, card_count in deck_description.items():
            for _ in range(card_count):
                cards.append(CardFactory.create_card(card_name))

        return Deck(cards)

    @staticmethod
    def load_config():
        """Reads the config file and stores it in `_config`"""
        with open(DeckFactory.CONFIG_FILE) as config_file:
            DeckFactory._config = json.load(config_file)


class CardFactory:
    @staticmethod
    def create_card(name: str) -> Card:
        pass
