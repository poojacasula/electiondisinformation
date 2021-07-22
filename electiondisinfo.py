import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import pandas as pd
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# # Creating list to append tweet data to
# tweets_list2 = []
# tweets_list3 = []

# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#HammerAndScorecard since:2020-06-01 until:2020-11-21').get_items()):
#     #only searching for 100 tweets, but you can change this
#     if i>100:
#         break
#     #you'll get date, ID, content, username, location, num of retweets, likes, replies, and quote tweets
#     tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.url, tweet.retweetCount, tweet.replyCount, tweet.likeCount, tweet.quoteCount])

# # for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#HammerAndScorecard since:2020-06-01 until:2020-11-21')).get_items():
# #         #only searching for 100 tweets, but you can change this
# #     if i>100:
# #         break
# #     #you'll get date, ID, content, username, location, num of retweets, likes, replies, and quote tweets
# #     tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.url, tweet.retweetCount, tweet.replyCount, tweet.likeCount, tweet.quoteCount])
    
# # Creating a dataframe from the tweets list above
# #tweets_df2 = pd.DataFrame(tweets_list2, columns=['Date', 'Tweet Id', 'Text', 'Username', 'Location', '#Retweets', '#Replies', '#Likes', '#QuoteTweets'])

# for k,tweet2 in enumerate(sntwitter.TwitterSearchScraper('hammer scorecard since:2020-06-01 until:2020-11-21').get_items()):
#         #only searching for 100 tweets, but you can change this
#     if k>100:
#         break
#     #you'll get date, ID, content, username, location, num of retweets, likes, replies, and quote tweets
#     tweets_list2.append([tweet2.date, tweet2.id, tweet2.content, tweet2.user.username, tweet2.url, tweet2.retweetCount, tweet2.replyCount, tweet2.likeCount, tweet2.quoteCount])

# tweets_df2 = pd.DataFrame(tweets_list2, columns=['Date', 'Tweet Id', 'Text', 'Username', 'Location', '#Retweets', '#Replies', '#Likes', '#QuoteTweets'])

data_url = ("hammerscorecard2.csv")
def load_data(nrows):
    data = pd.read_csv(data_url, nrows=nrows)
    return data

tweets_df2 = load_data(31976)

tweets_df2['Date'] = pd.to_datetime(tweets_df2['Date'])


def check_word_in_tweet(word, data):
    """Checks if a word is in a Twitter dataset's text. 
    Checks text and extended tweet (140+ character tweets) for tweets,
    retweets and quoted tweets.
    Returns a logical pandas Series.
    """
    contains_column = data['Text'].str.contains(word, case = False)
    return contains_column




cia = check_word_in_tweet('CIA', tweets_df2)
trump = check_word_in_tweet('Trump', tweets_df2)
fraud = check_word_in_tweet('fraud', tweets_df2)
election_fraud = check_word_in_tweet('election fraud', tweets_df2)

# Print proportion of tweets mentioning #python
#print("Proportion of tweets:", np.sum(hammerandscorecard) / tweets_df2.shape[0])
st. write('Total # of Tweets:', tweets_df2.shape[0])
st.write("Proportion of tweets mentioning CIA:", np.sum(cia) / tweets_df2.shape[0])
st.write("Proportion of tweets mentioning Trump:", np.sum(trump) / tweets_df2.shape[0])
st.write("Proportion of tweets mentioning Fraud:", np.sum(fraud) / tweets_df2.shape[0])
st.write("Proportion of tweets mentioning Election Fraud:", np.sum(election_fraud) / tweets_df2.shape[0])



words = pd.DataFrame([np.sum(cia), np.sum(trump), np.sum(fraud), np.sum(election_fraud)], ['cia', 'trump', 'fraud', 'election fraud'])
st.bar_chart(words)


# highest = 0

# for i,val in enumerate(tweets_df2['#Retweets']): 
#     if val > highest: 
#         highest = val 
#         st.write(highest, tweets_df2['Text'][i])
        
    
#Before CISA
st.subheader('Before CISA debunk')
Pre_start_date = tweets_df2['Date'][len(tweets_df2['Date'])-1]
#start_date = '2020-06-29 18:39:43+00:00'
Pre_end_date = '2020-11-07 16:29:01+00:00'
Pre_end_date = pd.to_datetime(Pre_end_date)

mask = (tweets_df2['Date'] >=Pre_start_date) & (tweets_df2['Date']<=Pre_end_date)
temp = tweets_df2.loc[mask]
index = temp.index
number_of_rows = len(index)
st.dataframe(tweets_df2[mask])
st.write('Total # of Tweets:', number_of_rows)


#After CISA
st.subheader('After CISA debunk')
Post_start_date = Pre_end_date
#start_date = '2020-06-29 18:39:43+00:00'
Post_end_date = tweets_df2['Date'][0]
Post_end_date = pd.to_datetime(Post_end_date)

mask2 = (tweets_df2['Date'] >=Post_start_date) & (tweets_df2['Date']<=Post_end_date)
temp2 = tweets_df2.loc[mask2]
index2 = temp2.index
number_of_rows2 = len(index2)
st.dataframe(tweets_df2[mask2])
st.write('Total # of Tweets:',number_of_rows2 )

st.subheader('Tweet Info Before Intervention')
# beforeCISA = pd.DataFrame(tweets_df2[mask]['#Retweets'].values, tweets_df2[mask]['Date'])
# #beforeCISA2 = pd.DataFrame(tweets_df2[mask]['#Likes'].values, tweets_df2[mask]['Date'])
# st.line_chart(beforeCISA)


#Likes = pd.DataFrame({'# of Likes':tweets_df2[mask]['#Likes'].values, '# of Retweets':tweets_df2[mask]['#Retweets'].values})
index = tweets_df2[mask]['Date']
beforeCISA = pd.DataFrame({'# of Likes':tweets_df2[mask]['#Likes'].values,'# of Replies':tweets_df2[mask]['#Replies'].values, '# of Retweets': tweets_df2[mask]['#Retweets'].values, '# of QuoteTweets': tweets_df2[mask]['#QuoteTweets'].values}, index = index)

st.line_chart(beforeCISA)

# temp = pd.DataFrame({'#Likes':tweets_df2['#Likes'], '#Retweets':tweets_df2['#Retweets'], '#QuoteTweets': tweets_df2['#QuoteTweets']})
# st.line_chart(temp)
#st.line_chart(tweets_df2['#Likes'])






# st.subheader('#Retweets Over Time After Intervention')
# afterCISA = pd.DataFrame(tweets_df2[mask2]['#Retweets'].values, tweets_df2[mask2]['Date'])
# st.line_chart(afterCISA)

st.subheader ('Tweet Info After Intervention')
index2 = tweets_df2[mask2]['Date']

afterCISA = pd.DataFrame(
    {'# of Likes':tweets_df2[mask2]['#Likes'].values,'# of Replies':tweets_df2[mask2]['#Replies'].values, '# of Retweets': tweets_df2[mask2]['#Retweets'].values, '# of QuoteTweets': tweets_df2[mask2]['#QuoteTweets'].values}
    , index = index2)
st.line_chart(afterCISA)









# Instantiate new SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Generate sentiment scores
sentiment_scores = tweets_df2['Text'].apply(sid.polarity_scores)
data_load_state = st.text('Loading data...')
sentiment = sentiment_scores.apply(lambda x: x['compound'])
tweets_df2['sentiment'] = sentiment

st.subheader('Positive Sentiment (aka > 0.6)')
positive = pd.DataFrame({ 
    'Date': tweets_df2[sentiment > 0.6]['Date'].values,
    'Text': tweets_df2[sentiment > 0.6]['Text'].values,
    'Sentiment': tweets_df2[sentiment>0.6]['sentiment'].values
})

#print(tweets_df2[sentiment > 0.6]['Date'])
st.dataframe(positive)


st.subheader('Negative Sentiment (aka < -0.6)')
negative = pd.DataFrame({ 
    'Date': tweets_df2[sentiment < -0.6]['Date'].values,
    'Text': tweets_df2[sentiment < -0.6]['Text'].values,
    'Sentiment': tweets_df2[sentiment < -0.6]['sentiment'].values
})
st.dataframe(negative)
# negative_woText = pd.DataFrame(tweets_df2[sentiment>0.6]['sentiment'].values, tweets_df2[sentiment > 0.6]['Date'].values )
# 
# st.line_chart(negative_woText)

sentimentOverTime = pd.DataFrame(tweets_df2['sentiment'].values, tweets_df2['Date'].values )

st.area_chart(sentimentOverTime)




# # Generate average sentiment scores for #javasrcipt
# sentiment_js = sentiment[ check_word_in_tweet('HammerAndScorecard', tweets_df2) ].resample('1 min').mean()



#tweets_df2.to_csv('hammerandscorecard.csv', index=False, encoding='utf-8')

# st.title('tracking Hammer and Scorecard ')


# DATA_URL = ('hammerandscorecard.csv')

# @st.cache
# def load_data(nrows):
#     data = pd.read_csv(DATA_URL, nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     return data

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load data into the dataframe.
# data = load_data(20)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)


