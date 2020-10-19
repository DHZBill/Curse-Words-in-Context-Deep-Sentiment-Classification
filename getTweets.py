import requests
import json
import csv
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
  set(["fuck","shit","pissed","screw"]), 
  set(["nigger","chink","niglet", "wetback"]),
  set(["dick","cunt","pussy","fag","queer","boner","dong","slut","dyke","pimp","whore","hoe","bitch","cock","tramp","cum","schlong","spunk","skank","motherfucker","tit","gay","mothafucker","screw","blowjob"]),
  set(["hell","damn"]),
  set(["ass","queaf","shart","urine","rimming","arse","shat","crap"]),
  set(["retard","spaz"]),
  set(["tit","motherfucker","cum","hoe","chink","gay"]),
  set(["son of a bitch","doggie style","fucked up","ass"])
]

allHashtags = [
 set(["happy","funny","greatmood", "superhappy",  "atlast","ecstatic","thankful", "feelinggood", "love","loveyou","joy", "yay","blessed", "thrilled", "lol", "motivation", "positive", "positivethinking", "excited", "exciting", "fun"]),
  set(["sad","heartbroken", "leftout", "sadness", "depressed","disappointment", "disappointed", "unhappy","foreveralone"]),
  set(["pissed","angry", "pissedoff", "furious", "mad", "hateyou","annoying", "ugh","anger", "fuming", "heated", "angrytweet","aggressive", "godie", "pieceofshit", "irritated"]),
  set(["afraid", "petrified", "scared","anxious", "worried", "frightened", "freakedout", "haunted"]),
  set(["sarcasm"])
]

#helper function
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
                getTweets(wen_bearer, "?q=%23" + hashtag + "%20" + curseword +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtag, writer, sentiment, cursewordCatg)
              except Exception as e:
                print("An exception occurred at", hashtag, curseword)
                print(e)

def findNumUniqueTweets():
    twitter = pd.read_csv('./well_formatted.csv')
    print("all", twitter.shape)
    firstrow = 0
    uniqueSet = set()
    for row in twitter.iterrows():
      if(firstrow == 0) :
        firstrow = row
        continue
      text = row[1][0]
      #print(text)
      uniqueSet.add(text)
    print("unique ones", len(uniqueSet))


findNumUniqueTweets()


