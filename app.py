from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

import os
import uuid

from model import predict_disease
from disease_info import get_disease_info
from satellite import get_satellite_data


app = Flask(__name__)


# Upload folder
UPLOAD_FOLDER = "uploads"

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER

# Maximum upload = 10 MB
app.config[
    "MAX_CONTENT_LENGTH"
] = 10 * 1024 * 1024


# Create upload folder
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# ------------------------------------------------
# HOME
# ------------------------------------------------

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------

@app.route("/health")
def health():

    return jsonify({

        "success": True,

        "application":
            "CropCare AI",

        "status":
            "running",

        "services": [

            "Google Lens Style Camera",

            "CNN Crop Disease Detection",

            "GPS",

            "Sentinel-2 NDVI"

        ]

    })


# ------------------------------------------------
# CROP IMAGE PREDICTION
# ------------------------------------------------

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # Check image
        if "image" not in request.files:

            return jsonify({

                "success": False,

                "message":
                    "No image received."

            })


        image = request.files[
            "image"
        ]


        if image.filename == "":

            return jsonify({

                "success": False,

                "message":
                    "Please select an image."

            })


        # Check file type
        if not allowed_file(
            image.filename
        ):

            return jsonify({

                "success": False,

                "message":
                    "Invalid image format."

            })


        # Create unique filename
        extension = os.path.splitext(
            image.filename
        )[1].lower()

        filename = (
            str(uuid.uuid4())
            +
            extension
        )

        image_path = os.path.join(
            app.config[
                "UPLOAD_FOLDER"
            ],
            filename
        )


        # Save image
        image.save(
            image_path
        )


        print(
            "Image saved:",
            image_path
        )


        # ----------------------------------------
        # CNN PREDICTION
        # ----------------------------------------

        prediction = predict_disease(
            image_path
        )


        disease = prediction[
            "disease"
        ]

        confidence = prediction[
            "confidence"
        ]


        # ----------------------------------------
        # DISEASE INFORMATION
        # ----------------------------------------

        info = get_disease_info(
            disease
        )


        # ----------------------------------------
        # GPS
        # ----------------------------------------

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )


        satellite_result = None


        # ----------------------------------------
        # SATELLITE
        # ----------------------------------------

        if (
            latitude
            and
            longitude
        ):

            try:

                satellite_result = (
                    get_satellite_data(
                        latitude,
                        longitude
                    )
                )

            except Exception as satellite_error:

                print(
                    "Satellite error:",
                    satellite_error
                )

                satellite_result = {

                    "success":
                        False,

                    "message":
                        "Satellite analysis failed."

                }


        # ----------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------

        response = {

            "success":
                True,

            "crop_disease": {

                "disease":
                    disease,

                "confidence":
                    confidence,

                "severity":
                    info["severity"],

                "description":
                    info["description"],

                "recommendation":
                    info["recommendation"],

                "prediction_mode":
                    prediction["mode"]

            },

            "gps": {

                "latitude":
                    latitude,

                "longitude":
                    longitude

            },

            "satellite":
                satellite_result

        }


        # Delete temporary image
        try:

            os.remove(
                image_path
            )

        except Exception:

            pass


        return jsonify(
            response
        )


    except Exception as error:

        print(
            "Prediction error:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Prediction failed.",

            "error":
                str(error)

        })


# ------------------------------------------------
# RUN
# ------------------------------------------------

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )