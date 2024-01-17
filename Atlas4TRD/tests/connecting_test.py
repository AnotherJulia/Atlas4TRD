import unittest
from core import Bubble, Connection


class TestConnection(unittest.TestCase):

    def setUp(self):
        self.bubble_1 = Bubble("bubble_1", "description_1")
        self.bubble_2 = Bubble("bubble_2", "description_2")
        self.connection = Connection(self.bubble_1, self.bubble_2)

    def test_connection(self):
        # Assert that the start bubble knows about its connection to the end bubble.
        self.assertIn(self.bubble_2, self.bubble_1.connections)

        # Assert end bubble does not have a connection back to start bubble
        self.assertNotIn(self.bubble_1, self.bubble_2.connections)


if __name__ == '__main__':
    unittest.main()