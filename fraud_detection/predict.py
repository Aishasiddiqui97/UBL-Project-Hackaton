"""
predict.py
----------
Loads the trained RandomForest model and label encoders, then exposes
a single public function `predict_transaction` that returns the fraud
probability and binary prediction label for an incoming transaction.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Artifact paths ─────────────────────────────────────────────────────────────
MODEL_PATH   = Path("fraud_detection/model.pkl")
ENCODER_PATH = Path("fraud_detection/encoder.pkl")

# ── Feature order must match training ─────────────────────────────────────────
FEATURE_COLUMNS = [
    "amount",
    "transaction_count",
    "is_new_location",
    "location",
    "transaction_type",
    "device_type",
]

CATEGORICAL_FEATURES = ["location", "transaction_type", "device_type"]


def _load_artifacts() -> tuple[Any, dict]:
    """Load model and encoder from disk.

    Returns:
        Tuple of (model, encoder_dict).

    Raises:
        FileNotFoundError: If either artifact is missing.
    """
    for path in (MODEL_PATH, ENCODER_PATH):
        if not path.exists():
            raise FileNotFoundError(
                f"Artifact not found: '{path}'. "
                "Run fraud_detection/train_model.py first."
            )

    model        = joblib.load(MODEL_PATH)
    encoder_dict = joblib.load(ENCODER_PATH)
    logger.info("Model and encoders loaded successfully.")
    return model, encoder_dict


def _build_feature_row(
    data: dict[str, Any],
    encoder_dict: dict,
) -> pd.DataFrame:
    """Convert a raw transaction dict into an encoded feature DataFrame.

    Args:
        data:         Raw transaction dictionary.
        encoder_dict: Fitted LabelEncoder instances keyed by column name.

    Returns:
        Single-row DataFrame ready for prediction.
    """
    row = {
        "amount":            float(data["amount"]),
        "transaction_count": int(data["transaction_count"]),
        "is_new_location":   int(bool(data["is_new_location"])),
        "location":          str(data["location"]),
        "transaction_type":  str(data["transaction_type"]),
        "device_type":       str(data["device_type"]),
    }

    df = pd.DataFrame([row], columns=FEATURE_COLUMNS)

    # Encode categoricals using the saved encoders
    for col in CATEGORICAL_FEATURES:
        le = encoder_dict[col]
        known_classes = list(le.classes_)
        value = df.at[0, col]

        # Map unseen categories to the first known class (fallback)
        if value not in known_classes:
            logger.warning(
                "Unseen value '%s' for '%s'. Defaulting to '%s'.",
                value, col, known_classes[0],
            )
            df.at[0, col] = known_classes[0]

        df[col] = le.transform(df[col].astype(str))

    return df


def predict_transaction(data: dict[str, Any]) -> dict[str, Any]:
    """Predict fraud probability for a single transaction.

    Args:
        data: Dictionary containing transaction fields:
              amount, location, transaction_count, transaction_type,
              device_type, is_new_location.

    Returns:
        Dictionary with:
        - ``fraud_probability`` (int): 0–100 percentage.
        - ``prediction``        (str): "Fraud" or "Normal".

    Example::

        result = predict_transaction({
            "amount": 850000,
            "location": "Islamabad",
            "transaction_count": 17,
            "transaction_type": "Transfer",
            "device_type": "Mobile",
            "is_new_location": True,
        })
        # {"fraud_probability": 92, "prediction": "Fraud"}
    """
    model, encoder_dict = _load_artifacts()
    feature_df = _build_feature_row(data, encoder_dict)

    # predict_proba returns [[prob_normal, prob_fraud]]
    proba: np.ndarray = model.predict_proba(feature_df)[0]
    fraud_prob_float: float = proba[1]
    fraud_probability: int  = round(fraud_prob_float * 100)

    prediction = "Fraud" if fraud_probability >= 50 else "Normal"

    logger.info(
        "Prediction → probability: %d%% | label: %s",
        fraud_probability, prediction,
    )

    return {
        "fraud_probability": fraud_probability,
        "prediction":        prediction,
    }


if __name__ == "__main__":
    sample = {
        "amount":            850_000,
        "location":          "Islamabad",
        "transaction_count": 17,
        "transaction_type":  "Transfer",
        "device_type":       "Mobile",
        "is_new_location":   True,
    }
    result = predict_transaction(sample)
    print(result)
