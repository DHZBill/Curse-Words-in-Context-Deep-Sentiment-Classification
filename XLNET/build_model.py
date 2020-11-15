
import tensorflow as tf
import keras
from transformers import TFXLNetModel, XLNetTokenizer

XLNET_MODEL = 'xlnet-base-cased'
MAX_SEQ_LEN = 50

def xlnet_model(num_classes, max_seq_len, mname = XLNET_MODEL):
    """ Creates a model by adding dense layers on top of XLNet for classification
    """
    # Define token ids as inputs
    word_inputs = keras.Input(shape=(max_seq_len,), name='word_inputs', dtype='int32')

    # Load XLNet model
    xlnet = TFXLNetModel.from_pretrained(mname)
    xlnet_encodings = xlnet(word_inputs)[0]

    # CLS
    text_encoding = tf.squeeze(xlnet_encodings[:, -1:, :], axis=1)
    # add drop out and dense layers
    text_encoding = keras.layers.Dropout(.5)(text_encoding)
    text_encoding = keras.layers.Dense(units=768, activation = 'tanh')(text_encoding)
    text_encoding = keras.layers.Dropout(.2)(text_encoding)

    # Final output
    outputs = tf.keras.layers.Dense(units=num_classes, activation='softmax', name='outputs')(text_encoding)

    # Compile model
    model = tf.keras.Model(inputs=[word_inputs], outputs=[outputs])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=4e-6), loss=keras.losses.SparseCategoricalCrossentropy(), metrics=[keras.metrics.SparseCategoricalAccuracy(name="acc")])

    # Early stopping on validation accuracy
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_acc', patience=4, min_delta=0.01, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_acc', factor=1e-6, patience=2, verbose=0, mode='auto',
                                          min_delta=0.001, cooldown=0, min_lr=1e-6)
    ]

    return model, callbacks