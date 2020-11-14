import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from hashtag_config import *
import matplotlib.patches as mpatches


sentiment_2019 = {0: 0.6450699238803328, 1: 0.30967132825868887, 2: 0.1774650380598336}
curseword_2019 = {
    2: 34.11347051475906,
    0: 40.17487344684768,
    6: 6.311222141871014,
    3: 15.758332785484189,
    4: 2.677886617141104,
    5: 0.2585847960905485,
    7: 0.6070168518396775,
    1: 0.0986128459667346,
}
sentiment_2018 = {0: 0.609860312243221, 1: 0.32588331963845524, 2: 0.1950698438783895}
curseword_2018 = {
    0: 40.4882433647159,
    2: 35.825803094100394,
    3: 13.131002507451388,
    6: 6.450773525098169,
    4: 2.8977622179117186,
    7: 0.7616974972796517,
    5: 0.3240762643705351,
    1: 0.12064152907224299,
}
sentiment_2017 = {0: 0.6295197778197212, 1: 0.2690700245368997, 2: 0.1852401110901394}
curseword_2017 = {
    3: 13.615629751515277,
    2: 35.48561787923601,
    0: 38.907750307221264,
    6: 7.435795963425049,
    4: 3.2992439232675843,
    5: 0.327008393909729,
    1: 0.13538564079065213,
    7: 0.7935681406344379,
}
sentiment_2016 = {0: 0.6323514211886305, 1: 0.2544186046511628, 2: 0.18382428940568477}
curseword_2016 = {
    2: 34.43614931237721,
    6: 8.263261296660119,
    0: 40.286836935166995,
    7: 1.0255402750491158,
    4: 3.406679764243615,
    3: 12.157170923379175,
    5: 0.3693516699410609,
    1: 0.0550098231827112,
}
sentiment_2012 = {0: 0.4536700038148656, 1: 0.2312839600367052, 2: 0.2731649980925672}
curseword_2012 = {
    2: 34.44333051008591,
    3: 14.011373653915959,
    0: 38.07667709539695,
    4: 3.5451921248682003,
    5: 0.5211484279121221,
    6: 8.599381190258068,
    7: 0.6481945620797539,
    1: 0.15470243548303458,
}
sentiment_2011 = {0: 0.44035641358826805, 1: 0.2175607945052905, 2: 0.279821793205866}
curseword_2011 = {
    3: 14.190828969217014,
    0: 39.385617575680165,
    2: 34.097585898582196,
    6: 7.935240771490612,
    4: 3.113424447566739,
    5: 0.526887214203602,
    7: 0.6194916336696896,
    1: 0.13092348958998595,
}

#need 2013, 2014, 2015
sentimentByYear = [sentiment_2011,sentiment_2012,sentiment_2016,sentiment_2016,sentiment_2016,sentiment_2016,sentiment_2017,sentiment_2018,sentiment_2019]
cursewordByYear = [curseword_2011,curseword_2012,curseword_2016,curseword_2016,curseword_2016,curseword_2016,curseword_2017,curseword_2018,curseword_2019]

def plotCurseWordCounts(figname, filename):
    count = {}
    twitter = pd.read_csv(filename)
    for row in twitter.iterrows():
        for i in range(len(allCurseWords)):
            for word in allCurseWords[i]:
                if word in row[1]["text"]:
                    if word in count:
                        count[word] += 1
                    else:
                        count[word] = 1
    print(count)

    labels = []
    values = []
    color = []
    colorMap = ["red", "blue", "purple", "orange", "green", "gray", "pink", "salmon"]

    for i in range(len(allCurseWords)):
        for word in allCurseWords[i]:
            if word in count:
                labels.append(word)
                values.append(count[word])
                color.append(colorMap[i])

    plt.figure(figsize=(30, 10))
    plt.barh(range(len(values)), values, align="center", color=color)
    plt.yticks(range(len(values)), labels)
    plt.xlabel("count")
    plt.tight_layout()
    patches = []
    for i in range(len(allCurseWords)):
        patches.append(mpatches.Patch(color=colorMap[i], label=cursewordsCatg[i]))
        plt.legend(handles=patches)

    # plt.show()
    plt.savefig(figname, bbox_inches="tight")


#plot curseword category distribution by year
def multilineCurseword():
    x = np.linspace(2011, 2019, 9)
    lines = []
    for i in range(len(cursewordsCatg)):
        lines.append([categories[i] for categories in cursewordByYear])
    fig, ax = plt.subplots()
    plt.title("Category Distribution Across Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    for i in range(len(cursewordsCatg)):
        ax.plot(x, lines[i], label=cursewordsCatg[i])
    ax.legend()
    plt.show()

#plot sentiment distribution by year
def multilineSentiment():
    x = np.linspace(2011, 2019, 9)
    positive = [ sentiment[0] for sentiment in sentimentByYear]
    negative = [ sentiment[1] for sentiment in sentimentByYear]
    sarcastic =[ sentiment[2] for sentiment in sentimentByYear]
    fig, ax = plt.subplots()
    plt.title("Sentiment Distribution Across Time")
    plt.xlabel("Year")
    plt.ylabel("Percentage")
    ax.plot(x, positive, label='Positive')
    ax.plot(x, negative, label='Negative')
    ax.plot(x, sarcastic, label='Sarcastic')
    ax.legend()
    plt.show()
    
multilineSentiment()
multilineCurseword()