from pathlib import Path 
import os
import pickle

import numpy as np
from flask import Flask, request, jsonify, render_template


##############################################################################
######################## LOADING THE PREDICTIVE MODEL ########################
##############################################################################


APP_DIR = Path(__file__).parent.absolute() 


with open(os.path.join(APP_DIR, "checkpoints/model.pkl"), "rb") as f:
    MODEL = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/metadata.pkl"), "rb") as f:
    METADATA = pickle.load(f)
    
with open(os.path.join(APP_DIR, "checkpoints/scaler.pkl"), "rb") as f:
    SCALER = pickle.load(f)
    
    
##############################################################################
########################### INITIALIZING FLASK APP ###########################
##############################################################################
    
    
# Create your Flask application instance with the name app. 
# To do so, pass the special variable __name__ that holds the 
# name of the current Python module or use another name of your choice.
app = Flask(__name__)

# Once you create the app instance, you use it to handle incoming web requests 
# and send responses to the user.


##############################################################################
########################### INITIALIZING FLASK APP ###########################
##############################################################################


# @app.route is a decorator that turns a regular Python function into a Flask 
# view function, which converts the function’s return value into an HTTP response 
# to be displayed by an HTTP client, such as a web browser. You pass the value '/' 
# to @app.route() to signify that this function will respond to web requests 
# for the URL '/', which is the main URL.

@app.route("/")
def hello_world():
    return "Hello world!"


@app.route("/metadata_json")
def info_json():
    return jsonify(METADATA)


# Web applications mainly use HTML to display information for the visitor, 
# so we’ll now work on incorporating HTML files in our app, which can be 
# displayed on the web browser.
# With the help of render_template() helper function we can render HTML 
# template files that exist in the 'templates' folder.

# The below return statement tells render_template() to look for a file 
# called 'result.html' in the 'templates' folder and passes METADATA as 
# output keyword argument to that file.

@app.route("/metadata")
def info():
    return render_template("result.html", output=METADATA)


@app.route("/input")
def home():
    return render_template("home.html")


# You can use the methods argument of the route() decorator to handle 
# different HTTP methods. By default, the requests are handled by the GET() method.

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        
        # An example of request.form:
        # request.form = ImmutableMultiDict([('mean concavity', '4.5'), ('worst area', '2.1'), ('mean area', '0.5')])
        
        # Getting the features.
        mean_concavity = float(request.form["mean concavity"])
        worst_area = float(request.form["worst area"])
        mean_area = float(request.form["mean area"])

        # Constructing the data and preparing for feeding into the model.
        data = np.array([mean_concavity, worst_area, mean_area]).reshape(1, -1)
        data = SCALER.transform(data)

        # Predicting the class and constructing output.
        pred_val = MODEL.predict(data)[0]
        result = f"{pred_val} - {METADATA['label2class'][pred_val]}"
        
        return render_template("result.html", output=result)


##############################################################################
########################### RUNNING THE APPLICATION ##########################
##############################################################################

# We run the app on localhost, which is a hostname that refers to the current device.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
    
# Flask-based APIs work locally on your computer without requiring an internet 
# connection because they run on your local machine as a server. This means that 
# when you run a Flask-based API on your computer, it creates a server that listens 
# for incoming requests on a specific port, and responds to those requests with the 
# appropriate data or actions.
# When you turn on the internet, the Flask-based API continues to work because it's 
# still running locally on your computer. However, if you want to make the API accessible 
# to other computers on the internet, you will need to configure your network settings to 
# allow incoming requests to the specific port that your API is running on. This usually 
# involves setting up port forwarding on your router, so that incoming requests to a 
# specific port are redirected to your computer's IP address.
