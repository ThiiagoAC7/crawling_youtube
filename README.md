# youtube crawler

Crawling youtube data 

## Dataset structure
```
    data/
    └──youtubers_list.json
    └──{youtuber_channel_name}
        └──videos_list.json
        └──comments/
            └──{video_id}_comments.json
            └──replies/
                └──{comment_id}_comments.json
```
### params
- Youtubers list:
    - youtuber: channel @ as shown in youtuber channel url 
    - channel_id: channel id 
    - channel_title: channel name
    - uploaded_videos_id: id to use with youtube data api playlistItems endpoint
    - num_subs: total number of subscribers 
    - num_videos: total number of videos
- Youtubers Videos list:
    - channel_id: channel id 
    - channel_title: channel name
    - youtuber: channel @ as shown in youtuber channel url 
    - nextPageToken: "The token that can be used as the value of the pageToken parameter to retrieve the next page in the result set", used to get more than the maxResults from yt data api
    - videos:
        - video_id: video id as shown in the video url
        - date_published: when video was published
        - video_title: video title
- Youtubers Video Comments list:
    - video_id: video id
    - date_published: date
    - video_title: title
    - comments:
        - comment_id: comment id
        - comment_text: text of the comment as its shown
        - comment_author_name: author's channel handle
        - comment_author_channel_id: author's channel id 
        - comment_like_count: number of likes comment has 
        - comment_publish_date: when comment was published 
