from pathlib import Path 
import os
import pickle
import time
import random

import numpy as np
from flask import jsonify
from prometheus_client import Counter, Gauge, Histogram, Summary


########################################################################
########### Load Model checkpoint, metadata and preprocessor. ##########
######################################################################## 

APP_DIR = Path(__file__).parent.absolute() 

with open(os.path.join(APP_DIR, "checkpoints/model.pkl"), "rb") as f:
    MODEL = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/metadata.pkl"), "rb") as f:
    METADATA = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/scaler.pkl"), "rb") as f:
    SCALER = pickle.load(f)


########################################################################
############################ Define metrics. ###########################
########################################################################

REQUEST_COUNTER = Counter("request_count", "The number of requests")
TARGET_GAUGE = Gauge("target_sum_sign", "Predicted class: +1 if class=1 else -1")
WAREA_HIST = Histogram("worst_area_hist", "worst_area histogram")
REQUEST_TIME = Summary("request_processing_seconds", "Time spent processing request")


########################################################################
########################## Define endpoints. ###########################
########################################################################
    
def summary():
    return "Breast cancer type predictor."


def info_json():
    return jsonify(METADATA)


@REQUEST_TIME.time()
def predict(mean_concavity, worst_area, mean_area):
    
    # Constructing the data and preparing for feeding into the model.
    data = np.array([mean_concavity, worst_area, mean_area]).reshape(1,-1)
    data = SCALER.transform(data)

    # Predicting the class and constructing output.
    pred_val = MODEL.predict(data)[0]
    result = {"label": str(pred_val), "class": str(METADATA["label2class"][pred_val])}
    
    ##########################################################################
    # Note that we artificially add sleep here to simulate different request 
    # processing times.
    sec = random.random() * 2
    time.sleep(sec)
    ##########################################################################
    
    REQUEST_COUNTER.inc()  # Increments by 1.
    
    if pred_val == 1:
        TARGET_GAUGE.inc()
    else:
        TARGET_GAUGE.dec()
    
    WAREA_HIST.observe(worst_area)

    return jsonify(result)
