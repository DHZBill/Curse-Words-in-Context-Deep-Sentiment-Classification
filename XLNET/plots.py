import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from hashtag_config import *
import matplotlib.patches as mpatches

sentiment_2017 = {0: 0.4931261207411835, 1: 0.39754646628525886, 2: 0.2534369396294083}
sentiment_2012 = {0: 0.3734812466983624, 1: 0.31509212242741785, 2: 0.3132593766508188}
sentiment_2019 = {0: 0.5269505291656411, 1: 0.4171486586266306, 2: 0.23652473541717942}
sentiment_2018 = {0: 0.5432692307692307, 1: 0.4269788182831661, 2: 0.2283653846153846}
sentiment_2013 = {0: 0.36210346654111, 1: 0.3881025248661056, 2: 0.318948266729445}
sentiment_2014 = {0: 0.4048573001917855, 1: 0.40012912291362057, 2: 0.2975713499041073}
sentiment_2016 = {0: 0.5416344987316642, 1: 0.3715672217933164, 2: 0.22918275063416785}
sentiment_2015 = {0: 0.46119307248236047, 1: 0.41409328324017225, 2: 0.26940346375881974}
sentiment_2011 = {0: 0.36297443841982957, 1: 0.2967467079783114, 2: 0.3185127807900852}
curseword_2017 = {3: 11.302337528898022, 2: 29.206267659902387, 6: 15.876359277335387, 0: 38.37486086137512, 4: 4.207552016439764, 5: 0.2688586351571196, 1: 0.11131089990581386, 7: 0.6524531209863859}
curseword_2012 = {2: 30.55602294455067, 6: 12.915487571701721, 3: 12.452772466539196, 0: 38.0, 4: 4.904015296367112, 5: 0.4611854684512428, 7: 0.5736137667304015, 1: 0.13690248565965582}
curseword_2019 = {2: 27.926184717369882, 0: 40.34578518319448, 6: 13.920988981456597, 3: 12.992923049359492, 4: 4.02579951625907, 5: 0.21141270267849144, 7: 0.49628236137239096, 1: 0.08062348830959419}
curseword_2018 = {0: 39.58993830090176, 2: 28.793545325106788, 3: 10.654010441385857, 4: 4.69672520170859, 6: 15.297579496915045, 7: 0.6112956810631229, 5: 0.26008542952064545, 1: 0.09682012339819648}
curseword_2013 = {3: 12.229279943086539, 0: 58.50398902383251, 2: 20.919762183037754, 4: 4.915900198180802, 6: 1.8710300320138218, 7: 0.9492352253671427, 5: 0.462421871030032, 1: 0.14838152345139488}
curseword_2014 = {3: 12.34558487113009, 0: 58.61420365004321, 2: 20.93945401860607, 4: 4.618473895582329, 6: 1.8440852015657567, 7: 1.16287936556352, 5: 0.3469574500533781, 1: 0.12836154745564538}
curseword_2016 = {2: 28.27024591219261, 6: 16.380198274752157, 0: 39.700012874983905, 7: 0.8400926998841252, 4: 4.374275782155272, 3: 10.087549890562636, 5: 0.30256212179734776, 1: 0.04506244367194541}
curseword_2015 = {3: 13.544375691268346, 0: 59.301109018623144, 2: 19.555794697037634, 4: 4.202911547544316, 6: 1.6590440319253879, 5: 0.34376588048904433, 1: 0.12256000956565928, 7: 1.2704391235464683}
curseword_2011 = {3: 12.648860156515822, 0: 39.47487807644323, 2: 30.350459339911534, 6: 12.101621866848134, 4: 4.290007939208348, 5: 0.4678462061925825, 7: 0.5500737212203698, 1: 0.11625269365997505}

#need 2013, 2014, 2015
sentimentByYear = [sentiment_2011,sentiment_2012,sentiment_2013,sentiment_2014,sentiment_2015,sentiment_2016,sentiment_2017,sentiment_2018,sentiment_2019]
cursewordByYear = [curseword_2011,curseword_2012,curseword_2013,curseword_2014,curseword_2015,curseword_2016,curseword_2017,curseword_2018,curseword_2019]

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
    plt.savefig("XLNET/plots/cat_line.png")
    #plt.show()

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
    ax.plot(x, positive, label='Empowering')
    ax.plot(x, negative, label='Upset')
    ax.plot(x, sarcastic, label='Sarcastic')
    ax.legend()
    plt.savefig("XLNET/plots/sent_line.png")
    #plt.show()

def plotSentimentBar():
    x = ['Empowering', 'Upset', 'Sarcastic']
    counts = [2701, 1013, 2720]
    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, counts, color = ['green', 'orange','blue'])
    plt.xlabel("Sentiment Label")
    plt.ylabel("Count")
    plt.title("Training Set Sentiment Class Distribution")

    plt.xticks(x_pos, x)
    plt.savefig("XLNET/plots/sent_bar.png")
    # plt.show()

# multilineSentiment()
# multilineCurseword()
# plotSentimentBar()