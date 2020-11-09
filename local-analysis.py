import json
from pprint import pprint
import csv
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob



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
'''
first_line = True
for i in range(0,60):
    num = ''
    if i < 10:
        num = '0' + str(i)
    else:
        num = str(i)
    with open(num + '.json') as f:
        with open('local-analysis-tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            #if first_line:
                #writer.writerow(["text", "curseword", "curseWordCatg", "date"])
                #first_line = False
            for line in f:
                data = json.loads(line)
                if 'text' in data.keys():
                    text = data["text"]
                else:
                    continue
                found = False
                for cursewordCatg, s in enumerate(allCurseWords):
                    for w in s:
                        if w in text:
                            # created_at entry format: 'Wed Sep 28 02:35:11 +0000 2011'
                            date = data['created_at']
                            date = date.split(' ')
                            date = date[1] + date[5]
                            writer.writerow([text, w, cursewordCatg, date]) #date is month-year (MonYYYY)
                            found = True
                        if found:
                            break
                    if found:
                        break
'''
#functions to apply to pandas
def sentiment_analysis(raw):
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    nltk.download('vader_lexicon')
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(raw)
    return scores

def get_lang(text):
    b = TextBlob(text)
    return b.detect_language()

#cleaning for csv using pandas
df = pd.read_csv('local-analysis-tweets.csv')
print(df.head())
print(df.shape)
df['lang']=df['text'].apply(get_lang)
print(df.head())

df_filtered = df[df['lang'] == 'eng'] 





'''
trouble words to check on:
hello, 'ass'
ignore other languages
ignore repititions (just in case)
'''