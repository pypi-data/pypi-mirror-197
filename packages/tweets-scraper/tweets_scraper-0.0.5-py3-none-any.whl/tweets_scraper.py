# Scrape tweets from Twitter
# https://www.youtube.com/watch?v=PUMMCLrVn8A
# https://pypi.org/project/snscrape/

import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import warnings
warnings.filterwarnings("ignore")
def get_tweets(keyword,no_of_tweets = 200):
    keyword = "#"+keyword
    scraper = sntwitter.TwitterSearchScraper(keyword)
    n_tweets = no_of_tweets
    tweets = []
    for i, tweet in tqdm(enumerate(scraper.get_items()),total = n_tweets):
        data = [
            tweet.id,
            tweet.date,
            tweet.content,
            tweet.username,
            tweet.lang,
            tweet.likeCount,
            tweet.retweetCount
            
        ]
        tweets.append(data)
        if i>n_tweets:
            break
    df = pd.DataFrame(tweets)
    df.columns = ["Tweet_id","Tweet_date","Tweet","Username","Tweet_lang","Tweet_likeCount","Tweet_retweetCount"]
    df.to_csv(f"{keyword[1:]}.csv",index = False)
    return df
# data = get_tweets(keyword="bitcoin",no_of_tweets=400)
# print(data.shape)