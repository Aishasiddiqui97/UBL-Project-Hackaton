"""
train_model.py
--------------
Trains a RandomForestClassifier on the preprocessed transaction dataset,
evaluates its performance, and persists the trained model via Joblib.
"""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

from fraud_detection.data_preprocessing import preprocess

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────
MODEL_PATH = Path("fraud_detection/model.pkl")


def train(
    n_estimators: int = 200,
    max_depth: int | None = None,
    random_state: int = 42,
    class_weight: str = "balanced",
) -> RandomForestClassifier:
    """Train a RandomForestClassifier and persist it.

    Args:
        n_estimators:  Number of trees in the forest.
        max_depth:     Maximum depth of each tree (None = unlimited).
        random_state:  Seed for reproducibility.
        class_weight:  Weight mode — 'balanced' handles class imbalance.

    Returns:
        Fitted RandomForestClassifier.
    """
    # ── 1. Preprocess data ────────────────────────────────────────────────────
    logger.info("Starting data preprocessing…")
    X_train, X_test, y_train, y_test, _ = preprocess()

    # ── 2. Initialise model ───────────────────────────────────────────────────
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        class_weight=class_weight,
        n_jobs=-1,          # Use all available CPU cores
    )

    # ── 3. Train ──────────────────────────────────────────────────────────────
    logger.info("Training RandomForestClassifier…")
    model.fit(X_train, y_train)
    logger.info("Training complete.")

    # ── 4. Evaluate ───────────────────────────────────────────────────────────
    y_pred = model.predict(X_test)

    accuracy  = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall    = recall_score(y_test, y_pred, zero_division=0)
    f1        = f1_score(y_test, y_pred, zero_division=0)

    print("\n" + "=" * 50)
    print("       MODEL EVALUATION METRICS")
    print("=" * 50)
    print(f"  Accuracy  : {accuracy  * 100:.2f}%")
    print(f"  Precision : {precision * 100:.2f}%")
    print(f"  Recall    : {recall    * 100:.2f}%")
    print(f"  F1 Score  : {f1        * 100:.2f}%")
    print("=" * 50)
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal", "Fraud"]))

    # ── 5. Persist model ──────────────────────────────────────────────────────
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    logger.info("Model saved → '%s'.", MODEL_PATH)

    return model


if __name__ == "__main__":
    train()
