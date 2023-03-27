import json
import logging

import typing as t
from flask import request, jsonify, Response, current_app
from gb_regressor.predict import make_prediction

from api.persistence.data_access import PredictionPersistence, ModelType

_logger = logging.getLogger(__name__)


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

        # Step 4: Prepare prediction response
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
