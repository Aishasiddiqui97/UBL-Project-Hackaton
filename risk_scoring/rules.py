"""
rules.py
--------
Business rules for the AFCIP risk scoring engine.
Each rule maps a condition to a point contribution.
The combined score is capped at MAX_SCORE (100).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ── Score cap ─────────────────────────────────────────────────────────────────
MAX_SCORE: int = 100


@dataclass(frozen=True)
class RiskRule:
    """Represents a single risk scoring rule.

    Attributes:
        name:        Human-readable label for logging/audit.
        description: Plain-English explanation of the condition.
        points:      Score contribution when the rule fires.
    """
    name:        str
    description: str
    points:      int


# ── Rule definitions ──────────────────────────────────────────────────────────
RULE_HIGH_AMOUNT = RiskRule(
    name="High Amount",
    description="Transaction amount exceeds 500,000",
    points=40,
)

RULE_HIGH_TRANSACTION_COUNT = RiskRule(
    name="High Transaction Count",
    description="Transaction count exceeds 10",
    points=30,
)

RULE_NEW_LOCATION = RiskRule(
    name="New Location",
    description="Transaction originates from a new/unfamiliar location",
    points=20,
)

RULE_HIGH_FRAUD_PROBABILITY = RiskRule(
    name="High Fraud Probability",
    description="ML model fraud probability exceeds 80%",
    points=10,
)

# Ordered list evaluated by the scoring engine
ALL_RULES: list[RiskRule] = [
    RULE_HIGH_AMOUNT,
    RULE_HIGH_TRANSACTION_COUNT,
    RULE_NEW_LOCATION,
    RULE_HIGH_FRAUD_PROBABILITY,
]


def evaluate_rules(
    amount:            float,
    transaction_count: int,
    is_new_location:   bool,
    fraud_probability: int,
) -> list[dict[str, Any]]:
    """Evaluate all business rules against a transaction and return fired rules.

    Args:
        amount:            Transaction amount.
        transaction_count: Number of transactions from this account.
        is_new_location:   Whether the location is new/unfamiliar.
        fraud_probability: ML model fraud probability (0–100).

    Returns:
        List of dicts with keys 'rule' and 'points' for every rule that fired.
    """
    fired: list[dict[str, Any]] = []

    if amount > 500_000:
        fired.append({"rule": RULE_HIGH_AMOUNT.name, "points": RULE_HIGH_AMOUNT.points})

    if transaction_count > 10:
        fired.append({
            "rule":   RULE_HIGH_TRANSACTION_COUNT.name,
            "points": RULE_HIGH_TRANSACTION_COUNT.points,
        })

    if is_new_location:
        fired.append({"rule": RULE_NEW_LOCATION.name, "points": RULE_NEW_LOCATION.points})

    if fraud_probability > 80:
        fired.append({
            "rule":   RULE_HIGH_FRAUD_PROBABILITY.name,
            "points": RULE_HIGH_FRAUD_PROBABILITY.points,
        })

    return fired
