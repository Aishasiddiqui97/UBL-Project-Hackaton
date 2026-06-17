"""
generate_dataset.py
-------------------
Generates a realistic dummy transaction dataset for AFCIP fraud detection.
Produces 5000 records with an 85/15 normal/fraud split.
Run once to create dataset/transactions.csv.
"""

import numpy as np
import pandas as pd

# ── Reproducibility ───────────────────────────────────────────────────────────
SEED = 42
rng = np.random.default_rng(SEED)

# ── Configuration ─────────────────────────────────────────────────────────────
TOTAL_RECORDS = 5000
FRAUD_RATIO = 0.15
N_FRAUD = int(TOTAL_RECORDS * FRAUD_RATIO)       # 750
N_NORMAL = TOTAL_RECORDS - N_FRAUD               # 4250

LOCATIONS = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]
TRANSACTION_TYPES = ["Transfer", "Withdrawal", "Deposit", "Payment"]
DEVICE_TYPES = ["Mobile", "Desktop", "ATM", "POS"]


def _generate_normal() -> pd.DataFrame:
    """Generate normal (non-fraud) transaction records."""
    return pd.DataFrame({
        "account_no": [f"ACC{rng.integers(1000, 9999)}" for _ in range(N_NORMAL)],
        "amount": rng.integers(1_000, 200_000, size=N_NORMAL),
        "location": rng.choice(LOCATIONS, size=N_NORMAL),
        "transaction_count": rng.integers(1, 10, size=N_NORMAL),
        "transaction_type": rng.choice(TRANSACTION_TYPES, size=N_NORMAL),
        "device_type": rng.choice(DEVICE_TYPES, size=N_NORMAL),
        # Normal transactions rarely come from new locations
        "is_new_location": rng.choice([0, 1], size=N_NORMAL, p=[0.85, 0.15]),
        "is_fraud": 0,
    })


def _generate_fraud() -> pd.DataFrame:
    """Generate fraudulent transaction records with realistic fraud indicators."""
    return pd.DataFrame({
        "account_no": [f"ACC{rng.integers(1000, 9999)}" for _ in range(N_FRAUD)],
        # Fraud tends to involve higher amounts
        "amount": rng.integers(300_000, 1_000_000, size=N_FRAUD),
        "location": rng.choice(LOCATIONS, size=N_FRAUD),
        # Fraud accounts show higher transaction counts
        "transaction_count": rng.integers(10, 50, size=N_FRAUD),
        # Transfers and Withdrawals dominate fraud
        "transaction_type": rng.choice(
            ["Transfer", "Withdrawal", "Payment", "Deposit"],
            size=N_FRAUD,
            p=[0.45, 0.35, 0.15, 0.05],
        ),
        "device_type": rng.choice(DEVICE_TYPES, size=N_FRAUD),
        # Fraud accounts frequently use new/unknown locations
        "is_new_location": rng.choice([0, 1], size=N_FRAUD, p=[0.25, 0.75]),
        "is_fraud": 1,
    })


def main() -> None:
    normal_df = _generate_normal()
    fraud_df = _generate_fraud()

    df = pd.concat([normal_df, fraud_df], ignore_index=True)
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    output_path = "dataset/transactions.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset saved → {output_path}")
    print(f"Total records  : {len(df)}")
    print(f"Normal (0)     : {(df['is_fraud'] == 0).sum()}")
    print(f"Fraud  (1)     : {(df['is_fraud'] == 1).sum()}")
    print(df.head())


if __name__ == "__main__":
    main()
