import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_gsheets import GSheetsConnection
import altair as alt

url: str = 'https://docs.google.com/spreadsheets/d/1Kr_h6lfZzji2X8fyfnd7bWAtH3ap_7-7Zmzj--UpA-Y/edit?usp=sharing'
conn: GSheetsConnection = st.experimental_connection('all_games', type=GSheetsConnection)

df: pd.DataFrame = conn.read(spreadsheet=url, worksheet=0)

st.header('Game Metacritic Analysis 1995-2021')
st.subheader('Raw Data dari Google Sheets')
st.write('Data mentah yang diambil dari Kaggle (https://www.kaggle.com/datasets/deepcontractor/top-video-games-19952021-metacritic/data)')

str="Not Available"
df['summary'].fillna("Not Available", inplace = True)
df['meta_score'] = df['meta_score'].div(10)
st.dataframe(df)

st.divider()
st.subheader('10 Game Terbaik')
st.write('10 game terbaik menurut meta score dan user review.')
top_10 = df.sort_values(by=['meta_score','user_review'], ascending=False).head(10)
st.dataframe(top_10)

st.divider()
st.subheader('10 Game Pilihan Metacritic')
st.write('10 game terbaik menurut meta score.')
meta_10 = df.sort_values(by=['meta_score'], ascending=False).head(10)
st.dataframe(meta_10)

st.divider()
st.subheader('10 Game Pilihan User')
st.write('10 game terbaik menurut user review.')

user_10 = df[~df['user_review'].str.contains('tbd')].reset_index().head(10).sort_values(by=['user_review'], ascending=False)
user_10['user_review'] = pd.to_numeric(user_10['user_review'])
st.dataframe(user_10)

st.divider()
st.subheader('Distribusi Video Game dalam Platform')
count_platform = df["platform"].value_counts().reset_index()
# count_platform.columns = ["Platform", "Count"]
# count_platform
platform_chart = (
    alt.Chart(count_platform).mark_bar().encode(
        x=alt.X('index',sort='-y'),
        y=alt.Y('platform')
    )
)
st.altair_chart(platform_chart,use_container_width=True)
st.write('PC memiliki jumlah video game terbanyak di antara platform lainnya. Akan tetapi, dalam ranking 10 teratas tidak terdapat platform PC.')