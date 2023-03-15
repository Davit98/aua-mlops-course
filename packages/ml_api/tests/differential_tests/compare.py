import math
import typing as t


def compare_differences(
    *,
    expected_predictions: t.List,
    actual_predictions: t.List,
    rel_tol: t.Optional[float] = None,  # |a-b|/max(a,b)
    abs_tol: t.Optional[float] = None,  # |a-b|
) -> None:

    if len(expected_predictions) != len(actual_predictions):
        raise ValueError('Lengths of predictions to compare are not equal!')

    thresholds = {}

    if abs_tol:
        thresholds["abs_tol"] = abs_tol

    if rel_tol:
        thresholds["rel_tol"] = rel_tol

    for index, (actual_prediction, expected_prediction) in enumerate(
        zip(actual_predictions, expected_predictions)
    ):
        if not math.isclose(expected_prediction, actual_prediction, **thresholds):
            raise ValueError(
                f"Price prediction {index} has changed by more "
                f"than the thresholds: {thresholds}: "
                f"{expected_prediction} (expected) vs "
                f"{actual_prediction} (actual)"
            )
