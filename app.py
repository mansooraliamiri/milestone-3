#Mansoorali Amiri
from comet_ml import API
from dotenv import load_dotenv
import os
import logging
from flask import Flask, jsonify, request
import pandas as pd
import pickle

load_dotenv()

class ModelHandler:
    def __init__(self):
        self.loaded_models_dir = 'loaded_models'
        self.classifier = None
        self.log_file = os.environ.get("FLASK_LOG", "flask.log")
        self.init_logging()

    def init_logging(self):
        logging.basicConfig(filename=self.log_file, level=logging.INFO)

    def load_model(self, model_name):
        if not os.path.isfile(os.path.join(self.loaded_models_dir, model_name)):
            logging.info(f'No local file {model_name} found. Attempting download from Comet.')
            self.download_model_from_comet(model_name)
        if os.path.isfile(os.path.join(self.loaded_models_dir, model_name)):
            self.classifier = pickle.load(open(os.path.join(self.loaded_models_dir, model_name), 'rb'))
            logging.info(f'Model {model_name} loaded successfully.')
        else:
            logging.error('Model download failed. Check API key and model details.')

    def download_model_from_comet(self, model_name, workspace, registry_name, version):
        api_key = os.getenv('COMET_KEY')
        request = {'workspace': workspace, 'registry_name': registry_name, 'version': version}
        API(api_key=api_key).download_registry_model(**request, output_path=self.loaded_models_dir)

    def predict(self, data):
        try:
            df = pd.read_json(data)
            predictions = self.classifier.predict_proba(df)[:, 1]
            return pd.DataFrame(predictions).to_json()
        except Exception as e:
            logging.error(f"An error occurred during prediction: {e}")
            return str(e)

app = Flask(__name__)
model_handler = ModelHandler()

@app.route('/logs', methods=['GET'])
def logs():
    if os.path.isfile(model_handler.log_file):
        with open(model_handler.log_file) as f:
            response = f.read().splitlines()
    else:
        response = f"{model_handler.log_file} is an invalid log file path."
        logging.info(response)
    return jsonify(response)

@app.route('/download_registry_model', methods=['POST'])
def download_registry_model():
    data = request.get_json()
    model_handler.download_model_from_comet(data['model_name'], data['workspace'], data['registry_name'], data['version'])
    model_handler.load_model(data['model_name'])
    response = f'Download and loading of {data["model_name"]} completed.'
    return jsonify(response)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify(model_handler.predict(data))

if __name__ == '__main__':
    model_handler.load_model('6-LGBM.pkl')  # Load default model on startup
    app.run(port=5000)
