from utilities.config import read_config


class Tree:

    def __init__(self, slug, initial_node_slug=None):
        from .node import TreeNode
        self.slug = slug
        self.nodes = []

        # Create initial bubble/node
        if initial_node_slug is None:
            node = TreeNode("Start", depth=0)
            self.nodes.append(node)
        else:
            node = TreeNode(initial_node_slug, depth=0)
            self.nodes.append(node)

    def create_node(self, slug, parent_slug, depth):
        from .node import TreeNode

        node = TreeNode(slug, depth)
        self.nodes.append(node)

        # let's find the parent node to attach
        parent = self.find_node(slug=parent_slug)
        parent.attach_child(node)

    def find_node(self, slug):
        node = next((node for node in self.nodes if node.slug == slug), None)

        if node is None: raise ValueError("Node not found")
        return node

    def build(self, decision_map_path):
        # Read the decision map from the JSON file
        decision_map = read_config(decision_map_path)

        depth_map = {'intake': 0}  # Depth map to keep track of node depths

        for parent_slug, children in decision_map.items():
            for child_slug in children.values():
                if child_slug not in depth_map:
                    # Increment depth for each new node
                    depth_map[child_slug] = depth_map[parent_slug] + 1
                    self.create_node(slug=child_slug, parent_slug=parent_slug, depth=depth_map[child_slug])



    def model(self):
        from matplotlib import pyplot as plt
        import networkx as nx

        G = nx.DiGraph()

        pos = {}  # Dictionary to store positions of nodes
        levels = {}  # Dictionary to store nodes at each depth

        # First, add nodes and edges to the graph
        for node in self.nodes:
            G.add_node(node.slug)
            children = node.return_children()
            for child in children:
                G.add_edge(node.slug, child.slug)

            # Compute levels
            depth = node.model_depth
            if depth in levels:
                levels[depth].append(node.slug)
            else:
                levels[depth] = [node.slug]

        # Assign positions based on levels with even spacing
        for level, nodes in levels.items():
            for i, node in enumerate(nodes):
                # Spacing: divide the space into (number of nodes + 1) segments
                x_value = (i + 1) / (len(nodes) + 1)
                pos[node] = (x_value, -level)  # Use negative for depth to get tree-like structure

        # Plot the graph
        plt.figure(figsize=(12, 12))
        nx.draw(G, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=15)
        plt.show()






