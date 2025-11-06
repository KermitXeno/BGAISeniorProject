# -*- coding: utf-8 -*-
"""
@author: elamr
"""
import sys, os
from keras.src.layers import Activation
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import to_categorical
import numpy as np

#db necesscities
import psycopg2
from dotenv import find_dotenv, load_dotenv

from db__connection import dbConnection as db

load_dotenv(find_dotenv(usecwd=True))
HOST = os.getenv("HOST")
PORT = os.getenv("PORT", 5432)
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

conn = psycopg2.connect(f"host={HOST} port={PORT} dbname={DBNAME} user={USER} password={PASSWORD} gssencmode=disable")
# kaggle
#from kaggle.api.kaggle_api_extended import KaggleApi
#api = KaggleApi()
#api.authenticate()
#path = api.dataset_download_files("jboysen/mri-and-alzheimers", path='./ModelTraining/BIOFM/data/', unzip=True)

df = db.getTableData(conn,'longitudinal_oasis')

print(df.head())
print(df.dtypes)

df.drop('id', axis=1, inplace=True)
df.drop('visit', axis=1, inplace=True)
df.drop('dominant_hand', axis=1, inplace=True)
df.drop('mri_id', axis=1, inplace=True)
# df.drop('visit', axis=1, inplace=True)
# df['M/F'] = df['sex'].map({'F':0, 'M':1})

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
df['CDR'] = df['cdr'].apply(map_cdr)

df = df.dropna()
df.convert_dtypes()
print(df.head())

df = db.getTableData(conn,'cross_sectional_oasis')

labels = to_categorical(df['cdr'], num_classes=4)
df.drop('cdr', axis=1, inplace=True)
df.convert_dtypes()
print(df.head())


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

# model.save("./ModelTraining/BIOFM/weights/BIOFMGENETV1.keras")
model.save("./BIOFM/weights/BIOFMGENETV1.keras") #Use this if there are pathing issues


