from embedbuilder import EmbedBuilder
from discord import Embed


class EmbedFactory:

    def create(self, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Welcome to Stay Away!")
            .description("You have successfully created a lobby")
            .field("Session ID", session_id)
            .embed()
        )

    def wait(self, player_count: int, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Waiting for players")
            .description(
                "You need a minimum of 4 players to start a game and can have a maximum of 12"
            )
            .field("Players", player_count)
            .footer("Session ID: " + session_id)
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

    def start(self, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("white")
            .title("Game started!")
            .description("You have all been dealt 4 cards")
            .footer("Session ID: " + session_id)
            .embed()
        )

    def error(self, message: str, session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour("red")
            .title("Error Occured!")
            .description(message)
            .footer("Session ID: " + session_id)
            .embed()
        )
    
    def draw(self, card_info: str, session_id: str) -> Embed:
        return(
            EmbedBuilder()
            .colour("white")
            .title("You have drawn the following card")
            .description(card_info)
            .footer("Session ID: " + session_id)
            .embed()
        )

    def play()
