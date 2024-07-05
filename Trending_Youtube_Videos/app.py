import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from youtube_data import get_video,cat,location




#Caching the api data to avoid making api calls everytime user interacts with the app
@st.cache
def fetch_get_video(region_code):
    return get_video(region_code)


#creating a function to return like/view counts as k(kilo) and M(million)
def transform(counts):
    if counts < 1000:
        return counts
    elif counts < 1000000:
        return f"{round(counts/1000,1)}k"
    else:
        return f"{round(counts/1000000,1)}M"



st.title('Trending YouTube Videos')

region = st.sidebar.radio('Select Region',['Global','INDIA','USA','CANADA','AUSTRALIA','SOUTH AFRICA'])
category_filter = st.sidebar.multiselect('Filter by Category',cat['title'].tolist())
sort_by = (st.sidebar.radio('Sort by',['Trend','Date','Likes','Views']))
trending_videos = fetch_get_video(location.index[location == region][0] if region != 'Global' else None)


filter_videos = trending_videos.copy()

if category_filter:
    filter_videos = filter_videos[filter_videos['category'].isin(category_filter)]

if sort_by !='Trend':
    filter_videos = filter_videos.sort_values(by=sort_by.lower(),ascending=False)



col1,col2= st.columns([2,1])
# just to contain the output in a particular width, creating 2 columns with 1st column twice in width as second column
with col1:
    for i,video in filter_videos.iterrows():
        st.image(video['thumbnail'],caption=f" {transform(video['views'])} Views  ❤️ {transform(video['likes'])}  ",width=450)
        st.write(f"[{video['title']}]({video['url']})")




