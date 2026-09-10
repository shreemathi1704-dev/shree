from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# GitHub Pages frontend-க்கு permission
CORS(app)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return jsonify({
        "success": True,
        "project": "AgriGuard AI",
        "message": "Flask Backend is Running Successfully!"
    })


# =========================
# HEALTH CHECK
# =========================

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "status": "online",
        "message": "AgriGuard AI Backend Connected"
    })


# =========================
# CROP ANALYSIS
# =========================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        image = request.files.get("image")

        if image is None:
            return jsonify({
                "success": False,
                "message": "No image received"
            }), 400

        # Image filename
        filename = image.filename

        print("Received image:", filename)

        # Demo AI result
        # Later replace this with your CNN model
        result = {
            "success": True,

            "crop_disease": {
                "disease": "Tomato Early Blight",
                "confidence": 94.5,
                "severity": "Moderate",
                "description":
                    "Possible early blight detected on the crop leaf.",
                "recommendation":
                    "Remove severely affected leaves and monitor the crop."
            },

            "satellite": {
                "success": True,
                "satellite": "Sentinel-2",
                "ndvi": 0.65,
                "field_condition": "Healthy",
                "message":
                    "Satellite analysis completed."
            }
        }

        return jsonify(result)

    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":

    port = int(
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