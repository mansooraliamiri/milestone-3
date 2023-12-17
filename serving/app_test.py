#from flask import Flask
#app = Flask(__name__)

#@app.route("/")
#def hello():
#    return "<h1 style='color:blue'>Hello There!</h1>"

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')

from flask import Flask, request, jsonify
import logging
import comet_ml
from joblib import load

class ModelHandler:
    def __init__(self):
        self.model = None
        self.init_logging()

    def init_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def load_model(self, model_name):
        try:
            self.model = load(model_name)
            self.logger.info(f'Model {model_name} loaded successfully.')
        except Exception as e:
            self.logger.error(f'Failed to load model {model_name}: {e}')

    def download_model_from_comet(self, model_name, workspace, registry_name, version):
        try:
            comet_api = comet_ml.API()
            comet_api.download_registry_model(registry_name, version, workspace, output_path=model_name)
            self.logger.info(f'Model {model_name} downloaded successfully from Comet.')
        except Exception as e:
            self.logger.error(f'Failed to download model from Comet: {e}')

    def predict(self, data):
        if self.model is None:
            self.logger.error('No model is loaded for prediction.')
            return None
        try:
            prediction = self.model.predict(data)
            return prediction
        except Exception as e:
            self.logger.error(f'Prediction failed: {e}')
            return None

app = Flask(__name__)
model_handler = ModelHandler()

@app.route('/logs', methods=['GET'])
def logs():
    # Implement the logic to return logs
    return jsonify({'logs': 'Logs data here'})

@app.route('/download_registry_model', methods=['POST'])
def download_registry_model():
    content = request.json
    model_handler.download_model_from_comet(content['model_name'], content['workspace'], content['registry_name'], content['version'])
    return jsonify({'status': 'Model download initiated'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model_handler.predict(data)
    if prediction is not None:
        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    model_handler.load_model('20162017.pkl')  # Load default model on startup
    app.run(port=5000, threaded=True)  # Using threaded mode for better performance with Flask
