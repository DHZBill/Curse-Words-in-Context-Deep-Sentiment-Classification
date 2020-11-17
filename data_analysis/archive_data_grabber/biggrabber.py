import json
from pprint import pprint
import csv
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from zipfile import ZipFile
import os.path
from os import path
import bz2
import random
import cleaner

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

cursewordsCatg_revised = {
7: "general",
0: "race",
1: "gender-sexuality",
1:"religion",
3: "other-body-parts",
4: "ableist",
5: "problem-words",
6:"multiple-worded"}

allCurseWords_revised= [
  set(["nigger","n*gger", "n*gg*r", "chink","niglet", "wetback"]),
  set(["dick","di*k", "d*ck", "cunt","pussy","pu**y","fag","queer","qu**r", "boner","dong","slut","sl*t","dyke","pimp","whore","hoe","bitch","b*tch", "bi*ch","cock","tramp","cum","schlong","spunk","skank","motherfucker","tit","gay","mothafucker","screw","blowjob"]),
  set(["hell","damn"]),
  set(["ass", "queaf","shart","urine","rimming","arse","shat","crap"]),
  set(["retard","spaz"]),
  set(["tit","cum","hoe","chink","gay"]),
  set(["son of a bitch","doggie style","fucked up"]),
  set(["fuck","fu*k", "f*ck", "f**k", "sh*t","shit","pissed","screw"]) 
]


#dates to check 2018\01\00-23\00-59
#unzip file debug

#unzip files
'''
Files collected: (Y, M, D)
2018-09-01 
2012-01-01
'''

def clean_tweet(s):
    s = cleaner.remove_stopwords(s)
    s = cleaner.remove_URL(s)
    s = cleaner.remove_emoji(s)
    s = cleaner.remove_hashtags(s)
    return s

#data collection
count = 0
first_line = True
for h in range(00, 24):
    hour = ''
    if h < 10:
        hour = '0' + str(h)
    else:
        hour = str(h)
    for i in range(0,60):
        sec = ''
        if i < 10:
            sec = '0' + str(i)
        else:
            sec = str(i)
        fname = "/Users/kezialopez/Desktop/git_projects/CurseWordsInContext/overtime/06/" + hour + "/"+ sec + '.json.bz2'
        if path.exists(fname):
            with bz2.open(fname, 'rt') as f:
                #TODO: NEW LOCAL
                with open('2011-10-06.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    if first_line:
                        writer.writerow(["text", "curseword", "curseWordCatg", "date"])
                        first_line = False
                    for line in f:
                        data = json.loads(line)
                        #debugging
                        #if random.randint(0, 10) == 9:
                            #print(data)
                        if 'text' in data.keys() and 'user' in data.keys() and 'lang' in data['user'].keys() and data['user']['lang'] == 'en':
                            text = data["text"]
                        else:
                            continue
                        found = False
                        text = cleaner.remove_userids(text)
                        for cursewordCatg_revised, s in enumerate(allCurseWords_revised):
                            for w in s:
                                text = cleaner.to_lower(text)
                                if w in text and cleaner.tweetIsNotTooShort(text):
                                    # created_at entry format: 'Wed Sep 28 02:35:11 +0000 2011'
                                    date = data['created_at']
                                    date = date.split(' ')
                                    date = date[1] + date[5]
                                    text = clean_tweet(text)
                                    writer.writerow([text, w, cursewordCatg_revised, date]) #date is month-year (MonYYYY)
                                    count+=1
                                    found = True
                                if found:
                                    break
                            if found:
                                break
        print("file " + "2011/10/06/" + hour + "/"+ sec + " all done")
    print("at hour: " + hour + " there are " + str(count) + " tweets ")

#notes: tweets will have 'userid' and 'RT'

'''
#functions to apply to pandas
def sentiment_analysis(raw):
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(raw)
    return scores

#cleaning for csv using pandas

df = pd.read_csv('local-analysis-tweets.csv')
print(df.head())
print(df.shape)
df['lang']=df['text'].apply(get_lang)
print(df.head())

df_filtered = df[df['lang'] == 'eng'] 


#trouble words to check on:
#hello, 'ass'
#ignore repititions (just in case)

#words like n*gga are usually preceeded by "f*ck"

'''