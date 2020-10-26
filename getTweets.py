import requests
import json
import csv
import string

import re
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

#bearer tokens to access Tweets through API
kez_bearer = "AAAAAAAAAAAAAAAAAAAAAChUGwEAAAAA7ump2ucNmOaE89xv70KhDZqL1qQ%3DVPQSNjNv7BIlk6sO2a0FfU7Rqu75nqFBv08t4KnYk6kavtx2KT"
wen_bearer = "AAAAAAAAAAAAAAAAAAAAADAzIgEAAAAAa8jC33lX8w0w74HSYSN%2B7jBSmkc%3Delyo4dNtxVtexSCUNBEpbeDSmRv8lXlK1dbcyMEr5OTgvX9FGO"

kLimitPerCurseWord = 10000
kCountPerRequest = 100
sentiments = {0: "positive", 1:"sad", 2:"angry", 3:"fear", 4:"sarcasm"}
cursewordsCatg = {
0: "general",
1: "race",
2: "gender-sexuality",
3:"religion",
4: "other-body-parts",
5: "ableist",
6: "problem-words",
7:"multiple-worded"}

allCurseWords= [
  set(["fuck","fu*k", "f*ck", "f**k", "sh*t","shit","pissed","screw"]), 
  set(["nigger","n*gger", "n*gg*r", "chink","niglet", "wetback"]),
  set(["dick","di*k", "d*ck", "cunt","pussy","pu**y","fag","queer","qu**r", "boner","dong","slut","sl*t","dyke","pimp","whore","hoe","bitch","b*tch", "bi*ch","cock","tramp","cum","schlong","spunk","skank","motherfucker","tit","gay","mothafucker","screw","blowjob"]),
  set(["hell","damn"]),
  set(["ass", "queaf","shart","urine","rimming","arse","shat","crap"]),
  set(["retard","spaz"]),
  set(["tit","cum","hoe","chink","gay"]),
  set(["son of a bitch","doggie style","fucked up"])
]

allHashtags = [
 set(["happy","funny","greatmood", "superhappy",  "atlast","ecstatic","thankful", "feelinggood", "love","loveyou","joy", "yay","blessed", "thrilled", "lol", "motivation", "positive", "positivethinking", "excited", "exciting", "fun"]),
  set(["sad","heartbroken", "leftout", "sadness", "depressed","disappointment", "disappointed", "unhappy","foreveralone"]),
  set(["pissed","angry", "pissedoff", "furious", "mad", "hateyou","annoying", "ugh","anger", "fuming", "heated", "angrytweet","aggressive", "godie", "pieceofshit", "irritated"]),
  set(["afraid", "petrified", "scared","anxious", "worried", "frightened", "freakedout", "haunted"]),
  set(["sarcasm"])
]

stopwords= set(["RT"])

def remove_stopwords(text):
    for stopword in stopwords:
       text = text.replace(stopword, '') 
    return text

def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub(r'',text)
def to_lower(text):
    return text.lower()
def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)
def remove_emoji(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
def remove_punct(text):
    table=str.maketrans('','',string.punctuation)
    return text.translate(table)
def remove_hashtags(text):
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())

def getTweets(bearer, params, curseword, hashtag, writer, sentiment, cursewordCatg): #deleted headers

  headers = {'Authorization': ('bearer '+bearer)}
  base_url = "https://api.twitter.com/1.1/search/tweets.json"
  uniqueTweets = set()
  while(len(uniqueTweets)<kLimitPerCurseWord):
    x = requests.get(base_url+params, headers = headers)
    res = json.loads(x.text)
    if(not res["statuses"]) :
      break
    for tweet in res["statuses"]:
      if(tweet["full_text"] not in uniqueTweets):
       # print(tweet["full_text"])
        writer.writerow([tweet["full_text"], sentiment, hashtag, curseword, cursewordCatg])
        uniqueTweets.add(tweet["full_text"])
      
    if("next_results" not in res["search_metadata"]):
      break
    params = res["search_metadata"]["next_results"]
  print("#", hashtag, curseword, "got", len(uniqueTweets), "tweets")


def runTweetsScraper():
  with open('well_formatted.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      #writer.writerow(["text", "curseword"]+allHashtags)
      for sentiment, hashtagSet in enumerate(allHashtags):
        for hashtag in hashtagSet:
          for cursewordCatg, cursewordSet in enumerate(allCurseWords):
            for curseword in cursewordSet:
              try:
                getTweets(kez_bearer, "?q=%23" + hashtag + "%20" + curseword +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtag, writer, sentiment, cursewordCatg)
              except Exception as e:
                print("An exception occurred at", hashtag, curseword)
                print(e)

def findUniqueTweets():
    twitter = pd.read_csv('./well_formatted.csv')
    twitter['text'] = twitter['text'].apply(lambda x : remove_hashtags(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_URL(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_html(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_emoji(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_punct(x))
    twitter['text'] = twitter['text'].apply(lambda x : to_lower(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_stopwords(x))

    twitter2 = twitter.sort_values(["text"])
    twitter2.drop_duplicates(subset= ["text"], inplace=True)

    print("all: ", twitter.shape)
    twitter2.to_csv("unique_tweets.csv", index=False)
    print("unique: ",twitter2.shape)

def extractLinesWithCurseWords():
  file1 = open('tweets_clean.csv', 'r') 
  Lines = file1.readlines() 
  #curse_words = ' ' + ' | '.join(allCurseWords[0]) + ' '
  count = 0
  # Strips the newline character 
  for line in Lines:
    for j in range(len(allCurseWords)):
      if any(x in line for x in allCurseWords[j]): 
        print("Line{}: {}".format(count, line.strip()))
        count +=1


runTweetsScraper()
findUniqueTweets()