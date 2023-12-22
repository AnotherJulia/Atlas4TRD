import networkx as nx
from matplotlib import pyplot as plt


def plot_bubbles_and_connections(bubbles, connections):
    G = nx.DiGraph()

    colors = []
    for bubble in bubbles:
        G.add_node(bubble.name)
        if bubble.type == 'state':
            colors.append('lightcoral')
        elif bubble.type == 'step':
            colors.append('aquamarine')
        else:
            colors.append('grey')

    for connection in connections:
        G.add_edge(connection.from_bubble.name, connection.to_bubble.name)

    plt.figure(figsize=(8, 6))
    pos = nx.kamada_kawai_layout(G)

    nx.draw_networkx(G, pos, node_color=colors, with_labels=True, node_size=1200)
    plt.title('Bubbles and Connections')
    plt.show()