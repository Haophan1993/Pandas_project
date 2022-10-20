from turtle import pd
import pandas as pd
import requests
import psycopg2 as ps


def connect_to_db(hostName, dbName, Port, UserName, Password):
    try:
        conn=ps.connect(host=hostName, database=dbName, port=Port, user=UserName, password=Password)
    except ps.OperationalError as e:
        raise e
    else:
        print('Connected to database')
    
    return conn

def create_table(curr):
    
    create_table_command =("""CREATE TABLE IF NOT EXISTS video1(
    video_id VARCHAR(255) PRIMARY KEY,
    video_title TEXT NOT NULL,
    upload_date DATE NOT NULL DEFAULT CURRENT_DATE,
    view_count INTEGER NOT NULL,
    like_count INTEGER NOT NULL,
    dislike_count INTEGER NOT NULL,
    favorite_count INTEGER NOT NULL,
    comment_count INTEGER NOT NULL
    );""")
    curr.execute(create_table_command)
    

def check_exist_video(curr, video_id):
    select_video=("""
                    SELECT video_id FROM video1
                    WHERE video_id=%s;""")

    curr.execute(select_video, (video_id,))
    
    return curr.fetchone()                                                              

def insert_data_to_table(curr, video_id, video_title, upload_date, view_count, like_count, dislike_count, favorite_count, comment_count):
    insert_video =("""
                    INSERT INTO video1 VALUES(%s, %s, %s, %s, %s, %s, %s, %s );""")
    curr.execute(insert_video, (video_id, video_title, upload_date, view_count, like_count, dislike_count, favorite_count, comment_count,))


def update_data_to_table(curr, video_title, upload_date, view_count, like_count, dislike_count, favorite_count, comment_count, video_id ):
    
    update_video=("""
                    UPDATE video1
                    SET video_title=%s,
                        upload_date=%s,
                        view_count=%s,
                        like_count=%s,
                        dislike_count=%s,
                        favorite_count=%s,
                        comment_count=%s
                    WHERE video_id=%s;""")
    curr.execute(update_video,(video_title, upload_date, view_count, like_count, dislike_count, favorite_count, comment_count, video_id,) )



API_KEY='AIzaSyBQvFKIQCnFRw7YN7U2b6c5iTzhKzrpHFs'
url='https://www.googleapis.com/youtube/v3/search?part=snippet,id&q=Honda&maxResults=50&order=date&pageToken=''&key='+API_KEY
response=requests.get(url).json()


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


#df.to_csv('out.csv')


#df=pd.read_csv('out.csv', index_col=0)

host_name='mydatabase-instance.cmbb90ngezbh.us-east-1.rds.amazonaws.com'
dbname='first_test_db'
port='5432'
username='minhphan'
password='minhphan12345'
conn=None

conn = connect_to_db(host_name,dbname, port, username, password)
curr=conn.cursor()
create_table(curr)

for i, row in df.iterrows():
    
    if check_exist_video(curr, row['VideoId']) ==None:

        insert_data_to_table(curr, row['VideoId'], row['VideoTitle'], row['UploadDate'], row['ViewCount'], row['LikeCount'], 
                           row['DislikeCount'], row['FavoriteCount'], row['CommentCount'])
    
    else:
        update_data_to_table(curr, row['VideoTitle'], row['UploadDate'], row['ViewCount'], row['LikeCount'], 
                           row['DislikeCount'], row['FavoriteCount'], row['CommentCount'], row['VideoId'] )


conn.commit()
curr.close()
conn.close()
print('Connection is closed')




