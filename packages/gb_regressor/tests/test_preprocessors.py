from gb_regressor.config.core import config
from gb_regressor.processing import preprocessors as pp


def test_drop_unnecessary_features_transformer(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs
    assert config.model_config.drop_features in X_train.columns

    transformer = pp.DropUnnecessaryFeatures(
        variables_to_drop=config.model_config.drop_features,
    )

    # When
    X_transformed = transformer.transform(X_train)

    # Then
    assert config.model_config.drop_features not in X_transformed.columns


def test_temporal_variable_estimator(pipeline_inputs):
    # Given
    X_train, X_test, y_train, y_test = pipeline_inputs

    transformer = pp.TemporalVariableEstimator(
        variables=config.model_config.temporal_vars,
        reference_variable=config.model_config.drop_features,
    )

    # When
    X_transformed = transformer.transform(X_train)

    # Then
    assert (X_transformed["YearRemodAdd"] == (X_train["YrSold"] - X_train["YearRemodAdd"])).all()
