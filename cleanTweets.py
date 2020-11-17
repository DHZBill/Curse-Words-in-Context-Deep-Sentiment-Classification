import requests
import json
import csv
import string
import urllib
import re
import pandas as pd  
from hashtag_config import *  

stopwords = set(["RT"])

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
  return text

def tweetIsNotTooShort(text):
  return len(text.split(' '))>6

def tweetContainsCurseWord(text):
  text = text.split(' ')
  for word in text:
    for i in range(len(allCurseWords)):
      for curseword in allCurseWords[i]:
        if(curseword in word):
          return True
  return False

def keepNonAmbigousTweets(text):
  wordSentiment = -1
  text = text.split(' ')
  for word in text:
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


def findUniqueTweets(infile, outfile):
    twitter = pd.read_csv(infile)
    print("all: ", twitter.shape)
    #twitter = twitter[twitter["curseword"] != "a**"]
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

    twitter2.to_csv(outfile, index=False)
    print("unique: ", twitter2.shape)
