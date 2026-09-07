DISEASE_INFO = {

    "Tomato_Early_Blight": {
        "crop": "Tomato",
        "disease": "Early Blight",
        "severity": "Moderate",
        "solution": [
            "Remove and destroy severely affected leaves.",
            "Improve air circulation between plants.",
            "Avoid overhead watering.",
            "Keep the area around the plants clean.",
            "Use an appropriate fungicide according to the product label and local agricultural guidance."
        ],
        "prevention": [
            "Maintain proper spacing between plants.",
            "Avoid keeping leaves wet for long periods.",
            "Remove infected plant debris.",
            "Monitor plants regularly."
        ]
    },

    "Tomato_Late_Blight": {
        "crop": "Tomato",
        "disease": "Late Blight",
        "severity": "Severe",
        "solution": [
            "Remove severely infected plant parts.",
            "Separate heavily infected plants where practical.",
            "Avoid overhead irrigation.",
            "Improve field ventilation.",
            "Consult an agricultural expert for an appropriate fungicide."
        ],
        "prevention": [
            "Monitor plants frequently.",
            "Avoid prolonged leaf wetness.",
            "Maintain good field sanitation.",
            "Use healthy planting material."
        ]
    },

    "Tomato_Healthy": {
        "crop": "Tomato",
        "disease": "Healthy",
        "severity": "Healthy",
        "solution": [
            "No visible disease was detected.",
            "Continue normal irrigation and nutrition.",
            "Keep monitoring the crop regularly."
        ],
        "prevention": [
            "Inspect leaves regularly.",
            "Maintain good field hygiene."
        ]
    },

    "Potato_Early_Blight": {
        "crop": "Potato",
        "disease": "Early Blight",
        "severity": "Moderate",
        "solution": [
            "Remove infected leaves.",
            "Keep the field free from infected plant debris.",
            "Avoid unnecessary leaf wetness.",
            "Improve air circulation.",
            "Use an appropriate fungicide according to local agricultural guidance."
        ],
        "prevention": [
            "Practice crop rotation.",
            "Use healthy planting material.",
            "Monitor plants regularly."
        ]
    },

    "Potato_Late_Blight": {
        "crop": "Potato",
        "disease": "Late Blight",
        "severity": "Severe",
        "solution": [
            "Remove severely affected plant parts.",
            "Reduce excessive moisture around plants.",
            "Improve field ventilation.",
            "Consult an agricultural expert for suitable treatment."
        ],
        "prevention": [
            "Monitor the crop frequently.",
            "Avoid prolonged leaf wetness.",
            "Maintain field sanitation."
        ]
    },

    "Potato_Healthy": {
        "crop": "Potato",
        "disease": "Healthy",
        "severity": "Healthy",
        "solution": [
            "No visible disease was detected.",
            "Continue normal crop care.",
            "Keep monitoring the crop."
        ],
        "prevention": [
            "Regularly inspect leaves.",
            "Maintain proper irrigation."
        ]
    },

    "Paddy_Bacterial_Leaf_Blight": {
        "crop": "Paddy",
        "disease": "Bacterial Leaf Blight",
        "severity": "Moderate",
        "solution": [
            "Monitor the affected area carefully.",
            "Avoid excessive nitrogen application.",
            "Maintain proper water management.",
            "Use healthy planting material.",
            "Consult an agricultural expert for locally suitable treatment."
        ],
        "prevention": [
            "Use healthy seeds or seedlings.",
            "Maintain proper field hygiene.",
            "Regularly monitor the crop."
        ]
    },

    "Paddy_Healthy": {
        "crop": "Paddy",
        "disease": "Healthy",
        "severity": "Healthy",
        "solution": [
            "No visible disease was detected.",
            "Continue normal crop management.",
            "Continue regular monitoring."
        ],
        "prevention": [
            "Maintain proper irrigation.",
            "Inspect the crop regularly."
        ]
    }
}


def get_disease_info(class_name):

    if class_name in DISEASE_INFO:
        return DISEASE_INFO[class_name]

    clean_name = class_name.replace("_", " ")

    parts = class_name.split("_")

    crop = parts[0]

    disease = " ".join(parts[1:])

    return {
        "crop": crop,
        "disease": disease,
        "severity": "Unknown",
        "solution": [
            "The detected condition is not yet in the recommendation database.",
            "Monitor the crop carefully.",
            "Consult a local agricultural expert before applying treatment."
        ],
        "prevention": [
            "Continue regular crop monitoring."
        ]
    }