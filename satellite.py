import ee
from datetime import datetime, timedelta


# =====================================================
# PUT YOUR GOOGLE CLOUD PROJECT ID HERE
# =====================================================

PROJECT_ID = "YOUR_PROJECT_ID"


earth_engine_ready = False


# =====================================================
# INITIALIZE GOOGLE EARTH ENGINE
# =====================================================

def initialize_earth_engine():

    global earth_engine_ready

    if earth_engine_ready:
        return

    try:

        ee.Initialize(
            project=PROJECT_ID
        )

        earth_engine_ready = True

        print("Earth Engine connected successfully.")

    except Exception as error:

        print("Earth Engine authentication required.")

        ee.Authenticate()

        ee.Initialize(
            project=PROJECT_ID
        )

        earth_engine_ready = True

        print("Earth Engine connected successfully.")


# =====================================================
# GET NDVI FROM SENTINEL-2
# =====================================================

def get_ndvi(latitude, longitude):

    initialize_earth_engine()

    latitude = float(latitude)
    longitude = float(longitude)

    # GPS point
    point = ee.Geometry.Point(
        [
            longitude,
            latitude
        ]
    )

    # Last 60 days
    end_date = datetime.utcnow()

    start_date = (
        end_date - timedelta(days=60)
    )

    start = start_date.strftime(
        "%Y-%m-%d"
    )

    end = end_date.strftime(
        "%Y-%m-%d"
    )

    # =================================================
    # SENTINEL-2 COLLECTION
    # =================================================

    images = (
        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )
        .filterBounds(point)
        .filterDate(
            start,
            end
        )
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                30
            )
        )
    )

    number_of_images = (
        images.size().getInfo()
    )

    print(
        "Satellite images found:",
        number_of_images
    )

    if number_of_images == 0:

        return {

            "success": False,

            "message":
                "No suitable Sentinel-2 image found."
        }

    # =================================================
    # CREATE MEDIAN IMAGE
    # =================================================

    image = images.median()

    # =================================================
    # NDVI
    #
    # NDVI = (NIR - RED) / (NIR + RED)
    #
    # Sentinel-2:
    # B8 = NIR
    # B4 = RED
    # =================================================

    ndvi_image = (
        image
        .normalizedDifference(
            [
                "B8",
                "B4"
            ]
        )
        .rename("NDVI")
    )

    # =================================================
    # GET NDVI AT GPS LOCATION
    # =================================================

    result = (
        ndvi_image
        .reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10,
            maxPixels=100000
        )
        .getInfo()
    )

    ndvi = result.get(
        "NDVI"
    )

    if ndvi is None:

        return {

            "success": False,

            "message":
                "NDVI value unavailable."
        }

    ndvi = round(
        float(ndvi),
        3
    )

    # =================================================
    # FIELD HEALTH
    # =================================================

    if ndvi < 0.20:

        status = "Very Low Vegetation"

        condition = "Critical"

    elif ndvi < 0.35:

        status = "Low Vegetation"

        condition = "High Stress"

    elif ndvi < 0.50:

        status = "Moderate Vegetation"

        condition = "Moderate Stress"

    elif ndvi < 0.70:

        status = "Healthy Vegetation"

        condition = "Healthy"

    else:

        status = "Very Healthy Vegetation"

        condition = "Very Healthy"

    # =================================================
    # RETURN RESULT
    # =================================================

    return {

        "success": True,

        "satellite":
            "Sentinel-2",

        "latitude":
            latitude,

        "longitude":
            longitude,

        "ndvi":
            ndvi,

        "field_status":
            status,

        "field_condition":
            condition,

        "images_found":
            number_of_images
    }