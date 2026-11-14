"""Serve the hotel booking cancellation model through a FastAPI service."""

import os
from typing import Any

from fastapi import Body, FastAPI, HTTPException
import uvicorn

from predict import predict_bookings


app = FastAPI(
    title="Hotel Booking Cancellation Prediction API",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: Any = Body(...)):
    if not isinstance(payload, (dict, list)):
        raise HTTPException(status_code=400, detail="Request body must be a booking object or a list of booking objects")
    try:
        return {"predictions": predict_bookings(payload)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":
    port = int(os.getenv("PORT", "9696"))
    uvicorn.run(app, host="0.0.0.0", port=port)
