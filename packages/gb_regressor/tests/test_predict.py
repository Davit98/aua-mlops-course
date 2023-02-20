from gb_regressor.config.core import config
from gb_regressor.predict import make_prediction
from regression_model.predict import make_prediction as alt_make_prediction
from sklearn.metrics import mean_squared_error


# the test below is designed to protect us against gradual degradation across many model changes and updates
def test_prediction_quality_against_benchmark(raw_training_data):
    # Given
    X = raw_training_data.drop(config.model_config.target, axis=1)
    y_true = raw_training_data[config.model_config.target]

    # Generate rough benchmarks (you would tweak depending on your model)
    benchmark_flexibility = 50000  # very relaxed benchmark :)
    # setting ndigits to -4 will round the value to the nearest 10,000 i.e. 210,000
    benchmark_lower_boundary = (
        round(y_true.iloc[0], ndigits=-4) - benchmark_flexibility
    )  # 210,000 - 50000 = 160000
    benchmark_upper_boundary = (
        round(y_true.iloc[0], ndigits=-4) + benchmark_flexibility
    )  # 210000 + 50000 = 260000

    # When
    subject = make_prediction(input_data=X[0:1])

    # Then
    assert subject is not None
    prediction = subject.get("predictions")[0]
    assert isinstance(prediction, float)
    assert prediction > benchmark_lower_boundary
    assert prediction < benchmark_upper_boundary


# the test below is designed to detect a sudden drop in model quality
def test_prediction_quality_against_another_model(raw_training_data):
    # Given
    X = raw_training_data.drop(config.model_config.target, axis=1)
    y_true = raw_training_data[config.model_config.target]
    y_pred_current = make_prediction(input_data=X)

    # the older model has these variable names reversed
    X.rename(
        columns={
            "FirstFlrSF": "1stFlrSF",
            "SecondFlrSF": "2ndFlrSF",
            "ThreeSsnPortch": "3SsnPorch",
        },
        inplace=True,
    )
    y_pred_alt = alt_make_prediction(input_data=X)

    # When
    current_mse = mean_squared_error(
        y_true=y_true.values, y_pred=y_pred_current["predictions"]
    )

    alternative_mse = mean_squared_error(
        y_true=y_true.values, y_pred=y_pred_alt["predictions"]
    )

    # Then
    assert current_mse < alternative_mse
