from time import time
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os
from matplotlib.lines import Line2D

from constants import CURR_PATH
from graphs.metrics_commenter_nets import community_to_dict_mapping



def community_layout(g, partition):
    """
    Compute the layout for a modular graph.


    Arguments:
    ----------
    g -- networkx.Graph or networkx.DiGraph instance
        graph to plot

    partition -- dict mapping int node -> int community
        graph partitions


    Returns:
    --------
    pos -- dict mapping int node -> (float x, float y)
        node positions

    """

    pos_communities = _position_communities(g, partition)

    pos_nodes = _position_nodes(g, partition)

    # combine positions
    pos = dict()
    for node in g.nodes():
        pos[node] = pos_communities[node] + pos_nodes[node]

    return pos


def _position_communities(g, partition):

    # create a weighted graph, in which each node corresponds to a community,
    # and each edge weight to the number of edges between communities
    between_community_edges = _find_between_community_edges(g, partition)

    communities = set(partition.values())
    hypergraph = nx.DiGraph()
    hypergraph.add_nodes_from(communities)
    for (ci, cj), edges in between_community_edges.items():
        hypergraph.add_edge(ci, cj, weight=len(edges))

    # find layout for communities
    # pos_communities = nx.circular_layout(hypergraph)
    pos_communities = nx.spring_layout(hypergraph,k=5,scale=10, seed=42)

    # set node positions to position of community
    pos = dict()
    for node, community in partition.items():
        pos[node] = pos_communities[community]

    return pos


def _find_between_community_edges(g, partition):

    edges = dict()

    for (ni, nj) in g.edges():
        ci = partition[ni]
        cj = partition[nj]

        if ci != cj:
            try:
                edges[(ci, cj)] += [(ni, nj)]
            except KeyError:
                edges[(ci, cj)] = [(ni, nj)]

    return edges


def _position_nodes(g, partition, **kwargs):
    """
    Positions nodes within communities.
    """

    communities = dict()
    for node, community in partition.items():
        try:
            communities[community] += [node]
        except KeyError:
            communities[community] = [node]

    pos = dict()
    for ci, nodes in communities.items():
        subgraph = g.subgraph(nodes)
        pos_subgraph = nx.spring_layout(subgraph)
        pos.update(pos_subgraph)

    return pos


def generate_random_colors(n: int):
    """
    returns a dict index: color
    """

    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
    colors = {}
    cmap1 = plt.get_cmap('Paired')
    cmap2 = plt.get_cmap('Set1')
    cmap3 = plt.get_cmap('tab10')


    # triess to fill colors with paired cmap
    for i in range(min(n, cmap1.N)):
        colors[i] = cmap1(i / cmap1.N)
    
    # if n > number of colors in paired, add colors from set1
    if n > cmap1.N:
        for i in range(cmap1.N, min(n, cmap1.N + cmap2.N)):
            colors[i] = cmap2((i - cmap1.N) / cmap2.N)
    
    # if n > number of colors in paired + set1, add colors from tab10 
    if n > cmap1.N + cmap2.N:
        for i in range(cmap1.N + cmap2.N, min(n, cmap1.N + cmap2.N + cmap3.N)):
            colors[i] = cmap3((i - cmap1.N - cmap2.N) / cmap3.N)
    
    return colors


def plot_communities(G, communities):

    print(f"plotting")
    plt.figure(figsize=(20, 16))

    colors = generate_random_colors(len(communities))


    # generate colors per community
    color_map = {}
    community_labels = {}
    for idx, (community, color) in enumerate(zip(communities, colors.values())):
        for node in community:
            if color_map.get(node) is None:
                color_map[node] = color
        community_labels[idx] = color

    node_colors = [color_map[node] for node in G.nodes() if color_map.get(node) is not None]

    # get positions oriented by communities
    start = time()
    comm_map = community_to_dict_mapping(G, communities)
    pos = community_layout(G, comm_map)
    del comm_map
    end = time()
    print(f"defined community layout...{end - start:.4f} sec")

    # plotting ...
    start = time()
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color=node_colors,
                           alpha=0.6)
    end = time()

    print(f"nodes drawn in {end - start: .4f} seconds")

    start = time()
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, alpha=0.6,
                           width=[0.001 * edge[2]['weight'] for edge in edges])
    end = time()
    print(f"edges drawn in {end - start: .4f} seconds")


    # add community labels
    for idx, community in enumerate(communities):
        # Calculate the centroid of the community to place the label
        x_coords = [pos[node][0] for node in community if node in pos]
        y_coords = [pos[node][1] for node in community if node in pos]
        if x_coords and y_coords:
            centroid_x, centroid_y = sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords)
            plt.text(centroid_x, centroid_y, f"{idx}", fontsize=12,
                     bbox=dict(facecolor=community_labels[idx], alpha=0.5, edgecolor='black', boxstyle='round,pad=0.3'))

    # Add legend box to show community colors
    legend_elements = [Line2D([0], [0], marker='o', color='w', label=f'Community {i}',
                              markerfacecolor=color, markersize=10)
                       for i, color in enumerate(colors.values())]
    plt.legend(handles=legend_elements, loc='upper right', title="Communities", fontsize=15, title_fontsize='13')

    # plt.title("Communities")
    os.makedirs(f"{CURR_PATH}imgs/", exist_ok=True)
    plt.savefig(f"{CURR_PATH}imgs/testeplotcommunitiesfinal.png")
    print(f"{CURR_PATH}imgs/testeplotcommunitiesfinal.png")
