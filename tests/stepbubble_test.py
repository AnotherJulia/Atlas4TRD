import unittest
import uuid
from core import StepBubble


class TestStepBubble(unittest.TestCase):
    def setUp(self):
        self.step_bubble = StepBubble('test_slug', 'test_description', 2, '../config/ad_config.json')

    def test_init(self):
        self.assertIsInstance(self.step_bubble.id, uuid.UUID)
        self.assertEqual(self.step_bubble.slug, 'test_slug')
        self.assertEqual(self.step_bubble.description, 'test_description')
        self.assertEqual(self.step_bubble.capacity, 2)
        self.assertIsInstance(self.step_bubble.treatment_parameters, dict)

    def test_add_agent(self):
        agent1 = 'Agent001'
        agent2 = 'Agent002'
        agent3 = 'Agent003'

        # Test adding agents within capacity
        self.step_bubble.add_agent(agent1)
        self.step_bubble.add_agent(agent2)
        self.assertIn(agent1, self.step_bubble.current_agents)
        self.assertIn(agent2, self.step_bubble.current_agents)

        # Test overcapacity and the waiting queue
        self.step_bubble.add_agent(agent3)
        self.assertIn(agent3, self.step_bubble.waiting_queue)
        self.assertNotIn(agent3, self.step_bubble.current_agents)

        # print(self.step_bubble)


if __name__ == '__main__':
    unittest.main()