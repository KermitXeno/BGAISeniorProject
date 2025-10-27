# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import os
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout
# kaggle
#from kaggle.api.kaggle_api_extended import KaggleApi
#api = KaggleApi()
#api.authenticate()
#path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)
print("Done downloading dataset")

df = pd.read_csv("./ModelTraining/BIOFM/data/oasis_longitudinal.csv", header=0)
#print head of df
print(df.head())

df.drop('Subject ID', axis=1, inplace=True)
df.drop('MR Delay', axis=1, inplace=True)
df.drop('Hand', axis=1, inplace=True)
df.drop('MRI ID', axis=1, inplace=True)
df.drop('Group', axis=1, inplace=True)
df.drop('Visit', axis=1, inplace=True)
df['M/F'] = df['M/F'].map({'F':0, 'M':1})
df['CDR'] = df['CDR'].map({0.0:0, 0.5:1, 1.0:2, 2.0:3})
df = df.dropna()
df.convert_dtypes()

print(df.head())
df.to_csv('./ModelTraining/BIOFM/data/clean_oasis.csv', index=False,  header=False)

labels = df['CDR']
df.drop('CDR', axis=1, inplace=True)
print(labels.head())

model = tf.keras.Sequential()
model.add(Dense(64, activation='relu', input_shape=(df.shape[1],)))
model.add(Dropout(0.05))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.05))
model.add(Dense(4, activation='softmax'))

optimizer = tf.keras.optimizers.SGD(learning_rate=0.0008)
model.compile(optimizer=optimizer, loss='poisson', metrics=['accuracy'])
model.fit(df, labels, epochs=64, batch_size=32, validation_split=0.2)



