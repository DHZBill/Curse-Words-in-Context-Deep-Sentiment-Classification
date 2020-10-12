import requests
import json
import csv

kLimitPerCurseWord = 100
allHashtags = ["sarcasm", "happy", "pissed", "angry", "sad", "annoying", "ugh", "funny", "motivation", "positive", "positivethinking", "anger"]
cursewords = ["asshole", "bitch", "crap", "cunt", "damn", "fuck", "hell", "shit", "slut", "nigga", "prick"]

def getTweets(params, curseword, hashtagIndex, writer):
  headers = {'Authorization': 'bearer AAAAAAAAAAAAAAAAAAAAADAzIgEAAAAAa8jC33lX8w0w74HSYSN%2B7jBSmkc%3Delyo4dNtxVtexSCUNBEpbeDSmRv8lXlK1dbcyMEr5OTgvX9FGO'}
  base_url = "https://api.twitter.com/1.1/search/tweets.json"
  uniqueTweets = set()
  while(len(uniqueTweets)<kLimitPerCurseWord):
    x = requests.get(base_url+params, headers = headers)
    res = json.loads(x.text)
    for tweet in res["statuses"]:
      if(tweet["text"] not in uniqueTweets):
       # print(tweet["text"])
        row = [0]*len(allHashtags)
        row[hashtagIndex] = 1
        writer.writerow([tweet["text"], curseword] + row)
        uniqueTweets.add(tweet["text"])
      
    if("next_results" not in res["search_metadata"]):
      break
    params = res["search_metadata"]["next_results"]


with open('trainng_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["text", "curseword"]+allHashtags)

    for hashtagIndex in range(0, len(allHashtags)):
        for curseword in cursewords:
            getTweets("?q=%23" + allHashtags[hashtagIndex] + "%20" + curseword +"&lang=en", curseword, hashtagIndex, writer)