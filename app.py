import os
import uuid

from flask import (
    Flask,
    request,
    jsonify
)

from flask_cors import CORS

from PIL import Image

from model import predict_disease

from disease_info import get_disease_info

from satellite import get_ndvi


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)


# ==========================================
# UPLOAD FOLDER
# ==========================================

UPLOAD_FOLDER = "uploads"

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


# ==========================================
# HOME
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "application":
            "AgriGuard AI",

        "status":
            "running",

        "services": [

            "Crop Disease Detection",

            "CNN AI",

            "GPS",

            "Google Earth Engine",

            "Sentinel-2 NDVI"

        ]

    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status":
            "running",

        "application":
            "AgriGuard AI",

        "cnn":
            "available",

        "satellite":
            "Google Earth Engine / Sentinel-2"

    })


# ==========================================
# ANALYZE
# ==========================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        # ------------------------------
        # IMAGE
        # ------------------------------

        image =
            request.files.get(
                "image"
            )

        if (
            image is None or
            image.filename == ""
        ):

            return jsonify({

                "success":
                    False,

                "message":
                    "Please capture or upload a crop image."

            }), 400


        # ------------------------------
        # FILE EXTENSION
        # ------------------------------

        if "." not in image.filename:

            return jsonify({

                "success":
                    False,

                "message":
                    "Invalid image file."

            }), 400


        extension =
            image.filename.rsplit(
                ".",
                1
            )[1].lower()


        if extension not in ALLOWED_EXTENSIONS:

            return jsonify({

                "success":
                    False,

                "message":
                    "Only JPG, JPEG, PNG and WEBP are allowed."

            }), 400


        # ------------------------------
        # CREATE FILE
        # ------------------------------

        filename =
            f"{uuid.uuid4().hex}.{extension}"


        image_path =
            os.path.join(
                UPLOAD_FOLDER,
                filename
            )


        image.save(
            image_path
        )


        # ------------------------------
        # VERIFY IMAGE
        # ------------------------------

        with Image.open(
            image_path
        ) as img:

            img.verify()


        # ------------------------------
        # CNN PREDICTION
        # ------------------------------

        prediction =
            predict_disease(
                image_path
            )


        disease =
            prediction["disease"]


        # ------------------------------
        # DISEASE INFORMATION
        # ------------------------------

        info =
            get_disease_info(
                disease
            )


        # ------------------------------
        # GPS
        # ------------------------------

        latitude =
            request.form.get(
                "latitude"
            )


        longitude =
            request.form.get(
                "longitude"
            )


        satellite = {

            "success":
                False,

            "message":
                "GPS not provided. Allow location permission for Sentinel-2 analysis."

        }


        # ------------------------------
        # SATELLITE
        # ------------------------------

        if (
            latitude and
            longitude
        ):

            try:

                satellite =
                    get_ndvi(

                        float(latitude),

                        float(longitude)

                    )

            except Exception as error:

                print(
                    "Satellite error:",
                    error
                )


                satellite = {

                    "success":
                        False,

                    "message":
                        "Satellite analysis failed.",

                    "error":
                        str(error)

                }


        # ------------------------------
        # RESPONSE
        # ------------------------------

        result = {

            "success":
                True,

            "crop_disease": {

                "disease":
                    prediction["disease"],

                "confidence":
                    prediction["confidence"],

                "prediction_mode":
                    prediction["mode"],

                "severity":
                    info["severity"],

                "description":
                    info["description"],

                "recommendation":
                    info["recommendation"]

            },

            "satellite":
                satellite

        }


        return jsonify(
            result
        )


    except Exception as error:

        print(
            "ANALYSIS ERROR:",
            error
        )


        return jsonify({

            "success":
                False,

            "message":
                "Analysis failed.",

            "error":
                str(error)

        }), 500


    finally:

        # ------------------------------
        # DELETE UPLOAD
        # ------------------------------

        try:

            if os.path.exists(
                image_path
            ):

                os.remove(
                    image_path
                )

        except Exception:

            pass


# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":

    port =
        int(
            os.environ.get(
                "PORT",
                5000
            )
        )


    app.run(

        host="0.0.0.0",

        port=port,

        debug=True

    )