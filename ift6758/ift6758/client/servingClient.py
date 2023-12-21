#Mansoorali Amiri
import json
import requests
import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

# Configuration du logger
logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self, transformer=None):
        if transformer is None:
            transformer = make_column_transformer(
                (OneHotEncoder(), ['shot_type', 'last_event_type']),
                remainder='passthrough'
            )
        self.transformer = transformer

    def load_data(self, data_link):
        if not isinstance(data_link, pd.DataFrame):
            data_df = pd.read_csv(data_link)
        else:
            data_df = data_link

        data_df = self.rename_columns(data_df)
        data_df = self.transform_data(data_df)
        return data_df

    @staticmethod
    def rename_columns(df):
        rename_dict = {
            'game date': 'game_date', 'period time': 'period_time',
            # Ajouter d'autres renommages ici
        }
        df.rename(columns=rename_dict, inplace=True)
        return df

    def transform_data(self, df):
        df['is_rebound'] = np.where(df['is_rebound'] == False, 0, 1)
        transformed = self.transformer.fit_transform(df)
        transformed_df = pd.DataFrame(transformed, columns=self.transformer.get_feature_names_out())
        transformed_df.dropna(inplace=True)
        return transformed_df


class ServingClient:
    def __init__(self, ip="0.0.0.0", port=8501, features=None):
        self.base_url = f"http://{ip}:{port}"
        self.features = features or ["distance"]
        self.data_loader = DataLoader()
        logger.info(f"Initialized with URL: {self.base_url}")

    def predict(self, X):
        try:
            logger.info("Requesting predictions")
            X_transformed = self.data_loader.load_data(X)
            response = requests.post(f"{self.base_url}/predict", json=json.loads(X_transformed.to_json()))
            return response.json()
        except Exception as e:
            logger.error(f"Prediction request failed: {e}")
            return None

    def fetch_logs(self):
        logger.info("Fetching server logs")
        response = requests.get(f"{self.base_url}/logs")
        return response.json()

    def download_registry_model(self, workspace, model, version):
        logger.info(f"Downloading model {model} version {version}")
        response = requests.post(f"{self.base_url}/download_registry_model",
                                 json={'workspace': workspace, 'model': model, 'version': version})
        print('download_registry_model: ', response)
        #return response
        return response.json()
    

