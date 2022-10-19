from turtle import pd
import pandas as pd
import numpy as ny
import requests

API_KEY='AIzaSyBQvFKIQCnFRw7YN7U2b6c5iTzhKzrpHFs'
url='https://www.googleapis.com/youtube/v3/search?part=snippet,id&q=Toyota&maxResults=20&order=date&pageToken=''&key='+API_KEY
response=requests.get(url).json()

print(response['items'])


