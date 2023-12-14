"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app

gunicorn can be installed via:

    $ pip install gunicorn

"""
import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import joblib
from ift6758.client.get_comet import get_comet_model

import ift6758



# Configuration des variables globales et de l'application Flask
LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")
MODELS_DIR = os.environ.get("FLASK_MODELS", "data/")
app = Flask(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, filemode='w')
global model, clf

#@app.before_first_request
#def setup():
#    print("Cette fonction est exécutée une fois avant le premier traitement de requête.")



#@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    global clf, model
    app.logger.info('Initialization')
    default_model = "logreg-distance-angle"
    model_path = Path(MODELS_DIR) / f"{default_model}.pkl"
    if not model_path.is_file():
        app.logger.info(f"Downloading {default_model} from COMET")
        get_comet_model(default_model, MODELS_DIR, download=True, workspace="morph-e")
    model = default_model
    clf = joblib.load(model_path)
    app.logger.info(f"Loaded default model: {default_model}")


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    
    with open(LOG_FILE, 'r') as log_file:
        log_data = log_file.readlines()
    return jsonify(log_data)


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Recommend (but not required) json with the schema:

        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }
    
    """
    # Get POST json data
    json = request.get_json()
    app.logger.info(json)

    # TODO: check to see if the model you are querying for is already downloaded



    global clf, model
    request_data = request.get_json()
    app.logger.info(request_data)
    new_model = request_data["model"]
    model_path = Path(MODELS_DIR) / f"{new_model}.pkl"
    model_exists = model_path.is_file()
    # TODO: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the 
    # currently loaded model
    if not model_exists:
        app.logger.info(f"Downloading {new_model} from COMET")
        get_comet_model(new_model, MODELS_DIR, download=True, workspace=request_data["workspace"], model_version=request_data["version"])
    # TODO: if yes, load that model and write to the log about the model change.  
    # eg: app.logger.info(<LOG STRING>)
    model = new_model
    clf = joblib.load(model_path)
    app.logger.info(f"Switched to model: {new_model}")
    response = {"new_classifier": new_model, "model_already_exists": model_exists}
    app.logger.info(response)
    # Tip: you can implement a "CometMLClient" similar to your App client to abstract all of this
    # logic and querying of the CometML servers away to keep it clean here
    return jsonify(response)  # response must be json serializable!


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions
    """

    
    #response = None
    # Get POST json data
    input_data = request.get_json()
    app.logger.info(input_data)
    df_pred = pd.read_json(input_data, orient="table")
    predictions = clf.predict(df_pred)
    probabilities = clf.predict_proba(df_pred)[:, 1]
    df_pred["predictionIsGoal"] = predictions
    df_pred["probaIsGoal"] = probabilities
    response_data = df_pred[["probaIsGoal", "predictionIsGoal"]].to_json()
    app.logger.info(response_data)
    
    return jsonify(response_data) # response must be json serializable!

# Code pour démarrer le serveur, si nécessaire
#if __name__ == "__main__":
#    from waitress import serve
#    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

