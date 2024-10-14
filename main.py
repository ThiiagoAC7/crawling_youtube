from graphs.metrics_commenter_nets import *
from graphs.plot_commenter_nets import *
from graphs.build_commenter_networks import *
from constants import CURR_PATH, CURR_YTBR

import networkx as nx
import pandas as pd


"""
If your input graph edge weights for self-loops do not represent already reduced communities you 
may want to remove the self-loops before inputting that graph
TODO: 
    - remove self loops from graph
"""


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

def build_networks():
    df = pd.read_csv(f"{CURR_PATH}comments.csv")

    build_co_commenter_net(df)
    build_video_commenter_net(df)
    # build_vid_co_commenter_net(df)


def main():
    co_commenter_path = f'{CURR_PATH}/co_commenter_network_filtered.pickle'
    # vid_commenter_path = f'{CURR_PATH}/video_commenter_network.pickle'
    vid_co_commenter_path = f'{CURR_PATH}/video_co_commenter_network_filtered.pickle'

    path = co_commenter_path 

    G = load_graph(path)


    print(path.split("/")[-1][:-7])
    # plot_graph(G, path.split("/")[-1][:-7],save=True)
    # G = filter_graph(G=G, min_edge_weight=10)

    res = 0.8 
    communities = calc_louvain_communities(G, resolution = res) 
    # communities = calc_greedy_modularity_communities(G, resolution = res) 
    # communities = calc_label_prop_communities(G)

    largest_community = max(communities, key=len)
    number_of_communities = len(communities)

    print(f"total number of communities: {number_of_communities}")
    print(f"largest community has {len(largest_community)} members.")
    
    modularity = calc_modularity(G, communities, res)
    print(f"    modularity measure : {modularity}")

    coverage, performance = calc_coverage_performance(G,communities)
    print(f"    coverage: {coverage}, performance: {performance}")

    #
    # # comm_map = community_to_dict_mapping(G, communities)
    #
    # plot_community_graph(G, communities,res=res,
    #                      path=path.replace(CURR_PATH,"").replace(".pickle","").replace("/",""))


if __name__ == "__main__":
    # build_networks()
    main()
