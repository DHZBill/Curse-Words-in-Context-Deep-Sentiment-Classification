import csv
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)

def countExamplesByCategory(filename):
    df = pd.read_csv(filename)
    print("sentiment 0", len(df[(df["sentiment"] == 0)]))
    print("sentiment 1", len(df[(df["sentiment"] == 1)]))
    print("sentiment 2", len(df[(df["sentiment"] == 2)]))

countExamplesByCategory("/Users/wenxindong/Desktop/CurseWordsInContext/XLNET/2011-10-06_predicted.csv")

countExamplesByCategory("/Users/wenxindong/Desktop/CurseWordsInContext/2011-10-06_predicted_wenxin.csv")

countExamplesByCategory("/Users/wenxindong/Desktop/CurseWordsInContext/2011-10-06_predicted_wenxin_2.csv")
