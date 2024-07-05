from googleapiclient.discovery import build
import pandas as pd
import api


class TrendingVideos():
    def __init__(self,category,location):
        self.api_key = api.api_key
        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.cat = category
        #Let's map some of ISO 3166-1 alpha-2 country code with country names to use in the web app
        self.location = location
        try:
            self.youtube = build(self.api_service_name, self.api_version, developerKey=self.api_key)
        except:
            print('Error! Anuthentication failed')

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
              category = self.cat.loc[int(item['snippet']['categoryId'])]['title'],
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
#call once and save the category details in a file to use it in filter
#video = TrendingVideos()
#category= video.get_category()
#category.to_csv('category.csv',index=False)


