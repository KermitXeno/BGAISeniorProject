#!/usr/bin/env python3
"""
Temporary Mock ModelAPI.py 
Use this while training your real models
"""

from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/predictMRI', methods=['POST'])
def predictMRI_api():
    """Mock MRI prediction - returns random realistic result"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Mock prediction - randomly select from actual classes
        classes = ['Mild Impairment', 'Moderate Impairment', 'No Impairment', 'Severe Impairment']
        # Simulate some logic based on filename or just pick randomly
        import random
        predicted_class = random.choice(classes)
        
        return jsonify({
            'prediction': predicted_class,
            'mock': True,
            'message': 'This is a mock response. Train real models to get actual predictions.'
        })
    
    return jsonify({'error': 'File processing error'}), 500

@app.route('/predictBIO', methods=['POST'])
def predictBIO_api():
    """Mock BIO prediction - returns realistic result based on input"""
    data = request.json.get('data')
    if not data or len(data) != 8:
        return jsonify({'error': 'Invalid input data. Expected 8 features.'}), 400
    
    # Mock prediction based on some simple heuristics
    age = data[1]
    mmse = data[4]
    
    # Simple mock logic: higher age and lower MMSE = more impairment
    if age > 80 and mmse < 20:
        predicted_class = 'Moderate Impairment'
    elif age > 70 and mmse < 25:
        predicted_class = 'Mild Impairment'  
    elif age > 65 and mmse < 27:
        predicted_class = 'Very Mild Impairment'
    else:
        predicted_class = 'No Impairment'
    
    return jsonify({
        'prediction': predicted_class,
        'mock': True,
        'message': 'This is a mock response. Train real models to get actual predictions.',
        'input_summary': f'Age: {age}, MMSE: {mmse}'
    })

@app.route('/')
def home():
    return jsonify({
        'status': 'Mock ModelAPI running',
        'message': 'This is a temporary mock service. Replace with real ModelAPI.py after training models.',
        'endpoints': ['/predictMRI', '/predictBIO']
    })

if __name__ == '__main__':
    print("🚀 Starting Mock ModelAPI.py...")
    print("=" * 50)
    print("⚠️  This is a MOCK service for testing!")
    print("   Real predictions require trained models.")
    print("   To train models:")
    print("   1. cd ModelTraining/BIOFM && python TrainBIO.py")
    print("   2. cd ModelTraining/AMRI && python TrainMRI.py")
    print("=" * 50)
    print("🌐 Mock API running on http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=True)