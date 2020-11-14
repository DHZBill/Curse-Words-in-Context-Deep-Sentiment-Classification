import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from hashtagConfig import *  
from plots import *
import matplotlib.patches as mpatches

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/labeled')

for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    count_examples_by_category('analysis_data/labeled/' + file)

def count_examples_by_category(filename):
    df = pd.read_csv(filename)
    zero = len(df[(df["sentiment"] == 0)])
    one = len(df[(df["sentiment"] == 1)])
    two = len(df[(df["sentiment"] == 2)])
    total = zero+two+two
    zero = zero/total
    one = one/total
    two = two/total
    print("sentiment_"+filename[0:4], "=" , {0: zero, 1: one, 2: two})

def CurseWordCategoryDistribution(filename):
    count = {}
    twitter = pd.read_csv(filename)
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
    print("curseword_"+filename[0:4], "=",count)


catDist2011= {0: 37.20681995211032, 4: 8.481666330092606, 2: 32.73807806594928, 6: 7.1690274932925595, 3: 13.204281222052332, 5: 0.4904364884747425, 1: 0.14424602602198308, 7: 0.5654444220061737}
catDist2020 = {2: 24.44503878042257, 6: 5.4426317197111524, 0: 44.637603637336184, 4: 2.366943032896496, 3: 21.476330569671035, 7: 0.9494517250601765, 5: 0.5215298208077026, 1: 0.16047071409467772}
