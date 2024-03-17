from __future__ import annotations
from enum import Enum, auto

import discord
from deck import DeckFactory, Deck, Card, CardType, CardKind
from embedfactory import EmbedFactory
from ui_handler import UiHandler
from viewbuilder import ViewBuilder
from viewfactory import ViewFactory


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

    def __init__(self, player_ids: list[int], handler: UiHandler) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))
        self._draw_deck = DeckFactory.create_deck(len(self._players))
        self._discard_deck = Deck([])
        self._current_player_index = 0
        self._ui_handler = handler

    @property
    def player_count(self) -> int:
        return len(self._players)

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]

    @property
    def next_player(self) -> Player:
        return self._players[(self._current_player_index + 1) % self.player_count]

    @property
    def game_over(self) -> bool:
        return False  # TODO

    async def start(self):
        self._draw_deck.shuffle()

        await self.deal_hands()

        while not self.game_over:
            await self.turn()
            self.advance()

    def draw_card(self) -> Card:
        card = self._draw_deck.draw()
        if card is not None:
            return card

        self._draw_deck, self._discard_deck = self._discard_deck, self._draw_deck
        self._draw_deck.shuffle()
        return self._draw_deck.draw()

    async def turn(self):
        drawn_card = self.draw_card()

        terminates_turn = False

        if drawn_card.kind == CardKind.PANIC:
            terminates_turn = drawn_card.terminates
            await self.play(drawn_card)
        else:
            self.current_player.give_card(drawn_card)
            card = await self.pick_card(self.current_player)
            is_playing = await self.discard_or_play(self.current_player, card)
            if is_playing:
                terminates_turn = card.terminates
                await self.play(card)
            self._discard_deck.add_card(card)

        if terminates_turn:
            return

        await self.swap_cards(self.current_player, self.next_player)

    def advance(self):
        self._current_player_index = (
            self._current_player_index + 1
        ) % self.player_count

    # def play_card_index(self, idx: int):
    #     self.play(self.current_player.hand[idx])

    async def play(self, card: Card):
        match card.card_type:
            case CardType.THE_THING | CardType.INFECTED:
                self.send_error("Cannot play this, dumb fuck!")
            case _:
                raise NotImplementedError()

    async def deal_hands(self):
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

        await self.broadcast_player_cards()

    def send_error(self, message: str) -> None:
        self._ui_handler._send_message(EmbedFactory.error("", message))

    async def broadcast_player_cards(self):
        for player in self._players:
            await self._ui_handler._send_message(
                player.pid, EmbedFactory.turn("", player.hand), ViewFactory.empty()
            )

    async def pick_card(self, player: Player) -> Card:
        """!!! REMOVES THE SELECTED CARD FROM THE HAND!!!"""
        view_builder = ViewBuilder()

        for idx, card in enumerate(player.hand):

            async def callback(interaction: discord.Interaction):
                self._ui_handler.set_user_response(player.pid, idx)

            view_builder = view_builder.add_buton(card.card_type, str(idx), callback)

        response = await self._ui_handler.send_user_prompt(
            player.pid, EmbedFactory.turn("", player.hand), view_builder.view()
        )

        return player.hand.pop(response)

    async def discard_or_play(self, player: Player, card: Card) -> bool:
        """if True play, otherwise discard"""
        view_builder = ViewBuilder()

        async def play_callback(interaction: discord.Interaction):
            self._ui_handler.set_user_response(player.pid, True)

        async def discard_callback(interaction: discord.Interaction):
            self._ui_handler.set_user_response(player.pid, False)

        return await self._ui_handler.send_user_prompt(
            player.pid,
            EmbedFactory.card_info(card),
            view_builder.add_buton("Play", "play", play_callback)
            .add_buton("Discard", "discard", discard_callback)
            .view(),
        )
