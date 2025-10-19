"""
@author: elamr
"""
#LSM model training utils
from keras.src.optimizers import optimizer
import tensorflow as tf
import keras
import pandas as pd
#kaggle
import kaggle  
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate() 
path = api.dataset_download_files("rabieelkharoua/alzheimers-disease-dataset", path='./ModelTraining/LSM/data/', unzip=True)
print("Done downloading dataset")

data = pd.read_csv('./ModelTraining/LSM/data/alzheimers_disease_data.csv')
data = data.drop(columns=['DoctorInCharge'])

labels = data['Diagnosis']
data = data.drop(columns=['Diagnosis'])

data = data.sample(frac=1).reset_index(drop=True)
labels = labels.sample(frac=1).reset_index(drop=True)

print(data.head())
print(labels.head())

model = keras.Sequential([
    keras.layers.InputLayer(input_shape=(33,)),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(1024, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])
optimizer = tf.keras.optimizers.SGD(learning_rate=0.0015)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(data, labels, epochs=128, batch_size=32, validation_split=0.2)
model.save('./ModelTraining/LSM/weights/LSMGENETV1.keras')


