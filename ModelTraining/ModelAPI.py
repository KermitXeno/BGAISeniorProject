# -*- coding: utf-8 -*-
"""
@author: elamr
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import keras
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)
CORS(app)

MRImodel = None
BIOModel = None

def load_models():
    global MRImodel, BIOModel
    if MRImodel is None:
        MRImodel = keras.saving.load_model("./ModelTraining/AMRI/weights/AMRIGENETV1.keras")
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.00015)
        MRImodel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy', 'mse'])
    if BIOModel is None:
        BIOModel = keras.saving.load_model("./ModelTraining/BIOFM/weights/BIOFMGENETV1.keras")
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        BIOModel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

def predictMRI(image_path):
    load_models()
    img = image.load_img(image_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    predictions = MRImodel.predict(img_array)
    return predictions[0]

@app.route('/predictMRI', methods=['POST'])
def predictMRI_api():
    data = request.json.get('image_path')
    if not data:
        return jsonify({'error': 'No image path provided.'}), 400
    result = predictMRI(data)
    classes = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    predicted_class = classes[np.argmax(result)]
    return jsonify({'prediction': predicted_class})
def predictBIO(features):
    load_models()
    features_array = np.array(features).reshape(1, -1)
    predictions = BIOModel.predict(features_array)
    return predictions[0]

@app.route('/predictBIO', methods=['POST'])
def predictBIO_api():
    data = request.json.get('features')
    if not data or len(data) != 8:
        return jsonify({'error': 'Invalid features provided. Expected 8 features.'}), 400
    result = predictBIO(data)
    classes = ['No Impairment', 'Very Mild Impairment', 'Mild Impairment', 'Moderate Impairment']
    predicted_class = classes[np.argmax(result)]
    confidence_scores = result[0].tolist()
    confidence = float(confidence_scores[np.argmax(result)])
    
    return jsonify({
        'prediction': predicted_class,
        'confidence': confidence,
        'all_scores': {classes[i]: float(confidence_scores[i]) for i in range(len(classes))},
        'status': 'success'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'API is running', 'models_loaded': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
