import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
from hashtag_config import *
import matplotlib.patches as mpatches

#Cached Sentiment Distribution for Archived Data From XLNET Model Classification
sentiment_2012 = {0: 0.35336944288126054, 1: 0.352771525042206, 2: 0.3233152785593697}
sentiment_2017 = {0: 0.4322958539106466, 1: 0.4858734351671069, 2: 0.2838520730446767}
sentiment_2011 = {0: 0.34445277361319343, 1: 0.3364567716141929, 2: 0.3277736131934033}
sentiment_2014 = {0: 0.40099255583126553, 1: 0.4101461262751585, 2: 0.29950372208436726}
sentiment_2016 = {0: 0.5095541401273885, 1: 0.4194267515923567, 2: 0.24522292993630573}
sentiment_2015 = {0: 0.45016032343510387, 1: 0.43301268646312563, 2: 0.2749198382824481}
sentiment_2013 = {0: 0.35762630178320726, 1: 0.3941076629717327, 2: 0.32118684910839634}
sentiment_2019 = {0: 0.46938775510204084, 1: 0.4797708557107053, 2: 0.2653061224489796}
sentiment_2018 = {0: 0.4975091767173571, 1: 0.4528710015731515, 2: 0.25124541164132147}
#Cached Curseword Category Distribution 2011-2019
curseword_2012 = {2: 15.436008788272025, 3: 5.567190451105601, 7: 41.7378679446493, 1: 29.508807544551658, 5: 7.168094975009957, 6: 0.21328262517505878, 0: 0.14133186005576184, 4: 0.22741581118063497}
curseword_2017 = {2: 15.133454262762374, 1: 26.00969903379854, 7: 46.555362232998924, 3: 5.045718728019843, 5: 6.600525672824196, 4: 0.20730759264058046, 0: 0.166586458371895, 6: 0.2813460185836449}
curseword_2011 = {2: 15.706511540626758, 7: 42.70501032088572, 1: 29.161193469694126, 5: 6.520923250140739, 3: 5.29649089885532, 0: 0.13604803903171328, 6: 0.24863951960968286, 4: 0.2251829611559392}
curseword_2014 = {2: 13.627602158828065, 7: 53.39437162683115, 1: 24.344641480339245, 5: 2.3959136468774096, 3: 5.564764841942945, 6: 0.3527370855821126, 4: 0.18504240555127216, 0: 0.13492675404780263}
curseword_2016 = {1: 26.259489302967562, 7: 47.09454796411318, 5: 6.880607315389924, 2: 14.113181504485853, 3: 5.065562456866805, 0: 0.0759144237405107, 4: 0.24154589371980675, 6: 0.2691511387163561}
curseword_2015 = {2: 14.35897435897436, 7: 54.26312005751258, 1: 23.359693266235322, 3: 5.147375988497484, 5: 2.2046489336208963, 0: 0.12461059190031153, 6: 0.3354900551162233, 4: 0.2060867481428229}
curseword_2013 = {7: 53.37259830120974, 1: 24.075279725044286, 2: 13.702363468439142, 3: 5.75347858343301, 5: 2.3907217587475587, 4: 0.23316728996017988, 0: 0.13172437809438733, 6: 0.3406664950716914}
curseword_2019 = {1: 28.192815931509397, 7: 43.71487064954402, 3: 5.188907500465289, 5: 7.131956076679694, 2: 15.328494323469197, 4: 0.11539177368323097, 0: 0.10050251256281408, 6: 0.22706123208635773}
curseword_2018 = {1: 27.720124531013013, 7: 45.258242196854795, 2: 13.311247704957292, 5: 6.649636784545382, 3: 6.4540592320587535, 6: 0.2873792607966792, 0: 0.1237327372874591, 4: 0.1955775524866289}
#Cached Sentiment Distribution PER CURSE WORDS CATEGORY From XLNET Model Classification
sentiment_per_category_2012 = {2: {0: 0.32145829865157316, 1: 0.3650740802397203, 2: 0.3134676211087065}, 3: {0: 0.31963997230556196, 1: 0.33879529194553426, 2: 0.3415647357489038}, 7: {1: 0.38457749730644913, 0: 0.27945205479452057, 2: 0.3359704478990303}, 1: {1: 0.26616449688683763, 0: 0.43601689380415376, 2: 0.29781860930900855}, 5: {1: 0.24126187488797277, 0: 0.45079763398458506, 2: 0.3079404911274422}, 6: {1: 0.4457831325301205, 0: 0.19879518072289157, 2: 0.35542168674698793}, 0: {1: 0.3181818181818182, 0: 0.42727272727272725, 2: 0.2545454545454545}, 4: {1: 0.4858757062146893, 0: 0.2033898305084746, 2: 0.3107344632768362}}
sentiment_per_category_2017 = {2: {1: 0.41022504892367906, 2: 0.2299412915851272, 0: 0.3598336594911937}, 1: {0: 0.4375177910617706, 1: 0.3327640193566752, 2: 0.22971818958155424}, 7: {0: 0.3130566157760814, 2: 0.24713740458015268, 1: 0.4398059796437659}, 3: {2: 0.25018341892883345, 1: 0.384446074834923, 0: 0.36537050623624356}, 5: {0: 0.4952327537857543, 1: 0.27089175546831185, 2: 0.2338754907459338}, 4: {0: 0.25, 1: 0.5357142857142857, 2: 0.21428571428571427}, 0: {0: 0.4444444444444444, 1: 0.26666666666666666, 2: 0.28888888888888886}, 6: {0: 0.2631578947368421, 1: 0.42105263157894735, 2: 0.3157894736842105}}
sentiment_per_category_2011 = {2: {0: 0.3106332138590203, 1: 0.37007168458781364, 2: 0.3192951015531661}, 7: {2: 0.3461496210040646, 1: 0.38492804569922, 0: 0.2689223332967154}, 1: {0: 0.4506113256113256, 1: 0.24050836550836552, 2: 0.3088803088803089}, 5: {0: 0.44532374100719424, 1: 0.24028776978417266, 2: 0.3143884892086331}, 3: {1: 0.32418069087688217, 0: 0.34809565987599644, 2: 0.32772364924712133}, 0: {0: 0.41379310344827586, 1: 0.20689655172413793, 2: 0.3793103448275862}, 6: {0: 0.18867924528301888, 1: 0.3584905660377358, 2: 0.4528301886792453}, 4: {1: 0.3333333333333333, 0: 0.25, 2: 0.4166666666666667}}
sentiment_per_category_2014 = {2: {0: 0.3598302687411598, 1: 0.38274398868458276, 2: 0.25742574257425743}, 7: {1: 0.3908523158008736, 0: 0.3293382910364247, 2: 0.2798093931627017}, 1: {0: 0.4454473475851148, 1: 0.2974663499604117, 2: 0.2570863024544735}, 5: {0: 0.45132743362831856, 1: 0.2582461786001609, 2: 0.2904263877715205}, 3: {1: 0.34741946657429856, 0: 0.39903013508832696, 2: 0.2535503983373744}, 6: {1: 0.43169398907103823, 0: 0.2677595628415301, 2: 0.3005464480874317}, 4: {1: 0.3958333333333333, 0: 0.1875, 2: 0.4166666666666667}, 0: {1: 0.3, 0: 0.44285714285714284, 2: 0.2571428571428571}}
sentiment_per_category_2016 = {1: {0: 0.5232588699080157, 1: 0.28488830486202366, 2: 0.19185282522996058}, 7: {0: 0.3903868698710434, 1: 0.3821805392731536, 2: 0.22743259085580306}, 5: {0: 0.5446339017051154, 1: 0.27382146439317956, 2: 0.1815446339017051}, 2: {0: 0.4371638141809291, 1: 0.3867970660146699, 2: 0.17603911980440098}, 3: {1: 0.34332425068119893, 0: 0.4373297002724796, 2: 0.21934604904632152}, 0: {0: 0.7272727272727273, 1: 0.2727272727272727, 2: 0.0}, 4: {1: 0.5142857142857142, 0: 0.2571428571428571, 2: 0.22857142857142856}, 6: {0: 0.41025641025641024, 1: 0.38461538461538464, 2: 0.20512820512820512}}
sentiment_per_category_2015 = {2: {0: 0.414218958611482, 1: 0.3781708945260347, 2: 0.2076101468624833}, 7: {2: 0.25234057586998765, 0: 0.3487016428192899, 1: 0.3989577813107225}, 1: {2: 0.22404595814526057, 0: 0.46922445629872794, 1: 0.3067295855560115}, 3: {0: 0.38733705772811916, 1: 0.36685288640595903, 2: 0.24581005586592178}, 5: {0: 0.5, 1: 0.24347826086956523, 2: 0.2565217391304348}, 0: {1: 0.2692307692307692, 0: 0.38461538461538464, 2: 0.34615384615384615}, 6: {1: 0.5142857142857142, 0: 0.21428571428571427, 2: 0.2714285714285714}, 4: {1: 0.4883720930232558, 0: 0.27906976744186046, 2: 0.23255813953488372}}
sentiment_per_category_2013 = {7: {1: 0.3827692831409038, 0: 0.3090125102833962, 2: 0.3082182065757}, 1: {2: 0.2819319539651594, 0: 0.4072070938934658, 1: 0.31086095214137477}, 2: {1: 0.3892817679558011, 0: 0.32917127071823205, 2: 0.28154696132596685}, 3: {1: 0.33710526315789474, 0: 0.37473684210526315, 2: 0.2881578947368421}, 5: {1: 0.27549081697276756, 0: 0.4566181127295757, 2: 0.26789107029765674}, 4: {1: 0.44155844155844154, 0: 0.3051948051948052, 2: 0.2532467532467532}, 0: {0: 0.4942528735632184, 1: 0.26436781609195403, 2: 0.2413793103448276}, 6: {0: 0.27111111111111114, 1: 0.4533333333333333, 2: 0.27555555555555555}}
sentiment_per_category_2019 = {1: {2: 0.19025613942434644, 0: 0.5084499603908107, 1: 0.30129390018484287}, 7: {2: 0.23552452316076294, 0: 0.3300408719346049, 1: 0.43443460490463215}, 3: {0: 0.42252510760401724, 1: 0.3744619799139168, 2: 0.203012912482066}, 5: {0: 0.5647181628392485, 1: 0.238517745302714, 2: 0.1967640918580376}, 2: {1: 0.41427877610490527, 0: 0.3727537639630889, 2: 0.21296745993200583}, 4: {1: 0.6451612903225806, 0: 0.1935483870967742, 2: 0.16129032258064516}, 0: {1: 0.3333333333333333, 0: 0.4074074074074074, 2: 0.25925925925925924}, 6: {1: 0.5081967213114754, 0: 0.19672131147540983, 2: 0.29508196721311475}}
sentiment_per_category_2018 = {1: {0: 0.5426925845932326, 2: 0.1769618430525558, 1: 0.28034557235421165}, 7: {0: 0.37313696093129906, 1: 0.40673780756680483, 2: 0.2201252315018961}, 2: {1: 0.42368815592203896, 0: 0.375712143928036, 2: 0.20059970014992504}, 5: {0: 0.5834333733493398, 1: 0.23769507803121248, 2: 0.1788715486194478}, 3: {1: 0.36054421768707484, 0: 0.44959802102659246, 2: 0.18985776128633272}, 6: {1: 0.5, 0: 0.2777777777777778, 2: 0.2222222222222222}, 0: {1: 0.22580645161290322, 0: 0.5483870967741935, 2: 0.22580645161290322}, 4: {0: 0.30612244897959184, 1: 0.3877551020408163, 2: 0.30612244897959184}}

sentimentByYear = [sentiment_2011,sentiment_2012,sentiment_2013,sentiment_2014,sentiment_2015,sentiment_2016,sentiment_2017,sentiment_2018,sentiment_2019]
cursewordByYear = [curseword_2011,curseword_2012,curseword_2013,curseword_2014,curseword_2015,curseword_2016,curseword_2017,curseword_2018,curseword_2019]
sentiment_per_categoryByYear = [sentiment_per_category_2011,sentiment_per_category_2012, sentiment_per_category_2013, sentiment_per_category_2014,sentiment_per_category_2015, sentiment_per_category_2016,sentiment_per_category_2017, sentiment_per_category_2018, sentiment_per_category_2019]

#plot curseword category distribution for a single year
#input: figure name to save as, filename: training set or prediction set
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

    plt.savefig(figname, bbox_inches="tight")


#plot curseword category distribution by year using cached data
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
    ax.legend(loc = "upper right")
    # plt.savefig("XLNET/plots/cleaned_cat_line.png")
    plt.show()

#plot sentiment distribution by year using cached data
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

#plot sentiment distribution throught time, per each curseword category 
def multilineSentimentByCategory():
    x = np.linspace(2011, 2019, 9)
    for i in range(len(cursewordsCatg)):
        positive = [ sentiment_per_category[i][0] for sentiment_per_category in sentiment_per_categoryByYear]
        negative = [ sentiment_per_category[i][1] for sentiment_per_category in sentiment_per_categoryByYear]
        sarcastic =[ sentiment_per_category[i][2] for sentiment_per_category in sentiment_per_categoryByYear]
        fig, ax = plt.subplots()
        plt.title("Sentiment Distribution Across Time For " + cursewordsCatg[i] + " Curse Words" )
        plt.xlabel("Year")
        plt.ylabel("Percentage")
        ax.plot(x, positive, label='Empowering')
        ax.plot(x, negative, label='Upset')
        ax.plot(x, sarcastic, label='Sarcastic')
        ax.legend()
        plt.savefig("XLNET/plots/sent_per_catg_"+ cursewordsCatg[i] + ".png")

#Plot Sentiment distribution in Training Set 
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

#Plot pie chart for average curseword category distribution using cached data
def plotCategoryPie():
    count = []
    labels = []
    for i in range(len(cursewordsCatg)):
        ave = 0
        for year in cursewordByYear:
            ave+= year[i]
        ave /= len(cursewordByYear)
        count.append([ave, cursewordsCatg[i]])
    for i in range(len(cursewordsCatg)):
        labels.append(count[i][1])
        count[i] = count[i][0]

    colors = ["red", "lightblue", "salmon", "orange", "green", "gray", "pink", "purple"]
    fig1, ax1 = plt.subplots()
    ax1.pie(count, labels=labels,
             startangle=90, radius=1.2, colors = colors)

    plt.title("Average Curse Words Class Distribution 2011-2019", y=1.08)
    plt.savefig("XLNET/plots/catg_pie.png")

