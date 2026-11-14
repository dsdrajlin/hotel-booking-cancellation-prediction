"""Load the persisted model and predict cancellation risk for bookings."""

from pathlib import Path
import argparse
import json

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "model.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "metadata.json"


def load_artifacts():
    model = joblib.load(MODEL_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    return model, metadata


def predict_bookings(records):
    """Return cancellation probabilities and labels for one or more bookings."""
    if isinstance(records, dict):
        records = [records]
    if not records:
        return []

    model, metadata = load_artifacts()
    features = metadata["features"]
    threshold = float(metadata["threshold"])
    frame = pd.DataFrame(records).reindex(columns=features)
    probabilities = model.predict_proba(frame)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    return [
        {
            "cancellation_probability": float(probability),
            "is_canceled_prediction": int(prediction),
            "threshold": threshold,
        }
        for probability, prediction in zip(probabilities, predictions)
    ]


def main():
    parser = argparse.ArgumentParser(description="Predict hotel booking cancellations")
    parser.add_argument("input", help="JSON file containing one booking object or a list of bookings")
    args = parser.parse_args()
    records = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(predict_bookings(records), indent=2))


if __name__ == "__main__":
    main()
