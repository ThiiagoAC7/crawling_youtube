import pickle
import networkx as nx
import pandas as pd
from tqdm import tqdm
from itertools import combinations

from constants import CURR_YTBR, CURR_PATH


def build_video_commenter_net(df: pd.DataFrame):
    G = nx.Graph()

    for _, row in tqdm(df.iterrows(), desc="building video-commenter network ...",total=len(df)):
        video = row["video_id"]
        commenter = row["comment_author_channel_id"]
        if G.has_edge(video, commenter):
            G[video][commenter]['weight'] += 1
        else:
            G.add_edge(video,commenter, weight=1)

    pickle.dump(G, open(f'{CURR_PATH}/video_commenter_network.pickle', 'wb'))


def build_co_commenter_net(df: pd.DataFrame):
    # each commenter id grouped by the video they commented on
    grouped_df = df.groupby('video_id')[
        'comment_author_channel_id'].apply(list)

    G = nx.Graph()

    for commenters in tqdm(grouped_df, desc="building co-commenter network...", total=len(grouped_df)):
        if len(commenters) > 1:
            for pair in combinations(commenters, 2):
                if G.has_edge(pair[0], pair[1]):
                    # weight increases if commenters have commented on the same video
                    G[pair[0]][pair[1]]['weight'] += 1
                else:
                    # edge between commenters who commented on the same video
                    G.add_edge(pair[0], pair[1], weight=1)

    pickle.dump(G, open(f'{CURR_PATH}/co_commenter_network.pickle', 'wb'))


# def main():
#     DATA = f"{CURR_PATH}comments.csv"
#     df = pd.read_csv(DATA)
#     # build_co_commenter_net(df)
#     build_video_commenter_net(df)
#
#
# if __name__ == "__main__":
#     main()
