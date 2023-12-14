import json
import requests
import pandas as pd
import logging
import pickle
from ift6758.data.load import *
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 5000, features=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features
        #self.scaler = pickle.load(open('data.pkl','rb'))
        # any other potential initialization

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.
        
        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """
        # Convert des DataFrame à JSON
        data_json = X.to_json(orient='split')
        X = NHLDataDownloader.load_data(X)

        # Send the POST request to the server
        response = requests.post(f"{self.base_url}/predict", json=data_json)

        # Vérifier si la réponse est réussie
        if response.status_code == 200:
            # Convert the response to DataFrame
            response_data = response.json()
            result_df = pd.DataFrame(response_data)
        else:
            # Handle errors 
            result_df = pd.DataFrame({'error': ['Error occurred while making prediction']})

        return result_df
        #raise NotImplementedError("TODO: implement this function")

    def logs(self) -> dict:
        """Get server logs"""
        logger = logging.getLogger(__name__)

        try:
            # Log avant d'envoyer la demande
            logger.info("Sending request to server to get logs")

            # Envoyer la requête GET au serveur pour les journaux
            response = requests.get(f"{self.base_url}/logs")

            # Enregistrer l'état de la réponse
            logger.info(f"Received response with status code: {response.status_code}")

            if response.status_code == 200:
                # Bien reçu les logs
                logs_data = response.json()
                return logs_data
            else:
                # Handle non-successful demande
                logger.error(f"Error in getting logs: {response.status_code}")
                return {"error": f"Failed to get logs: {response.status_code}"}

        except Exception as e:
            # Log exceptions
            logger.exception("Exception occurred while getting logs")
            return {"error": str(e)}
        #raise NotImplementedError("TODO: implement this function")

    def download_registry_model(self, workspace: str, model: str, version: str) -> dict:
        """
        Triggers a "model swap" in the service; the workspace, model, and model version are
        specified and the service looks for this model in the model registry and tries to
        download it. 

        See more here:

            https://www.comet.ml/docs/python-sdk/API/#apidownload_registry_model
        
        Args:
            workspace (str): The Comet ML workspace
            model (str): The model in the Comet ML registry to download
            version (str): The model version to download
        """
        logger = logging.getLogger(__name__)

        try:
            # Log pour les détails de la demande
            logger.info(f"Requesting to download model: {model}, version: {version} from workspace: {workspace}")

            # Préparer les données pour la requête POST
            data = {
                "workspace": workspace,
                "model": model,
                "version": version
            }

            # Envoyer la requête POST au serveur Flask
            response = requests.post(f"{self.base_url}/download_model", json=data)

            # Log l'état de la réponse
            logger.info(f"Received response with status code: {response.status_code}")

            if response.status_code == 200:
                # Successfully télécharger
                download_info = response.json()
                return download_info
            else:
                # Handle non-successful la demande
                logger.error(f"Error in time  downloading model: {response.status_code}")
                return {"error": f"Failed to download model: {response.status_code}"}

        except Exception as e:
            # Log exceptions
            logger.exception("Exception occurred while downloading model")
            return {"error": str(e)}
        #raise NotImplementedError("TODO: implement this function")
