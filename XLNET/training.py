
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from preprocess import *
from build_model import *
plt.style.use('seaborn')

PATH_CSV_TRAIN = "unique_tweets.csv"

df = pd.read_csv(PATH_CSV_TRAIN)

def preprocess(df):
    data = df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=False)
    data.loc[data['sentiment'] == 2, 'sentiment'] = 1
    data.loc[data['sentiment'] == 3, 'sentiment'] = 1
    data.loc[data['sentiment'] == 4, 'sentiment'] = 2
    data = data.drop(data.query('sentiment == 0').sample(frac=0.5).index)
    data = data.drop(data.query('sentiment == 2').sample(frac=0.4).index)
    return data

def split(df):
    train_val, test = train_test_split(df, test_size=0.15, random_state=42)
    train, val = train_test_split(train_val, test_size=0.2, random_state=196)
    return train, val, test

def prepare_train_val_test(train, val, test):
    tokenizer = XLNetTokenizer.from_pretrained(XLNET_MODEL)
    xlnet_train = XLNetData(train, tokenizer, 50)
    xlnet_val = XLNetData(val, tokenizer, 50)
    xlnet_test = XLNetData(test, tokenizer, 50)
    return xlnet_train, xlnet_val, xlnet_test

dataf = preprocess(df)

train, val, test = split(dataf)
xlnet_train, xlnet_val, xlnet_test = prepare_train_val_test(train, val, test)
model, callbacks = xlnet_model(xlnet_train.num_classes, MAX_SEQ_LEN)
model.summary()
hist = model.fit(x=xlnet_train.x, y=xlnet_train.y, class_weight=xlnet_train.weights, epochs=20, batch_size=16, validation_data=(xlnet_val.x, xlnet_val.y), callbacks=callbacks)

_, test_acc = model.evaluate(xlnet_test.x, xlnet_test.y)
print(test_acc)
_, train_acc = model.evaluate(xlnet_train.x, xlnet_train.y)
print(train_acc)
_, val_acc = model.evaluate(xlnet_val.x, xlnet_val.y)

test['prediction'] = model.predict(xlnet_test.x).argmax(axis=-1)
print(classification_report(test['sentiment'], test['prediction']))

### MODEL IS SAVED BUT IT GIVES EORRS WHEN LOADING MODEL WITH keras.models.load_model('XLNET_TEST')
#model.save('XLNET_TEST')

pred_df = pd.read_csv('local-analysis-tweets.csv')
pred_df['sentiment']=0
pred_data =XLNetData(pred_df, tokenizer=XLNetTokenizer.from_pretrained(XLNET_MODEL), max_len=50)
pred_df['sentiment']= model.predict(pred_data.x).argmax(axis=-1)
pred_df.to_csv('predictions.csv')