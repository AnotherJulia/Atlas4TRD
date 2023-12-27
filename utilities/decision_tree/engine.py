import numpy as np

from utilities.config import read_config


class TreeEngine:

    def __init__(self, tree, leaf_template, leaf_count, decision_map_path):
        from .leaf import Leaf

        self.tree = tree
        self.leaf_template = leaf_template
        self.decision_map = read_config(decision_map_path)

        config_path = "../../config/agent_params.json"
        self.leaves = [Leaf(config_path, current_node_slug="intake") for _ in range(leaf_count)]
        self.end_nodes_count = {}

        self.end_nodes = self._determine_end_nodes()

    def process_leaves(self):
        for leaf in self.leaves:
            current_node = leaf.current_node
            while current_node not in self.end_nodes:  # Assuming you have a list of end nodes in your tree
                next_node = self.decide_next_node(leaf, current_node)
                current_node = next_node
            self.end_nodes_count[current_node] = self.end_nodes_count.get(current_node, 0) + 1

    def _determine_end_nodes(self):
        end_nodes = []
        for node in self.tree.nodes:  # Assuming the tree object has a 'nodes' attribute
            if not node.children:
                end_nodes.append(node.slug)  # Using node slug instead of the node object
        print(end_nodes)
        return end_nodes


    def decide_next_node(self, leaf, current_node):

        # Check if the current node is in the decision map
        if current_node in self.decision_map:
            node_decision = self.decision_map[current_node]

            # Handling for 'intake' node
            if current_node == "intake":
                return node_decision["psychosis"] if leaf.psychosis else node_decision["default"]

            # Handling for 'psychosis' and 'no_psychosis' nodes based on symptom severity
            elif current_node in ["psychosis", "no_psychosis"]:
                return node_decision.get(leaf.symptom_severity, current_node)

        # Default return if current_node not in decision_map or no matching criteria
        else:
            raise EnvironmentError("No decision available")

    def clean(self):
        self.end_nodes_count = {}
        for leaf in self.leaves:
            leaf.clean()

    def calculate_percentages(self):
        total_leaves = len(self.leaves)
        return {node_slug: count / total_leaves * 100 for node_slug, count in self.end_nodes_count.items()}

    def run_simulations(self, num_simulations):
        aggregated_results = {}

        for _ in range(num_simulations):
            self.process_leaves()
            percentages = self.calculate_percentages()

            for node, percentage in percentages.items():
                if node not in aggregated_results:
                    aggregated_results[node] = []
                aggregated_results[node].append(percentage)

            self.clean()  # Ensure this method resets the engine state correctly

        # Calculate average percentages
        average_percentages = {node: np.mean(percentages) for node, percentages in aggregated_results.items()}
        return {"average_percentages": average_percentages, "aggregated_results": aggregated_results}

    def plot_distributions(self, num_simulations, verbose=False):
        from matplotlib import pyplot as plt

        results = self.run_simulations(num_simulations)
        average_percentages = results["average_percentages"]
        aggregated_results = results["aggregated_results"]

        nodes = list(average_percentages.keys())
        percentages = list(average_percentages.values())
        variances = [np.var(aggregated_results[node]) for node in nodes]

        if verbose:
            print(average_percentages)

        # Plot average percentages
        plt.figure(figsize=(10, 6))
        plt.bar(nodes, percentages, color='skyblue')
        plt.xlabel('Nodes')
        plt.ylabel('Average Percentage')
        plt.title('Average Distribution of Leaves Across End Nodes')
        plt.xticks(rotation=45)
        plt.show()

        # Plot variances
        plt.figure(figsize=(10, 6))
        plt.bar(nodes, variances, color='skyblue')
        plt.xlabel('Nodes')
        plt.ylabel('Variance in Percentages')
        plt.title('Variance of Leaf Percentages Across End Nodes')
        plt.xticks(rotation=45)
        plt.show()


