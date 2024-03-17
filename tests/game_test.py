import unittest
from game import *


class GameTests(unittest.TestCase):
    def test_game_creation(self):
        game = Game(["1", "2", "3", "4"])
        self.assertEqual(game.player_count, 4)

    def test_game_start(self):
        game = Game(["1", "2", "3", "4", "5"])
        game.start()

        for player in game._players:
            self.assertEqual(len(player.hand), 4)

        self.assertEqual(
            len(list(filter(lambda p: p.role == Role.THE_THING, game._players))), 1
        )

        self.assertEqual(
            len(list(filter(lambda p: p.role == Role.HUMAN, game._players))),
            game.player_count - 1,
        )


if __name__ == "__main__":
    unittest.main()
