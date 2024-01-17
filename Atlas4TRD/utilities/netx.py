import networkx as nx
import matplotlib.pyplot as plt


def generate_networkx_graph(environment):
    from core import StateBubble, StepBubble

    G = nx.DiGraph()

    bubbles = environment.bubbles
    connections = environment.connections

    # TODO: Add node size varying by capacity

    colors = []
    for bubble in bubbles:
        G.add_node(bubble.slug)
        if isinstance(bubble, StateBubble):
            colors.append('lightcoral')
        elif isinstance(bubble, StepBubble):
            colors.append('lightseagreen')
        else:
            colors.append('grey')

    for connection in connections:
        G.add_edge(connection.start.slug, connection.end.slug)

    pos = {}  # Initialize a dictionary to hold positions of nodes
    levels = {}  # A dictionary to hold nodes at each level
    for bubble in bubbles:
        depth = bubble.depth
        if depth in levels:
            levels[depth].append(bubble.slug)
        else:
            levels[depth] = [bubble.slug]

    for level, nodes in levels.items():
        for i, node in enumerate(nodes):
            x_value = i * 1.0 / len(nodes)
            pos[node] = (x_value, level)

    plt.figure(figsize=(12, 12))
    ax = plt.gca()
    ax.set_axis_off()

    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=1200)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

    plt.title('Bubbles and Connections', size=16)
    plt.show()