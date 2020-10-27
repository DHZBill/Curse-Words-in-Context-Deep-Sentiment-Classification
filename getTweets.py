import requests
import json
import csv
import string
import urllib
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


allEmojis = [
  set([" ;) ", ":)))", " =) ", " :] ", " :P ", " :-P ", " :D ", " ;D ", ":>", ":3 ",  ";-)", ":-D"]),
  set([" :( ", " :(((", " =(((", " =( ", ":-(", ":^(", ":'(", ":-<" ]),
  set([" >:S ", " >:{ ", " >: ", " x-@"  , " :@ ", ":-@ ", " :-/ ", ":/ "]),
  set([" :-o ", " :$ ", " :-O ", " o_O ", " O_o ", " :‑O ", " :O ", " :‑o ", " :o ", " :-0 ", " 8‑0 ",">:O",  " :-l ", " ,:-| "]),
]

stopwords= set(["RT"])

def remove_stopwords(text):
    for stopword in stopwords:
       text = text.replace(stopword, '') 
    text = text.replace('"', '') 
    return text

def remove_URL(text):
    url = re.compile(r'https?://\S+|www\.\S+')
    return url.sub("URL",text)
def to_lower(text):
    return text.lower()
def remove_html(text):
    html=re.compile(r'<.*?>')
    return html.sub(r'',text)
def remove_repeatCharacters(text):
   return re.sub(r'(.)\1{2,}',r'\1', text)
def remove_hashtags(text):
  array = text.split(' ')
  isPreviousHashtag = False
  previousWord = ""
  isLast = True
  #print("before", array[::-1])
  for word in array[::-1]:
    if(len(word)<1 or word == 'URL' or word == 'USERID'):
      continue

    if(word[0] == '#'):
      
      if(isPreviousHashtag):
        text = text.replace(word, "")
        text = text.replace(previousWord, "")
      if(isLast):
        text = text.replace(word, "")
        isLast = False
      previousWord = word
      isPreviousHashtag = True
      
    else:
      isPreviousHashtag = False
  #print("after", text)
  return text
#  return re.sub("(?:\\s*#\\w+)+\\s*$", "", text)

def tweetIsNotTooShort(text):
  return len(text.split(' '))>5
def tweetContainsCurseWord(text):
  text = text.split(' ')
  for word in text:
    for i in range(len(allCurseWords)):
      if( word in allCurseWords[i]):
        return True
  return False
def keepNonAmbigousTweets(text):
  wordSentiment = -1
  text = text.split(' ')
  for word in text:
    #print(word)
    #word could be #hashtag, :), or hello
    for i in range(len(allEmojis)):
      if( word in allEmojis[i]):
        if(wordSentiment==-1):
          wordSentiment = i
        elif(wordSentiment!=i):
          return False
    for i in range(len(allHashtags)):
      if( word[1:] in allHashtags[i]):
        if(wordSentiment==-1):
          wordSentiment = i
        elif(wordSentiment!=i):
          return False
  if (wordSentiment == -1):
    return False
  return True
          
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
def remove_userids(text):
    text = text.split(' ')
    res = ""
    for piece in text:
      if len(piece)>=1 and piece[0] != '@':
        res+= piece + " "
      else:
        res+= " USERID "
   
    return res

def getTweets(bearer, params, curseword, hashtag, writer, sentiment, cursewordCatg): #deleted headers
  
  headers = {'Authorization': ('bearer '+bearer)}
  base_url = "https://api.twitter.com/1.1/search/tweets.json"
  uniqueTweets = set()
  while(len(uniqueTweets)<kLimitPerCurseWord):
    x = requests.get(base_url+params, headers = headers)
    res = json.loads(x.text)
    if("statuses" not in res) :
      break
    for tweet in res["statuses"]:
      if(tweet["full_text"] not in uniqueTweets):
        print(curseword, hashtag, tweet["full_text"])
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
              hashtag_urlencoded = urllib.parse.quote_plus(hashtag)
              curseword_urlencoded = urllib.parse.quote_plus(curseword)
              try:
                getTweets(kez_bearer, "?q=%23" + hashtag + "%20" + curseword +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtag, writer, sentiment, cursewordCatg)
                #getTweets(kez_bearer, "?q=%23" + hashtag_urlencoded + "%20" + curseword_urlencoded +"&lang=en&tweet_mode=extended&count="+str(kCountPerRequest), curseword, hashtag, writer, sentiment, cursewordCatg)
              except Exception as e:
                print("An exception occurred at", hashtag, curseword)
                print(e)

def findUniqueTweets():
    twitter = pd.read_csv('./well_formatted.csv')
    print("all: ", twitter.shape)
    twitter = twitter[twitter['curseword'] != "a**" ]
    twitter.drop_duplicates(subset= ["text"], inplace=True)
    print("after dropping duplicates: ", twitter.shape)

    #step 0: convert everything to lower case, remove stop words
    twitter['text'] = twitter['text'].apply(lambda x : to_lower(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_stopwords(x))

    #step 1: replace @USERID with USERID
    twitter['text'] = twitter['text'].apply(lambda x : remove_userids(x))
    #step 2: replace links with URL
    twitter['text'] = twitter['text'].apply(lambda x : remove_URL(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_html(x))
    #step 3: replace "happyyyyy" with happy, ":))))" with ":)"
    twitter['text'] = twitter['text'].apply(lambda x : remove_repeatCharacters(x))
    #step 4: remove tweets containing 0, or more than one sentiment labels eg. #happy and #sad,  :) and :(, #happy and :(
    twitter = twitter[twitter['text'].apply(keepNonAmbigousTweets) == True]
    print("after dropping ambigious tweets: ", twitter.shape)

    #step 5: remove hashtags from the end of the text
    twitter['text'] = twitter['text'].apply(lambda x : remove_hashtags(x))

    #step 6: remove tweets that don't contain curseword
    twitter = twitter[twitter['text'].apply(tweetContainsCurseWord) == True]
    print("after dropping tweets without cursewords: ", twitter.shape)

    #step 7: remove tweets that are less than 6 words long
    twitter = twitter[twitter['text'].apply(tweetIsNotTooShort) == True]
    print("after dropping short tweets: ", twitter.shape)

    #step 8: remove emojis, punctuation
    twitter['text'] = twitter['text'].apply(lambda x : remove_emoji(x))
    twitter['text'] = twitter['text'].apply(lambda x : remove_punct(x))
    
    twitter2 = twitter.sort_values(["text"])
    twitter2.drop_duplicates(subset= ["text"], inplace=True)
    print("after dropping duplicates: ", twitter2.shape)

    twitter2.to_csv("unique_tweets.csv", index=False)
    print("unique: ",twitter2.shape)

def extractLinesWithCurseWordsTXT(filename, sentiment, hashtag):
  with open('well_formatted.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      file1 = open(filename, 'r') 
      Lines = file1.readlines() 
      count = 0
      # Strips the newline character 
      for line in Lines:
        for j in range(len(allCurseWords)):
          if any(x in line for x in allCurseWords[j]):
            line = line.split('\t')
            if(float(line[3].strip())>0.65):
              print("Line{}: {}".format(count, line[1]))
              writer.writerow([line[1] + " "+ hashtag, sentiment, "UNDEFINED", "UNDEFINED", "UNDEFINED"])
              count +=1
              
def extractLinesWithEmojiesCSV():
  with open('well_formatted.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      file1 = pd.read_csv('1billion.csv') 
      count = 0
      # Strips the newline character 
      for line in file1.itertuples():
        try:
          #print(line[6])
          comment = line[6]
          for j in range(len(allCurseWords)):
            if any(x in comment for x in allCurseWords[j]) :
              for k in range(len(allEmojis)):
                if any(x in comment for x in allEmojis[k]):
                  print(k, "Line{}: {}".format(count, comment))
                  writer.writerow([comment, k, "UNDEFINED", "UNDEFINED", "UNDEFINED"])
                  count +=1
        except Exception as e: 
          print("ignore this idea")

def extractLinesWithCurseWordsCSV():
  with open('well_formatted.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      file1 = pd.read_csv('sarcasm.csv') 
      count = 0
      # Strips the newline character 
      for line in file1.itertuples():
        try:
          if(count>5000):
            break
          #print(line[6])
          comment = line.comment
          if(line.label!=1):
            continue
          for j in range(len(allCurseWords)):
            if any(x in comment for x in allCurseWords[j]) :
              print("Line{}: {}".format(count, comment))
              writer.writerow([comment + " #sarcasm ", 4, "UNDEFINED", "UNDEFINED", j])
              count +=1
        except Exception as e: 
          print("ignore this idea") 

def countExamplesByCategory():
  df = pd.read_csv('./unique_tweets.csv')
  print("positive", len(df[(df['sentiment']==0)]))
  print("angry", len(df[(df['sentiment']==2)]))
  print("fear", len(df[(df['sentiment']==3)]))
  print("sarcasm", len(df[(df['sentiment']==4)]))
  print("sad", len(df[(df['sentiment']==1)]))

#runTweetsScraper()
#extractLinesWithCurseWordsCSV()

findUniqueTweets()
countExamplesByCategory()
#print(remove_hashtags("I #find it #funny hello #sarcasm #hello#hello"))