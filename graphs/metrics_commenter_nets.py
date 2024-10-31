import pandas as pd
import networkx as nx
import numpy as np

import matplotlib.pyplot as plt

from cdlib import algorithms, evaluation, viz

from collections import defaultdict


def compute_graph_metrics(G: nx.Graph, communities: list, resolution: int = 1):
    metrics = { }

    mod = calc_modularity(G, communities, resolution)
    cov, per = calc_coverage_performance(G, communities)

    metrics["num_nodes"] = G.number_of_nodes()
    metrics["num_edges"] = G.number_of_edges()
    metrics["avg_degree"] = calc_avg_degree(G)
    metrics["avg_clustering_coef"] = calc_avg_clustering_coef(G)
    metrics["modularity"] = mod
    metrics["coverage"] = cov
    metrics["performance"] = per
    metrics["graph_density"] = nx.density(G) 
    metrics["largest_community"] = len(max(communities, key=len))
    metrics["number_of_communities"] = len(communities)

    return metrics


def calc_per_community_metrics(G: nx.Graph, communities: list):

    metrics_list = []

    subG = nx.Graph()

    for id, c in enumerate(communities):
        subG = G.subgraph(c)

        degree_centrality = nx.degree_centrality(subG)
        avg_degree_centrality = sum(
            degree_centrality.values()) / len(degree_centrality)

        metrics_list.append({
            "id": id,
            "nodes": subG.number_of_nodes(),
            "edges": subG.number_of_edges(),
            "density": nx.density(subG),
            "avg_degree": calc_avg_degree(subG),
            "avg_clustering_coef": calc_avg_clustering_coef(subG),
            "conductance": calc_conductance(G, subG),
            "avg_degree_centrality": avg_degree_centrality,
        })

    return metrics_list


def compute_clique_metrics(G: nx.Graph):
    metrics = {
        "num_max_cliques": 0,
        "max_clique_size": 0,
        "avg_clique_size": 0,
        "median_clique_size": 0,
        "avg_degree_clique": 0,
        "avg_clustering_coef_clique": 0,
        "max_clique_idx": -1,
    }

    cliques = nx.find_cliques(G)
    # count only cliques that have at least 5 members
    cliques = [c for c in cliques if len(c) >= 5]

    clique_sizes = [len(c) for c in cliques]
    metrics["num_max_cliques"] = np.sum([1 for c in cliques])
    metrics["max_clique_size"] = max(clique_sizes)
    metrics["avg_clique_size"] = np.mean(clique_sizes)
    metrics["median_clique_size"] = np.median(clique_sizes)
    metrics["max_clique_idx"] = clique_sizes.index(max(clique_sizes))

    clique_members = set([node for c in cliques for node in c])
    subG = G.subgraph(list(clique_members))
    del G
    metrics["avg_degree_clique"] = calc_avg_degree(subG)
    metrics["avg_clustering_coef_clique"] = calc_avg_clustering_coef(
        subG)
    return metrics


def calc_avg_clustering_coef(G: nx.Graph):
    """
    Calculates clustering coeficcient of a given graph 
    and saves values to a .csv

    Params:
    - G: graph 
    """

    avg_clustering_coef = nx.average_clustering(G, weight="weight", count_zeros=True)
    return avg_clustering_coef


def calc_avg_degree(G: nx.Graph):
    avg_degree = 2 * G.number_of_edges() / G.number_of_nodes()
    return avg_degree


def calc_modularity(G: nx.Graph, communities: list, resolution=1):
    """
    Network modularity is a metric that quantifies the quality of a network's community structure. 
    It measures how well a network can be divided into distinct communities  where:
    - Nodes within the same community have many connections to each other
    - Nodes in different communities have fewer connections between them
    """

    modularity = nx.community.modularity(G, communities, resolution)
    return modularity


def calc_coverage_performance(G: nx.Graph, communities: list):
    """
    - coverage : the ratio of the number of intra-community edges to the total number of edges 
    in the graph.
    - performance : number of intra-community edges plus inter-community non-edges divided by the 
    total number of potential edges
    """

    coverage, performance = nx.community.partition_quality(G, communities)
    return coverage, performance


def calc_conductance(G:nx.Graph , subG: nx.Graph):
    """
    calc conductance based on cdlib.evaluation.conductance
    """

    ms = len(subG.edges())
    edges_outside = 0

    for n in subG.nodes():
        neighbors = G.neighbors(n)
        for n1 in neighbors:
            if n1 not in subG:
                edges_outside +=1

    try:
        ratio = float(edges_outside) / ((2 * ms) + edges_outside)
    except:
        ratio = 0

    return ratio 

def calc_k_cliques_communities(G: nx.Graph, k=5):
    print(f"calculating communities with k_cliques_method, k={k} ...")

    communities = list(
        nx.community.k_clique_communities(G, k, backend="paralel"))
    print(f"{len(communities)} found")
    return communities


def calc_label_prop_communities(G: nx.Graph):
    """
    The algorithm is probabilistic and the found communities may vary on different executions.
    - define seed param
    """

    communities = nx.community.asyn_lpa_communities(G,
                                                    weight="weight")
    return list(communities)


def calc_louvain_communities(G: nx.Graph, resolution=1):
    """
    If resolution is less than 1, the algorithm favors larger communities. 
    Greater than 1 favors smaller communities
    """
    communities = nx.community.louvain_communities(G,
                                                   weight='weight',
                                                   resolution=resolution,
                                                   seed=42,
                                                   )
    return communities


def calc_greedy_modularity_communities(G: nx.Graph, resolution=1):
    communities = nx.community.greedy_modularity_communities(G,
                                                             weight="weight",
                                                             resolution=resolution)
    return communities


def community_to_dict_mapping(G: nx.Graph, communities):
    """
    maps each node to its corresponding community

    params:
    - G: graph
    - communities: communities generated with nx community detection algorithms
    """

    comm_map = {}

    for idx, comm in enumerate(list(communities)):
        for node in comm:
            comm_map[node] = idx

    return comm_map


def cdlib_calc_communities(G: nx.Graph, resolution=1., alg="louvain"):
    communities = []
    if alg == "louvain":
        communities = algorithms.louvain(G, resolution=resolution)
    elif alg == "leiden":
        communities = algorithms.leiden(G)  # weights
    else:
        print(f"add {alg} to cdlib calc communities function")

    node_comm_map = communities.to_node_community_map()
    comm_node_map = defaultdict(set)
    for node, comms in node_comm_map.items():
        for comm in comms:
            comm_node_map[comm].add(node)
    communities = list(comm_node_map.values())
    return communities


# def cdlib_visualize_communities(graph: nx.Graph, communities):
#     # fix edge
#     pos = nx.spring_layout(graph)
#     figsize = (20, 20)
#     nodesize = 20
#     # viz.plot_community_graph(graph, communities, pos)
#     viz.plot_network_highlighted_clusters(
#         graph, communities, pos, figsize=figsize, node_size=nodesize)
#     plt.show()
