from dotenv import load_dotenv
import os

# list of youtuber names as they appear in their channels url handle
YTBRS_LIST = [
    "felipeneto",
    "enaldinho",
]

# data paths
PATH = "./data/"
YOUTUBERS_PATH = PATH+"youtubers.json"


# api key
load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")
