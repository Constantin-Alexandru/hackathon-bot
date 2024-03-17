from __future__ import annotations
from enum import Enum, auto

import discord
from deck import DeckFactory, Deck, Card, CardType, CardKind
from embedfactory import EmbedFactory
from ui_handler import UiHandler
from viewbuilder import ViewBuilder
from viewfactory import ViewFactory
import random


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
    _dead_players: list[Player]
    _draw_deck: Deck
    _discard_deck: Deck
    _current_player_index: int
    _ui_handler: UiHandler

    def __init__(self, player_ids: list[int], handler: UiHandler) -> None:
        self._players = list(map(lambda pid: Player(pid), player_ids))
        self._dead_players = []
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
    def previous_player(self) -> Player:
        return self._players[(self._current_player_index - 1) % self.player_count]

    @property
    async def game_over(self) -> bool:
        if len(self._players) == 1:
            if self._players[0].role == Role.HUMAN:
                await self.broadcast_message(EmbedFactory.game_won_humans(""))
            else:
                await self.broadcast_message(EmbedFactory.game_won_thing(""))
            return True

        humans = [p for p in self._players if p.role == Role.HUMAN]
        infected = [p for p in self._players if p.role != Role.HUMAN]

        if len(self._players) == len(humans):
            await self.broadcast_message(EmbedFactory.game_won_humans(""))
        elif len(self._players == len(infected)):
            await self.broadcast_message(EmbedFactory.game_won_thing(""))

    async def start(self):
        self._draw_deck.shuffle()
        print("Deck is shuffled")

        await self.deal_hands()

        print("Cards are dealt")
        while not await self.game_over:
            print(f"It's player {self._current_player_index}'s turn")
            await self.turn()
            self.advance()
            await self.broadcast_player_cards()

    def draw_card(self) -> Card:
        card = self._draw_deck.draw()
        if card is not None:
            return card

        self._draw_deck, self._discard_deck = self._discard_deck, self._draw_deck
        self._draw_deck.shuffle()
        return self._draw_deck.draw()

    def draw_non_panic(self) -> Card:
        card = self.draw_card()
        while card.kind == CardKind.PANIC:
            self._discard_deck.add_card(card)
            card = self.draw_card()
        return card

    async def turn(self):
        drawn_card = self.draw_card()

        terminates_turn = False

        if drawn_card.kind == CardKind.PANIC:
            terminates_turn = drawn_card.terminates
            await self._ui_handler._send_message(
                self.current_player.pid, EmbedFactory.panicDrawn("", drawn_card)
            )
            await self.play(drawn_card)
        else:
            self.current_player.deal_card(drawn_card)
            card = await self.pick_card(self.current_player)

            if card.card_type != CardType.THE_THING:
                is_playing = await self.discard_or_play(self.current_player, card)
                if is_playing:
                    terminates_turn = card.terminates
                    await self.play(card)
            else:
                self.current_player.hand.append(card)

        if terminates_turn:
            return

        await self.swap_cards(self.current_player, self.next_player)

    def advance(self):
        self._current_player_index = (
            self._current_player_index + 1
        ) % self.player_count

    async def play(self, card: Card):
        match card.card_type:
            case CardType.THE_THING | CardType.INFECTED:
                await self.send_error("Cannot play this, dumb fuck!")
            case CardType.FLAMETHROWER:
                target_player = await self.pick_adjacent_player()
                await self.kill(target_player)
            case CardType.SUSPICIOUS:
                target_player = await self.pick_adjacent_player()
                await self.show_random_card(target_player)

        print(f"Card {card.card_type} played")
        self._discard_deck.add_card(card)

    async def show_random_card(self, target_player: Player):
        card_to_show = random.choice(target_player.hand)
        await self._ui_handler._send_message(
            self.current_player.pid,
            EmbedFactory.card_info(card_to_show),
            ViewBuilder().view(),
        )

    async def pick_adjacent_player(self) -> Player:
        async def next_player(interaction: discord.Interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(
                self.current_player.pid, self.next_player
            )

        async def previous_player(interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(
                self.current_player.pid, self.previous_player
            )

        view_builder = ViewBuilder()

        return await self._ui_handler.send_user_prompt(
            self.current_player.pid,
            EmbedFactory.pick_adjacent_player(""),
            view_builder.add_buton("Next Player", "next", next_player)
            .add_buton("Previous Player", "previous", previous_player)
            .view(),
        )

    async def kill(self, player: Player):
        self._players.remove(player)
        self._dead_players.append(player)
        await self._ui_handler._send_message(
            player.pid, EmbedFactory.dead(""), ViewBuilder().view()
        )

    async def swap_cards(self, offering_player: Player, receiving_player: Player):
        offered_card = await self.pick_swap_card(offering_player)

        if offered_card.card_type == CardType.THE_THING:
            offering_player.hand.append(offered_card)
            return

        print(
            f"Player {offering_player.pid} offers {offered_card.card_type} to {receiving_player.pid}"
        )

        print(f"Player {receiving_player.pid} accepts")
        response_card = await self.pick_swap_card(receiving_player)

        if response_card.card_type == CardType.THE_THING:
            receiving_player.hand.append(response_card)
            return

        print(
            f"Player {receiving_player.pid} chose to respond with {response_card.card_type}"
        )
        offering_player.give_card(response_card)
        receiving_player.give_card(offered_card)

    async def pick_swap_card(self, player: Player):
        selected_card = await self.pick_swap_card_prompt(player)

        if player.role == Role.HUMAN:
            while selected_card.card_type == CardType.INFECTED:
                player.deal_card(selected_card)
                selected_card = await self.pick_swap_card_prompt(player)
        elif player.role == Role.INFECTED:
            while all(card.card_type != CardType.INFECTED for card in player.hand):
                player.deal_card(selected_card)
                selected_card = await self.pick_swap_card_prompt(player)
        elif player.role == Role.THE_THING:
            while all(card.card_type != CardType.THE_THING for card in player.hand):
                player.deal_card(selected_card)
                selected_card = await self.pick_swap_card_prompt(player)

        return selected_card

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

        print("Generated player hands")
        await self.broadcast_player_cards()
        print("Player hands broadcasted")

    async def send_error(self, message: str) -> None:
        await self._ui_handler._send_message(
            self.current_player.pid,
            EmbedFactory.error("", message),
            ViewFactory.empty(),
        )

    async def broadcast_player_cards(self):
        for player in self._players:
            await self._ui_handler._send_message(
                player.pid,
                (
                    EmbedFactory.turn("", player.hand)
                    if player.pid == self.current_player.pid
                    else EmbedFactory.waitForTurn(
                        "",
                        f"Waiting for player {self._current_player_index + 1} to play",
                    )
                ),
                ViewFactory.empty(),
            )

    async def broadcast_message(self, embed: discord.Embed):
        for player in self._players:
            await self._ui_handler._send_message(player.pid, embed, ViewFactory.empty())

        for player in self._dead_players:
            await self._ui_handler._send_message(player.pid, embed, ViewFactory.empty())

    async def pick_card(self, player: Player) -> Card:
        """!!! REMOVES THE SELECTED CARD FROM THE HAND!!!"""
        view_builder = ViewBuilder()

        for idx, card in enumerate(player.hand):

            async def callback(interaction: discord.Interaction):
                await ack(interaction)
                self._ui_handler.set_user_response(
                    player.pid, int(interaction.data["custom_id"])
                )

            view_builder.add_buton(card.card_type, str(idx), callback)

        response = await self._ui_handler.send_user_prompt(
            player.pid, EmbedFactory.turn("", player.hand), view_builder.view()
        )

        print(f"Response card: {player.hand[response]}")

        return player.hand.pop(response)

    async def pick_swap_card_prompt(self, player: Player):
        view_builder = ViewBuilder()

        for idx, card in enumerate(player.hand):

            async def callback(interaction: discord.Interaction):
                await ack(interaction)
                self._ui_handler.set_user_response(
                    player.pid, int(interaction.data["custom_id"])
                )

            view_builder = view_builder.add_buton(card.card_type, str(idx), callback)

        response = await self._ui_handler.send_user_prompt(
            player.pid, EmbedFactory.swap_cards("", player.hand), view_builder.view()
        )

        return player.hand.pop(response)

    async def discard_or_play(self, player: Player, card: Card) -> bool:
        """if True play, otherwise discard"""
        view_builder = ViewBuilder()

        async def play_callback(interaction: discord.Interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(player.pid, True)

        async def discard_callback(interaction: discord.Interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(player.pid, False)

        return await self._ui_handler.send_user_prompt(
            player.pid,
            EmbedFactory.card_info(card),
            view_builder.add_buton("Play", "play", play_callback)
            .add_buton("Discard", "discard", discard_callback)
            .view(),
        )

    async def accept_or_defend(self, player: Player) -> bool:
        view_builder = ViewBuilder()

        async def accept_callback(interaction: discord.Interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(player.pid, True)

        async def defend_callback(interaction: discord.Interaction):
            await ack(interaction)
            self._ui_handler.set_user_response(player.pid, False)

        return await self._ui_handler.send_user_prompt(
            player.pid,
            EmbedFactory.accept_defend(""),
            view_builder.add_buton("Accept", "accept", accept_callback)
            .add_buton("Defend", "defend", defend_callback)
            .view(),
        )


async def ack(inter: discord.Interaction):
    try:
        await inter.response.send_message()
    except Exception:
        pass
