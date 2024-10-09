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
    metrics["avg_clustering_coef_clique"] = calc_avg_clustering_coef(G, list(clique_members))

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
    avg_clustering_coef =  nx.average_clustering(G, weight="weight")
    print(f"    clustering coefficient: {avg_clustering_coef}")
    return avg_clustering_coef


def calc_avg_degree(G: nx.Graph):
    avg_degree = 2 * G.number_of_edges() / G.number_of_nodes()
    return avg_degree


def calc_modularity(G: nx.Graph):
    """
    Network modularity is a metric that quantifies the quality of a network's community structure. 
    It measures how well a network can be divided into distinct communities  where:
    - Nodes within the same community have many connections to each other
    - Nodes in different communities have fewer connections between them
    """
    # todo ...
    pass


def calc_k_cliques_communities(G: nx.Graph, k=5, consider_cliques=False):
    print(f"calculating communities with k_cliques_method, k={k} ...")

    cliques = None
    if consider_cliques:
        nx.find_cliques(G)

    communities = list(nx.community.k_clique_communities(G, k, cliques))
    print(f"{len(communities)} found")
    return communities


def calc_fast_label_prop(G: nx.Graph):
    weight = ...
    communities = nx.community.fast_label_propagation_communities(G, weight)
    return communities


def calc_louvain_communities(G: nx.Graph, resolution=1):
    """
    If resolution is less than 1, the algorithm favors larger communities. 
    Greater than 1 favors smaller communities
    """
    communities = nx.community.louvain_communities(G,
                                                   weight='weight',
                                                   resolution=1,
                                                   )
    return communities
