"""
main.py
-------
FastAPI application for the AFCIP fraud detection and risk scoring engine.

Endpoint:
    POST /analyze-transaction

Flow:
    Receive Transaction → Predict Fraud Probability → Calculate Risk Score
    → Generate Risk Level → Return JSON Response
"""

from __future__ import annotations

import logging
import time
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from fraud_detection.predict import predict_transaction
from risk_scoring.scoring import calculate_risk_score
from utils.helpers import format_response, sanitize_input

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="AFCIP — Anti Financial Crime Investigation Platform",
    description=(
        "AI/ML-powered fraud detection and risk scoring engine. "
        "Submit a transaction to receive a fraud probability, "
        "prediction label, risk score, and risk status."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allow all origins in development; restrict in production) ───────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class TransactionRequest(BaseModel):
    """Input schema for a transaction analysis request."""

    account_no: str = Field(
        ...,
        min_length=1,
        description="Unique account identifier.",
        examples=["1002"],
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Transaction amount (must be greater than 0).",
        examples=[850000],
    )
    location: str = Field(
        ...,
        min_length=1,
        description="City where the transaction occurred.",
        examples=["Islamabad"],
    )
    transaction_count: int = Field(
        ...,
        ge=0,
        description="Number of transactions made by the account (>= 0).",
        examples=[17],
    )
    transaction_type: str = Field(
        ...,
        min_length=1,
        description="Type of transaction: Transfer, Withdrawal, Deposit, Payment.",
        examples=["Transfer"],
    )
    device_type: str = Field(
        ...,
        min_length=1,
        description="Device used: Mobile, Desktop, ATM, POS.",
        examples=["Mobile"],
    )
    is_new_location: bool = Field(
        ...,
        description="True if the transaction location is new/unfamiliar.",
        examples=[True],
    )

    @field_validator("location")
    @classmethod
    def location_not_empty(cls, v: str) -> str:
        """Ensure location is not blank after stripping whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("location cannot be empty or whitespace.")
        return stripped

    @field_validator("transaction_type", "device_type", "account_no")
    @classmethod
    def string_not_empty(cls, v: str) -> str:
        """Ensure string fields are not blank after stripping whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Field cannot be empty or whitespace.")
        return stripped

    model_config = {"json_schema_extra": {
        "example": {
            "account_no":        "1002",
            "amount":            850000,
            "location":          "Islamabad",
            "transaction_count": 17,
            "transaction_type":  "Transfer",
            "device_type":       "Mobile",
            "is_new_location":   True,
        }
    }}


class TransactionResponse(BaseModel):
    """Output schema for the transaction analysis response."""

    fraud_probability: int = Field(
        ...,
        ge=0,
        le=100,
        description="ML model fraud probability (0–100%).",
    )
    prediction: str = Field(
        ...,
        description="Binary label: 'Fraud' or 'Normal'.",
    )
    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Aggregated risk score (0–100).",
    )
    status: str = Field(
        ...,
        description="Risk level: 'Low Risk', 'Medium Risk', or 'High Risk'.",
    )


# ── Exception handler ─────────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler — prevents raw tracebacks leaking to clients."""
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again."},
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok", "service": "AFCIP AI/ML Engine"}


@app.post(
    "/analyze-transaction",
    response_model=TransactionResponse,
    tags=["Fraud Detection"],
    summary="Analyze a transaction for fraud and risk",
)
def analyze_transaction(request: TransactionRequest) -> dict[str, Any]:
    """Analyze a transaction and return fraud probability + risk score.

    **Flow:**
    1. Sanitize and validate input.
    2. Call the ML model to get fraud probability.
    3. Apply business rules to calculate a risk score.
    4. Return a structured JSON response.

    Args:
        request: Validated ``TransactionRequest`` payload.

    Returns:
        ``TransactionResponse`` containing fraud_probability, prediction,
        risk_score, and status.

    Raises:
        HTTPException 422: Pydantic validation failure (auto-handled by FastAPI).
        HTTPException 500: Internal model or scoring error.
    """
    logger.info("Received transaction analysis request for account: %s", request.account_no)
    _start = time.perf_counter()

    # ── Step 1: Build input dict (sanitize strings) ────────────────────────
    transaction_data = sanitize_input(request.model_dump())

    # ── Step 2: Fraud prediction ───────────────────────────────────────────
    try:
        prediction_result = predict_transaction(transaction_data)
    except FileNotFoundError as exc:
        logger.error("Model artifacts missing: %s", exc)
        raise HTTPException(
            status_code=503,
            detail=(
                "ML model artifacts not found. "
                "Please train the model first by running: "
                "python -m fraud_detection.train_model"
            ),
        ) from exc
    except Exception as exc:
        logger.exception("Fraud prediction failed: %s", exc)
        raise HTTPException(status_code=500, detail="Fraud prediction failed.") from exc

    fraud_probability: int = prediction_result["fraud_probability"]
    prediction_label:  str = prediction_result["prediction"]

    # ── Step 3: Risk scoring ───────────────────────────────────────────────
    try:
        scoring_result = calculate_risk_score(
            amount=request.amount,
            transaction_count=request.transaction_count,
            is_new_location=request.is_new_location,
            fraud_probability=fraud_probability,
        )
    except Exception as exc:
        logger.exception("Risk scoring failed: %s", exc)
        raise HTTPException(status_code=500, detail="Risk scoring failed.") from exc

    risk_score: int = scoring_result["risk_score"]
    status:     str = scoring_result["status"]

    # ── Step 4: Format and return response ────────────────────────────────
    response = format_response(
        fraud_probability=fraud_probability,
        prediction=prediction_label,
        risk_score=risk_score,
        status=status,
    )

    logger.info(
        "Analysis complete → account: %s | fraud: %d%% | score: %d | status: %s | elapsed: %.4fs",
        request.account_no, fraud_probability, risk_score, status,
        time.perf_counter() - _start,
    )

    return response
