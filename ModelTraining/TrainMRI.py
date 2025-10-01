# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 16:05:50 2025

@author: elamr
"""
#ML training
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow import keras
#math utilities
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
#data frame utils
import pandas as pd
#image processing
import cv2
#kaggle
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

#path = api.dataset_download_files("lukechugh/best-alzheimer-mri-dataset-99-accuracy", path='ModelTraining/data', unzip=TRUE)
print("Done downloading dataset")
#train data loading
train_data = keras.utils.image_dataset_from_directory(
    directory='./ModelTraining/data/Combined Dataset/train',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(224, 224),
    color_mode='rgb',
    shuffle=True,
    verbose=True
)
#test data loading
test_data = keras.utils.image_dataset_from_directory(
    directory='./ModelTraining/data/Combined Dataset/test',
    labels='inferred',
    label_mode='int',
    batch_size=32,
    image_size=(224, 224),
    color_mode='rgb',
    shuffle=True,
    verbose=True
)
#image preprocessing
def process(image, label):
    image = preprocess_input(image)
    return image, label

train = train_data.map(process)
test = test_data.map(process)

#print("Class Names:", train_dataset.class_names)
#print("Class Names:", test_dataset.class_names)

#model creation
model = tf.keras.Sequential([
    layers.Conv2D(256, (11, 11), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D((3, 3)),
    layers.BatchNormalization(),
    layers.Conv2D(128, (5, 5), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    layers.BatchNormalization(),
    layers.Flatten(),
    layers.Dense(2048, activation='relu'),
    layers.Dense(2048, activation='relu'),
    layers.Dense(4),
])
#early stopping
ES = EarlyStopping(
    monitor="val_loss",
    min_delta=0.01,
    patience=11,
    verbose=1,
    mode="auto",
    restore_best_weights=True,
    start_from_epoch=0,
)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#start training
history = model.fit(train, batch_size= 32, epochs=5,validation_data=test, callbacks=[ES])

e=pd.DataFrame(model.history)
e[['accuracy','val_accuracy']].plot()
e[['loss','val_loss']].plot()