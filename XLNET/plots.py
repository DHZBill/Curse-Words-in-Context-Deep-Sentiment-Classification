import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from hashtag_config import *
import matplotlib.patches as mpatches

# sentiment_2017 = {0: 0.4931261207411835, 1: 0.39754646628525886, 2: 0.2534369396294083}
# sentiment_2012 = {0: 0.3734812466983624, 1: 0.31509212242741785, 2: 0.3132593766508188}
# sentiment_2019 = {0: 0.5269505291656411, 1: 0.4171486586266306, 2: 0.23652473541717942}
# sentiment_2018 = {0: 0.5432692307692307, 1: 0.4269788182831661, 2: 0.2283653846153846}
# sentiment_2013 = {0: 0.36210346654111, 1: 0.3881025248661056, 2: 0.318948266729445}
# sentiment_2014 = {0: 0.4048573001917855, 1: 0.40012912291362057, 2: 0.2975713499041073}
# sentiment_2016 = {0: 0.5416344987316642, 1: 0.3715672217933164, 2: 0.22918275063416785}
# sentiment_2015 = {0: 0.46119307248236047, 1: 0.41409328324017225, 2: 0.26940346375881974}
# sentiment_2011 = {0: 0.36297443841982957, 1: 0.2967467079783114, 2: 0.3185127807900852}
# curseword_2017 = {3: 11.302337528898022, 2: 29.206267659902387, 6: 15.876359277335387, 0: 38.37486086137512, 4: 4.207552016439764, 5: 0.2688586351571196, 1: 0.11131089990581386, 7: 0.6524531209863859}
# curseword_2012 = {2: 30.55602294455067, 6: 12.915487571701721, 3: 12.452772466539196, 0: 38.0, 4: 4.904015296367112, 5: 0.4611854684512428, 7: 0.5736137667304015, 1: 0.13690248565965582}
# curseword_2019 = {2: 27.926184717369882, 0: 40.34578518319448, 6: 13.920988981456597, 3: 12.992923049359492, 4: 4.02579951625907, 5: 0.21141270267849144, 7: 0.49628236137239096, 1: 0.08062348830959419}
# curseword_2018 = {0: 39.58993830090176, 2: 28.793545325106788, 3: 10.654010441385857, 4: 4.69672520170859, 6: 15.297579496915045, 7: 0.6112956810631229, 5: 0.26008542952064545, 1: 0.09682012339819648}
# curseword_2013 = {3: 12.229279943086539, 0: 58.50398902383251, 2: 20.919762183037754, 4: 4.915900198180802, 6: 1.8710300320138218, 7: 0.9492352253671427, 5: 0.462421871030032, 1: 0.14838152345139488}
# curseword_2014 = {3: 12.34558487113009, 0: 58.61420365004321, 2: 20.93945401860607, 4: 4.618473895582329, 6: 1.8440852015657567, 7: 1.16287936556352, 5: 0.3469574500533781, 1: 0.12836154745564538}
# curseword_2016 = {2: 28.27024591219261, 6: 16.380198274752157, 0: 39.700012874983905, 7: 0.8400926998841252, 4: 4.374275782155272, 3: 10.087549890562636, 5: 0.30256212179734776, 1: 0.04506244367194541}
# curseword_2015 = {3: 13.544375691268346, 0: 59.301109018623144, 2: 19.555794697037634, 4: 4.202911547544316, 6: 1.6590440319253879, 5: 0.34376588048904433, 1: 0.12256000956565928, 7: 1.2704391235464683}
# curseword_2011 = {3: 12.648860156515822, 0: 39.47487807644323, 2: 30.350459339911534, 6: 12.101621866848134, 4: 4.290007939208348, 5: 0.4678462061925825, 7: 0.5500737212203698, 1: 0.11625269365997505}
sentiment_2012 = {0: 0.35336944288126054, 1: 0.352771525042206, 2: 0.3233152785593697}
sentiment_2017 = {0: 0.4322958539106466, 1: 0.4858734351671069, 2: 0.2838520730446767}
sentiment_2011 = {0: 0.34445277361319343, 1: 0.3364567716141929, 2: 0.3277736131934033}
sentiment_2014 = {0: 0.40099255583126553, 1: 0.4101461262751585, 2: 0.29950372208436726}
sentiment_2016 = {0: 0.5095541401273885, 1: 0.4194267515923567, 2: 0.24522292993630573}
sentiment_2015 = {0: 0.45016032343510387, 1: 0.43301268646312563, 2: 0.2749198382824481}
sentiment_2013 = {0: 0.35762630178320726, 1: 0.3941076629717327, 2: 0.32118684910839634}
sentiment_2019 = {0: 0.46938775510204084, 1: 0.4797708557107053, 2: 0.2653061224489796}
sentiment_2018 = {0: 0.4975091767173571, 1: 0.4528710015731515, 2: 0.25124541164132147}
curseword_2012 = {2: 15.436008788272025, 3: 5.567190451105601, 7: 41.7378679446493, 1: 29.508807544551658, 5: 7.168094975009957, 6: 0.21328262517505878, 0: 0.14133186005576184, 4: 0.22741581118063497}
curseword_2017 = {2: 15.133454262762374, 1: 26.00969903379854, 7: 46.555362232998924, 3: 5.045718728019843, 5: 6.600525672824196, 4: 0.20730759264058046, 0: 0.166586458371895, 6: 0.2813460185836449}
curseword_2011 = {2: 15.706511540626758, 7: 42.70501032088572, 1: 29.161193469694126, 5: 6.520923250140739, 3: 5.29649089885532, 0: 0.13604803903171328, 6: 0.24863951960968286, 4: 0.2251829611559392}
curseword_2014 = {2: 13.627602158828065, 7: 53.39437162683115, 1: 24.344641480339245, 5: 2.3959136468774096, 3: 5.564764841942945, 6: 0.3527370855821126, 4: 0.18504240555127216, 0: 0.13492675404780263}
curseword_2016 = {1: 26.259489302967562, 7: 47.09454796411318, 5: 6.880607315389924, 2: 14.113181504485853, 3: 5.065562456866805, 0: 0.0759144237405107, 4: 0.24154589371980675, 6: 0.2691511387163561}
curseword_2015 = {2: 14.35897435897436, 7: 54.26312005751258, 1: 23.359693266235322, 3: 5.147375988497484, 5: 2.2046489336208963, 0: 0.12461059190031153, 6: 0.3354900551162233, 4: 0.2060867481428229}
curseword_2013 = {7: 53.37259830120974, 1: 24.075279725044286, 2: 13.702363468439142, 3: 5.75347858343301, 5: 2.3907217587475587, 4: 0.23316728996017988, 0: 0.13172437809438733, 6: 0.3406664950716914}
curseword_2019 = {1: 28.192815931509397, 7: 43.71487064954402, 3: 5.188907500465289, 5: 7.131956076679694, 2: 15.328494323469197, 4: 0.11539177368323097, 0: 0.10050251256281408, 6: 0.22706123208635773}
curseword_2018 = {1: 27.720124531013013, 7: 45.258242196854795, 2: 13.311247704957292, 5: 6.649636784545382, 3: 6.4540592320587535, 6: 0.2873792607966792, 0: 0.1237327372874591, 4: 0.1955775524866289}


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
    plt.savefig("XLNET/plots/cleaned_cat_line.png")
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
    plt.savefig("XLNET/plots/cleaned_sent_line.png")
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
multilineCurseword()
# plotSentimentBar()