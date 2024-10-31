from graphs.feature_similarity import merge_channel_dfs
from graphs.metrics_commenter_nets import *
from graphs.plot_commenter_nets import *
from graphs.build_commenter_networks import *
from graphs.plot_communities import *
from graphs.feature_similarity import plot_feature_simmilarity

from crawler.crawling import Crawling
from constants import CURR_PATH, CURR_YTBR

import networkx as nx
import pandas as pd
import pickle
import os


def run_crawler():
    craw = Crawling()
    craw.build_channels_list()
    # craw.build_youtubers_videos_list()
    # craw.build_videos_comments_df()


def save_graph_metrics(G: nx.Graph, communities, res):
    print(f"calculating graph metrics ...")

    metrics = compute_graph_metrics(G, communities, res)

    df = pd.DataFrame([metrics])
    os.makedirs(f"{CURR_PATH}metrics/", exist_ok=True)
    df.to_csv(f"{CURR_PATH}metrics/commenter_network_metrics.csv")

def save_community_metrics(G: nx.Graph, communities):
    print(f"calculating community metrics ...")

    metrics = calc_per_community_metrics(G, communities)

    df = pd.DataFrame(metrics)
    os.makedirs(f"{CURR_PATH}metrics/", exist_ok=True)
    df.to_csv(f"{CURR_PATH}metrics/commenter_network_community_metrics.csv")

def save_clique_metrics(G: nx.Graph):
    print(f"calculating clique metrics ...")

    metrics = compute_clique_metrics(G)
    
    df = pd.DataFrame([metrics])
    os.makedirs(f"{CURR_PATH}metrics/", exist_ok=True)
    df.to_csv(f"{CURR_PATH}metrics/commenter_network_clique_metrics.csv")


def build_networks():
    df = pd.read_csv(f"{CURR_PATH}comments.csv")

    build_co_commenter_net(df)
    build_video_commenter_net(df)
    # build_vid_co_commenter_net(df)


def filter_and_save_graph(path):
    name = path.split("/")[-1].replace(".pickle", "")
    print(f"filtering and saving {name} of youtuber {CURR_YTBR}")

    G = load_graph(path)
    # mininum number of videos users co-commented on
    G = filter_graph(G, min_edge_weight=10)

    pickle.dump(G, open(f'{CURR_PATH}/{name}_filtered_noselfloop.pickle', 'wb'))
    print(f"saved ..")


def community_metrics(path, save_metrics=True, plot=True):
    G = load_graph(path)

    print(f'{path.split("/")[-1][:-7]} - {CURR_YTBR}')

    res = 0.8

    communities = calc_louvain_communities(G, res)

    if save_metrics:
        save_graph_metrics(G, communities, res)
        save_community_metrics(G, communities)
        save_clique_metrics(G)
        comm_map = []
        for i, c in enumerate(list(communities)):
            for node in c:
                comm_map.append({
                    "commenter" : node,
                    "community" : i,
                })

        comm_map_df = pd.DataFrame(comm_map)
        comm_map_df.to_csv(f"{CURR_PATH}metrics/communities.csv", index=False)


    if plot:
        # todo: legenda com index de cada comunidade
        plot_communities(G, communities)
        # plot_community_graph(G, communities,res=res,
        #                      path=path.replace(CURR_PATH,"").replace(".pickle","").replace("/",""))


"""
If your input graph edge weights for self-loops do not represent already reduced communities you 
may want to remove the self-loops before inputting that graph

- Modularity
- Conductance
- Community Size
- Density
- https://github.com/cjhutto/vaderSentiment

"""

def main():
    co_commenter_path = f'{CURR_PATH}/co_commenter_network.pickle'
    co_commenter_ftr_path = f'{CURR_PATH}/co_commenter_network_filtered.pickle'
    co_commenter_nsl_path = f'{CURR_PATH}/co_commenter_network_filtered_noselfloop.pickle'

    print(f"current youtuber: {CURR_YTBR}")

    community_metrics(co_commenter_nsl_path, save_metrics=True, plot=True)



if __name__ == "__main__":
    # run_crawler()
    main()
