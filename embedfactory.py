from embedbuilder import EmbedBuilder
from discord import Embed, Colour
from game import Card, CardKind


class EmbedFactory:

    @staticmethod
    def error(session_id: str, error_msg: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.red())
            .title("Error Occured!")
            .description(error_msg)
            .footer("Session ID: " + session_id)
            .embed()
        )

    @staticmethod
    def waitForStart(session_id: str, player_count: int) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.light_grey())
            .title("Waiting for players")
            .description(
                "You need a minimum of 4 players to start a game and can have a maximum of 12"
            )
            .field("Players", f"{player_count} / 12")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def waitForTurn(session_id: str, action: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.blurple())
            .title("Waiting for your turn...")
            .description(action)
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def turn(session_id: str, cards: list[Card]) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.gold())
            .title("It is your turn")
            .description("Pick your action")
            .field("Card 1", cards[0].name)
            .field("Card 2", cards[1].name)
            .field("Card 3", cards[2].name)
            .field("Card 4", cards[3].name)
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def card_info(card: Card) -> Embed:
        return (
            EmbedBuilder()
            .colour(self.card_colour(card))
            .title(card.name)
            .description(card.description)
            .field("Card Type: ", self.card_type(card))
            .embed()
        )

    @staticmethod
    def game_won_humans(session_id: str) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.green())
            .title("The Thing has lost the game!")
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
            .title("The Thing has won the game!")
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
            .title("Game Over!")
            .description("The game has ended")
            .footer(f"Session ID: {session_id}")
            .embed()
        )

    @staticmethod
    def rules(self) -> Embed:
        return (
            EmbedBuilder()
            .colour(Colour.light_grey)
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

    # Returns the corresponding colour based on the type of card
    def card_colour(self, card: Card) -> Colour:
        if card.kind == CardKind.ROLE:
            return Colour.red()
        if card.kind == CardKind.PANIC:
            return Colour.pink()
        if card.kind == CardKind.ACTION:
            return Colour.green()
        if card.kind == CardKind.DEFENSE:
            return Colour.blue()

    # Returns a string for the card type
    def card_type(self, card: Card) -> str:
        if card.kind == CardKind.ROLE:
            return "Role"
        if card.kind == CardKind.PANIC:
            return "Panic"
        if card.kind == CardKind.ACTION:
            return "Action"
        if card.kind == CardKind.DEFENSE:
            return "Defense"
