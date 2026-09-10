DISEASE_INFO = {

    "Healthy": {

        "severity":
            "Healthy",

        "description":
            "The crop leaf appears healthy based on the AI classification.",

        "recommendation":
            "Continue regular monitoring, proper irrigation, balanced nutrition and good crop management."

    },


    "Tomato Early Blight": {

        "severity":
            "Moderate",

        "description":
            "The AI classification is consistent with characteristics commonly associated with tomato early blight.",

        "recommendation":
            "Remove severely affected leaves where practical, improve airflow and avoid unnecessary overhead watering. Consult local agricultural guidance."

    },


    "Tomato Late Blight": {

        "severity":
            "High",

        "description":
            "The AI classification is consistent with characteristics commonly associated with tomato late blight.",

        "recommendation":
            "Monitor affected and nearby plants carefully and seek region-specific agricultural guidance promptly."

    },


    "Potato Early Blight": {

        "severity":
            "Moderate",

        "description":
            "The AI classification is consistent with characteristics commonly associated with potato early blight.",

        "recommendation":
            "Maintain field sanitation, remove severely affected material where appropriate and monitor nearby plants."

    },


    "Potato Late Blight": {

        "severity":
            "High",

        "description":
            "The AI classification is consistent with characteristics commonly associated with potato late blight.",

        "recommendation":
            "Monitor the crop carefully and seek local agricultural guidance for appropriate disease-management decisions."

    },


    "Rice Blast": {

        "severity":
            "High",

        "description":
            "The AI classification is consistent with characteristics commonly associated with rice blast.",

        "recommendation":
            "Monitor the crop regularly and follow region-specific agricultural disease-management recommendations."

    },


    "AI model not installed": {

        "severity":
            "Not Available",

        "description":
            "The backend is working, but a trained crop disease CNN model has not been installed.",

        "recommendation":
            "Place your crop_disease_model.keras file inside backend/models/."

    }

}


def get_disease_info(
    disease
):

    return DISEASE_INFO.get(

        disease,

        {

            "severity":
                "Unknown",

            "description":
                "No information is available for this model class.",

            "recommendation":
                "Consult a qualified agricultural expert."

        }

    )