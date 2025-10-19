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

#test image loading
#picturePath = "./ModelTraining/AMRI/demoIMG/MildImpairment (1).jpg"
#imgmild= image.load_img(picturePath, target_size = (128, 128)) 

def predictMRI(img):
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)
    result = MRImodel.predict(img)   
    return result
#testing
#print(predict(imgmild))

def predictLSM(data):
    LSMmodel = keras.saving.load_model("./ModelTraining/LSM/weights/LSMGENETV1.keras")
    optimizer = tf.keras.optimizers.SGD(learning_rate=0.0015)
    LSMmodel.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    data = np.expand_dims(data, axis=0)
    result = LSMmodel.predict(data)
    return result

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

@app.route('/predictLSM', methods=['POST'])
def predictLSM_api():
    data = request.json.get('data')
    if not data or len(data) != 33:
        return jsonify({'error': 'Invalid input data'}), 400
    result = predictLSM(np.array(data))
    classes = ['Alzheimer\'s Disease', 'No Alzheimer\'s Disease']
    predicted_class = classes[np.argmax(result)]
    return jsonify({'prediction': predicted_class})