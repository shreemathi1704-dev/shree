import ee
from datetime import datetime, timedelta


# CHANGE THIS
# Put your Google Earth Engine Cloud Project ID here.
PROJECT_ID = "YOUR_PROJECT_ID"

earth_engine_ready = False


def initialize_earth_engine():

    global earth_engine_ready

    if earth_engine_ready:
        return

    try:

        ee.Initialize(
            project=PROJECT_ID
        )

        earth_engine_ready = True

        print(
            "Google Earth Engine connected."
        )

    except Exception as error:

        print(
            "Earth Engine authentication required."
        )

        print(error)

        ee.Authenticate()

        ee.Initialize(
            project=PROJECT_ID
        )

        earth_engine_ready = True

        print(
            "Google Earth Engine connected."
        )


def get_satellite_data(
    latitude,
    longitude
):

    initialize_earth_engine()

    latitude = float(latitude)
    longitude = float(longitude)

    point = ee.Geometry.Point(
        [
            longitude,
            latitude
        ]
    )

    # Last 60 days
    end_date = datetime.utcnow()

    start_date = (
        end_date -
        timedelta(days=60)
    )

    start = start_date.strftime(
        "%Y-%m-%d"
    )

    end = end_date.strftime(
        "%Y-%m-%d"
    )

    # Sentinel-2
    collection = (
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
        collection
        .size()
        .getInfo()
    )

    print(
        "Sentinel-2 images:",
        number_of_images
    )

    if number_of_images == 0:

        return {
            "success": False,
            "message":
                "No suitable Sentinel-2 image found."
        }

    # Median image
    image = collection.median()

    # NDVI = (NIR - RED) / (NIR + RED)
    #
    # Sentinel-2:
    # B8 = NIR
    # B4 = RED

    ndvi_image = (
        image
        .normalizedDifference(
            ["B8", "B4"]
        )
        .rename("NDVI")
    )

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

    # Field condition
    if ndvi < 0.20:

        field_status = "Very Low Vegetation"
        field_condition = "Critical"

    elif ndvi < 0.35:

        field_status = "Low Vegetation"
        field_condition = "High Stress"

    elif ndvi < 0.50:

        field_status = "Moderate Vegetation"
        field_condition = "Moderate Stress"

    elif ndvi < 0.70:

        field_status = "Healthy Vegetation"
        field_condition = "Healthy"

    else:

        field_status = "Very Healthy Vegetation"
        field_condition = "Very Healthy"

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
            field_status,

        "field_condition":
            field_condition,

        "images_found":
            number_of_images
    }