import os
import json
import googleapiclient.discovery
from constants import YTBRS_LIST, PATH, YOUTUBERS_PATH, DEVELOPER_KEY
import googleapiclient.errors
import pandas as pd

from utils import *

"""
1. import data as json from pandas OR
2. change to save as .csv 
- YOUTUBERS:
    - Controversos X Nao controversos
"""


class Crawling:

    def __init__(self):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

        self._api_service_name = "youtube"
        self._api_version = "v3"

        self.yt_channel_ids = []

        if not os.path.exists(PATH):
            os.makedirs(PATH)

        self._build_youtube_client()

    def _build_youtube_client(self):
        self.youtube = googleapiclient.discovery.build(self._api_service_name,
                                                       self._api_version,
                                                       developerKey=DEVELOPER_KEY)

    def build_channels_list(self):
        """
        builds youtubers_channel_list dataset
        """
        youtubers = []
        for name in YTBRS_LIST:

            print(f"Crawling info from @{name} ...")

            # make request to yt API with channel user @
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                # forUsername=name
                forHandle=name
            )

            response = request.execute()

            # saving data as json to ./data/{youtuber name}
            ytbr_data = parse_channel_info(response, name)
            youtubers.append(ytbr_data)

        print(f"got channels info. saving at {YOUTUBERS_PATH}")
        save_data_to_json(youtubers, YOUTUBERS_PATH)

    def build_youtubers_videos_list(self):
        """
        builds youtubers_videos_list json dataset
        with latest videos_data for each youtuber specified
        """
        if not os.path.exists(YOUTUBERS_PATH):
            self.build_channels_list()

        youtubers_list = []
        with open(YOUTUBERS_PATH) as f:
            youtubers_list = json.load(f)

        for channel in youtubers_list:
            print(
                f"Crawling info from : {channel['channel_title']}, @{channel['youtuber']} ...")

            # get only videos by channel id
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel["channel_id"],
                order="date",  # viewcount
                type="video",
                maxResults=50,
            )

            response = request.execute()

            _path = PATH+channel['youtuber']
            os.makedirs(_path, exist_ok=True)
            parse_search_videos(response, channel, _path)

    def build_videos_comments_df(self):
        datasets = self._get_youtuber_datasets_path()

        # get each youtuber's videos dataset
        for path in datasets:
            video_data = []
            with open(path+"videos_list.json") as f:
                video_data = json.load(f)

            # print(video_data["videos"])

            print(
                f"crawling comments from {video_data['channel_title']}'s videos")

            # creating folder structure, doesnt override if exists
            os.makedirs(path+"/comments", exist_ok=True)

            self._get_comments_from_video_ids(video_data["videos"],
                                              path)

    def _get_youtuber_datasets_path(self):
        """
        returns all youtuber datasets path as a list
        """
        data = []

        # getting youtuber folders
        for item in os.listdir(PATH):
            _item_path = os.path.join(PATH, item)
            if os.path.isdir(_item_path):
                data.append(_item_path+"/")
        return data

    def _get_comments_from_video_ids(self, videos, path):
        """
        iterates through each video, gets its comments and comment replies.
        saves dataset to its determined directory, comments/ or replies/.
        Params:
        - videos: videos list, with video_id, date, video_title
        - path: current youtuber path, i.e ./data/{youtuber}/
        """
        df = pd.DataFrame()
        for v in videos:
            print(f"    comments from {v['video_title']}")

            # gets comment from current video v
            request = self.youtube.commentThreads().list(
                part="snippet,replies,id",
                videoId=v["video_id"],
                maxResults=100,
                order="relevance",
            )

            response = {}
            try:
                response = request.execute()
            except googleapiclient.errors.HttpError as e:
                if e.error_details[0]["reason"] == "commentsDisabled":
                    print( f"skipping current video: {e.error_details[0]['message']}")

            # parses response, with selected params
            if response:
                print(f"    parsing comments and appending to dataframe")
                _d = parse_comment_threads(
                    response,
                    v["video_id"],
                    v["video_title"],
                    path
                )
                df = pd.concat([df, pd.DataFrame(_d)], ignore_index=True)
        print(f"saving...")
        df.to_csv(f'{path}_comments.csv')


def main():
    craw = Crawling()
    # craw.build_youtubers_videos_list()
    craw.build_videos_comments_df()


if __name__ == "__main__":
    main()
