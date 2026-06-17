"""
helpers.py
----------
Shared utility functions used across the AFCIP AI/ML platform.
"""

from __future__ import annotations

import logging
import time
from functools import wraps
from typing import Any, Callable


# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def timer(func: Callable) -> Callable:
    """Decorator: logs the execution time of a function.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that logs elapsed time after each call.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start   = time.perf_counter()
        result  = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("'%s' executed in %.4f seconds.", func.__name__, elapsed)
        return result
    return wrapper


def sanitize_input(data: dict[str, Any]) -> dict[str, Any]:
    """Sanitize transaction input by stripping whitespace from string values.

    Args:
        data: Raw input dictionary.

    Returns:
        Dictionary with string values stripped of leading/trailing whitespace.
    """
    return {
        key: (value.strip() if isinstance(value, str) else value)
        for key, value in data.items()
    }


def clamp(value: int | float, min_val: int | float, max_val: int | float) -> int | float:
    """Clamp *value* to the inclusive range [min_val, max_val].

    Args:
        value:   Input value.
        min_val: Lower bound (inclusive).
        max_val: Upper bound (inclusive).

    Returns:
        Value clamped within [min_val, max_val].
    """
    return max(min_val, min(value, max_val))


def format_response(
    fraud_probability: int,
    prediction:        str,
    risk_score:        int,
    status:            str,
) -> dict[str, Any]:
    """Build the standard AFCIP analysis response dictionary.

    Args:
        fraud_probability: ML model output (0–100).
        prediction:        "Fraud" or "Normal".
        risk_score:        Calculated risk score (0–100).
        status:            Risk level label.

    Returns:
        Standardised response dictionary.
    """
    return {
        "fraud_probability": fraud_probability,
        "prediction":        prediction,
        "risk_score":        risk_score,
        "status":            status,
    }
