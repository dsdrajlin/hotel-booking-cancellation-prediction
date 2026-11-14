"""Train and persist the final hotel booking cancellation model."""

from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "hotel_bookings.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "model.joblib"
METADATA_PATH = MODEL_DIR / "metadata.json"

TARGET = "is_canceled"
DIRECT_LEAKAGE = ["reservation_status", "reservation_status_date"]
STRICT_TIMING_EXCLUDED = ["booking_changes", "days_in_waiting_list"]
EXCLUDED_FEATURES = [TARGET, *DIRECT_LEAKAGE, *STRICT_TIMING_EXCLUDED, "company"]
THRESHOLD = 0.40
RANDOM_STATE = 42

XGB_PARAMS = {
    "n_estimators": 200,
    "max_depth": 7,
    "learning_rate": 0.12,
    "subsample": 0.9,
    "colsample_bytree": 1.0,
    "min_child_weight": 1,
}


def build_pipeline(numeric_features, categorical_features):
    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="constant", fill_value=0))]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Missing")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )
    model = XGBClassifier(
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",
        random_state=RANDOM_STATE,
        n_jobs=1,
        **XGB_PARAMS,
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])


def train():
    bookings_raw = pd.read_csv(DATA_PATH, dtype={"agent": "str", "company": "str"})
    bookings = bookings_raw.drop_duplicates(keep="first").copy()
    X = bookings.drop(columns=EXCLUDED_FEATURES)
    y = bookings[TARGET].astype(int)

    categorical_features = X.select_dtypes(include=["str"]).columns.tolist()
    numeric_features = X.select_dtypes(include=["number"]).columns.tolist()
    pipeline = build_pipeline(numeric_features, categorical_features)
    pipeline.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    metadata = {
        "model_file": str(MODEL_PATH.relative_to(PROJECT_ROOT)),
        "target": TARGET,
        "threshold": THRESHOLD,
        "feature_set": "full",
        "features": X.columns.tolist(),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "excluded_features": EXCLUDED_FEATURES,
        "raw_rows": int(len(bookings_raw)),
        "training_rows_after_deduplication": int(len(bookings)),
        "removed_duplicate_rows": int(len(bookings_raw) - len(bookings)),
        "xgboost_params": XGB_PARAMS,
        "random_state": RANDOM_STATE,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metadata to {METADATA_PATH}")


if __name__ == "__main__":
    train()
