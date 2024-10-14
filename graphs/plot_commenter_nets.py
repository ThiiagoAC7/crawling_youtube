import pickle
import matplotlib.pyplot as plt
import networkx as nx
import time

from constants import CURR_PATH, CURR_YTBR


def plot_graph(G: nx.Graph, name: str, save: bool = True,
               edge_weight: float = 0.001, title: str = "Commenter Network",
               alpha=0.6):
    print('plotting ...')
    plt.figure(figsize=(20, 20))

    colors = get_node_type_colors(G)

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=20,
                           node_color=colors, alpha=alpha)
    print('Nodes desenhados ...')

    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos,
                           width=[edge_weight * edge[2]['weight'] for edge in edges])
    print('edges desenhados ...')

    plt.title(title)
    plt.axis('off')  # Turn off the axis
    if save:
        plt.savefig(f"{CURR_PATH}{name}.png")
        print(f"figure saved as {CURR_PATH}{name}.png ")
    else:
        plt.show()


def plot_community_graph(G, communities, figsize=(20, 16),
                         title="Network Communities", res=1, path=""):
    """
    plot the graph with communities in different colors.
    """
    print(f"plotting...")
    plt.figure(figsize=figsize)

    unique_communities = list(communities)
    colors = generate_distinct_colors(len(unique_communities))

    color_map = {}
    for community, color in zip(unique_communities, colors):
        for node in list(community):
            if color_map.get(node) == None:
                color_map[node] = color
            else:
                print(f"node {node} belongs to more than one community")

    del communities,  colors
    node_colors = [color_map[node]
                   for node in G.nodes() if color_map.get(node) != None]

    start = time.time()  # Start timer
    pos = nx.spring_layout(G)
    end = time.time()

    print(f"    layout defined... {end - start:.3f} seconds")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=20, alpha=0.6)
    print(f"    nodes drawn ... {end - start:.3f} seconds")

    start = time.time()
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, alpha=0.6,
                           width=[0.001 * edge[2]['weight'] for edge in edges])
    end = time.time()
    print(f"    edges drawn ... {end - start:.3f} seconds")

    plt.title(title)
    plt.savefig(
        f"{CURR_PATH}imgs/POSrandom_{path}_communities_colored_resolution_{str(res).replace('.','_')}")


def get_node_type_colors(G: nx.Graph):
    node_colors = []
    for node, data in G.nodes(data=True):
        if data["type"] == "video":
            node_colors.append('green')
        else:
            node_colors.append('red')

    return node_colors


def generate_random_colors(n: int):
    colors = {}
    cmap = plt.get_cmap('tab20b', n)
    for i in range(n):
        colors[i] = cmap(i)
    return colors


def generate_distinct_colors(n):
    colors = {}
    for i in range(n):
        hue = i / n
        colors[i] = plt.cm.hsv(hue)
    return colors


def filter_graph(G: nx.Graph, min_degree=1, top_n_nodes=0, min_edge_weight=1) -> nx.Graph:
    """
    Filter a large graph by degree and edge weight.

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

    G = G.subgraph(high_degree_nodes[:top_n_nodes]).copy()

    del high_degree_nodes, node_degrees
    # filter edges by weight
    edges_to_remove = []
    for u, v, data in G.edges(data=True):
        if (G.nodes[u].get('type') == 'commenter' and G.nodes[v].get('type') == 'commenter'):
            if data['weight'] < min_edge_weight:
                edges_to_remove.append((u, v))

    # reomve edges and isolated nodes inplace
    G.remove_edges_from(edges_to_remove)
    G.remove_nodes_from(list(nx.isolates(G)))

    print(
        f"    filtered graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


def load_graph(path: str) -> nx.Graph:
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


# def __plot_elbow_point(path):
#     df = pd.read_csv(path)
#
#     plt.figure(figsize=(10, 6))
#     plt.plot(df['threshold'], df['coef_value'],
#              marker='o', linestyle='-', color='b')
#
#     plt.title('Clustering Coefficient vs Threshold', fontsize=14)
#     plt.xlabel('Threshold', fontsize=12)
#     plt.ylabel('Clustering Coefficient', fontsize=12)
#
#     plt.xticks(ticks=range(1, 26))
#
#     for i, txt in enumerate(df['coef_value']):
#         plt.text(df['threshold'][i], df['coef_value'][i],
#                  f'{txt:.3f}', fontsize=10, ha='center')
#
#     plt.grid(True)
#     # plt.show()
#     plt.savefig(f"{CURR_PATH}imgs/clustering_coef_x_treshold25.png")
