import streamlit as st
st.title("firstproject")
import pymongo
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import date
from io import StringIO

st.title("Twitter scraping")
# Setting variables to be used below
maxTweets = 100
# Creating list to append tweet data to
tweets_list2 = []
# Using TwitterSearchScraper to scrape data and append tweets to list
tag_the_user=st.sidebar.text_input("Enter the User_Hashtag:")
from_date=st.sidebar.date_input("From_date(YYYY-MM-DD):")
end_date=st.sidebar.date_input("End_date(YYYY-MM-DD):")
tweets_count=st.sidebar.number_input("enter the count:",min_value=1,max_value=100)
def convert_dataframe(dataframe):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return dataframe.to_csv().encode('utf-8')
if st.button('Click me'):
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{tag_the_user} since:{from_date} until:{end_date}").get_items()):
        if i>maxTweets:
            break
        tweets_list2.append([ tweet.id,
                        tweet.user.username,
                        tweet.url,
                        tweet.rawContent,
                        tweet.replyCount,
                        tweet.retweetCount,
                        tweet.likeCount,
                        tweet.lang,
                        tweet.source,
                        tweet.date,])


tweets_df2 = pd.DataFrame(tweets_list2, columns=['Tweet Id','Username', 'URL', 'Content', 'Replay Count', 'Re Tweet', 'Like Count', 'Lang', 'Source','Datetime'])
tweets_df2
tweet_download = convert_dataframe(tweets_df2)

dic_values=tweets_df2.to_dict('list')
# dic_values
   


kamal = pymongo.MongoClient("mongodb+srv://Kamalesh:4747@cluster0.wghtcrc.mongodb.net/test")
db=kamal.project1
project2=db.twitter
project2.insert_one(dic_values)
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#     To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)
    dataframe = pd.read_csv(uploaded_file)
    dic_value2=dataframe.to_dict('list')
    dic_value2
    project2.insert_one(dic_value2)
    st.success('Upload to MongoDB Successful!', icon="✅")
    

#Download file 
upload_file = convert_dataframe(dataframe)
st.download_button(
    label="Download scraping data as CSV",
    data=tweet_download,
    file_name='scraped_data.csv',
    mime='text/csv')
st.download_button(
    label="Download upload data as CSV",
    data=upload_file,
    file_name='upload_file_data.csv',
    mime='text/csv')
