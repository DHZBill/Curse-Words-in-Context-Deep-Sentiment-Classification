from clean_tweets import tweetContainsCurseWord
import pandas as pd
import os

def drop_tweets_without_curseword(filename):

    pred_df = pd.read_csv('XLNET/analysis_data/labeled/' + filename, skipinitialspace=True, usecols=['text', 'sentiment'])
    print("before", pred_df.shape)
    pred_df = pred_df[pred_df["text"].apply(tweetContainsCurseWord) == True]
    #uncomment this line to replace file
    pred_df.to_csv('XLNET/analysis_data/labeled/cleaned/' + "cleaned_" + filename, index = False)
    print("after", pred_df.shape)


dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/labeled')

for file in os.listdir(dir_analysis_data):
    print(file)
    if(file=="cleaned"):
        continue
    drop_tweets_without_curseword(file)