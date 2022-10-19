from turtle import pd
import pandas as pd
import numpy as ny
import requests

API_KEY='AIzaSyBQvFKIQCnFRw7YN7U2b6c5iTzhKzrpHFs'
url='https://www.googleapis.com/youtube/v3/search?part=snippet,id&q=Toyota&maxResults=5&order=date&pageToken=''&key='+API_KEY
response=requests.get(url).json()
print('Working on dev branch')


for video in response['items']:
    
    video_id=video['id']['videoId']
    video_title = video['snippet']['title']
    upload_date= str(video['snippet']['publishedAt']).split('T')[0]
    print(video_id)
    print(video_title)
    print(upload_date)
    print()


