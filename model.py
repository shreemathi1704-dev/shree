import os

import numpy as np

from PIL import Image


# ==========================================
# MODEL LOCATION
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "crop_disease_model.keras"
)


# ==========================================
# CLASS NAMES
# ==========================================

CLASS_NAMES = [

    "Healthy",

    "Tomato Early Blight",

    "Tomato Late Blight",

    "Potato Early Blight",

    "Potato Late Blight",

    "Rice Blast"

]


_model = None


# ==========================================
# LOAD MODEL
# ==========================================

def load_model():

    global _model


    if _model is not None:

        return _model


    if not os.path.exists(
        MODEL_PATH
    ):

        print(
            "WARNING: CNN model not found:"
        )

        print(
            MODEL_PATH
        )

        return None


    try:

        import tensorflow as tf


        _model =
            tf.keras.models.load_model(
                MODEL_PATH
            )


        print(
            "CNN model loaded successfully."
        )


        return _model


    except Exception as error:

        print(
            "CNN model loading error:"
        )

        print(
            error
        )


        return None


# ==========================================
# PREDICT
# ==========================================

def predict_disease(
    image_path
):

    model =
        load_model()


    # ======================================
    # MODEL NOT FOUND
    # ======================================

    if model is None:

        return {

            "disease":
                "AI model not installed",

            "confidence":
                0.0,

            "mode":
                "Backend running - CNN model required"

        }


    # ======================================
    # IMAGE
    # ======================================

    image =
        Image.open(
            image_path
        ).convert(
            "RGB"
        )


    # ======================================
    # RESIZE
    # ======================================

    image =
        image.resize(
            (224, 224)
        )


    # ======================================
    # NUMPY
    # ======================================

    array =
        np.asarray(
            image,
            dtype=np.float32
        )


    # ======================================
    # NORMALIZATION
    # ======================================

    array =
        array / 255.0


    # ======================================
    # BATCH DIMENSION
    # ======================================

    array =
        np.expand_dims(
            array,
            axis=0
        )


    # ======================================
    # PREDICTION
    # ======================================

    predictions =
        model.predict(
            array,
            verbose=0
        )[0]


    # ======================================
    # BEST CLASS
    # ======================================

    index =
        int(
            np.argmax(
                predictions
            )
        )


    confidence =
        float(
            predictions[index]
        ) * 100


    # ======================================
    # CLASS
    # ======================================

    if index >= len(
        CLASS_NAMES
    ):

        disease =
            "Unknown"

    else:

        disease =
            CLASS_NAMES[index]


    return {

        "disease":
            disease,

        "confidence":
            round(
                confidence,
                2
            ),

        "mode":
            "CNN AI Model"

    }