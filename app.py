import os
import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

from model import predict_disease
from disease_info import get_disease_info
from satellite import get_ndvi


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)

# Allow GitHub Pages / other frontend domains
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)


# --------------------------------------------------
# UPLOAD FOLDER
# --------------------------------------------------

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "success": True,
        "application": "AgriGuard AI",
        "message": "Flask backend is running successfully!",
        "services": [
            "CNN Crop Disease Detection",
            "GPS Location",
            "Sentinel-2 NDVI"
        ]
    })


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "success": True,
        "status": "online",
        "backend": "Flask",
        "application": "AgriGuard AI",
        "message": "Backend connection successful"
    })


# --------------------------------------------------
# ANALYZE CROP
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # -----------------------------
        # GET IMAGE
        # -----------------------------

        image = request.files.get("image")

        if image is None:

            return jsonify({
                "success": False,
                "message": "No crop image received."
            }), 400


        if image.filename == "":

            return jsonify({
                "success": False,
                "message": "Please select a crop image."
            }), 400


        # -----------------------------
        # CHECK FILE TYPE
        # -----------------------------

        extension = ""

        if "." in image.filename:
            extension = image.filename.rsplit(".", 1)[1].lower()


        if extension not in ALLOWED_EXTENSIONS:

            return jsonify({
                "success": False,
                "message": "Only JPG, JPEG, PNG and WEBP images are allowed."
            }), 400


        # -----------------------------
        # SAVE IMAGE
        # -----------------------------

        filename = str(uuid.uuid4()) + "." + extension

        image_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        image.save(image_path)


        # -----------------------------
        # CHECK IMAGE
        # -----------------------------

        try:

            with Image.open(image_path) as img:

                img.verify()

        except Exception:

            return jsonify({
                "success": False,
                "message": "Invalid image file."
            }), 400


        # -----------------------------
        # CNN PREDICTION
        # -----------------------------

        prediction = predict_disease(image_path)

        disease_name = prediction["disease"]

        confidence = prediction["confidence"]

        prediction_mode = prediction["mode"]


        # -----------------------------
        # DISEASE INFORMATION
        # -----------------------------

        disease_data = get_disease_info(
            disease_name
        )


        # -----------------------------
        # GET GPS
        # -----------------------------

        latitude = request.form.get(
            "latitude"
        )

        longitude = request.form.get(
            "longitude"
        )


        # -----------------------------
        # DEFAULT SATELLITE RESPONSE
        # -----------------------------

        satellite_result = {

            "success": False,

            "message":
            "GPS location was not provided.",

            "latitude": latitude,

            "longitude": longitude,

            "ndvi": None,

            "field_condition":
            "Unavailable",

            "images_found": 0
        }


        # -----------------------------
        # SENTINEL-2 ANALYSIS
        # -----------------------------

        if latitude and longitude:

            try:

                latitude = float(latitude)

                longitude = float(longitude)


                satellite_result = get_ndvi(
                    latitude,
                    longitude
                )

            except Exception as satellite_error:

                satellite_result = {

                    "success": False,

                    "message":
                    "Satellite analysis failed: "
                    + str(satellite_error),

                    "latitude": latitude,

                    "longitude": longitude,

                    "ndvi": None,

                    "field_condition":
                    "Unavailable",

                    "images_found": 0
                }


        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------

        response = {

            "success": True,

            "crop_disease": {

                "disease":
                disease_name,

                "confidence":
                confidence,

                "prediction_mode":
                prediction_mode,

                "severity":
                disease_data["severity"],

                "description":
                disease_data["description"],

                "recommendation":
                disease_data["recommendation"]
            },

            "satellite":
            satellite_result
        }


        return jsonify(response)


    except Exception as error:

        print(
            "ANALYZE ERROR:",
            str(error)
        )

        return jsonify({

            "success": False,

            "message":
            "Backend analysis error: "
            + str(error)

        }), 500


    finally:

        # -----------------------------
        # DELETE TEMP IMAGE
        # -----------------------------

        try:

            if "image_path" in locals():

                if os.path.exists(
                    image_path
                ):

                    os.remove(
                        image_path
                    )

        except Exception:

            pass


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    print()
    print("=" * 50)
    print("🌱 AgriGuard AI Flask Backend")
    print("=" * 50)
    print("Backend running on:")
    print(
        f"http://127.0.0.1:{port}"
    )
    print()
    print("Health check:")
    print(
        f"http://127.0.0.1:{port}/health"
    )
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )