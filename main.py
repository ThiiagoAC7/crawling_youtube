import os
import json
import googleapiclient.discovery

from dotenv import load_dotenv
from youtubers import YTBRS_LIST


PATH = "./data/"
YOUTUBERS_PATH = PATH+"youtubers.json"
VIDEO_IDS_PATH = PATH+"video_ids_path.json"

load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")

class Crawling:

    def __init__(self):

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

        self._api_service_name = "youtube"
        self._api_version = "v3"

        self.yt_channel_ids = []

        if not os.path.exists(PATH):
            os.makedirs(PATH)

        self._build()

    def _build(self):
        self.youtube = googleapiclient.discovery.build(
            self._api_service_name, self._api_version, developerKey = DEVELOPER_KEY)


    def _parse_json(self,request):
        return json.dumps(request,indent=4)

    def save_data_to_json(self, data, path):
        print(f"Saving info at {path}")
        with open(path, "w") as f:
            f.write(self._parse_json(data))

    def _get_video_ids(self, response, channel):
        """
        builds youtubers_videos_list json dataset with the format:
        - channel_title
        - channel_id
        - handle 
        - nextPageToken
        - videos:
            - video_id
            - date_published
            - video_title
        """
        videos_data = {}
        videos_data["channel_title"] = channel["channel_title"]
        videos_data["channel_id"] = channel["channel_id"]
        videos_data["youtuber"] = channel["youtuber"]
        videos_data["nextPageToken"] = response["nextPageToken"]
        videos_data["videos"] = []
        items = response["items"]

        for i in items:
            _video_info = {}
            _video_info["video_id"] = i["id"]["videoId"]
            _snippets = i["snippet"]
            _video_info["date_published"] = _snippets["publishedAt"]
            _video_info["video_title"] = _snippets["title"]
            # video_dict["video_desc"] = _snippets["description"]
            videos_data["videos"].append(_video_info)

        return videos_data

    def build_youtubers_videos_list(self):
        """
        builds youtubers_videos_list json dataset
        with latest videos_data for each youtuber specified
        """
        if not os.path.exists(YOUTUBERS_PATH):
            self.get_ytbrs_channel_ids()
        
        youtubers_list = []
        with open(YOUTUBERS_PATH) as f:
            youtubers_list = json.load(f)

        for channel in youtubers_list:
            print(f"Crawling info from : {channel['channel_title']}, @{channel['youtuber']} ...")

            request = self.youtube.search().list(
                part="snippet",
                channelId=channel["channel_id"],
                order="date", #viewcount
                type="video",
                maxResults=50,
            )

            response = request.execute()
            videos_data = self._get_video_ids(response,channel)

            os.makedirs(PATH+channel['youtuber'], exist_ok=True)

            _path = f"{PATH}{channel['youtuber']}/videos_list.json" 
            self.save_data_to_json(videos_data,_path)


    def get_ytbrs_channel_ids(self):
        """
        builds youtubers_channel_list dataset
        with channel infos:
            - channel @ 
            - channel_id
            - channel_title
            - uploaded_videos_id
            - num_subs
            - num_Videos
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

            # get response specific infos
            items = response["items"][0]

            _id = items["id"]
            _title = items["snippet"]["title"]
            _videos_id = items["contentDetails"]["relatedPlaylists"]["uploads"] 
            _subs_count = items["statistics"]["subscriberCount"]
            _video_count = items["statistics"]["videoCount"]


            # saving data as json to ./data/{youtuber name}
            ytbr_data = {
                "youtuber":name,
                "channel_id":_id,
                "channel_title":_title,
                "uploaded_videos_id":_videos_id,
                "num_subs":_subs_count,
                "num_videos":_video_count,
            }

            youtubers.append(ytbr_data)


        print(f"got channels info. saving at {YOUTUBERS_PATH}")
        self.save_data_to_json(youtubers, YOUTUBERS_PATH)


def main():
    craw = Crawling()
    craw.build_youtubers_videos_list()



if __name__ == "__main__":
    main()
