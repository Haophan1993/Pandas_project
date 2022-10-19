from turtle import pd
import pandas as pd
import numpy as ny
import requests

API_KEY='AIzaSyBQvFKIQCnFRw7YN7U2b6c5iTzhKzrpHFs'
url='https://www.googleapis.com/youtube/v3/search?part=snippet,id&q=Toyota&maxResults=50&order=date&pageToken=''&key='+API_KEY
response=requests.get(url).json()
print('Working on dev branch')

df=pd.DataFrame(columns=['VideoId','VideoTitle', 'UploadDate','ViewCount', 'LikeCount','DislikeCount', 'FavoriteCount','CommentCount'])

for video in response['items']:
    
    video_id=video['id']['videoId']
    video_title = video['snippet']['title']
    upload_date= str(video['snippet']['publishedAt']).split('T')[0]
    details_url ='https://www.googleapis.com/youtube/v3/videos?part=statistics&id='+video_id + '&key='+API_KEY
    details_response = requests.get(details_url).json()
    view_count=0
    like_count=0
    dislike_count=0
    favorite_count=0
    comment_count=0
    #print(details_response['items'][0]['statistics'])

    for statis in details_response['items'][0]['statistics']:
        
        if statis=='viewCount':
            view_count=details_response['items'][0]['statistics']['viewCount']
        elif statis=='likeCount':
            like_count=details_response['items'][0]['statistics']['likeCount']
        elif statis=='dislikeCount':
            dislike_count=details_response['items'][0]['statistics']['dislikeCount']
        elif statis=='favoriteCount':
            favorite_count=details_response['items'][0]['statistics']['favoriteCount']
        elif statis=='commentCount':
            comment_count=details_response['items'][0]['statistics']['commentCount']
        
    dt=[video_id, video_title, upload_date, view_count, like_count, dislike_count, favorite_count, comment_count]    
    df=pd.concat([df,pd.DataFrame([dt], columns=['VideoId','VideoTitle', 'UploadDate','ViewCount', 'LikeCount','DislikeCount', 'FavoriteCount','CommentCount'])], ignore_index=True)
    
df.to_csv('out.csv')





