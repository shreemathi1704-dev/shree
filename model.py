import os
import numpy as np
import tensorflow as tf

MODEL_PATH = "crop_disease_model.keras"

# IMPORTANT:
# These names MUST be in the exact same order
# as the classes used when training your CNN.
CLASS_NAMES = [
    "Healthy",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Potato Early Blight",
    "Potato Late Blight",
    "Rice Blast"
]

model = None


def load_model():
    global model

    if model is not None:
        return model

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "crop_disease_model.keras not found. "
            "Place your trained model in the project folder."
        )

    print("Loading CNN model...")

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    print("CNN model loaded successfully.")

    return model


def predict_disease(image_path):

    loaded_model = load_model()

    # Load image
    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224),
        color_mode="rgb"
    )

    # Convert image to array
    image_array = tf.keras.utils.img_to_array(image)

    # Normalize
    image_array = image_array / 255.0

    # Add batch dimension
    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # Prediction
    predictions = loaded_model.predict(
        image_array,
        verbose=0
    )[0]

    # Check number of classes
    if len(predictions) != len(CLASS_NAMES):
        raise ValueError(
            f"Model has {len(predictions)} outputs, "
            f"but CLASS_NAMES contains {len(CLASS_NAMES)} classes."
        )

    # Find highest probability
    class_index = int(np.argmax(predictions))

    confidence = float(
        predictions[class_index] * 100
    )

    disease = CLASS_NAMES[class_index]

    return {
        "disease": disease,
        "confidence": round(confidence, 2),
        "mode": "CNN AI"
    }