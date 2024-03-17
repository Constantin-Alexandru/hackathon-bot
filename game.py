from __future__ import annotations
from enum import Enum, auto

import discord
from deck import DeckFactory, Deck, Card, CardType, CardKind
from embedfactory import EmbedFactory
from ui_handler import UiHandler
from viewbuilder import ViewBuilder


class Player:
    pid: int
    hand: list[Card]
    role: Role

    def __init__(self, pid: int) -> None:
        self.pid = pid
        self.hand = list()
        self.role = Role.HUMAN

    def deal_card(self, card: Card) -> None:
        if card.card_type == CardType.THE_THING:
            self.role = Role.THE_THING
        self.hand.append(card)

    def give_card(self, card: Card) -> None:
        self.hand.append(card)


class Role(Enum):
    HUMAN = auto()
    INFECTED = auto()
    THE_THING = auto()


class Game:
    _players: list[Player]
    _draw_deck: Deck
    _discard_deck: Deck
    _current_player_index: int
    _ui_handler: UiHandler
    _lobby_id: str

    def __init__(
        self, player_ids: list[int], handler: UiHandler, lobby_id: str
    ) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))
        self._draw_deck = DeckFactory.create_deck(len(self._players))
        self._discard_deck = Deck([])
        self._current_player_index = 0
        self._ui_handler = handler
        self._lobby_id = lobby_id

    @property
    def player_count(self) -> int:
        return len(self._players)

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]

    def start(self):
        self._draw_deck.shuffle()

        self.deal_hands()

    def draw_card(self) -> Card:
        card = self._draw_deck.draw()
        if card is not None:
            return card

        self._draw_deck, self._discard_deck = self._discard_deck, self._draw_deck
        self._draw_deck.shuffle()
        return self._draw_deck.draw()

    def turn_start(self):
        drawn_card = self.draw_card()

        if drawn_card.kind == CardKind.PANIC:
            self.play(drawn_card)
        else:
            self.current_player.give_card(drawn_card)

        # TODO: Tell frontend what's happened

    async def turn(self):
        drawn_card = self.draw_card()

        if drawn_card.kind == CardKind.PANIC:
            self.play(drawn_card)
        else:
            self.current_player.give_card(drawn_card)
            response = await self._ui_handler.send_user_prompt(
                self.current_player.pid,
                EmbedFactory.rules(),
                ViewBuilder()
                .add_buton(
                    "Suck Cock",
                    discord.ButtonStyle.primary,
                    False,
                    f"{self._lobby_id}_{self.current_player.pid}_suck.cock",
                )
                .view(),
            )
            print(f"response: {response}")

    def play_card_index(self, idx: int):
        self.play(self.current_player.hand[idx])

    def play(self, card: Card):
        match card.card_type:
            case CardType.THE_THING | CardType.INFECTED:
                self.update_interface("Cannot play this, dumb fuck!")
            case _:
                raise NotImplementedError()

    def deal_hands(self):
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

    def update_interface(self, message: str) -> None:
        print(message)
