import requests
import json
import csv

#bearer tokens to access Tweets through API
kez_bearer = "AAAAAAAAAAAAAAAAAAAAAChUGwEAAAAA7ump2ucNmOaE89xv70KhDZqL1qQ%3DVPQSNjNv7BIlk6sO2a0FfU7Rqu75nqFBv08t4KnYk6kavtx2KT"
wen_bearer = "AAAAAAAAAAAAAAAAAAAAADAzIgEAAAAAa8jC33lX8w0w74HSYSN%2B7jBSmkc%3Delyo4dNtxVtexSCUNBEpbeDSmRv8lXlK1dbcyMEr5OTgvX9FGO"


kLimitPerCurseWord = 10000
kCountPerRequest = 100
allHashtags = ["sarcasm", "happy", "pissed", "angry", "sad", "annoying", "ugh", "funny", 
"motivation", "positive", "positivethinking", "anger", "excited", "exciting", "fun", 
"aggressive", "love", "lol", "hateyou", "loveyou", "pissedoff", "furious", "mad", 
"afraid", "petrified", "scared","anxious", "worried","joy", "yay","blessed", "thrilled",
"sadness", "depressed","disappointment", "disappointed", "unhappy","foreveralone", "godie", "pieceofshit", "irritated",
"fuming", "heated", "angrytweet", "frightened", "freakedout", "haunted", "greatmood", "thankful", "feelinggood", 
"superhappy", "ecstatic", "atlast", "heartbroken", "leftout"]


cursewords = set(["asshole", "bitch", "crap", "cunt", 
"damn", "fuck", "hell", "shit", "slut", "nigga", "prick", 
"nigger","dick","retard","tit","son of a bitch",
"queaf","spaz","motherfucker","doggie style",
"pissed","niglet","pussy","shart","cum","fucked up",
"wetback","fag","urine","hoe","ass",
"queer",
"rimming",
"chink",
"boner","arse",
"gay",
"shat",
"slut",
"crap",
"dyke",
"pimp",
"whore",
"hoe",
"cock",
"tramp",
"schlong",
"spunk",
"skank",
"gay",
"mothafucker",
"screw",
"blowjob"
])

def getTweets(bearer, params, curseword, hashtagIndex, writer): #deleted headers

  headers = {'Authorization': ('bearer '+bearer)}
  base_url = "https://api.twitter.com/1.1/search/tweets.json"
  uniqueTweets = set()
  while(len(uniqueTweets)<kLimitPerCurseWord):
    x = requests.get(base_url+params, headers = headers)
    res = json.loads(x.text)
    for tweet in res["statuses"]:
      if(tweet["full_text"] not in uniqueTweets):
       # print(tweet["full_text"])
        row = [0]*len(allHashtags)
        row[hashtagIndex] = 1
        writer.writerow([tweet["full_text"], curseword] + row)
        uniqueTweets.add(tweet["full_text"])
      
    if("next_results" not in res["search_metadata"]):
      break
    params = res["search_metadata"]["next_results"]
  print("#", allHashtags[hashtagIndex], curseword, "got", len(uniqueTweets), "tweets")



with open('trainng_data_twitter.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["text", "curseword"]+allHashtags)

    for hashtagIndex in range(0, len(allHashtags)):
        for curseword in cursewords:
          try:
            getTweets(kez_bearer, "?q=%23" + allHashtags[hashtagIndex] + "%20" + curseword +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtagIndex, writer)
          except Exception as e:
            print("An exception occurred at", hashtagIndex, allHashtags[hashtagIndex], curseword)
            print(e)

