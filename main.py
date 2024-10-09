from metrics_commenter_nets import *
from plot_commenter_nets import *
from build_commenter_networks import *
from constants import CURR_PATH, CURR_YTBR

import networkx as nx
import pandas as pd


def plots(G: nx.Graph):
    plot_co_commenter_graph(G, save=False)
    # plot_video_commenter_graph(G)


def save_graph_metrics(G: nx.Graph):

    metrics = compute_graph_metrics(G)

    print(metrics)
    df = pd.DataFrame([metrics])
    df.to_csv(f"{CURR_PATH}commenter_network_metrics.csv")


def save_clique_metrics(G: nx.Graph):

    metrics = compute_clique_metrics(G)

    print(metrics)

    df = pd.DataFrame([metrics])
    df.to_csv(f"{CURR_PATH}commenter_network_clique_metrics.csv")


def main():
    co_commenter_path = f'{CURR_PATH}/co_commenter_network.pickle'
    vid_commenter_path = f'{CURR_PATH}/video_commenter_network.pickle'

    G = load_graph(co_commenter_path)
    G = filter_graph(G=G,
                     min_edge_weight=10)

    communities = calc_louvain_communities(G, resolution = 2.0) 
    # communities = calc_k_cliques_communities(G, consider_cliques=True)

    largest_community = max(communities, key=len)

    print(f"    total number of communities: {len(communities)}")
    print(f"    largest community has {len(largest_community)} members.")

    plot_communities(G, communities)


if __name__ == "__main__":
    main()
