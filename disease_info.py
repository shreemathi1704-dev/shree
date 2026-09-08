DISEASE_INFO = {

    "Healthy": {
        "description":
            "The crop leaf appears healthy with no major visible disease symptoms.",

        "severity":
            "None",

        "recommendation":
            "Continue regular monitoring, proper irrigation, balanced nutrition and good field management."
    },

    "Tomato Early Blight": {
        "description":
            "Early blight is a fungal disease that can cause dark circular lesions and leaf damage.",

        "severity":
            "Moderate",

        "recommendation":
            "Remove severely affected leaves, improve airflow around plants and avoid unnecessary overhead watering. Consult a local agricultural expert for treatment decisions."
    },

    "Tomato Late Blight": {
        "description":
            "Late blight can produce dark lesions and may spread rapidly under favorable environmental conditions.",

        "severity":
            "High",

        "recommendation":
            "Monitor affected plants and nearby plants carefully. Remove severely infected material where appropriate and seek local agricultural guidance."
    },

    "Potato Early Blight": {
        "description":
            "Potato early blight commonly produces dark lesions on leaves.",

        "severity":
            "Moderate",

        "recommendation":
            "Remove severely affected plant material and maintain good field sanitation."
    },

    "Potato Late Blight": {
        "description":
            "Potato late blight can spread rapidly and cause serious crop damage.",

        "severity":
            "High",

        "recommendation":
            "Monitor the field carefully and obtain region-specific disease-management advice from an agricultural expert."
    },

    "Rice Blast": {
        "description":
            "Rice blast is a fungal disease that can affect rice leaves and other plant parts.",

        "severity":
            "High",

        "recommendation":
            "Monitor the crop regularly and follow region-specific agricultural disease-management recommendations."
    }
}


def get_disease_info(disease):

    return DISEASE_INFO.get(
        disease,
        {
            "description":
                "Information for this prediction is unavailable.",

            "severity":
                "Unknown",

            "recommendation":
                "Consult an agricultural expert."
        }
    )