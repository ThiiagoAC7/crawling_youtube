import pandas as pd
import networkx as nx
import numpy as np


def compute_graph_metrics(G: nx.Graph):
    print(f"calculating graph metrics ...")
    metrics = {
        "num_nodes": 0,
        "num_edges": 0,
        "avg_degree": 0,
        "avg_clustering_coef": 0,
        "modularity": 0,
    }

    metrics["num_nodes"] = G.number_of_nodes()
    metrics["num_edges"] = G.number_of_edges()
    metrics["avg_degree"] = calc_avg_degree(G)
    metrics["avg_clustering_coef"] = calc_avg_clustering_coef(G)

    return metrics


def compute_clique_metrics(G: nx.Graph):
    print(f"calculating clique metrics ...")
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
    G = G.subgraph(list(clique_members))
    metrics["avg_degree_clique"] = calc_avg_degree(G)
    metrics["avg_clustering_coef_clique"] = calc_avg_clustering_coef(
        G, list(clique_members))

    return metrics


def calc_avg_clustering_coef(G: nx.Graph, nodes=None):
    """
    Calculates clustering coeficcient of a given graph 
    and saves values to a .csv

    Params:
    - G: graph 
    - threshold: Edge weights threshold
    """
    print('calculating clustering coefficient coefs ...')
    avg_clustering_coef = nx.average_clustering(G, weight="weight")
    print(f"    clustering coefficient: {avg_clustering_coef}")
    return avg_clustering_coef


def calc_avg_degree(G: nx.Graph):
    avg_degree = 2 * G.number_of_edges() / G.number_of_nodes()
    return avg_degree


def calc_modularity(G: nx.Graph, communities: list, resolution=1):
    """
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.modularity.html#networkx.algorithms.community.quality.modularity
    Network modularity is a metric that quantifies the quality of a network's community structure. 
    It measures how well a network can be divided into distinct communities  where:
    - Nodes within the same community have many connections to each other
    - Nodes in different communities have fewer connections between them
    """

    modularity = nx.community.modularity(G, communities, resolution)
    return modularity


def calc_coverage_performance(G: nx.Graph, communities: list):
    """
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.partition_quality.html#networkx.algorithms.community.quality.partition_quality
    - coverage: the ratio of the number of intra-community edges to the total number of edges in the graph
        - higher coverage indicates that most edges are within communities rather than between them
        - returns: percentage of the edges that are internal to communities
    - performance: partition is the ratio of correctly classified pairs of nodes (nodes in 
    the same community and connected by an edge or nodes in different communities and not connected).
        - returns: percentage of nodes that are correctly classified 
    """

    coverage, performance = nx.community.partition_quality(G, communities)
    return coverage, performance


def calc_partition_quality():
    """
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.quality.partition_quality.html#networkx.algorithms.community.quality.partition_quality
    """
    # todo ...
    pass


def calc_k_cliques_communities(G: nx.Graph, k=5):
    print(f"calculating communities with k_cliques_method, k={k} ...")

    communities = list(
        nx.community.k_clique_communities(G, k, backend="paralel"))
    print(f"{len(communities)} found")
    return communities


def calc_label_prop_communities(G: nx.Graph):
    """
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.label_propagation.asyn_lpa_communities.html#r40d53c2ae55e-1
    The algorithm is probabilistic and the found communities may vary on different executions.
    - define seed param
    """

    communities = nx.community.asyn_lpa_communities(G,
                                                    weight="weight")
    return communities


def calc_louvain_communities(G: nx.Graph, resolution=1):
    """
    If resolution is less than 1, the algorithm favors larger communities. 
    Greater than 1 favors smaller communities
    """
    communities = nx.community.louvain_communities(G,
                                                   weight='weight',
                                                   resolution=resolution,
                                                   )
    return communities


def calc_greedy_modularity_communities(G: nx.Graph, resolution=1):
    """
    https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.modularity_max.greedy_modularity_communities.html#networkx.algorithms.community.modularity_max.greedy_modularity_communities
    """
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
