from flask import Flask, request, jsonify  # Flask framework for API
import tensorflow as tf  # TensorFlow for loading the model and predictions
import numpy as np  # NumPy for numerical operations
import cv2  # OpenCV for image processing

# Load model
MODEL_PATH = "plant_disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels
CLASS_LABELS = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_", 
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
    "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", 
    "Grape___healthy", "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", "Potato___Late_blight", 
    "Potato___healthy", "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot", "Tomato___Early_blight", 
    "Tomato___Late_blight", "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", 
    "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

# Confidence threshold
CONFIDENCE_THRESHOLD = 0.10  # Adjust as needed

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({'error': 'Invalid image format'}), 400

        img = cv2.resize(img, (224, 224)) / 255.0  # Resize and normalize
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        predictions = model.predict(img)[0]  # Get predictions

        # Ensure model output size matches the class labels
        if len(predictions) != len(CLASS_LABELS):
            return jsonify({'error': 'Model output size mismatch'}), 500

        # Collect results above confidence threshold
        results = sorted(
            [{"disease": CLASS_LABELS[i], "confidence": float(predictions[i])} for i in range(len(predictions))],
            key=lambda x: x["confidence"],
            reverse=True
        )[:5]


        # Sort results by confidence (highest first)
        results = sorted(results, key=lambda x: x["confidence"], reverse=True)

        return jsonify({"predictions": results})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
