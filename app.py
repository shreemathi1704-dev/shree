from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import cv2
import base64

app = Flask(__name__)
CORS(app) # Frontend-ல் இருந்து வரக்கூடிய requests-ஐ அனுமதிக்க

# 1. உங்கள் AI மாடலை இங்கே லோட் செய்யவும்
# MODEL_PATH = 'crop_disease_model.h5'
# model = tf.keras.models.load_model(MODEL_PATH)

# நோய்களின் பெயர்கள் (Class Labels)
CLASS_NAMES = ['Early Blight', 'Late Blight', 'Healthy Leaf', 'Yellow Leaf Curl Virus']

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1] # Base64 string பிரித்தல்
        
        # Base64-ஐ பிம்பமாக (Image Array) மாற்றுதல்
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Model-க்கு ஏற்றபடி 224x224 அளவுக்கு மாற்றி Preprocessing செய்தல்
        img_resized = cv2.resize(img, (224, 224))
        img_array = np.expand_dims(img_resized / 255.0, axis=0)

        # 2. 100% உண்மையான மாடல் Prediction
        # predictions = model.predict(img_array)
        # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        # confidence = round(100 * np.max(predictions[0]), 2)

        # (எடுத்துக்காட்டிற்கு மட்டும் static data - உங்கள் model லோட் செய்தவுடன் மேலே உள்ள 3 வரிகளை Un-comment செய்யவும்)
        predicted_class = "Tomato Late Blight"
        confidence = 98.45
        recommendation = "Fungicide தெளிக்கவும் மற்றும் பாதிக்கப்பட்ட இலைகளை அகற்றவும்."

        return jsonify({
            'success': True,
            'disease': predicted_class,
            'confidence': f"{confidence}%",
            'recommendation': recommendation
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000, debug=True)