import os
import json
import googleapiclient.discovery
from constants import YTBRS_LIST, PATH, YOUTUBERS_PATH, DEVELOPER_KEY

from utils import parse_comment_threads, parse_search_videos
from utils import parse_channel_info, save_data_to_json


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

            request = self.youtube.search().list(
                part="snippet",
                channelId=channel["channel_id"],
                order="date",  # viewcount
                type="video",
                maxResults=50,
            )

            response = request.execute()
            videos_data = parse_search_videos(response, channel)

            os.makedirs(PATH+channel['youtuber'], exist_ok=True)
            _path = f"{PATH}{channel['youtuber']}/videos_list.json"
            save_data_to_json(videos_data, _path)

    def build_videos_comments_list(self):
        datasets = self._get_youtuber_datasets_path()

        for path in datasets:
            video_data = []
            with open(path+"videos_list.json") as f:
                video_data = json.load(f)

            print(
                f"crawling comments from {video_data['channel_title']}'s videos")

            os.makedirs(path+"/comments", exist_ok=True)
            self._get_comments_from_video_ids(video_data["videos"],
                                              path+"/comments/")
            # todo: replies

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
        for v in videos:
            print(f"    comments from {v['video_title']}")

            request = self.youtube.commentThreads().list(
                part="snippet,replies,id",
                videoId=v["video_id"],
                maxResults=100,
                order="relevance",
            )

            response = request.execute()

            comments_data = parse_comment_threads(
                response, v["video_id"], v["video_title"])

            _path = f"{path}{v['video_id']}_comments.json"
            print(f"        got comments, saving at {_path}")
            save_data_to_json(comments_data, _path)


def main():
    craw = Crawling()
    # craw.build_youtubers_videos_list()
    craw.build_videos_comments_list()


if __name__ == "__main__":
    main()
