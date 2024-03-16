import unittest
from game import *


class GameTests(unittest.TestCase):
    def test_game_creation(self):
        game = Game(["1", "2", "3", "4"])
        self.assertEqual(game.player_count, 4)


class DeckTests(unittest.TestCase):
    def test_new_deck(self):
        deck = Deck(
            [
                Card("The Thing", "You are The Thing", CardKind.ROLE),
                Card(
                    "Infected",
                    "If you got this card from another player, you are infected!",
                    CardKind.ROLE,
                ),
                Card("Flamethrower", "Kill an adjacent player", CardKind.ACTION),
            ]
        )

        self.assertEqual(deck.size, 3)

    def test_deck_shuffles(self):
        deck = Deck(
            [
                Card("The Thing", "You are The Thing", CardKind.ROLE),
                Card(
                    "Infected",
                    "If you got this card from another player, you are infected!",
                    CardKind.ROLE,
                ),
                Card("Flamethrower", "Kill an adjacent player", CardKind.ACTION),
            ]
        )

        size_before = deck.size
        set_before = set(deck._cards)

        deck.shuffle()

        size_after = deck.size
        set_after = set(deck._cards)
        self.assertEqual(size_before, size_after, "The size of the deck changed")
        self.assertEqual(
            set_before, set_after, "The deck changed which cards are in it"
        )

    def test_deck_add_card(self):
        deck = Deck(
            [
                Card("The Thing", "You are The Thing", CardKind.ROLE),
                Card(
                    "Infected",
                    "If you got this card from another player, you are infected!",
                    CardKind.ROLE,
                ),
                Card("Flamethrower", "Kill an adjacent player", CardKind.ACTION),
            ]
        )

        size_before = deck.size
        card_to_add = Card(
            "Analysis", "See the hand of an adjacent player", CardKind.ACTION
        )

        deck.add_card(card_to_add)

        size_after = deck.size
        self.assertEqual(size_after - size_before, 1, "Card should be added only once")

        self.assertNotEqual(
            deck.draw(), card_to_add, "Cards should not be added to the top"
        )

    def test_draw(self):
        deck = Deck(
            [
                Card("The Thing", "You are The Thing", CardKind.ROLE),
                Card(
                    "Infected",
                    "If you got this card from another player, you are infected!",
                    CardKind.ROLE,
                ),
                Card("Flamethrower", "Kill an adjacent player", CardKind.ACTION),
            ]
        )

        size_before = deck.size

        drawn_card = deck.draw()

        self.assertEqual(
            Card("The Thing", "You are The Thing", CardKind.ROLE),
            drawn_card,
            "Not drawing from the top of the deck",
        )

        self.assertEqual(deck.size - size_before, -1, "Deck did not shrink")

    def test_top_card_type(self):
        deck = Deck(
            [
                Card("The Thing", "You are The Thing", CardKind.ROLE),
                Card(
                    "Infected",
                    "If you got this card from another player, you are infected!",
                    CardKind.ROLE,
                ),
                Card("Flamethrower", "Kill an adjacent player", CardKind.ACTION),
            ]
        )

        self.assertEqual(deck.top_card_kind, CardKind.ROLE)


if __name__ == "__main__":
    unittest.main()
