import pandas as pd
import os

def count_examples_by_category(filename):
    df = pd.read_csv(filename)
    print("sentiment 0", len(df[(df["sentiment"] == 0)]))
    print("sentiment 1", len(df[(df["sentiment"] == 1)]))
    print("sentiment 2", len(df[(df["sentiment"] == 2)]))

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_analysis_data = os.path.join(dir_path, 'analysis_data/labeled')

for file in os.listdir(dir_analysis_data):
    filename = os.path.splitext(file)[0]
    count_examples_by_category('analysis_data/labeled/' + file)
