#!/usr/bin/env bash

kaggle competitions download -c house-prices-advanced-regression-techniques -p gb_regressor/datasets
unzip -o gb_regressor/datasets/house-prices-advanced-regression-techniques.zip -d gb_regressor/datasets
mv gb_regressor/datasets/train.csv gb_regressor/datasets/houseprice.csv