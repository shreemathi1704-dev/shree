import os
import json

from datetime import datetime, timedelta

import ee


# ==========================================
# EARTH ENGINE PROJECT
# ==========================================

PROJECT_ID = os.environ.get(
    "EE_PROJECT_ID",
    "YOUR_EARTH_ENGINE_PROJECT_ID"
)


_initialized = False


# ==========================================
# INITIALIZE EARTH ENGINE
# ==========================================

def initialize_earth_engine():

    global _initialized


    if _initialized:

        return


    service_json =
        os.environ.get(
            "EE_SERVICE_ACCOUNT_JSON"
        )


    # ======================================
    # DEPLOYED SERVER
    # ======================================

    if service_json:

        info =
            json.loads(
                service_json
            )


        credentials =
            ee.ServiceAccountCredentials(

                info["client_email"],

                key_data=service_json

            )


        ee.Initialize(

            credentials=credentials,

            project=PROJECT_ID

        )


    # ======================================
    # LOCAL COMPUTER
    # ======================================

    else:

        ee.Initialize(
            project=PROJECT_ID
        )


    _initialized = True


# ==========================================
# NDVI
# ==========================================

def get_ndvi(
    latitude,
    longitude
):

    initialize_earth_engine()


    latitude =
        float(latitude)


    longitude =
        float(longitude)


    # ======================================
    # GPS POINT
    # ======================================

    point =
        ee.Geometry.Point(
            [
                longitude,
                latitude
            ]
        )


    # ======================================
    # DATE RANGE
    # ======================================

    end_date =
        datetime.utcnow()


    start_date =
        end_date - timedelta(
            days=60
        )


    start =
        start_date.strftime(
            "%Y-%m-%d"
        )


    end =
        end_date.strftime(
            "%Y-%m-%d"
        )


    # ======================================
    # SENTINEL-2
    # ======================================

    collection = (

        ee.ImageCollection(
            "COPERNICUS/S2_SR_HARMONIZED"
        )

        .filterBounds(
            point
        )

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


    # ======================================
    # IMAGE COUNT
    # ======================================

    count =
        int(
            collection
            .size()
            .getInfo()
        )


    print(
        "Sentinel-2 images:",
        count
    )


    if count == 0:

        return {

            "success":
                False,

            "message":
                "No suitable Sentinel-2 image found for this location.",

            "latitude":
                latitude,

            "longitude":
                longitude,

            "images_found":
                0

        }


    # ======================================
    # MEDIAN IMAGE
    # ======================================

    image =
        collection.median()


    # ======================================
    # NDVI
    #
    # NDVI = (NIR - RED)
    #        --------------
    #        (NIR + RED)
    #
    # Sentinel-2:
    # B8 = NIR
    # B4 = RED
    # ======================================

    ndvi_image = (

        image
        .normalizedDifference(
            [
                "B8",
                "B4"
            ]
        )

        .rename(
            "NDVI"
        )

    )


    # ======================================
    # GET VALUE
    # ======================================

    result = (

        ndvi_image

        .reduceRegion(

            reducer=
                ee.Reducer.mean(),

            geometry=
                point,

            scale=
                10,

            maxPixels=
                100000

        )

        .getInfo()

    )


    ndvi =
        result.get(
            "NDVI"
        )


    if ndvi is None:

        return {

            "success":
                False,

            "message":
                "NDVI value unavailable at this location.",

            "latitude":
                latitude,

            "longitude":
                longitude,

            "images_found":
                count

        }


    ndvi =
        round(
            float(ndvi),
            3
        )


    # ======================================
    # FIELD CONDITION
    # ======================================

    if ndvi < 0.20:

        field_status =
            "Very Low Vegetation"

        field_condition =
            "Critical"


    elif ndvi < 0.35:

        field_status =
            "Low Vegetation"

        field_condition =
            "High Stress"


    elif ndvi < 0.50:

        field_status =
            "Moderate Vegetation"

        field_condition =
            "Moderate Stress"


    elif ndvi < 0.70:

        field_status =
            "Healthy Vegetation"

        field_condition =
            "Healthy"


    else:

        field_status =
            "Very Healthy Vegetation"

        field_condition =
            "Very Healthy"


    # ======================================
    # RESPONSE
    # ======================================

    return {

        "success":
            True,

        "satellite":
            "Sentinel-2 SR Harmonized",

        "message":
            "Connected to Google Earth Engine. NDVI calculated from Sentinel-2 imagery.",

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
            count

    }