import unittest
import uuid
from core import Bubble  # Replace 'your_module' with the module where your Bubble class is defined

class TestBubble(unittest.TestCase):

    def setUp(self):
        self.bubble = Bubble('test_slug', 'test_description')

    def test_init(self):
        self.assertIsInstance(self.bubble.id, uuid.UUID)
        self.assertEqual(self.bubble.slug, 'test_slug')
        self.assertEqual(self.bubble.description, 'test_description')
        self.assertEqual(self.bubble.current_agents, [])

    def test_add_agent(self):
        agent = 'Agent001'
        self.bubble.current_agents.append(agent)
        self.assertIn(agent, self.bubble.current_agents)

if __name__ == '__main__':
    unittest.main()