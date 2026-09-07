import os
import json
import numpy as np
import tensorflow as tf

from PIL import Image


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "crop_disease_model.keras"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "model",
    "class_names.json"
)

IMAGE_SIZE = (224, 224)

model = None
class_names = []


def load_model():

    global model

    if not os.path.exists(MODEL_PATH):

        print("Model not found:")
        print(MODEL_PATH)

        return False

    try:

        model = tf.keras.models.load_model(
            MODEL_PATH
        )

        print("AI model loaded successfully.")

        return True

    except Exception as e:

        print("Model loading error:", e)

        return False


def load_class_names():

    global class_names

    if not os.path.exists(CLASS_NAMES_PATH):

        print("class_names.json not found.")

        return False

    try:

        with open(
            CLASS_NAMES_PATH,
            "r"
        ) as file:

            class_names = json.load(file)

        print(
            "Classes loaded:",
            class_names
        )

        return True

    except Exception as e:

        print(
            "Class loading error:",
            e
        )

        return False


def prepare_image(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    image = image.resize(
        IMAGE_SIZE
    )

    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = image_array / 255.0

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


def predict_image(image_path):

    global model
    global class_names

    if model is None:

        if not load_model():

            raise Exception(
                "AI model is not available."
            )

    if not class_names:

        if not load_class_names():

            raise Exception(
                "Class names are not available."
            )

    image = prepare_image(
        image_path
    )

    prediction = model.predict(
        image,
        verbose=0
    )[0]

    index = int(
        np.argmax(prediction)
    )

    confidence = float(
        prediction[index] * 100
    )

    predicted_class = class_names[index]

    return predicted_class, confidence