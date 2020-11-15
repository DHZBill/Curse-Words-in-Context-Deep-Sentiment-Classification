from clean_tweets import tweetContainsCurseWord
import pandas as pd

def drop_tweets_without_curseword(filename):

    pred_df = pd.read_csv('XLNET/analysis_data/labeled/' + filename)
    print("before", pred_df.shape)
    pred_df = pred_df[pred_df["text"].apply(tweetContainsCurseWord) == True]
    #uncomment this line to replace file
    #pred_df.to_csv('XLNET/analysis_data/labeled/' + filename)
    print("after", pred_df.shape)

drop_tweets_without_curseword("2011-10-06_labeled.csv")
drop_tweets_without_curseword("2012-01-01_labeled.csv")