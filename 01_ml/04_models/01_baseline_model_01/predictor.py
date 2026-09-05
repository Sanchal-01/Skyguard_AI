
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model


# Find the project root from this file location
PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "01_ml" / "04_models" / "01_baseline_model_01"


# Load trained artifacts
imputer = joblib.load(
    MODELS_DIR / "imputer.pkl"
)

scaler = joblib.load(
    MODELS_DIR / "scaler.pkl"
)

label_encoder = joblib.load(
    MODELS_DIR / "label_encoder.pkl"
)

model = load_model(
    MODELS_DIR / "anomaly_model.keras"
)


# Features expected by the model
FEATURES = [
    "avg_temp",
    "min_temp",
    "max_temp",
    "relative_humidity",
    "wind_speed",
    "air_pressure",
    "rainfall",
    "elevation",
    "latitude",
    "longitude",
]


def predict(weather_data):
    """
    Predict the anomaly category for one AWS observation.

    Parameters
    ----------
    weather_data : dict
        Dictionary containing the 10 weather features.

    Returns
    -------
    dict
        Prediction, class ID and confidence.
    """

    # Convert input data into a DataFrame
    input_df = pd.DataFrame(
        [weather_data],
        columns=FEATURES
    )

    # Apply the same preprocessing used during training
    input_imputed = imputer.transform(input_df)

    # Convert back to DataFrame so feature names are preserved
    input_imputed_df = pd.DataFrame(
        input_imputed,
        columns=FEATURES
    )

    input_scaled = scaler.transform(
        input_imputed_df
    )

    # Get class probabilities
    probabilities = model.predict(
        input_scaled,
        verbose=0
    )[0]

    # Select the class with the highest probability
    predicted_id = int(
        np.argmax(probabilities)
    )

    predicted_class = label_encoder.inverse_transform(
        [predicted_id]
    )[0]

    confidence = float(
        probabilities[predicted_id]
    )

    return {
        "prediction": predicted_class,
        "prediction_id": predicted_id,
        "confidence": confidence,
        "model": "baseline_mlp_soft_weights"
    }
