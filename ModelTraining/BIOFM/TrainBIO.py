# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import os
from keras.src.layers import Activation
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import to_categorical
import numpy as np
# kaggle
#from kaggle.api.kaggle_api_extended import KaggleApi
#api = KaggleApi()
#api.authenticate()
#path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)
print("Done downloading dataset")

df = pd.read_csv("./ModelTraining/BIOFM/data/oasis_longitudinal.csv", header=0)

print(df.head())
print(df.dtypes)

df.drop('Subject ID', axis=1, inplace=True)
df.drop('MR Delay', axis=1, inplace=True)
df.drop('Hand', axis=1, inplace=True)
df.drop('MRI ID', axis=1, inplace=True)
df.drop('Group', axis=1, inplace=True)
df.drop('Visit', axis=1, inplace=True)
df['M/F'] = df['M/F'].map({'F':0, 'M':1})

def map_cdr(value):
    if value == 0.0:
        return 0
    elif value == 0.5:
        return 1
    elif value == 1.0:
        return 2
    elif value == 2.0:
        return 3
    else:
        return -1
df['CDR'] = df['CDR'].apply(map_cdr)

df = df.dropna()
df.convert_dtypes()

print(df.head())
df.to_csv('./ModelTraining/BIOFM/data/clean_oasis.csv', index=False,  header=False)

labels = to_categorical(df['CDR'], num_classes=4)
df.drop('CDR', axis=1, inplace=True)

model = tf.keras.Sequential()
model.add(Dense(512, activation='sigmoid', input_shape=(8,)))
model.add(Dense(256, activation='sigmoid'))
model.add(Dense(128, activation='sigmoid'))
model.add(Dense(64, activation='sigmoid'))
model.add(BatchNormalization())
model.add(Dense(32, activation='softmax'))
model.add(Dropout(0.05))
model.add(Dense(32, activation='softmax'))
model.add(Dropout(0.05))
model.add(Dense(32, activation='softmax'))
model.add(Dropout(0.05))
model.add(Dense(32, activation='softmax'))
model.add(Dropout(0.05))
model.add(Dense(4))

optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
loser = keras.losses.BinaryCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loser, metrics=['accuracy'])
model.fit(x=df, y=labels, epochs=64, batch_size=32)

model.save("./ModelTraining/BIOFM/weights/BIOFMGENETV1.keras")



