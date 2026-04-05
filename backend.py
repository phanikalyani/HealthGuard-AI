import numpy as np

def predict_diabetes_risk(preg, glucose, bp, skin, insulin, bmi, dpf, age):
    """
    AI-based risk scoring logic inspired by ML feature weighting.
    Returns probability between 0 and 1.
    """

    # Normalize values
    glucose_score = glucose / 200
    bmi_score = bmi / 50
    age_score = age / 90
    insulin_score = insulin / 300

    # Weighted risk calculation (ML-inspired)
    risk = (
        glucose_score * 0.35 +
        bmi_score * 0.25 +
        age_score * 0.20 +
        insulin_score * 0.10 +
        dpf * 0.10
    )

    # Clamp between 0 and 1
    return round(min(max(risk, 0.05), 0.95), 2)
