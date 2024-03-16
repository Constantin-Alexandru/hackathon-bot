import unittest
from game import Game


class GameTests(unittest.TestCase):
    def test_game_creation(self):
        game = Game(["1", "2", "3", "4"])
        self.assertEqual(game.player_count, 4)


if __name__ == "__main__":
    unittest.main()
