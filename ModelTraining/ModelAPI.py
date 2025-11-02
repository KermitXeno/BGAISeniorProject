# -*- coding: utf-8 -*-
"""
@author: elamr
"""

from flask import Flask, jsonify, request, send_from_directory
import tensorflow as tf
import keras
from keras.preprocessing import image
import numpy as np

MRImodel = keras.saving.load_model("./ModelTraining/AMRI/weights/AMRIGENETV1.keras")
optimizer = tf.keras.optimizers.SGD(learning_rate=0.00015)
MRImodel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy','mse'])

BIOModel = keras.saving.load_model("./ModelTraining/BIOFM/weights/BIOFMGENETV1.keras")
optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
BIOModel.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

#test image loading
picturePath = "./ModelTraining/AMRI/demoIMG/MildImpairment (1).jpg"
imgmild= image.load_img(picturePath, target_size = (128, 128)) 

#test data for the bio model array with values 0,75,12,2.0,18.0,1479,0.657,1.187
testdata = [0, 75, 12, 2.0, 18.0 ,1479, 0.657, 1.187]

def predictMRI(img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    result = MRImodel.predict(img)   
    return result
print(predictMRI(imgmild))

def predictBIO(data):
    data = np.array(data)
    data = np.expand_dims(data, axis = 0)
    result = BIOModel.predict(data)
    return result
print(predictBIO(testdata))

app = Flask(__name__)
@app.route('/predictMRI', methods=['POST'])
def predictMRI_api():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        img = image.load_img(file, target_size=(128, 128))
        result = predictMRI(img)
        classes = ['Mild Impairment', 'Moderate Impairment', 'No Impairment', 'Severe Impairment']
        predicted_class = classes[np.argmax(result)]
        return jsonify({'prediction': predicted_class})
    return jsonify({'error': 'File processing error'}), 500

@app.route('/predictBIO', methods=['POST'])
def predictBIO_api():
    data = request.json.get('data')
    if not data or len(data) != 8:
        return jsonify({'error': 'Invalid input data. Expected 8 features.'}), 400
    result = predictBIO(data)
    classes = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    predicted_class = classes[np.argmax(result)]
    return jsonify({'prediction': predicted_class})
