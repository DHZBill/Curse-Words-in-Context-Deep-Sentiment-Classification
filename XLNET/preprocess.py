import numpy as np
from sklearn.utils import class_weight
from transformers import XLNetTokenizer
from build_model import XLNET_MODEL
class XLNetData:
    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'sentiment'
    TOKENIZER = XLNetTokenizer.from_pretrained(XLNET_MODEL)
    def __init__(self, data, max_len):
        self.data = data
        self.tokenizer = XLNetData.TOKENIZER
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
