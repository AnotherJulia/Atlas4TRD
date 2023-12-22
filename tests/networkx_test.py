import unittest
from utilities import generate_networkx_graph
from core import Environment, Bubble, Connection  # Replace 'your_module' with your actual module name

class TestGenerateNetworkxGraph(unittest.TestCase):

    def test_generate_graph(self):
        # Set up an environment with some bubbles and connections
        environment = Environment()

        bubble1 = Bubble('1', 'b1')
        environment.add_bubble(bubble1)

        bubble2 = Bubble('2', 'b2')
        environment.add_bubble(bubble2)

        connection1 = Connection(bubble1, bubble2)
        environment.add_connection(connection1)

        # we cannot test the graph visually, we can only make sure it does not raise any errors.
        try:
            generate_networkx_graph(environment)
            self.assertTrue(True)  # if no error, the test passes.
        except Exception as e:
            self.fail(f"generate_networkx_graph raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()