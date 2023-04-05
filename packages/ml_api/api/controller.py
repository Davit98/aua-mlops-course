import json
import logging

import typing as t
from flask import request, jsonify, Response, current_app

from gb_regressor import __version__ as shadow_version
from regression_model import __version__ as live_version
from prometheus_client import Histogram, Gauge, Info
from gb_regressor.predict import make_prediction

from api.persistence.data_access import PredictionPersistence, ModelType
from api.config import APP_NAME

_logger = logging.getLogger(__name__)

PREDICTION_TRACKER = Histogram(
    name='house_price_prediction_dollars',
    documentation='ML Model Prediction on House Price',
    labelnames=['app_name', 'model_name', 'model_version']
)

PREDICTION_GAUGE = Gauge(
    name='house_price_gauge_dollars',
    documentation='ML Model Prediction on House Price for min max calcs',
    labelnames=['app_name', 'model_name', 'model_version']
)

PREDICTION_GAUGE.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version)

MODEL_VERSIONS = Info(
    'model_version_details',
    'Capture model version information',
)

MODEL_VERSIONS.info({
    'live_model': ModelType.LASSO.name,
    'live_version': live_version,
    'shadow_model': ModelType.GRADIENT_BOOSTING.name,
    'shadow_version': shadow_version})


class PredictionResult(t.NamedTuple):
    errors: t.Any
    predictions: t.List
    model_version: str


def health():
    if request.method == "GET":
        return jsonify({"status": "ok"})


def predict():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2a: Get and save live model predictions
        persistence = PredictionPersistence(db_session=current_app.db_session)
        result = persistence.make_save_predictions(
            db_model=ModelType.LASSO, input_data=json_data
        )

        # Step 2b: Get and save shadow predictions
        shadow_result = persistence.make_save_predictions(  # noqa
            db_model=ModelType.GRADIENT_BOOSTING, input_data=json_data
        )

        # Step 3: Handle errors
        if result.errors:
            _logger.warning(f"errors during prediction: {result.errors}")
            return Response(json.dumps(result.errors), status=400)

        # Step 4: Monitoring
        for _prediction in result.predictions:
            PREDICTION_TRACKER.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version).observe(_prediction)

            PREDICTION_GAUGE.labels(
                app_name=APP_NAME,
                model_name=ModelType.LASSO.name,
                model_version=live_version).set(_prediction)

        # Step 5: Prepare prediction response
        return jsonify(
            {
                "predictions": result.predictions,
                "version": result.model_version,
                "errors": result.errors,
            }
        )


def predict_alt():
    if request.method == "POST":
        # Step 1: Extract POST data from request body as JSON
        json_data = request.get_json()

        # Step 2: Access the model prediction function (also validates data)
        result = make_prediction(input_data=json_data)

        # Step 3: Handle errors
        errors = result.get("errors")
        if errors:
            return Response(json.dumps(errors), status=400)

        # Step 4: Split out results
        predictions = result.get("predictions").tolist()
        version = result.get("version")

        # Step 5: Save predictions
        persistence = PredictionPersistence(db_session=current_app.db_session)
        prediction_result = PredictionResult(
            errors=errors,
            predictions=predictions,
            model_version=version,
        )
        persistence.save_predictions(
            inputs=json_data,
            prediction_result=prediction_result,
            db_model=ModelType.GRADIENT_BOOSTING,
        )

        # Step 6: Prepare prediction response
        return jsonify(
            {"predictions": predictions, "version": version, "errors": errors}
        )
