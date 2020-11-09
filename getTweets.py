import requests
import json
import csv
import string
import urllib
import re
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from hashtagConfig import *  
from cleanTweets import *

# bearer tokens to access Tweets through API
kez_bearer = "AAAAAAAAAAAAAAAAAAAAAChUGwEAAAAA7ump2ucNmOaE89xv70KhDZqL1qQ%3DVPQSNjNv7BIlk6sO2a0FfU7Rqu75nqFBv08t4KnYk6kavtx2KT"
wen_bearer = "AAAAAAAAAAAAAAAAAAAAADAzIgEAAAAAJPxcIOtIqGIiZ5ARrz59FVuD4GA%3DeDvmoV2QIWj7XqvxDHqQJqDUsYzJT8yTcW80t4ZfWStPCYAJTT"

kLimitPerCurseWord = 10000
kCountPerRequest = 100

def getTweets(
    bearer, params, curseword, hashtag, writer, sentiment, cursewordCatg
):  # deleted headers
    print("getting Tweets: ", curseword, hashtag, sentiment)
    headers = {"Authorization": ("bearer " + bearer)}
    base_url = "https://api.twitter.com/1.1/search/tweets.json"
    uniqueTweets = set()
    while len(uniqueTweets) < kLimitPerCurseWord:
        x = requests.get(base_url + params, headers=headers)
        res = json.loads(x.text)
        if "statuses" not in res:
            break
        for tweet in res["statuses"]:
            if tweet["full_text"] not in uniqueTweets:
                print(curseword, hashtag, tweet["full_text"])
                writer.writerow([tweet["full_text"], sentiment, hashtag, curseword, cursewordCatg])
                uniqueTweets.add(tweet["full_text"])
        if "next_results" not in res["search_metadata"]:
            break
        params = res["search_metadata"]["next_results"]
    print("#", hashtag, curseword, "got", len(uniqueTweets), "tweets")

def runTweetsScraper():
    with open("training_data/well_formatted.csv", "a", newline="") as file:
        writer = csv.writer(file)
        for sentiment, hashtagSet in enumerate(allHashtags):
            for hashtag in hashtagSet:
                for cursewordCatg, cursewordSet in enumerate(allCurseWords):
                    for curseword in cursewordSet:
                        try:
                            getTweets(
                                wen_bearer,
                                "?q=%23"
                                + hashtag
                                + "%20"
                                + curseword
                                + "&lang=en&tweet_mode=extended&count="
                                + str(kCountPerRequest),
                                curseword,
                                hashtag,
                                writer,
                                sentiment,
                                cursewordCatg,
                            )
                            # getTweets(kez_bearer, "?q=%23" + hashtag_urlencoded + "%20" + curseword_urlencoded +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtag, writer, sentiment, cursewordCatg)
                        except Exception as e:
                            print("An exception occurred at", hashtag, curseword)
                            print(e)


def findUniqueTweets():
    twitter = pd.read_csv("training_data/well_formatted.csv")
    print("all: ", twitter.shape)
    twitter = twitter[twitter["curseword"] != "a**"]
    twitter.drop_duplicates(subset=["text"], inplace=True)
    print("after dropping duplicates: ", twitter.shape)

    # step 0: convert everything to lower case, remove stop words
    twitter["text"] = twitter["text"].apply(lambda x: to_lower(x))
    twitter["text"] = twitter["text"].apply(lambda x: remove_stopwords(x))

    # step 1: replace @USERID with USERID
    twitter["text"] = twitter["text"].apply(lambda x: remove_userids(x))
    # step 2: replace links with URL
    twitter["text"] = twitter["text"].apply(lambda x: remove_URL(x))
    twitter["text"] = twitter["text"].apply(lambda x: remove_html(x))
    # step 3: replace "happyyyyy" with happy, ":))))" with ":)"
    twitter["text"] = twitter["text"].apply(lambda x: remove_repeatCharacters(x))
    # step 4: remove tweets containing 0, or more than one sentiment labels eg. #happy and #sad,  :) and :(, #happy and :(
    twitter = twitter[twitter["text"].apply(keepNonAmbigousTweets) == True]
    print("after dropping ambigious tweets: ", twitter.shape)

    # step 5: remove hashtags from the end of the text
    twitter["text"] = twitter["text"].apply(lambda x: remove_hashtags(x))

    # step 6: remove tweets that don't contain curseword
    twitter = twitter[twitter["text"].apply(tweetContainsCurseWord) == True]
    print("after dropping tweets without cursewords: ", twitter.shape)

    # step 7: remove emojis, punctuation
    twitter["text"] = twitter["text"].apply(lambda x: remove_emoji(x))
    twitter["text"] = twitter["text"].apply(lambda x: remove_punct(x))

    # step 8: remove tweets that are less than 6 words long
    twitter = twitter[twitter["text"].apply(tweetIsNotTooShort) == True]
    print("after dropping short tweets: ", twitter.shape)

    twitter2 = twitter.sort_values(["text"])
    twitter2.drop_duplicates(subset=["text"], inplace=True)
    print("after dropping duplicates: ", twitter2.shape)

    twitter2.to_csv("training_data/unique_tweets.csv", index=False)
    print("unique: ", twitter2.shape)


def countExamplesByCategory(filename):
    df = pd.read_csv(filename)
    print("positive", len(df[(df["sentiment"] == 0)]))
    print("angry", len(df[(df["sentiment"] == 2)]))
    print("fear", len(df[(df["sentiment"] == 3)]))
    print("sarcasm", len(df[(df["sentiment"] == 4)]))
    print("sad", len(df[(df["sentiment"] == 1)]))


#run the following three lines to get more tweets, and clean them
runTweetsScraper()
findUniqueTweets()
countExamplesByCategory("training_data/unique_tweets.csv")
