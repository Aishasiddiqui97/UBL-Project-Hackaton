"""
scoring.py
----------
Computes the final risk score and maps it to a risk level for the AFCIP
platform using business rules defined in risk_scoring/rules.py.
"""

from __future__ import annotations

import logging
from typing import Any

from risk_scoring.rules import MAX_SCORE, evaluate_rules

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Risk level thresholds ──────────────────────────────────────────────────────
RISK_LEVELS: list[tuple[int, int, str]] = [
    (0,  30,  "Low Risk"),
    (31, 70,  "Medium Risk"),
    (71, 100, "High Risk"),
]


def _determine_risk_level(score: int) -> str:
    """Map a numeric score to a risk level label.

    Args:
        score: Capped risk score in the range [0, 100].

    Returns:
        Risk level string: 'Low Risk', 'Medium Risk', or 'High Risk'.
    """
    for low, high, label in RISK_LEVELS:
        if low <= score <= high:
            return label
    # Fallback — should never reach here if score is correctly capped
    return "High Risk"


def calculate_risk_score(
    amount:            float,
    transaction_count: int,
    is_new_location:   bool,
    fraud_probability: int,
) -> dict[str, Any]:
    """Calculate the risk score and level for a transaction.

    Evaluates all configured business rules, sums the points, caps the result
    at MAX_SCORE (100), and determines the corresponding risk level.

    Args:
        amount:            Transaction amount.
        transaction_count: Number of transactions for the account.
        is_new_location:   True if the transaction comes from a new location.
        fraud_probability: ML fraud probability as an integer (0–100).

    Returns:
        Dictionary with:
        - ``risk_score`` (int): Aggregated and capped risk score.
        - ``status``     (str): Risk level label.
        - ``fired_rules`` (list): Rules that contributed to the score.

    Example::

        result = calculate_risk_score(
            amount=850_000,
            transaction_count=17,
            is_new_location=True,
            fraud_probability=92,
        )
        # {"risk_score": 100, "status": "High Risk", "fired_rules": [...]}
    """
    fired_rules = evaluate_rules(
        amount=amount,
        transaction_count=transaction_count,
        is_new_location=is_new_location,
        fraud_probability=fraud_probability,
    )

    raw_score  = sum(r["points"] for r in fired_rules)
    risk_score = min(raw_score, MAX_SCORE)       # Cap at 100
    status     = _determine_risk_level(risk_score)

    logger.info(
        "Risk score: %d | Status: %s | Rules fired: %s",
        risk_score, status, [r["rule"] for r in fired_rules],
    )

    return {
        "risk_score":  risk_score,
        "status":      status,
        "fired_rules": fired_rules,
    }


if __name__ == "__main__":
    sample_result = calculate_risk_score(
        amount=850_000,
        transaction_count=17,
        is_new_location=True,
        fraud_probability=92,
    )
    print(sample_result)
