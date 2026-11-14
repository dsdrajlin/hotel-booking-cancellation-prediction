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

Some planned files and directories may be added as the project develops.

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

The service listens on port `9696`. A `GET /` request returns a health-check response, and a `POST /predict` request accepts the same booking JSON format used by `predict.py`.

## Status

Project setup and initial dataset selection are complete. Data analysis, model development, local deployment, and cloud deployment are planned.

## Acknowledgments

Dataset source: [Hotel Booking Demand on Kaggle](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand).
