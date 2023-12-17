#Mansoorali Amiri
import os
import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import VarianceThreshold, SelectKBest, chi2
from xgboost import XGBClassifier
import shap
from dotenv import load_dotenv
from comet_ml import Experiment

# Ensure the parent directory is in the path for module imports
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils import load_data 
from notebooks.plot_m3 import *

# Load environment variables
load_dotenv()
COMET_API_KEY = os.getenv('COMET_KEY')

# Function for normalization
def normalize_data(df_X):
    cols = ['x_coordinate', 'y_coordinate', 'game_time(s)', 'prev_event_x', 'prev_event_y',
            'time_since_prev_event', 'distance_to_prev_event', 'speed_since_prev_event',
            'shot_distance', 'shot_angle', 'change_in_angle', 'time_since_pp']
    zscore = (df_X[cols] - df_X[cols].mean()) / df_X[cols].std(ddof=0)
    minmax = (df_X[cols] - df_X[cols].min()) / (df_X[cols].max() - df_X[cols].min())
    return zscore, minmax

# Function for feature selection
def select_features(df_X, df_y, model):
    zscore, minmax = normalize_data(df_X)
    results = {
        'base': evaluate_model(model, df_X, df_y),
        'z_score': evaluate_model(model, zscore, df_y),
        'minmax': evaluate_model(model, minmax, df_y),
        'low_var': evaluate_low_variance(model, df_X, df_y),
        'univar': evaluate_univariate(model, minmax, df_y),
        'fwd_search': evaluate_forward_search(model, df_X, df_y)
    }
    return results

# Evaluation functions
def evaluate_model(model, X, y):
    return np.mean(cross_val_score(model, X.to_numpy(), y.to_numpy(), cv=5))

def evaluate_low_variance(model, df_X, df_y):
    sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
    X_new = sel.fit_transform(df_X)
    return np.mean(cross_val_score(model, X_new, df_y, cv=5))

def evaluate_univariate(model, X, y):
    X_new = SelectKBest(chi2, k=10).fit_transform(X, y)
    return np.mean(cross_val_score(model, X_new, y, cv=5))

def evaluate_forward_search(model, df_X, df_y):
    pass

# SHAP Analysis function
def analyze_shap(model, X, y):
    trained_model = model.fit(X, y)
    explainer = shap.Explainer(trained_model)
    shap_values = explainer(X)
    shap.plots.waterfall(shap_values[0])
    plt.close()

def main():
    feature_list = [...]  
    df_X, df_y, _, _ = load_data(...)  

    params = {...} 
    xgb_model = XGBClassifier(**params)
      
    results = select_features(df_X, df_y, xgb_model)
    analyze_shap(xgb_model, df_X, df_y)
    
    file_name = "xgb_feature.pkl"
    pickle.dump(xgb_model, open(file_name, "wb"))
    
    experiment = Experiment(api_key=COMET_KEY, project_name="milestone3", workspace="ift6758")
    experiment.log_metrics(results)
    experiment.log_model('best_features', file_name)
    print('Results:', results)

if __name__ == "__main__":
    main()
