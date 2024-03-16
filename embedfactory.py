from embedbuilder import EmbedBuilder
from discord import Embed
from game import Card


class EmbedFactory:

    def error(self, session_id: str, error_msg: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("red")
            .title("Error Occured!")
            .description(error_msg)
            .footer("Session ID: " + session_id)
            .embed()
        )

    def waitForStart(self, session_id: str, player_count: int) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Waiting for players")
            .description(
                "You need a minimum of 4 players to start a game and can have a maximum of 12"
            )
            .field("Players", player_count)
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    def waitForTurn(self, session_id: str, action: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Waiting for your turn...")
            .description(action)
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    def turn(self, session_id: str, cards: list[Card]) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("It is your turn")
            .description("")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    def card_info(self, card: Card) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title(card.name)
            .description(card.description)
            .field("Card Type: ", card.kind)
            .embed()
        )

    def game_won_humans(self, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("The Thing has lost the game!")
            .description(
                "The Thing has been eliminated and all remaining players are not infected."
            )
            .footer(f"Session ID: {session_id}")
        )

    def game_won_thing(self, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("The Thing has won the game!")
            .description(
                "All remaining players have are now infected, the Thing and the infected have won."
            )
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    def game_over(self, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .title("Game Over!")
            .description("The game has ended")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    def rules(self) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Rules of Stay Away!")
            .description(
                "At the start of the game 4 cards will be dealt to each player. The player who recieves 'The Thing' ..."
            )
            .embed()
        )
