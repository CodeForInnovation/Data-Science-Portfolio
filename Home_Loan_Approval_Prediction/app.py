import streamlit as st
import pandas as pd
from youtube_data import TrendingVideos




#Using cache data to avoid calling the api multiple times in a session
@st.cache_data
def fetch_get_video(region_code,cat):
    video = TrendingVideos(cat)
    return video.get_video(region_code)

#Using cache resource to save the data permanently after building app
@st.cache_resource
def get_cat():
    cat =pd.read_csv('category.csv',index_col ='id')
    return cat

cat = get_cat()

#Let's map some of ISO 3166-1 alpha-2 country code with country names to use in the web app
@st.cache_resource
def get_location():
    return pd.Series(data=['INDIA','USA','CANADA','AUSTRALIA','SOUTH AFRICA'],
                              index =['IN','US','CA','AU','ZA'])

location = get_location()
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

#fetching the trending videos based on region code and to get the global trend, we need to pass None
trending_videos = fetch_get_video(location.index[location == region][0] if region != 'Global' else None,cat)


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




