import unittest
from utils import characters, create_session_id


class SessionIDTest(unittest.TestCase):
    def test_length(self):
        self.assertEqual(len(create_session_id()), 5)
        self.assertEqual(len(create_session_id(7)), 7)
        self.assertEqual(len(create_session_id(8)), 8)
        self.assertEqual(len(create_session_id(10)), 10)
        self.assertEqual(len(create_session_id(2)), 2)
        self.assertEqual(len(create_session_id(26)), 26)

    def test_characters(self):
        self.assertTrue(not any(char not in characters for char in create_session_id()))
        self.assertTrue(
            not any(char not in characters for char in create_session_id(7))
        )
        self.assertTrue(
            not any(char not in characters for char in create_session_id(8))
        )
        self.assertTrue(
            not any(char not in characters for char in create_session_id(10))
        )
        self.assertTrue(
            not any(char not in characters for char in create_session_id(2))
        )
        self.assertTrue(
            not any(char not in characters for char in create_session_id(26))
        )


if __name__ == "__main__":
    unittest.main()
