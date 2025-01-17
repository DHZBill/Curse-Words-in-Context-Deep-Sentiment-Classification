import json
import csv
import string
import urllib
import re

stopwords = set(["rt"])

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
