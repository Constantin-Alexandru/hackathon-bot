from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from random import shuffle
import json


class CardKind(Enum):
    ROLE = auto()
    PANIC = auto()
    ACTION = auto()
    DEFENSE = auto()
    OBSTACLE = auto()


class CardType(str, Enum):
    THE_THING = "The Thing"
    INFECTED = "Infected"
    FLAMETHROWER = "Flamethrower"
    ANALYSIS = "Analysis"
    AXE = "Axe"
    SUSPICIOUS = "Suspicious"
    WHISKEY = "Whiskey"
    RESOLUTE = "Resolute"
    WATCH_YOUR_BACK = "Watch Your Back"
    CHANGE_PLACES = "Change Places"
    YOUD_BETTER_RUN = "You'd Better Run"
    SEDUCTION = "Seduction"
    SCARY = "Scary"
    IM_COMFORTABLE = "I'm Comfortable"
    NO_THANKS = "No Thanks"
    MISSED = "Missed"
    NO_BARBECUE = "No Barbecue"
    QUARANTINE = "Quarantine"
    BARRED_DOOR = "Barred Door"
    ROTTEN_ROPES = "Rotten Ropes"
    ONE_TWO_THREE = "One Two Three"
    FOUR_FIVE_SIX = "Four Five Six"
    WHERES_THE_PARTY = "Wheres The Party"
    GET_OUT_OF_HERE = "Get Out Of Here"
    FORGETFUL = "Forgetful"
    RING_AROUND_THE_ROSIE = "Ring Around The Rosie"
    LETS_BE_FRIENDS = "Lets Be Friends"
    BLIND_DATE = "Blind Date"
    OOOPS = "Ooops"
    BETWEEN_US = "Between Us"
    REVELATIONS = "Revelations"


@dataclass(eq=True, frozen=True)
class Card:
    card_type: CardType

    @property
    def kind(self) -> CardKind:
        match self.card_type:
            case CardType.THE_THING | CardType.INFECTED:
                return CardKind.ROLE
            case CardType.FLAMETHROWER | \
                CardType.ANALYSIS | \
                CardType.AXE | \
                CardType.SUSPICIOUS | \
                CardType.WHISKEY | \
                CardType.RESOLUTE | \
                CardType.WATCH_YOUR_BACK | \
                CardType.CHANGE_PLACES | \
                CardType.YOUD_BETTER_RUN | \
                CardType.SEDUCTION:
                return CardKind.ACTION
            case CardType.SCARY | \
                CardType.IM_COMFORTABLE | \
                CardType.NO_THANKS | \
                CardType.MISSED | \
                CardType.NO_BARBECUE:
                return CardKind.DEFENSE
            case CardType.QUARANTINE | CardType.BARRED_DOOR:
                return CardKind.OBSTACLE
            case CardType.ROTTEN_ROPES | \
                CardType.ONE_TWO_THREE | \
                CardType.FOUR_FIVE_SIX | \
                CardType.WHERES_THE_PARTY | \
                CardType.GET_OUT_OF_HERE | \
                CardType.FORGETFUL | \
                CardType.RING_AROUND_THE_ROSIE | \
                CardType.LETS_BE_FRIENDS | \
                CardType.BLIND_DATE | \
                CardType.OOOPS | \
                CardType.BETWEEN_US | \
                CardType.REVELATIONS:
                return CardKind.PANIC


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
            DeckFactory._load_config()

        deck_description = DeckFactory._config.get(str(player_count))
        cards: list[Card] = []

        for card_name, card_count in deck_description.items():
            for _ in range(card_count):
                cards.append(CardFactory.create_card(card_name))

        return Deck(cards)

    @staticmethod
    def _load_config():
        """Reads the config file and stores it in `_config`"""
        with open(DeckFactory.CONFIG_FILE) as config_file:
            DeckFactory._config = json.load(config_file)


class CardFactory:
    @staticmethod
    def create_card(name: str) -> Card:
        return Card(name)
