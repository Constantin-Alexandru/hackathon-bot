from __future__ import annotations
from enum import Enum, auto
from deck import DeckFactory, Deck, Card, CardType


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
    _draw_deck: Deck
    _discard_deck: Deck

    def __init__(self, player_ids: list[str]) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))
        self._draw_deck = DeckFactory.create_deck(len(self._players))
        self._discard_deck = Deck([])

    @property
    def player_count(self) -> int:
        return len(self._players)

    def start(self):
        self._draw_deck.shuffle()

        self.deal_cards()

    def deal_cards(self):
        deal_deck = Deck([])
        the_thing = self._draw_deck.get_the_thing()
        assert the_thing is not None
        deal_deck.add_card(the_thing)

        cards_to_deal = self.player_count * 4

        while deal_deck.size <= cards_to_deal:
            card_to_deal = self._draw_deck.get_deal_card()
            assert card_to_deal is not None
            deal_deck.add_card(card_to_deal)

        deal_deck.shuffle()

        for player in self._players:
            for _ in range(4):
                player.deal_card(deal_deck.draw())
