import json

"""
parsing responses from youtube data api
"""

def _parse_json(request):
    return json.dumps(request, indent=4)


def save_data_to_json(data, path):
    print(f"Saving info at {path}")
    with open(path, "w") as f:
        f.write(_parse_json(data))


def parse_comment_threads(response, video_id, video_title, path):
    items = response["items"]
    comments_data = {}
    # comments_data["nextPageToken"] = response["nextPageToken"] # todo: fix 
    comments_data["video_id"] = video_id
    comments_data["video_title"] = video_title
    comments_data["comments"] = []

    for i in items:
        tlc = i["snippet"]["topLevelComment"]
        _comment = {}
        _comment["comment_id"] = tlc["id"]
        _comment["comment_text"] = tlc["snippet"]["textDisplay"]
        _comment["comment_author_name"] = tlc["snippet"]["authorDisplayName"]
        _comment["comment_author_channel_id"] = tlc["snippet"]["authorChannelId"]["value"]
        _comment["comment_like_count"] = tlc["snippet"]["likeCount"]
        _comment["comment_publish_date"] = tlc["snippet"]["publishedAt"]

        comments_data["comments"].append(_comment)

        if int(i["snippet"]["totalReplyCount"]) > 0:
            parse_replies(i["replies"], tlc["id"], path)


    _path = f"{path+'/comments/'}{video_id}_comments.json"
    print(f"        got comments, saving at {_path}")
    save_data_to_json(comments_data, _path)

def parse_replies(replies, parent_id, path):
    subcomments = replies["comments"]

    replies_data = {}
    replies_data["parent_comment"] = parent_id 
    replies_data["replies"] = []

    for s in subcomments:
        _subcomment = {}
        _subcomment["reply_id"] = s["id"]
        _subcomment["reply_text"] = s["snippet"]["textDisplay"]
        _subcomment["reply_parent_comment_id"] = s["snippet"]["parentId"]
        _subcomment["reply_author_name"] = s["snippet"]["authorDisplayName"]
        _subcomment["reply_author_channel_id"] = s["snippet"]["authorChannelId"]["value"]
        _subcomment["reply_like_count"] = s["snippet"]["likeCount"]
        _subcomment["reply_publish_date"] = s["snippet"]["publishedAt"]

        replies_data["replies"].append(_subcomment)

    _path = f"{path+'/replies/'}{parent_id}_comments.json"
    print(f"        got replies, saving at {_path}")
    save_data_to_json(replies_data, _path)

def parse_search_videos(response, channel):
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


def parse_channel_info(response, name):
    # get response specific infos
    items = response["items"][0]

    _id = items["id"]
    _title = items["snippet"]["title"]
    _videos_id = items["contentDetails"]["relatedPlaylists"]["uploads"]
    _subs_count = items["statistics"]["subscriberCount"]
    _video_count = items["statistics"]["videoCount"]

    ytbr_data = {
        "youtuber": name,
        "channel_id": _id,
        "channel_title": _title,
        "uploaded_videos_id": _videos_id,
        "num_subs": _subs_count,
        "num_videos": _video_count,
    }

    return ytbr_data
