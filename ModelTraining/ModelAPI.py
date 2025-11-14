from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import io

app = Flask(__name__)
CORS(app)
BIOModel = None
MRIModel = None

def load_bio_model():
    """Load the BIO model for CDR prediction"""
    global BIOModel
    if BIOModel is None:
        try:
            model_path = "./BIOFM/weights/BIOFMGENETV1.keras"
            print(f"Attempting to load model from: {model_path}")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Use the correct API for loading models
            BIOModel = tf.keras.models.load_model(model_path)
            
            # Optional: recompile if needed
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
            BIOModel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            print("BIO model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading BIO model: {e}")
            import traceback
            traceback.print_exc()
            return False
    return True

def predict_bio_cdr(features):
    """
    Predict CDR levels from biomarker features
    
    Args:
        features: List of 8 biomarker values [M/F, Age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
    
    Returns:
        Raw model predictions as numpy array
    """
    if not load_bio_model():
        raise Exception("BIO model not available")
    
    # Reshape features for model input
    features_array = np.array(features).reshape(1, -1)
    
    # Get raw predictions (logits)
    predictions = BIOModel.predict(features_array, verbose=0)
    
    return predictions[0]  # Return first (and only) prediction

def load_mri_model():
    """Load the MRI model for impairment prediction"""
    global MRIModel
    if MRIModel is None:
        try:
            model_path = "./AMRI/weights/AMRIGENETV1.keras"
            print(f"Attempting to load MRI model from: {model_path}")
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"MRI Model file not found: {model_path}")
            
            MRIModel = tf.keras.models.load_model(model_path)
            
            # Optional: recompile if needed
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
            MRIModel.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
            print("MRI model loaded successfully")
            print(f"Model input shape: {MRIModel.input_shape}")
            print(f"Model output shape: {MRIModel.output_shape}")
            return True
        except Exception as e:
            print(f"Error loading MRI model: {e}")
            import traceback
            traceback.print_exc()
            return False
    return True

def preprocess_image(image_file):
    """
    Preprocess uploaded image for MRI model prediction
    
    Args:
        image_file: Uploaded image file
    
    Returns:
        Preprocessed image array ready for model input
    """
    try:
        # Read image
        image = Image.open(io.BytesIO(image_file.read()))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize to model's expected input size (128x128 based on the error message)
        image = image.resize((128, 128))
        
        # Convert to numpy array and normalize
        image_array = np.array(image, dtype=np.float32)
        image_array = image_array / 255.0  # Normalize to [0, 1]
        
        # Add batch dimension
        image_array = np.expand_dims(image_array, axis=0)
        
        # Debug: Print image statistics
        print(f"Preprocessed image shape: {image_array.shape}")
        print(f"Image min value: {np.min(image_array):.4f}")
        print(f"Image max value: {np.max(image_array):.4f}")
        print(f"Image mean: {np.mean(image_array):.4f}")
        print(f"Image std: {np.std(image_array):.4f}")
        
        return image_array
        
    except Exception as e:
        raise Exception(f"Image preprocessing failed: {str(e)}")

def predict_mri_impairment(image_array):
    """
    Predict impairment levels from MRI scan
    
    Args:
        image_array: Preprocessed image array
    
    Returns:
        Raw model predictions as numpy array
    """
    if not load_mri_model():
        raise Exception("MRI model not available")
    
    print(f"Making prediction with input shape: {image_array.shape}")
    
    # Get raw predictions
    predictions = MRIModel.predict(image_array, verbose=0)
    
    print(f"Raw model output: {predictions}")
    print(f"Output shape: {predictions.shape}")
    
    return predictions[0]  # Return first (and only) prediction   

def compare_predictions_and_decide(raw_predictions, labels):
    """
    Compare the 4 prediction values and make an intelligent decision
    
    Args:
        raw_predictions: Array of 4 raw prediction values
        labels: List of 4 corresponding labels
    
    Returns:
        Dictionary with detailed comparison and decision
    """
    # Convert raw predictions to probabilities using softmax
    exp_preds = np.exp(raw_predictions - np.max(raw_predictions))  # Numerical stability
    probabilities = exp_preds / np.sum(exp_preds)
    
    # Create detailed comparison of all 4 values
    comparison = []
    for i, (prob, label) in enumerate(zip(probabilities, labels)):
        comparison.append({
            "label": label,
            "probability": float(prob),
            "percentage": f"{prob * 100:.2f}%",
            "rank": 0  # Will be filled below
        })
    
    # Sort by probability (highest first) and assign ranks
    comparison_sorted = sorted(comparison, key=lambda x: x["probability"], reverse=True)
    for i, item in enumerate(comparison_sorted):
        item["rank"] = i + 1
    
    # Get top predictions
    highest = comparison_sorted[0]
    second = comparison_sorted[1]
    third = comparison_sorted[2]
    fourth = comparison_sorted[3]
    
    # Calculate differences between predictions
    margin_1st_2nd = highest["probability"] - second["probability"]
    margin_2nd_3rd = second["probability"] - third["probability"]
    
    # Decision logic based on comparison of all values
    decision_confidence = ""
    decision_rationale = ""
    clinical_significance = ""
    
    if highest["probability"] >= 0.85:
        decision_confidence = "Very High"
        decision_rationale = f"Overwhelming evidence for {highest['label']} ({highest['percentage']}) with large margin over {second['label']} ({second['percentage']})"
        clinical_significance = "Strong clinical indication"
    elif highest["probability"] >= 0.70 and margin_1st_2nd >= 0.20:
        decision_confidence = "High"
        decision_rationale = f"Strong evidence for {highest['label']} ({highest['percentage']}) with significant margin over alternatives"
        clinical_significance = "Clear clinical indication"
    elif highest["probability"] >= 0.55 and margin_1st_2nd >= 0.15:
        decision_confidence = "Moderate"
        decision_rationale = f"Moderate evidence for {highest['label']} ({highest['percentage']}), but also consider {second['label']} ({second['percentage']})"
        clinical_significance = "Clinical correlation advised"
    elif highest["probability"] >= 0.40 and margin_1st_2nd >= 0.10:
        decision_confidence = "Low"
        decision_rationale = f"Weak evidence for {highest['label']} ({highest['percentage']}). Close competition with {second['label']} ({second['percentage']})"
        clinical_significance = "Additional testing recommended"
    else:
        decision_confidence = "Uncertain"
        decision_rationale = f"Very close probabilities: {highest['label']} ({highest['percentage']}) vs {second['label']} ({second['percentage']}). Margins too small for confident diagnosis"
        clinical_significance = "Inconclusive - repeat imaging or alternative methods needed"
    
    # Generate detailed recommendations based on all comparisons
    recommendations = generate_recommendations(comparison_sorted, margin_1st_2nd)
    
    return {
        "primary_finding": highest["label"],
        "primary_confidence": highest["percentage"],
        "secondary_finding": second["label"], 
        "secondary_confidence": second["percentage"],
        "decision_confidence": decision_confidence,
        "decision_rationale": decision_rationale,
        "clinical_significance": clinical_significance,
        "margin_analysis": {
            "1st_vs_2nd_margin": f"{margin_1st_2nd:.1%}",
            "2nd_vs_3rd_margin": f"{margin_2nd_3rd:.1%}"
        },
        "full_comparison": comparison_sorted,
        "recommendations": recommendations
    }

def generate_recommendations(sorted_predictions, confidence_margin):
    """Generate clinical recommendations based on prediction comparison"""
    primary = sorted_predictions[0]
    secondary = sorted_predictions[1]
    
    recommendations = []
    
    # Base recommendations on primary finding
    if "No Impairment" in primary["label"]:
        if primary["probability"] >= 0.80:
            recommendations.extend([
                "Continue routine cognitive monitoring",
                "Maintain healthy lifestyle habits",
                "Annual follow-up recommended"
            ])
        else:
            recommendations.extend([
                "Monitor cognitive function closely",
                "Consider repeat imaging in 6-12 months",
                "Lifestyle interventions as prevention"
            ])
    
    elif "Very Mild Impairment" in primary["label"]:
        recommendations.extend([
            "Neuropsychological assessment recommended",
            "Monitor progression with regular follow-ups",
            "Consider cognitive training programs",
            "Lifestyle modifications (diet, exercise, sleep)"
        ])
    
    elif "Mild Impairment" in primary["label"]:
        recommendations.extend([
            "Neurological consultation strongly recommended",
            "Comprehensive cognitive battery testing",
            "Follow-up MRI in 3-6 months",
            "Discuss early intervention strategies"
        ])
    
    elif "Moderate Impairment" in primary["label"]:
        recommendations.extend([
            "Urgent neurological consultation required",
            "Comprehensive medical workup",
            "Discuss treatment options immediately",
            "Consider specialist referral"
        ])
    
    # Add uncertainty-based recommendations
    if confidence_margin < 0.20:
        recommendations.extend([
            "Results show uncertainty - clinical correlation essential",
            "Consider additional imaging modalities",
            "Repeat scan may be warranted"
        ])
    
    return recommendations

@app.route('/')
def home():
    return "Flask is working!"

@app.route('/test')
def test():
    return "Test endpoint works!"

@app.route('/status')
def status():
    return {"status": "API is running smoothly"}

# Add a debug endpoint to check TensorFlow/Keras versions
@app.route('/debug-versions', methods=['GET'])
def debug_versions():
    return jsonify({
        'tensorflow_version': tf.__version__,
        'keras_version': tf.keras.__version__,
        'current_directory': os.getcwd(),
        'bio_model_file_exists': os.path.exists("./BIOFM/weights/BIOFMGENETV1.keras"),
        'mri_model_file_exists': os.path.exists("./AMRI/weights/AMRIGENETV1.keras")
    })

# Add a test endpoint to verify model variability
@app.route('/test-model-variability', methods=['POST'])
def test_model_variability():
    """Test endpoint to verify model gives different outputs for different inputs"""
    try:
        # Create different test inputs
        test_input_1 = np.zeros((1, 128, 128, 3))  # All black image
        test_input_2 = np.ones((1, 128, 128, 3))   # All white image
        test_input_3 = np.random.random((1, 128, 128, 3))  # Random noise
        
        if not load_mri_model():
            return jsonify({"error": "MRI model not available"}), 500
        
        pred1 = MRIModel.predict(test_input_1, verbose=0)
        pred2 = MRIModel.predict(test_input_2, verbose=0)
        pred3 = MRIModel.predict(test_input_3, verbose=0)
        
        # Show detailed comparison
        labels = ["Mild Impairment", "Moderate Impairment", "No Impairment", "Very Mild Impairment"]
        
        comparison1 = compare_predictions_and_decide(pred1[0], labels)
        comparison2 = compare_predictions_and_decide(pred2[0], labels)
        comparison3 = compare_predictions_and_decide(pred3[0], labels)
        
        return jsonify({
            "test_results": {
                "all_black_image": {
                    "raw_predictions": pred1[0].tolist(),
                    "analysis": comparison1
                },
                "all_white_image": {
                    "raw_predictions": pred2[0].tolist(),
                    "analysis": comparison2
                },
                "random_noise": {
                    "raw_predictions": pred3[0].tolist(),
                    "analysis": comparison3
                },
                "predictions_are_different": not (np.allclose(pred1[0], pred2[0]) and np.allclose(pred2[0], pred3[0]))
            },
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/biofm', methods=['POST'])
def biofm():
    """
    Endpoint for predicting CDR levels using the BioFM model.
    Expects JSON with keys:
        sex (1/0 or 'M'/'F'), age, EDUC, SES, MMSE, eTIV, nWBV, ASF
    Returns raw logits, softmax probabilities, and predicted class.
    """
    try:
        # Get input data
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({
                'error': 'No features provided. Expected JSON with "features" key.',
                'status': 'error'
            }), 400
        
        features = data['features']
        
        # Validate input
        if not isinstance(features, list) or len(features) != 8:
            return jsonify({
                'error': 'Invalid features. Expected array of 8 numerical values: [M/F, Age, EDUC, SES, MMSE, eTIV, nWBV, ASF]',
                'status': 'error'
            }), 400
        
        # Validate data types
        try:
            validated_features = [
                float(features[0]),  # M/F (0 or 1)
                float(features[1]),  # Age
                float(features[2]),  # EDUC
                float(features[3]),  # SES
                float(features[4]),  # MMSE
                float(features[5]),  # eTIV
                float(features[6]),  # nWBV
                float(features[7])   # ASF
            ]
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': f'Invalid data types in features: {str(e)}',
                'status': 'error'
            }), 400
        
        # Make prediction
        raw_predictions = predict_bio_cdr(validated_features)
        
        # CDR classification labels
        cdr_labels = [
            "CDR 0 (No Dementia)",
            "CDR 0.5 (Very Mild Dementia)", 
            "CDR 1 (Mild Dementia)",
            "CDR 2 (Moderate Dementia)"
        ]
        
        # Apply softmax to convert raw predictions to probabilities
        exp_preds = np.exp(raw_predictions - np.max(raw_predictions))  # Numerical stability
        probabilities = exp_preds / np.sum(exp_preds)
        
        # Create interpretation with percentages
        interpretation = {}
        for i, label in enumerate(cdr_labels):
            interpretation[label] = f"{probabilities[i] * 100:.1f}%"
        
        # Find predicted class (highest probability)
        predicted_class_index = np.argmax(probabilities)
        predicted_class = cdr_labels[predicted_class_index]
        max_confidence = f"{probabilities[predicted_class_index] * 100:.1f}%"
        
        # Prepare response
        response = {
            'raw_predictions': raw_predictions.tolist(),
            'cdr_labels': cdr_labels,
            'interpretation': interpretation,
            'predicted_class': predicted_class,
            'max_confidence': max_confidence,
            'input_data': validated_features,
            'status': 'success'
        }
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/amri', methods=['POST'])
def amri():
    """
    Endpoint for predicting impairment levels from MRI scans.
    Expects a file upload with an MRI image.
    Returns intelligent analysis with detailed comparison of all 4 prediction values.
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided. Expected multipart/form-data with "file" field.',
                'status': 'error'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected.',
                'status': 'error'
            }), 400
        
        # Validate file type
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.dcm'}
        file_ext = os.path.splitext(file.filename.lower())[1]
        if file_ext not in allowed_extensions:
            return jsonify({
                'error': f'Invalid file type. Supported formats: {", ".join(allowed_extensions)}',
                'status': 'error'
            }), 400
        
        print(f"Processing file: {file.filename}")
        
        # Preprocess the image
        image_array = preprocess_image(file)
        
        # Make prediction
        raw_predictions = predict_mri_impairment(image_array)
        
        # MRI impairment classification labels
        impairment_labels = [
            "Mild Impairment",
            "Moderate Impairment", 
            "No Impairment",
            "Very Mild Impairment"
        ]
        
        # Perform detailed comparison of all 4 prediction values
        decision_analysis = compare_predictions_and_decide(raw_predictions, impairment_labels)
        
        # Enhanced console output showing comparison
        print(f"=== MRI Analysis Results for {file.filename} ===")
        print(f"Raw predictions: {raw_predictions}")
        print(f"Detailed comparison:")
        for item in decision_analysis["full_comparison"]:
            print(f"  Rank {item['rank']}: {item['label']} = {item['percentage']} (prob: {item['probability']:.4f})")
        print(f"Primary Finding: {decision_analysis['primary_finding']} ({decision_analysis['primary_confidence']})")
        print(f"Secondary Finding: {decision_analysis['secondary_finding']} ({decision_analysis['secondary_confidence']})")
        print(f"Confidence Level: {decision_analysis['decision_confidence']}")
        print(f"Decision: {decision_analysis['decision_rationale']}")
        print(f"Margin Analysis: 1st vs 2nd = {decision_analysis['margin_analysis']['1st_vs_2nd_margin']}")
        
        # Prepare enhanced response
        response = {
            'raw_predictions': raw_predictions.tolist(),
            'impairment_labels': impairment_labels,
            'predicted_class': decision_analysis['primary_finding'],
            'max_confidence': decision_analysis['primary_confidence'],
            'decision_analysis': decision_analysis,
            'debug_info': {
                'filename': file.filename,
                'image_stats': {
                    'mean': float(np.mean(image_array)),
                    'std': float(np.std(image_array)),
                    'min': float(np.min(image_array)),
                    'max': float(np.max(image_array))
                }
            },
            'status': 'success'
        }
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            'error': f'MRI analysis failed: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("Starting Flask API server...")
    app.run(debug=True, host='0.0.0.0', port=5001)