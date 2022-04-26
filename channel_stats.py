import pandas as pd
import streamlit as st
import YouTubeAPI as youTube
import config
import plotly.express as px
from numerize import numerize

# set the layout and title of app
st.set_page_config(layout='wide')
st.title('YouTube Channel Data')

with st.expander('About this app'):
    st.write('This app allows user to download the list of videos posted by YouTube Channel using YouTube API.')
    st.image('https://d15-a.sdn.cz/d_15/c_img_F_G/8YsBZzN.jpeg?fl=cro,0,0,798,450%7Cres,1024,,1%7Cwebp,75', width=100)


# hide the sidebar
st.markdown(""" <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """,
            unsafe_allow_html=True)


with st.form('youTube_channel_id'):
    youTubeChannelID = st.text_input(label='YouTube Channel ID', placeholder='Paste the youtube channel id here...for '
                                                                             'eg. UCkS7Vxu4PjM99w0Is6idjcg')
    st.form_submit_button(label='Get Channel Stats')

if youTubeChannelID == '':
    st.stop()
else:
    list_of_videos = youTube.get_channel_videos(youTubeChannelID)
    youTube.video_table(list_of_videos)
    video_stats = youTube.get_videos_stats(config.video_id)
    youTube.stat_table(video_stats)
    df = pd.DataFrame(zip(config.channel_id, config.channel_name,
                          config.video_id, config.video_type, config.video_title,
                          config.video_description, config.view_count, config.like_count,
                          config.dislike_count, config.favoriteCount, config.commentCount,
                          config.publishedAt), columns=config.video_table)

    st.markdown(""" ## YouTube Channel Details """)
    st.write('Channel Name: ', config.channel_name[0])

    # metrics
    total_videos, total_views, total_likes, total_comments = st.columns(4)
    total_videos.metric("Total Videos", len(config.video_id))
    total_views.metric("Total Views", numerize.numerize(float(df['view_count'].astype(int).sum()), 2))
    total_likes.metric("Total Likes", numerize.numerize(float(df['like_count'].astype(int).sum()), 2))
    total_comments.metric("Total Comments", numerize.numerize(float(df['commentCount'].astype(int).sum()), 4))

    # display dataframe
    st.dataframe(df.head(10))

    # Download data
    csv = youTube.convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{config.channel_name[0]}.csv',
        mime='text/csv',
    )

    # visualization
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['year'] = df['publishedAt'].dt.year
    df['month'] = df['publishedAt'].dt.month
    df['week'] = df['publishedAt'].dt.isocalendar().week

    videos_per_year = df.groupby('year')['video_id'].count().reset_index()
    videos_per_year.columns = ['Year', 'Count']
    fig_videos_per_year = px.bar(videos_per_year, x='Year', y='Count', title='Videos posted per Year')
    st.plotly_chart(fig_videos_per_year)

    # reset the data
    config.reset_data()


