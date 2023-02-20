from pathlib import Path

import pytest
from gb_regressor.config.core import (
    create_and_validate_config,
    fetch_config_from_yaml,
)
from pydantic import ValidationError

TEST_CONFIG_TEXT = """
package_name: gb_regressor
training_data_file: houseprice.csv
test_data_file: test.csv
drop_features: YrSold
pipeline_name: gb_regression
pipeline_save_file: gb_regression_output_v
target: SalePrice
variables_to_rename:
  old: new
features:
  - LotArea
numerical_vars:
  - LotArea
categorical_vars:
  - BsmtQual
temporal_vars: YearRemodAdd
numerical_na_not_allowed:
  - LotArea
test_size: 0.1
random_state: 0
n_estimators: 50
rare_label_tol: 0.01
rare_label_n_categories: 5
loss: squared_error
allowed_loss_functions:
  - squared_error
  - absolute_error
  - huber
"""

INVALID_TEST_CONFIG_TEXT = """
package_name: gb_regressor
training_data_file: houseprice.csv
test_data_file: test.csv
drop_features: YrSold
pipeline_name: gb_regression
pipeline_save_file: gb_regression_output_v
target: SalePrice
features:
  - LotArea
numerical_vars:
  - LotArea
categorical_vars:
  - BsmtQual
temporal_vars: YearRemodAdd
numerical_na_not_allowed:
  - LotArea
test_size: 0.1
random_state: 0
n_estimators: 50
rare_label_tol: 0.01
rare_label_n_categories: 5
loss: squared_error
allowed_loss_functions:
  - huber
"""


def test_fetch_config_structure(tmpdir):  # tmpdir is a pytest built-in fixture
    # Given
    # We make use of the pytest built-in tmpdir fixture
    configs_dir = Path(tmpdir)
    sample_config = configs_dir / "sample_config.yml"
    sample_config.write_text(TEST_CONFIG_TEXT)
    parsed_config = fetch_config_from_yaml(cfg_path=sample_config)

    # When
    config = create_and_validate_config(parsed_config=parsed_config)

    # Then
    assert config.model_config
    assert config.app_config


def test_config_validation_raises_error_for_invalid_config(tmpdir):
    # Given
    # We make use of the pytest built-in tmpdir fixture
    configs_dir = Path(tmpdir)
    sample_config = configs_dir / "sample_config.yml"

    # invalid config attempts to set a prohibited loss
    # function which we validate against an allowed set of
    # loss function parameters.
    sample_config.write_text(INVALID_TEST_CONFIG_TEXT)
    parsed_config = fetch_config_from_yaml(cfg_path=sample_config)

    # When
    with pytest.raises(ValidationError) as e_info:
        create_and_validate_config(parsed_config=parsed_config)

    # Then
    assert "not in the allowed set" in str(e_info.value)


def test_missing_config_field_raises_validation_error(tmpdir):
    # Given
    # We make use of the pytest built-in tmpdir fixture
    configs_dir = Path(tmpdir)
    sample_config = configs_dir / "sample_config.yml"

    TEST_CONFIG_TEXT = """package_name: gb_regressor"""
    sample_config.write_text(TEST_CONFIG_TEXT)
    parsed_config = fetch_config_from_yaml(cfg_path=sample_config)

    # When
    with pytest.raises(ValidationError) as e_info:
        create_and_validate_config(parsed_config=parsed_config)

    # Then
    assert "field required" in str(e_info.value)
    assert "pipeline_name" in str(e_info.value)
