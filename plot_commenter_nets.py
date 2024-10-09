import pickle
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from colorsys import hsv_to_rgb
from numpy import random

from constants import CURR_PATH, CURR_YTBR

def plot_co_commenter_graph(G, save=True):
    print('plotting ...')
    plt.figure(figsize=(20, 20))

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='red')
    print('Nodes desenhados ...')

    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos,
                           width=[0.001 * edge[2]['weight'] for edge in edges])
    print('edges desenhados ...')

    plt.title("Co-commenter Network")
    plt.axis('off')  # Turn off the axis
    if save:
        plt.savefig(f"{CURR_PATH}co_commenter_network_thresh_10.png")
    else:
        plt.show()


def plot_video_commenter_graph(G):
    print("plotting ...")
    node_colors = []
    for node in G.nodes():
        if len(node) == 11:  # video_id has fixed length
            node_colors.append('green')  # Video nodes are blue
        else:
            node_colors.append('red')   # Commenter nodes are red

    pos = nx.spring_layout(G)
    plt.figure(figsize=(20, 20))

    print("defined layout")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=20)

    print("nodes drawn ...")

    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos,
                           width=[0.01 * edge[2]['weight'] for edge in edges])

    print("edges drawn ...")

    plt.title("Video-Commenter Network ")
    plt.axis('off')  # Turn off the axis
    plt.show()
    # plt.savefig(f"./data/{ytbr}/video_commenter_network.png")


def plot_elbow_point(path):
    df = pd.read_csv(path)

    plt.figure(figsize=(10, 6))
    plt.plot(df['threshold'], df['coef_value'],
             marker='o', linestyle='-', color='b')

    plt.title('Clustering Coefficient vs Threshold', fontsize=14)
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Clustering Coefficient', fontsize=12)

    plt.xticks(ticks=range(1, 26))

    for i, txt in enumerate(df['coef_value']):
        plt.text(df['threshold'][i], df['coef_value'][i],
                 f'{txt:.3f}', fontsize=10, ha='center')

    plt.grid(True)
    # plt.show()
    plt.savefig(f"{CURR_PATH}imgs/clustering_coef_x_treshold25.png")


def plot_communities(G: nx.Graph, communities):
    print(f"plotting ...")
    # Compute positions for the node clusters as if they were themselves nodes in a supergraph using a larger scale factor
    superpos = nx.spring_layout(G, scale=50, seed=429)

    print(f"calculating positions for each supernode ...")
    # Use the "supernode" positions as the center of each node cluster
    centers = list(superpos.values())
    del superpos
    pos = {}
    for center, comm in zip(centers, communities):
        pos.update(nx.spring_layout(nx.subgraph(G, comm), center=center))

    del centers
    print(f"drawing nodes with separate colors per community ...")
    colors = generate_random_colors(len(communities))
    color_map = {}
    for community, color in zip(communities, colors):
        for node in list(community):
            if color_map.get(node) == None:
                color_map[node] = color
            else:
                print(f"node {node} belongs to more than one community")

    del colors
    node_colors = [color_map[node] for node in G.nodes() if color_map.get(node) != None]  
    nodelist = [node for node in G.nodes() if node in color_map]

    del communities
    nx.draw_networkx_nodes(G, pos=pos, nodelist=nodelist, node_color=node_colors, node_size=20)

    print(f"drawing edges ...")
    egdelist = [(u, v, data) for u, v, data in G.edges(data=True) if u in color_map and v in color_map]
    nx.draw_networkx_edges(G, pos=pos, edgelist=egdelist,
                           width=[0.001 * edge[2]['weight'] for edge in egdelist])
    plt.show()


def generate_random_colors(n:int):
    cmap = plt.get_cmap('tab20b', n)  
    colors = [cmap(i) for i in range(n)]  
    return colors


def filter_graph(G : nx.Graph, min_degree=1, top_n_nodes=0, min_edge_weight=1) -> nx.Graph:
    """
    Filter a large graph for visualization.

    Params:
    - G: networkx Graph object
    - min_degree: minimum degree for a node to be included
    - top_n_nodes: number of top nodes by degree to include
    - min_edge_weight: minimum weight for an edge to be included

    Return:
    - filtered_G: filtered networkx Graph object
    """
    print(f"filtering graph ...")
    if top_n_nodes == 0:
        top_n_nodes = G.number_of_nodes()

    # filter nodes by degree
    node_degrees = dict(G.degree())
    high_degree_nodes = [node for node,
                         degree in node_degrees.items() if degree >= min_degree]

    subgraph = G.subgraph(high_degree_nodes[:top_n_nodes])

    # filter edges by weight
    filtered_G = nx.Graph()
    for u, v, data in subgraph.edges(data=True):
        if data['weight'] >= min_edge_weight:
            filtered_G.add_edge(u, v, **data)

    filtered_G.remove_nodes_from(list(nx.isolates(filtered_G)))

    print(f"    original graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"    filtered graph: {filtered_G.number_of_nodes()} nodes, {filtered_G.number_of_edges()} edges")

    return filtered_G


def load_graph(path : str) -> nx.Graph:
    """
    Loads graph saved in pickle format

    Params:
    - path: Path where graph was saved
    - filter: Filter graph to aid in visualization
    - threshold: edge weights thershold value
    - n: top n nodes to show 

    Return:
    - G: graph 
    """
    print(f"loading graph ...")
    G = pickle.load(open(path, 'rb'))
    print(f"    graph nodes: {G.number_of_nodes()}")
    print(f"    graph edges: {G.number_of_edges()}")
    return G


# def main():
#     co_commenter_path = f'{PATH}/co_commenter_network.pickle'
#     vid_commenter_path = f'{PATH}/video_commenter_network.pickle'
#
#     G = load_graph(co_commenter_path)
#     G = filter_graph(G=G,
#                      min_edge_weight=10)
#     # calc_avg_degree(G)
#     plot_co_commenter_graph(G, save=False)
#
#     # G = load_graph(vid_commenter_path, filter=True)
#     # plot_video_commenter_graph(G)
#
#
# if __name__ == "__main__":
#     main()
