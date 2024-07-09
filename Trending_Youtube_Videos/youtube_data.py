from googleapiclient.discovery import build
import pandas as pd
import os


class TrendingVideos():
    def __init__(self,cat):
        self.api_key = os.getenv('API_KEY')
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.cat = cat
        self.youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)

     #function to call the api and retrive the trending video details based on the region code
    def get_video(self,region):
    
        #creating the trending video api service, for more information please refer https://developers.google.com/youtube/v3

        df_video=[]
        request = self.youtube.videos().list(
        part="snippet,contentDetails,statistics",
        chart="mostPopular",
        regionCode=region,
        maxResults=10)
        response=request.execute()
        for item in response['items']:
            df = dict(video_id = item['id'],
              title = item['snippet']['title'],
              views = int(item['statistics']['viewCount']),
              likes = int(item['statistics']['likeCount']),
              comments = int(item['statistics']['commentCount']),
              region = 'Global' if region is None else region,
              category_id = int(item['snippet']['categoryId']),
              category = self.cat.loc[int(item['snippet']['categoryId'])],
              date = item['snippet']['publishedAt'],
              thumbnail = item['snippet']['thumbnails']['high']['url'],
              url = f"https://www.youtube.com/watch?v={item['id']}",
              channel_name = item['snippet']['channelTitle'],
              description = item['snippet']['description'])
            df_video.append(df)
        return pd.DataFrame(df_video)

        #Code to get the category id and title. Since it is same for all the regions, we will be using this api
    def get_category(self):
        
        request = self.youtube.videoCategories().list(
        part="snippet",
        regionCode="IN")
        response = request.execute()
        category =[]
        for item in response['items']:
            cat = dict(id=item['id'],title = item['snippet']['title'])
            category.append(cat)
        return pd.DataFrame(category)



