import pandas as pd
import os
from prepare_inputs import XLNetData
from build_model import xlnet_model
from clean_tweets import clean_tweets_df
model, _ = xlnet_model(3, 50)
model.load_weights('trained_model/model_weights')

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/source')

for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    pred_df = pd.read_csv('analysis_data/source/' + file)
    pred_df = clean_tweets_df(pred_df)
    pred_df['sentiment'] = 0
    pred_data = XLNetData(pred_df, max_len=50)
    pred_df['sentiment'] = model.predict(pred_data.x).argmax(axis=-1)
    pred_df.to_csv('analysis_data/labeled/' + filename + '_labeled.csv')
    print(filename + 'COMPLETED!')