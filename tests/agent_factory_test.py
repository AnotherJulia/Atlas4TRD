import unittest
from core import Factory


class TestAgentFactory(unittest.TestCase):

    def setUp(self):
        self.factory = Factory('../config/agent_params.json')

    def test_create_agent(self):
        agent = self.factory.create_agent('bubble1')
        self.assertIn(agent.episode_duration, ['acute', 'subacute', 'chronic'])
        self.assertIn(agent.symptom_severity, ['mild', 'moderate', 'severe'])
        self.assertIn(agent.psychosis, [True, False])
        self.assertIn(agent.functional_impairment, ['mild', 'moderate', 'severe'])
        self.assertIn(agent.treatment_failures, ['0', '1-2', '3+'])
        print(agent)

    def test_create_agents(self):
        agents = self.factory.create_agents(10, "bubble1")
        self.assertEqual(len(agents), 10)
        for agent in agents: print(agent)


if __name__ == '__main__':
    unittest.main()
