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

LSMmodel = keras.saving.load_model("./ModelTraining/LSM/weights/LSMGENETV1.keras")
optimizer = tf.keras.optimizers.SGD(learning_rate=0.0015)
LSMmodel.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
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

#def predictLSb(data):

# basically this is unfinished but what we want to do here is take the prediction from the LS model and the prediction from the BIO predisposition model
# and combine them in such a way that we can deliver a metric to give a doctor better idea of the patients chance of developing alzheimers based on both factors.
# from my research it seems that bio/genetic factors contribute to alzheimers development just like lifestyle factors, so in theory we can weight the two models prediction
# against each other to come to a good metric for risk assesment, ill leave that up to yall ~Gary
def predictLSMB(data):
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

#this will be the route for the LSM model prediction it should return the metric given by predictLSMB function

