def extractLinesWithCurseWordsTXT(filename, sentiment = -1, hashtag = ""):
  with open('testset2.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      file1 = open(filename, 'r') 
      Lines = file1.readlines() 
      count = 0
      # Strips the newline character 
      for line in Lines:
        line = line.split('\t')
        #print(line)
        word = re.compile('[^a-zA-Z]').sub("", line[2])
        if(word in sentimentToNumber):
          sentiment = sentimentToNumber[word]
          line = line[1]
          for j in range(len(allCurseWords)):
            if any(x in line for x in allCurseWords[j]):
              #line = line.split('\t')
              #print(line)
              #if(float(line[3].strip())>0.65):
                #print("Line{}: {}".format(count, line), word, sentiment)
                writer.writerow([line, sentiment, word, "UNDEFINED", "UNDEFINED"])
                count +=1
              
def extractLinesWithEmojiesCSV():
  with open('well_formatted.csv', 'a', newline='') as file:
      writer = csv.writer(file)
      file1 = pd.read_csv('text_emotion.csv') 
      count = 0
      # Strips the newline character 
      for line in file1.iterrows():
        try:
          comment = line[1]["content"]
          for j in range(len(allCurseWords)):
            if any(x in comment for x in allCurseWords[j]) :
              # for k in range(len(allEmojis)):
              #   if any(x in comment for x in allEmojis[k]):
              if(line[1]["sentiment"] in sentimentMap):

                sentimentLabel = sentimentMap[line[1]["sentiment"]]                
                print(line[1]["sentiment"],sentimentLabel,  "Line{}: {}".format(count, comment))

                #writer.writerow([comment, sentimentLabel, "UNDEFINED", "UNDEFINED", "UNDEFINED"])
                count +=1
        except Exception as e: 
          pass
          #print("ignore this idea")

def extractLinesWithCurseWordsCSV():
  with open('testset.csv', 'w', newline='') as file:
      writer = csv.writer(file)
      file1 = pd.read_csv('sarcasm.csv') 
      count = 0
      # Strips the newline character 
      for line in file1.itertuples():
        try:
          if(count>5300):
            continue
          #print(line[6])
          comment = line.comment
          if(line.label!=1):
            continue
          for j in range(len(allCurseWords)):
            if any(x in comment for x in allCurseWords[j]) :
              if(len(comment)<50):
                continue
              count +=1
              if(count>5000):
                print("Line{}: {}".format(count, comment))
                writer.writerow([comment, 4, "UNDEFINED", "UNDEFINED", j])
              
        except Exception as e: 
          print("ignore this idea") 
