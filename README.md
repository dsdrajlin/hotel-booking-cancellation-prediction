# Hotel Booking Cancellation Prediction

## Project overview

This project explores whether a hotel booking will be canceled, using information available when the booking is made. The goal is to build and evaluate a binary classification model that could help hotels anticipate cancellations and support booking and capacity planning.

The target variable is `is_canceled`. The model is intended to predict this outcome when a booking is made, using only information available at that time. Features that reveal the booking’s eventual outcome will be excluded from the model inputs.

## Dataset

The project uses the [Hotel Booking Demand dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand). The CSV file is stored at `data/raw/hotel_bookings.csv`.

The target variable is `is_canceled` (`1` for a canceled booking and `0` otherwise). The dataset contains records for city and resort hotel bookings, with booking, guest, and stay information.

See the [data dictionary](docs/data_dictionary.md) for technical definitions of the source columns. The project notebooks document data-preparation findings and modeling decisions.

## Project plan

- Explore and prepare the data, including missing-value and target analysis.
- Compare and tune multiple classification models, and analyze feature importance.
- Save a reproducible training workflow and the selected model.
- Serve predictions through a web API and run the service locally with Docker.
- Deploy the service to the cloud and document how to access it.

## Repository structure

```text
.
├── data/
│   └── raw/
│       └── hotel_bookings.csv
├── docs/
│   └── data_dictionary.md
├── notebooks/       # Data preparation, EDA, and model selection
├── src/             # Training, prediction, and web service scripts
├── models/          # Trained model artifacts
├── Dockerfile
├── requirements.txt
└── README.md
```

Additional deployment files may be added as the project develops.

## Environment setup

The project uses Python and the dependencies listed in `requirements.txt`. From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the workflow locally

The scripts follow the project instructions:

- `src/train.py` trains the selected XGBoost pipeline and saves the model artifact and metadata under `models/`.
- `src/predict.py` loads the saved artifact and runs inference for a JSON booking object or a list of booking objects.
- `src/serve.py` starts the FastAPI web service and exposes the prediction endpoint.

From the project root, activate the project environment and run:

```bash
python src/train.py
python src/predict.py data/sample_booking.json
cd src
python serve.py
```

The service listens on port `9696`. A `GET /` request returns a health-check response:

```bash
curl http://localhost:9696/
```

To request a prediction, use the sample booking from a second terminal opened at the project root:

```bash
curl -X POST http://localhost:9696/predict \
  -H "Content-Type: application/json" \
  --data-binary @data/sample_booking.json
```

The response contains the estimated cancellation probability, the binary prediction, and the threshold used by the final workflow:

```json
{
  "predictions": [
    {
      "cancellation_probability": 0.1804,
      "is_canceled_prediction": 0,
      "threshold": 0.4
    }
  ]
}
```

`cancellation_probability` is the model's estimated probability of cancellation. `is_canceled_prediction` is `1` when that probability is at least the selected threshold and `0` otherwise.

## Run with Docker

The Docker image contains the serving code, dependencies, and trained model artifacts. From the project root:

```bash
docker build -t hotel-booking-cancellation .
docker run --rm -p 9696:9696 hotel-booking-cancellation
```

Once the container is running, use the same `curl` commands described above.

## Cloud deployment on Render

The Dockerized API is also deployed as a Render Web Service. Render builds the service from the repository `Dockerfile` and provides a public HTTPS URL:

```text
https://hotel-booking-cancellation-prediction-6nai.onrender.com
```

The health check can be tested with:

```bash
curl https://hotel-booking-cancellation-prediction-6nai.onrender.com/
```

To send the example booking to the deployed service, run the following command from the project root:

```bash
curl -X POST https://hotel-booking-cancellation-prediction-6nai.onrender.com/predict \
  -H "Content-Type: application/json" \
  --data-binary @data/sample_booking.json
```

The deployed service returns the same prediction as the local and Docker deployments:

```json
{
  "predictions": [
    {
      "cancellation_probability": 0.1804,
      "is_canceled_prediction": 0,
      "threshold": 0.4
    }
  ]
}
```

The free Render instance may spin down after inactivity, so the first request after a period without traffic can take longer while the service starts again.

## Acknowledgments

Dataset source: [Hotel Booking Demand on Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand).
