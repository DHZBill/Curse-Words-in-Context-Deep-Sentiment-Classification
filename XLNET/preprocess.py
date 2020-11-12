import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
import transformers
import keras
import nltk
import re
import os

from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from transformers import TFXLNetModel, XLNetTokenizer
from build_model import *
from sklearn.utils import class_weight

class XLNetData:
    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'sentiment'

    def __init__(self, data, tokenizer, max_len):
        self.data = data
        self.tokenizer = tokenizer
        self.sequence_len = max_len
        self.num_classes = data[XLNetData.LABEL_COLUMN].nunique()
        self.x = self._get_inputs()['inp_tok']
        self.y = data[XLNetData.LABEL_COLUMN]
        self.weights = self._get_weights()

    def _get_inputs(self):
        x = self.data[XLNetData.DATA_COLUMN]
        inps = [self.tokenizer.encode_plus(t, max_length=self.sequence_len, pad_to_max_length=True, add_special_tokens=True) for t in
                x]
        inp_tok = np.array([a['input_ids'] for a in inps])
        ids = np.array([a['attention_mask'] for a in inps])
        segments = np.array([a['token_type_ids'] for a in inps])
        return {'inp_tok' : inp_tok, 'ids' : ids, 'segments': segments}

    def _get_weights(self):
        class_weights = class_weight.compute_class_weight('balanced',
                                                          np.unique(self.y),
                                                          self.y)
        weights = {i: class_weights[i] for i in range(self.num_classes)}
        return weights
