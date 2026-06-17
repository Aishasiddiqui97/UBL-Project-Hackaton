"""
data_preprocessing.py
---------------------
Handles loading, cleaning, encoding, and splitting of transaction data
for the fraud detection model.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
DATASET_PATH = Path("dataset/transactions.csv")
ENCODER_PATH = Path("fraud_detection/encoder.pkl")

CATEGORICAL_FEATURES = ["location", "transaction_type", "device_type"]
NUMERIC_FEATURES = ["amount", "transaction_count", "is_new_location"]
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "is_fraud"


def load_data(path: Path = DATASET_PATH) -> pd.DataFrame:
    """Load the transactions CSV into a DataFrame.

    Args:
        path: Path to the CSV file.

    Returns:
        Raw DataFrame.

    Raises:
        FileNotFoundError: If the CSV does not exist at *path*.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. "
            "Run dataset/generate_dataset.py first."
        )
    df = pd.read_csv(path)
    logger.info("Loaded %d records from '%s'.", len(df), path)
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Fill or drop missing values.

    - Numeric columns  → fill with median.
    - Categorical cols → fill with mode.
    - Rows still NaN   → dropped.

    Args:
        df: Raw DataFrame.

    Returns:
        Cleaned DataFrame.
    """
    before = len(df)

    for col in NUMERIC_FEATURES:
        if col in df.columns and df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            logger.info("Filled missing '%s' with median %.2f.", col, median_val)

    for col in CATEGORICAL_FEATURES:
        if col in df.columns and df[col].isnull().any():
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            logger.info("Filled missing '%s' with mode '%s'.", col, mode_val)

    df = df.dropna(subset=[TARGET])
    after = len(df)
    if before != after:
        logger.warning("Dropped %d rows with missing target values.", before - after)

    return df


def encode_categorical(
    df: pd.DataFrame,
    fit: bool = True,
    encoder_dict: dict[str, LabelEncoder] | None = None,
) -> Tuple[pd.DataFrame, dict[str, LabelEncoder]]:
    """Encode categorical columns using LabelEncoder.

    Args:
        df:           DataFrame to encode.
        fit:          If True, fit new encoders; if False, use *encoder_dict*.
        encoder_dict: Pre-fitted encoders (required when *fit=False*).

    Returns:
        Tuple of (encoded DataFrame, encoder dictionary).
    """
    if encoder_dict is None:
        encoder_dict = {}

    df = df.copy()
    for col in CATEGORICAL_FEATURES:
        if col not in df.columns:
            logger.warning("Column '%s' not found — skipping encoding.", col)
            continue

        if fit:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoder_dict[col] = le
        else:
            le = encoder_dict[col]
            # Handle unseen labels gracefully by mapping to the last known class
            known_classes = list(le.classes_)
            df[col] = df[col].astype(str).apply(
                lambda x: x if x in known_classes else known_classes[0]
            )
            df[col] = le.transform(df[col])

    return df, encoder_dict


def get_features_and_target(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Extract feature matrix X and target vector y.

    Args:
        df: Fully pre-processed DataFrame.

    Returns:
        Tuple of (X, y).
    """
    X = df[ALL_FEATURES].copy()
    y = df[TARGET].copy()
    return X, y


def preprocess(
    path: Path = DATASET_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, LabelEncoder]]:
    """Full preprocessing pipeline: load → clean → encode → split.

    Args:
        path:         Path to the raw CSV.
        test_size:    Fraction of data reserved for testing.
        random_state: Random seed for reproducibility.

    Returns:
        Tuple of (X_train, X_test, y_train, y_test, encoder_dict).
    """
    df = load_data(path)
    df = handle_missing_values(df)
    df, encoder_dict = encode_categorical(df, fit=True)

    X, y = get_features_and_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(
        "Split → train: %d | test: %d", len(X_train), len(X_test)
    )

    # Persist encoders so the prediction module can reuse them
    joblib.dump(encoder_dict, ENCODER_PATH)
    logger.info("Encoder saved → '%s'.", ENCODER_PATH)

    return X_train, X_test, y_train, y_test, encoder_dict


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _ = preprocess()
    logger.info("Preprocessing complete. X_train shape: %s", X_train.shape)
