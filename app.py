from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from satellite import get_ndvi


# =====================================================
# CREATE FLASK APP
# =====================================================

app = Flask(__name__)


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =====================================================
# SATELLITE API
# =====================================================

@app.route(
    "/satellite",
    methods=["POST"]
)
def satellite():

    try:

        data = request.get_json()

        latitude = data.get(
            "latitude"
        )

        longitude = data.get(
            "longitude"
        )

        if latitude is None:

            return jsonify({

                "success": False,

                "message":
                    "Latitude is missing."
            })

        if longitude is None:

            return jsonify({

                "success": False,

                "message":
                    "Longitude is missing."
            })

        result = get_ndvi(
            latitude,
            longitude
        )

        return jsonify(
            result
        )

    except Exception as error:

        print(
            "ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "message":
                str(error)
        })


# =====================================================
# RUN SERVER
# =====================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )