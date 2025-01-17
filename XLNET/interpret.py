# from plots import *
import os
import pandas as pd
from hashtag_config import *
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/labeled/cleaned/')

#Outputs sentiment class distribution for a given year
def count_examples_by_category(year, filename):
    df = pd.read_csv(filename, lineterminator='\n')
    zero = len(df[(df["sentiment"] == 0)])
    one = len(df[(df["sentiment"] == 1)])
    two = len(df[(df["sentiment"] == 2)])
    total = zero+two+two
    zero = zero/total
    one = one/total
    two = two/total
    print("sentiment_"+year, "=" , {0: zero, 1: one, 2: two})

#Outputs curseword category distribution for a given year
def CurseWordCategoryDistribution(year, filename):
    count = {}
    twitter = pd.read_csv(filename, lineterminator='\n')
    for row in twitter.iterrows():
        for i in range(len(allCurseWords)):
            for word in allCurseWords[i]:
                if(word in row[1]["text"]):
                    if i in count:
                        count[i] +=1
                    else:
                        count[i]  = 1
    total = 0
    for i in range(len(allCurseWords)):
        total += count[i]
    for i in range(len(allCurseWords)):
        count[i] = count[i]*100/total
    print("curseword_"+year, "=",count)

#Outputs sentiment class distribution per curse word category for a given year
def SentimentDistributionPerCurseWordCategory(year, filename):
    count = {}
    twitter = pd.read_csv(filename, lineterminator='\n')
    for row in twitter.iterrows():
        for i in range(len(allCurseWords)):
            for word in allCurseWords[i]:
                if(word in row[1]["text"]):
                    if i in count:
                        if row[1]["sentiment"] in count[i]:
                            count[i][row[1]["sentiment"]] +=1
                        else:
                            count[i][row[1]["sentiment"]] = 1

                    else:
                        count[i]  = {row[1]["sentiment"]: 1}
    
    for i in range(len(allCurseWords)):
        if 0 not in  count[i]:
             count[i][0] = 0
        if 1 not in count[i]:
             count[i][1] = 0
        if 2 not in count[i]:
             count[i][2] = 0
        total = count[i][0] + count[i][1] + count[i][2]
        count[i][1]/= total
        count[i][2]/= total
        count[i][0]/= total

    print("sentiment_per_category_"+year, "=",count)




for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    count_examples_by_category(file[8:12], 'XLNET/analysis_data/labeled/cleaned/' + file)
    
for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    CurseWordCategoryDistribution(file[8:12], 'XLNET/analysis_data/labeled/cleaned/' + file)

for file in os.listdir(dir_analysis_data):
    SentimentDistributionPerCurseWordCategory(file[8:12],'XLNET/analysis_data/labeled/cleaned/' + file)