import requests
import glob
import json
import csv
import string
import urllib
import re
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from hashtagConfig import *
from cleanTweets import *

YEAR = "2015"
MONTH = "03"
DAY = "15"
JSON_ROOT = "/Users/wenxindong/Downloads/2015S/**/*.json"
CSV_ROOT = "data_analysis/" + YEAR + "_" + MONTH + "_" + DAY + ".csv"

def json_to_csv(infile, writer):
    items = []
    with open(infile) as f:
        d = f.readlines()  # Twitter's JSON first line is bogus
        for tweet in d:
            try:
                j = json.loads(tweet)
                text = ""
                if "lang" not in j.keys() or j["lang"] != "en":
                    continue

                if "extended_tweet" in j.keys():
                    # print(j["extended_tweet"]["full_text"])
                    text = j["extended_tweet"]["full_text"]
                else:
                    text = j["text"]
                    # print(j["text"])
                if tweetContainsCurseWord(text):
                    writer.writerow([text])
            except:
                pass


def cleanArchiveTweets(infile, outfile):
    twitter = pd.read_csv(infile)
    print("all: ", twitter.shape)
    # twitter = twitter[twitter["curseword"] != "a**"]
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
    # twitter = twitter[twitter["text"].apply(keepNonAmbigousTweets) == True]
    # print("after dropping ambigious tweets: ", twitter.shape)

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

    twitter2.to_csv(outfile, index=False)
    print("unique: ", twitter2.shape)


with open(CSV_ROOT, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["text"])
    for filepath in glob.iglob(JSON_ROOT, recursive=True):
        print(filepath)
        json_to_csv(filepath, writer)

cleanArchiveTweets(CSV_ROOT, CSV_ROOT)
