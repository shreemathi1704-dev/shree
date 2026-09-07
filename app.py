import os
import uuid

from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory
)

from werkzeug.utils import secure_filename

from model import (
    load_model,
    load_class_names,
    predict_image
)

from disease_info import (
    get_disease_info
)

from database import (
    initialize_database,
    save_prediction,
    get_predictions
)


# ==========================================
# APPLICATION
# ==========================================

app = Flask(__name__)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads"
)


os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_DIR


ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


# ==========================================
# FILE VALIDATION
# ==========================================

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


# ==========================================
# FRONTEND
# ==========================================

@app.route("/")
def index():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


@app.route("/<path:filename>")
def frontend_file(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "success",
        "message": "AgriGuard AI is running"
    })


# ==========================================
# AI PREDICTION
# ==========================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    try:

        if "image" not in request.files:

            return jsonify({
                "status": "error",
                "message": "No image received."
            }), 400


        image = request.files[
            "image"
        ]


        if image.filename == "":

            return jsonify({
                "status": "error",
                "message": "Empty image."
            }), 400


        if not allowed_file(
            image.filename
        ):

            return jsonify({
                "status": "error",
                "message":
                    "Invalid image format."
            }), 400


        # Create unique filename
        original_name = secure_filename(
            image.filename
        )

        extension = os.path.splitext(
            original_name
        )[1]

        filename = (
            str(uuid.uuid4())
            + extension
        )


        image_path = os.path.join(
            UPLOAD_DIR,
            filename
        )


        image.save(
            image_path
        )


        # AI prediction
        predicted_class, confidence = (
            predict_image(
                image_path
            )
        )


        # Get solution
        info = get_disease_info(
            predicted_class
        )


        crop = info["crop"]

        disease = info["disease"]

        solution = info["solution"]

        prevention = info["prevention"]


        # ----------------------------------
        # Severity
        # ----------------------------------

        if disease.lower() == "healthy":

            severity = "Healthy"

        elif confidence >= 90:

            severity = info.get(
                "severity",
                "Moderate"
            )

        elif confidence >= 70:

            severity = "Mild"

        else:

            severity = "Low Confidence"


        # ----------------------------------
        # Save history
        # ----------------------------------

        save_prediction(

            image_name=filename,

            crop=crop,

            disease=disease,

            confidence=round(
                confidence,
                2
            ),

            severity=severity,

            solution="; ".join(
                solution
            )

        )


        # ----------------------------------
        # Response
        # ----------------------------------

        return jsonify({

            "status": "success",

            "crop": crop,

            "disease": disease,

            "confidence": round(
                confidence,
                2
            ),

            "severity": severity,

            "solution": solution,

            "prevention": prevention

        })


    except Exception as error:

        print(
            "Prediction error:",
            error
        )

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


# ==========================================
# HISTORY
# ==========================================

@app.route(
    "/api/history",
    methods=["GET"]
)
def history():

    try:

        data = get_predictions()

        return jsonify({

            "status": "success",

            "data": data

        })

    except Exception as error:

        return jsonify({

            "status": "error",

            "message": str(error)

        }), 500


# ==========================================
# START
# ==========================================

if __name__ == "__main__":

    initialize_database()

    load_class_names()

    load_model()

    print("")
    print(
        "===================================="
    )
    print(
        "       AGRIGUARD AI"
    )
    print(
        "   LIVE CROP DISEASE SCANNER"
    )
    print(
        "===================================="
    )
    print(
        "Open: http://127.0.0.1:5000"
    )
    print(
        "===================================="
    )
    print("")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )