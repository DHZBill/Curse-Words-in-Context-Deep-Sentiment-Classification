import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

allHashtags0 = ["sarcasm", "happy", "pissed", "angry", "sad", "annoying", "ugh", "funny", 
"motivation", "positive", "positivethinking", "anger", "excited", "exciting", "fun", 
"aggressive", "love", "lol", "hateyou", "loveyou", "pissedoff", "furious", "mad", 
"afraid", "petrified", "scared","anxious", "worried","joy", "yay","blessed", "thrilled",
"sadness", "depressed","disappointment", "disappointed", "unhappy","foreveralone", "godie", "pieceofshit", "irritated",
"fuming", "heated", "angrytweet", "frightened", "freakedout", "haunted", "greatmood", "thankful", "feelinggood", 
"superhappy", "ecstatic", "atlast", "heartbroken", "leftout"]

def preprocessTrainingData():
    twitter = pd.read_csv('./trainng_data_twitter.csv')
    #print(twitter.head(3))
    #print(twitter.shape)
    with open('training_data_twitter.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(["text", "sentiment","hashtag", "curseword", "cursewordCatg"])
      firstrow = 0
      for row in twitter.iterrows():
        if(firstrow == 0) :
          firstrow = row
          continue
        text = row[1][0]
        curseword = row[1][1]
        curwordCat = "NO CATEGORY"
        for i in range(0, 8):
          if (curseword in allCurseWords[i]):
            curwordCat = i
            break

        sentiment = "NO SENTIMENT"
        hashtag = "NO HASHTAG"
        for i in range(2, len(row[1])):
          #print(row[1][i])
          if(row[1][i]==1): #found sentiment
            hashtag = allHashtags0[i-2]
            for j in range(5):
              if(hashtag in allHashtags[j]):
                sentiment = j
                break
            break
        writer.writerow([text, sentiment, hashtag, curseword, curwordCat])
            

#preprocessTrainingData()