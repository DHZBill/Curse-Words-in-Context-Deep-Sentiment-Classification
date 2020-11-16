# from plots import *
import os
import pandas as pd
from hashtag_config import *
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/labeled/cleaned/')

def count_examples_by_category(year, filename):
    df = pd.read_csv(filename, lineterminator='\n')
    # print(df.keys())
    # print(df.head(2))
    zero = len(df[(df["sentiment"] == 0)])
    one = len(df[(df["sentiment"] == 1)])
    two = len(df[(df["sentiment"] == 2)])
    # print(zero, one, two)
    total = zero+two+two
    zero = zero/total
    one = one/total
    two = two/total
    print("sentiment_"+year, "=" , {0: zero, 1: one, 2: two})

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



for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    count_examples_by_category(file[8:12], 'XLNET/analysis_data/labeled/cleaned/' + file)
    
for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    CurseWordCategoryDistribution(file[8:12], 'XLNET/analysis_data/labeled/cleaned/' + file)

