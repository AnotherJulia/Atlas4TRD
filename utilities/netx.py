import networkx as nx
import matplotlib.pyplot as plt

from core import StateBubble, StepBubble


def generate_networkx_graph(environment):
    G = nx.DiGraph()

    bubbles = environment.bubbles
    connections = environment.connections

    colors = []
    for bubble in bubbles:
        G.add_node(bubble.slug)
    if isinstance(bubble, StateBubble):
        colors.append('lightcoral')
    elif isinstance(bubble, StepBubble):
        colors.append('aquamarine')
    else:
        colors.append('grey')

    for connection in connections:
        G.add_edge(connection.start.slug, connection.end.slug)

    plt.figure(figsize=(8, 6))
    pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx(G, pos, node_color=colors, with_labels=True, node_size=1200)
    plt.title('Bubbles and Connections')
    plt.show()