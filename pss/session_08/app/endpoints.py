from pathlib import Path 
import os
import pickle

import numpy as np
from flask import render_template, jsonify


APP_DIR = Path(__file__).parent.absolute() 


with open(os.path.join(APP_DIR, "checkpoints/model.pkl"), "rb") as f:
    MODEL = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/metadata.pkl"), "rb") as f:
    METADATA = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/scaler.pkl"), "rb") as f:
    SCALER = pickle.load(f)


def hello_world():
    return "Hello world!"


def info_json():
    return jsonify(METADATA)


def predict(mean_concavity, worst_area, mean_area):
    
    # Constructing the data and preparing for feeding into the model.
    data = np.array([mean_concavity, worst_area, mean_area]).reshape(1,-1)
    data = SCALER.transform(data)

    # Predicting the class and constructing output.
    pred_val = MODEL.predict(data)[0]
    result = {"label": str(pred_val), "class": str(METADATA["label2class"][pred_val])}

    return jsonify(result)
