import requests
import csv
import json

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

def get_tweets(event=None, context=None):
    url = 'https://archive.org/download/archiveteam-twitter-stream-2018-10/twitter-2018-10-01.tar/2018%2F10%2F01%2F00%2F29.json.bz2'
    r = requests.get(url, allow_redirects=True)
    open('test.json', 'wb').write(r.content)

    first_line = True
    with open('test.json') as f:
        with open('local-analysis-tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if first_line:
                writer.writerow(["text", "curseword", "curseWordCatg", "date"])
                first_line = False
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
                            print([text, w, cursewordCatg, date])
                        if found:
                            break
                    if found:
                        break