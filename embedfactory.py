from __future__ import annotations
from embedbuilder import EmbedBuilder
from discord import Embed, Colour
from game import Card, CardKind


class EmbedFactory:

    @staticmethod
    def error(session_id: str, error_msg: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.red())
            .title(":x: Error Occured! :x:")
            .description(error_msg)
            .footer("Session ID: " + session_id)
            .embed()
        )

    @staticmethod
    def waitForStart(session_id: str, player_count: int) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.light_grey() if player_count < 4 else Colour.green())
            .title(f":video_game: Session ID: {session_id} :video_game:")
            .description("One session of the game can have between 4 and 12 players.")
            .field("Players", f"{player_count} / 12")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def waitForTurn(session_id: str, action: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.blurple())
            .title(":hourglass: Waiting for your turn... :hourglass:")
            .description(action)
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def turn(session_id: str, cards: list[Card]) -> Embed:
        embed = (
            EmbedBuilder()
            .colour(Colour.gold())
            .title(":white_check_mark: It is your turn :white_check_mark:")
            .description("Pick your action")
        )

        for card in cards:
            embed.tooltip(card.card_type, card.description)

        return embed.footer(f"Session ID: {session_id}").embed()

    @staticmethod
    def accept_defend(session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.gold())
            .title("A trade was offered. What do you do?")
            .description("Will you accept or defend?")
            .footer(f"Session ID: {session_id}")
        )

    @staticmethod
    def swap_cards(session_id: str, cards: list[Card]) -> Embed:
        embed = (
            EmbedBuilder()
            .colour(Colour.gold())
            .title("Choose a card to swap")
            .description("Pick any of your cards to swap")
        )

        for card in cards:
            embed.tooltip(card.card_type, card.description)

        embed.footer(f"Session ID: {session_id}")

        return embed.embed()

    @staticmethod
    def defend_cards(session_id: str, cards: list[Card]) -> Embed:
        embed = (
            EmbedBuilder()
            .colour(Colour.gold())
            .title("Choose a card to defend")
            .description("Pick any of your cards to defend")
        )

        for card in cards:
            embed.tooltip(card.card_type, card.description)

        embed.footer(f"Session ID: {session_id}")

        return embed.embed()

    @staticmethod
    def card_info(card: Card) -> Embed:
        return (
            EmbedBuilder()
            .colour(EmbedFactory.card_colour(card))
            .title(f":black_joker: {card.card_type} :black_joker:")
            .description(card.card_type)
            .field("Card Type: ", EmbedFactory.card_type(card))
            .embed()
        )

    @staticmethod
    def game_won_humans(session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.green())
            .title(":trophy: The Thing has lost the game! :trophy:")
            .description(
                "The Thing has been eliminated and all remaining players are not infected."
            )
            .footer(f"Session ID: {session_id}")
        )

    @staticmethod
    def game_won_thing(session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.dark_grey())
            .title(":x: The Thing has won the game! :x:")
            .description(
                "All remaining players have are now infected, the Thing and the infected have won."
            )
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def game_over(session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.light_grey())
            .title(":x: Game Over! :x:")
            .description("The game has ended")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def rules() -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.light_grey())
            .title("Rules of Stay Away!")
            .description(
                "At the start of the game 4 cards will be dealt to each player. \
                \n One player will recieve a card known as 'The Thing'. \
                \n \
                \n The Thing must infect all other players in order to win. \
                \n The uninfected must eliminate The Thing and all of the  \
                infected to win. \
                \n \
                \n Each turn, a player will draw a card and add it to their hand. \
                \n They must then either play or discard a card.\
                \n Discarding a card will remove it from your hand and have no effect. \
                \n Playing a card will trigger the effect described on that card \
                \n and also remove it from your deck. \
                \n \
                \n For example, if you play a card which states 'Eliminate an adjacent player', \
                \n you can choose a player to eliminate whereas if you discard it then it \
                \n will take no affect. Discarded cards may not be viewed by other players, \
                \n whilst cards you play will be visible to all players \
                \n \
                \n At the end of your turn, you will trade one card with the next player \
                \n but you will neither of you will know what the other player will give you. \
                \n \
                \n The Thing can infect a player by trading them an 'Infected' card. \
                \n Humans and Infected cannot give 'Infected' cards in trades. \
                \n Infected must keep at least one infected card in their hand. \
                \n If any player, regardless of if they are infected, has 4 infected \
                \n cards in their deck they will be eliminated from the game."
            )
            .embed()
        )

    @staticmethod
    def card_colour(card: Card) -> Colour:
        """Returns the corresponding colour based on the type of card"""
        if card.kind == CardKind.ROLE:
            return Colour.red()
        if card.kind == CardKind.PANIC:
            return Colour.pink()
        if card.kind == CardKind.ACTION:
            return Colour.green()
        if card.kind == CardKind.DEFENSE:
            return Colour.blue()
        else:
            return Colour.gold()

    @staticmethod
    def card_type(card: Card) -> str:
        """Returns a string for the card type"""
        if card.kind == CardKind.ROLE:
            return "Role"
        if card.kind == CardKind.PANIC:
            return "Panic"
        if card.kind == CardKind.ACTION:
            return "Action"
        if card.kind == CardKind.DEFENSE:
            return "Defense"
