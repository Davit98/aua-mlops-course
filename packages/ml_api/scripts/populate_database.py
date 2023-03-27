import os
import time
import typing as t
from random import randint

import pandas as pd
import requests
from gb_regressor.config.core import config
from gb_regressor.processing.data_management import load_dataset

LOCAL_URL = f'http://{os.getenv("DB_HOST", "localhost")}:5001'
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

LOT_AREA_MAP = {"min": 1470, "max": 56600}
FIRST_FLR_SF_MAP = {"min": 407, "max": 5095}
SECOND_FLR_SF_MAP = {"min": 0, "max": 1862}


def _generate_random_int(value_ranges: t.Dict) -> int:
    """Generate random integer within a min and max range."""
    random_value = randint(value_ranges["min"], value_ranges["max"])

    return random_value


def _prepare_inputs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepare input data by removing key rows with NA values."""
    clean_inputs_df = dataframe.dropna(
        subset=config.model_config.features + ["KitchenQual", "LotFrontage"]
    ).copy()

    clean_inputs_df.loc[:, "FirstFlrSF"] = clean_inputs_df["FirstFlrSF"].apply(
        lambda _: _generate_random_int(FIRST_FLR_SF_MAP)
    )
    clean_inputs_df.loc[:, "SecondFlrSF"] = clean_inputs_df["SecondFlrSF"].apply(
        lambda _: _generate_random_int(SECOND_FLR_SF_MAP)
    )
    clean_inputs_df.loc[:, "LotArea"] = clean_inputs_df["LotArea"].apply(
        lambda _: _generate_random_int(LOT_AREA_MAP)
    )

    return clean_inputs_df


def populate_database(n_predictions: int = 500) -> None:
    """
    Manipulate the test data to generate random
    predictions and save them to the database.
    Before running this script, ensure that the
    API and Database docker containers are running.
    """

    print(f"Preparing to generate: {n_predictions} predictions.")

    # Load the gradient boosting test dataset which
    # is included in the model package
    test_inputs_df = load_dataset(file_name="test.csv")
    clean_inputs_df = _prepare_inputs(dataframe=test_inputs_df).reset_index(drop=True)

    if len(clean_inputs_df) < n_predictions:
        print(
            f"If you want {n_predictions} predictions, you need to"
            "extend the script to handle more predictions."
        )

    for index, data in clean_inputs_df.iterrows():
        if index >= n_predictions:
            break

        response = requests.post(
            f"{LOCAL_URL}/v1/predictions/lasso",
            headers=HEADERS,
            json=[data.to_dict()],
        )
        response.raise_for_status()

        if index % 50 == 0:
            print(f"{index} predictions complete")

            # prevent overloading the server
            # time.sleep(0.5)

    print("Prediction generation complete.")


if __name__ == "__main__":
    populate_database(n_predictions=500)
