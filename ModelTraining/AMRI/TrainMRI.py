# -*- coding: utf-8 -*-
"""
@author: elamr
"""
#ML training
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Conv2D, BatchNormalization, Dropout, Flatten
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras import regularizers
#math utilities
import matplotlib.pyplot as plt
import numpy as np
import os
#data frame utils
import pandas as pd
#kaggle
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
path = api.dataset_download_files("lukechugh/best-alzheimer-mri-dataset-99-accuracy", path='./ModelTraining/AMRI/data/', unzip=True)
print("Done downloading dataset")

train_data = keras.utils.image_dataset_from_directory(
    directory='./ModelTraining/AMRI/data/Combined Dataset/train',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(128, 128),
    color_mode='rgb',
    shuffle=True,
    verbose=True
)

test_data = keras.utils.image_dataset_from_directory(
    directory='./ModelTraining/AMRI/data/Combined Dataset/test',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(128, 128),
    color_mode='rgb',
    shuffle=True,
    verbose=True
)

def process(image, label):
    image = preprocess_input(image)
    return image, label
train = train_data.map(process)
test = test_data.map(process)

EXTmodel = ResNet50V2(
    include_top=False,
    weights="imagenet",
    input_shape=(128, 128, 3),
    classes=4 
)
EXTmodel.trainable = True
set_trainable = False

model = tf.keras.Sequential()
model.add(EXTmodel)
model.add(Flatten())
model.add(Dense(32, activation='selu',  kernel_regularizer=regularizers.l2(0.0005)))
model.add(Dropout(0.2))
model.add(Dense(32, activation='selu',  kernel_regularizer=regularizers.l2(0.0005)))
model.add(Dropout(0.2))
model.add(Dense(32, activation='selu',  kernel_regularizer=regularizers.l2(0.0005)))
model.add(Dropout(0.2))
model.add(Dense(32, activation='selu',  kernel_regularizer=regularizers.l2(0.0005)))
model.add(Dropout(0.2))
model.add(Dense(4, activation='softmax',))

ES = EarlyStopping(
    monitor="val_loss",
    min_delta=0.01,
    patience=10,
    verbose=1,
    mode="auto",
    restore_best_weights=True,
    start_from_epoch=0,
)
optimizer = tf.keras.optimizers.SGD(learning_rate=0.00015)
model.compile(optimizer = optimizer, loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])
fitted = model.fit(train, batch_size = 32, epochs = 42,validation_data = test, callbacks = ES)
model.save('./ModelTraining/AMRI/weights/AMRIGENETV1.keras')
 