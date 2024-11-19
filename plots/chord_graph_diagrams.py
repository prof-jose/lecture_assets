"""
Script to reproduce the chord diagram and networkx graph
that I use in some lectures.
"""

# !pip install mpl_chord_diagram

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import pandas as pd
from mpl_chord_diagram import chord_diagram

DATA = "association_data.txt"


def create_flow(data, artists):
    """
    Create a flow matrix from the data.
    """
    flow = np.zeros((len(artists), len(artists)))

    for i, artist1 in enumerate(artists):
        for j, artist2 in enumerate(artists):
            if artist1 == artist2:
                continue
            flow[i, j] = data.contents.str.contains(artist1).astype(int).dot(data.contents.str.contains(artist2).astype(int))

    return flow


def main():

    with open(DATA, 'rt') as f:
        data = f.readlines()
    data = pd.DataFrame(data, columns=['contents'])

    artists = [
        "Dire Straits",
        "The Beach Boys",
        "The Beatles",
        "Garbage",
        "Muse",
        "Tina Turner",
        "Norah Jones",
        "John Mayer"
    ]

    flow = create_flow(data, artists)
    rotations = [False]*3 + [True]*2 + [False]*3

    chord_diagram(flow, artists, rotate_names=rotations, sort="distance", cmap="PuOr", show=False)

    # Save the figure
    plt.savefig("chord_diagram.png", dpi=300)
    plt.clf()

    # create networkx graph from flow matrix

    G = nx.from_numpy_array(flow)
    G = nx.relabel_nodes(G, dict(enumerate(artists)))

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='white', font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=1)#flow.flatten()/flow.max()*5)

    # add edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.savefig("networkx_graph.png", dpi=300)


if __name__ == "__main__":
    main()