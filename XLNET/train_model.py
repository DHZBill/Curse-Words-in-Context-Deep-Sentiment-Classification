import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from prepare_inputs import *
from build_model import *
plt.style.use('seaborn')

PATH_CSV_TRAIN = "unique_tweets.csv"

df = pd.read_csv(PATH_CSV_TRAIN)

# Balance the dataset for better accuracy across all classes
def preprocess(df):
    data = df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=False)
    data.loc[data['sentiment'] == 2, 'sentiment'] = 1
    data.loc[data['sentiment'] == 3, 'sentiment'] = 1
    data.loc[data['sentiment'] == 4, 'sentiment'] = 2
    data = data.drop(data.query('sentiment == 0').sample(frac=0.25, random_state=42).index)
    data = data.drop(data.query('sentiment == 2').sample(frac=0.25, random_state=42).index)
    data = data.append(data[data['sentiment']==1])
    print(data['sentiment'].value_counts())
    return data

# Split the data into train, validation, and test set
def split(df):
    train_val, test = train_test_split(df, test_size=0.15, random_state=42)
    train, val = train_test_split(train_val, test_size=0.2, random_state=196)
    return train, val, test

# Prepare model input
dataf = preprocess(df)
train, val, test = split(dataf)
xlnet_train = XLNetData(train, 50)
xlnet_val = XLNetData(val, 50)
xlnet_test = XLNetData(test, 50)

# Build and train the model
model, callbacks = xlnet_model(xlnet_train.num_classes, MAX_SEQ_LEN)
model.summary()
hist = model.fit(x=xlnet_train.x, y=xlnet_train.y, class_weight=xlnet_train.weights,
                 epochs=30, batch_size=32, validation_data=(xlnet_val.x, xlnet_val.y),
                 callbacks=callbacks)

# Evaluate accuracy on test, training, and validation dataset
_, test_acc = model.evaluate(xlnet_test.x, xlnet_test.y)
print(test_acc)
_, train_acc = model.evaluate(xlnet_train.x, xlnet_train.y)
print(train_acc)
_, val_acc = model.evaluate(xlnet_val.x, xlnet_val.y)

# F1 scores output saved
test['prediction'] = model.predict(xlnet_test.x).argmax(axis=-1)
print(classification_report(test['sentiment'], test['prediction']))
report = classification_report(test['sentiment'], test['prediction'], output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_df.to_csv('evaluation/classification_report.csv')

# Confusion matrix plotted and saved
cm =confusion_matrix(test['sentiment'], test['prediction'])
index = ['Empowered','Upset','Sarcastic']
columns = ['Empowered','Upset','Sarcastic']
cm_df = pd.DataFrame(cm,columns,index)
plt.figure(figsize=(10,6))
cm_plot = sns.heatmap(cm_df, annot=True)
plt.tight_layout()
plt.savefig('evaluation/confusion_matrix.png')
plt.close()

# Learning curve plotted and saved
plt.plot(hist.history['acc'])
plt.plot(hist.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.tight_layout()
plt.savefig('evaluation/learning_curve.png')

# Save the trained model weights.
model.save_weights('trained_model/model_weights')
