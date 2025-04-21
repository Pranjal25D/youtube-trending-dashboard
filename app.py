import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="YouTube Trending Analysis", layout="wide")
st.title("📊 YouTube Trending Video Analysis (India 🇮🇳)")

# Load Data
df = pd.read_csv("INvideos.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['publish_date'] = df['publish_time'].dt.date

# Sidebar
st.sidebar.header("Filter Options")
categories = df['category_id'].unique().tolist()
selected_categories = st.sidebar.multiselect("Select Category ID(s)", categories)

channel_input = st.sidebar.text_input("Filter by Channel Name (optional)")

filtered_df = df.copy()
if selected_categories:
    filtered_df = filtered_df[filtered_df['category_id'].isin(selected_categories)]

if channel_input:
    filtered_df = filtered_df[filtered_df['channel_title'].str.contains(channel_input, case=False)]

st.subheader("🔥 Top 10 Trending Videos by Views")
top_videos = filtered_df.sort_values(by='views', ascending=False).head(10)
st.dataframe(top_videos[['title', 'channel_title', 'views', 'likes']])

# Scatter Plot: Views vs Likes
st.subheader("📈 Views vs Likes")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=filtered_df, x='views', y='likes', ax=ax1)
ax1.set_title("Views vs Likes")
st.pyplot(fig1)

# Bar Chart: Top Channels
st.subheader("🏆 Top 10 Channels by Video Count")
top_channels = filtered_df['channel_title'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_channels.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_ylabel("Video Count")
ax2.set_title("Top 10 Channels")
st.pyplot(fig2)

# Word Cloud
st.subheader("🔤 Word Cloud of Tags")
all_tags = " ".join(filtered_df['tags'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_tags)
fig3, ax3 = plt.subplots()
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off")
st.pyplot(fig3)
