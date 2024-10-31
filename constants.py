from dotenv import load_dotenv
import os

# list of youtuber names as they appear in their channels url handle
# https://www.viewstats.com/, justificar pelo artigo
YTBRS_LIST = [
    "felipeneto",      # 
    "enaldinho",       #
    "geleia0",         #
    "RobinHoodGamer1", #
    "rezendeevil",     # alguns shorts
    "natanporai",      # alguns shorts
    "camilaloures",    #
    "AuthenticGames",  # alguns videos com comentarios desativados
    "cadresplayer",    # muito pouco -> shorts (?)
    "brancoala",       #
]

# crawler paths
CRAWLER_PATH = "./data/"
YOUTUBERS_PATH = CRAWLER_PATH+"youtubers.json"


# api key
load_dotenv()
DEVELOPER_KEY = os.getenv("API_KEY")


# networks constants
CURR_YTBR = "felipeneto"
CURR_PATH = f"./data/{CURR_YTBR}/"
