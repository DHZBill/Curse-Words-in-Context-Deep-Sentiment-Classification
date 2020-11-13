import pandas as pd
from keras.models import load_model
from keras.models import model_from_json
from preprocess import XLNetData
from build_model import xlnet_model

model, _ = xlnet_model(3, 50)
model.load_weights('model_weights')

pred_df = pd.read_csv('AnalysisData/2011-10-06.csv')
#pred_df = pd.read_csv('unique_tweets_new.csv')
pred_df['sentiment']=0
pred_data =XLNetData(pred_df, max_len=50)
pred_df['sentiment']= model.predict(pred_data.x).argmax(axis=-1)
pred_df.to_csv('2011-10-06_predicted.csv')