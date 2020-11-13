import pandas as pd
from keras.models import load_model
from keras.models import model_from_json
from preprocess import XLNetData
from build_model import xlnet_model
from cleanTweets import *

model, _ = xlnet_model(3, 50)
model.load_weights('XLNET_TEST_WENXIN_WEIGHTS')
pred_df = pd.read_csv('XLNET/AnalysisData/2011-10-06.csv')

#more cleaning
pred_df.drop_duplicates(subset=["text"], inplace=True)
pred_df["text"] = pred_df["text"].apply(lambda x: to_lower(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_stopwords(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_userids(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_URL(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_html(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_repeatCharacters(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_hashtags(x))
pred_df = pred_df[pred_df["text"].apply(tweetContainsCurseWord) == True]
pred_df["text"] = pred_df["text"].apply(lambda x: remove_emoji(x))
pred_df["text"] = pred_df["text"].apply(lambda x: remove_punct(x))
pred_df = pred_df[pred_df["text"].apply(tweetIsNotTooShort) == True]
pred_df = pred_df.sort_values(["text"])
pred_df.drop_duplicates(subset=["text"], inplace=True)


#predicting
pred_df['sentiment']=0
pred_data =XLNetData(pred_df, max_len=50)
pred_df['sentiment']= model.predict(pred_data.x).argmax(axis=-1)
pred_df.to_csv('2011-10-06_predicted_wenxin_2.csv')