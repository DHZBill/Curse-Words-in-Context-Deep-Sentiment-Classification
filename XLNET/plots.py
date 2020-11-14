import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from hashtagConfig import *  
import matplotlib.patches as mpatches


def plotCurseWordCounts(figname, filename):
    count = {}
    twitter = pd.read_csv(filename)
    for row in twitter.iterrows():
        for i in range(len(allCurseWords)):
            for word in allCurseWords[i]:
                if(word in row[1]["text"]):
                    if word in count:
                        count[word] +=1
                    else:
                        count[word]  = 1
    print(count)

    labels = []
    values =[]
    color = []
    colorMap = ["red", "blue", "purple", "orange", "green", "gray", "pink", "salmon"]

    for i in range(len(allCurseWords)):
        for word in allCurseWords[i]:
            if(word in count):
                labels.append(word)
                values.append(count[word])
                color.append(colorMap[i])
            

    plt.figure(figsize=(30,10))
    plt.barh(range(len(values)), values, align='center', color = color)
    plt.yticks(range(len(values)), labels)
    plt.xlabel("count")
    plt.tight_layout()
    patches = []
    for i in range(len(allCurseWords)):
        patches.append(mpatches.Patch(color=colorMap[i], label=cursewordsCatg[i]))
        plt.legend(handles=patches)

    #plt.show()
    plt.savefig(figname, bbox_inches='tight')

def multilineSentiment():
    x = np.linspace(2011, 2020, 8)
    y = [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.8 ]
    z = [ 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.8, 0.1]
    k = [ 0.3, 0.4, 0.3, 0.2, 0.1, 0.8, 0.1, 0.2]

    fig, ax = plt.subplots()
    plt.title('Sentiment Distribution Across Time')
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.legend(['Positive','Negative', 'Sarcastic'])
    ax.plot(x,y)
    ax.plot(x,z)
    ax.plot(x,k)
    plt.show()