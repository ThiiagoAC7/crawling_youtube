import pickle
import networkx as nx
import pandas as pd
from tqdm import tqdm
from itertools import combinations

from typing import Optional
from constants import CURR_YTBR, CURR_PATH


def build_video_commenter_net(df: pd.DataFrame, G: Optional[nx.Graph] = None, weighted=True) -> nx.Graph:
    """
    params:
    - df: youtube dataframe
    - G: optional graph param, if None, dumps the graph to current path. If not none, builds and returns G
    - weighted: to consider graph weights or not
    """
    graph_is_none = G is None
    if graph_is_none:
        G = nx.Graph()

    for _, row in tqdm(df.iterrows(), desc="building video-commenter network ...", total=len(df)):
        video = row["video_id"]
        commenter = row["comment_author_channel_id"]

        # set Node types 
        if not G.has_node(video):
            G.add_node(video, type="video")
        if not G.has_node(commenter):
            G.add_node(commenter, type="commenter")

        has_edge = G.has_edge(video, commenter)
        if has_edge and weighted:
            G[video][commenter]['weight'] += 1
        elif not has_edge:
            G.add_edge(video, commenter, weight=1)


    if graph_is_none:
        print(f"saving...")
        print(f"graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        pickle.dump(G, open(f'{CURR_PATH}/video_commenter_network.pickle', 'wb'))
    return G


def build_co_commenter_net(df: pd.DataFrame, G: Optional[nx.Graph] = None) -> nx.Graph:
    graph_is_none = G is None
    if graph_is_none:
        G = nx.Graph()

    #  video_ids -> list of commenters
    grouped_df = df.groupby('video_id')[
        'comment_author_channel_id'].apply(list)

    for commenters in tqdm(grouped_df, desc="building co-commenter network...", total=len(grouped_df)):
        if len(commenters) > 1:
            for pair in combinations(commenters, 2):

                # node types param
                if not G.has_node(pair[0]):
                    G.add_node(pair[0], type="commenter")
                if not G.has_node(pair[1]):
                    G.add_node(pair[1], type="commenter")

                if G.has_edge(pair[0], pair[1]):
                    # weight increases if commenters have commented on the same video
                    G[pair[0]][pair[1]]['weight'] += 1
                else:
                    # edge between commenters who commented on the same video
                    G.add_edge(pair[0], pair[1], weight=1)

    if graph_is_none:
        print(f"saving...")
        print(f"graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        pickle.dump(G, open(f'{CURR_PATH}/co_commenter_network.pickle', 'wb'))
    return G


def build_vid_co_commenter_net(df: pd.DataFrame):

    G = nx.Graph()
    G = build_video_commenter_net(df,G, weighted=False)
    G = build_co_commenter_net(df,G)

    pickle.dump(G, open(f'{CURR_PATH}/video_co_commenter_network.pickle', 'wb'))
    print(f"video_co_commenter_network of youtuber {CURR_YTBR} saved at {CURR_PATH}")
    print(f"graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")



