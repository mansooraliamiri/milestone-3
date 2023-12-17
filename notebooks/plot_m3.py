#Mansoorali Amiri
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import roc_curve, auc
from sklearn.calibration import CalibrationDisplay
from comet_ml import Experiment

FIGURE_PATH = os.path.join(os.path.dirname(__file__), '..', 'figures', 'ms3')

# Function to save and log figures
def save_log_figure(figure, figure_name, plot_num, experiment):
    fig_path = os.path.join(FIGURE_PATH, f'{plot_num}_{figure_name}.png')
    plt.savefig(fig_path)
    plt.close()
    if experiment:
        experiment.log_figure(figure_name=figure_name, figure=figure)

# Function for ROC AUC plot
def plot_roc(y_vals, y_preds, model_names, plot_num, experiment=None):
    fig = plt.figure(figsize=(10, 10))
    for idx, y_pred in enumerate(y_preds):
        fpr, tpr, _ = roc_curve(y_vals, y_pred)
        plt.plot(fpr, tpr, label=f"Model {model_names[idx]} AUC: {auc(fpr, tpr):.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="navy")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title(f"Plot {plot_num}: ROC")
    plt.legend(loc="lower right")
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.show()
    save_log_figure(fig, 'roc', plot_num, experiment)

# Function for Cumulative Goal plot
def plot_cum_goal(y_vals, y_preds, model_names, plot_num, experiment=None):
    fig = plt.figure(figsize=(10, 10))
    for idx, y_pred in enumerate(y_preds):
        cum_data = cum_goal_data(y_vals, y_pred)
        sns.ecdfplot(data=cum_data, x=100 - cum_data['percentile'], label=model_names[idx])
    adjust_plot_labels()
    plt.title(f"Plot {plot_num}: Cum. Goals")
    plt.show()
    save_log_figure(fig, 'cum_goals', plot_num, experiment)

def cum_goal_data(y_vals, y_pred):
    percentile = 100 * stats.rankdata(y_pred, "min") / len(y_pred)
    return pd.DataFrame({'percentile': percentile, 'goal': y_vals})

# Function for Goal Rate plot
def plot_goal_rate(y_vals, y_preds, model_names, plot_num, experiment=None):
    fig = plt.figure(figsize=(10, 10))
    for idx, y_pred in enumerate(y_preds):
        df = prepare_goal_rate(y_vals, y_pred)
        sns.lineplot(x=100 - df['percentile'], y=df['goal_rate'], label=model_names[idx])
    adjust_plot_labels()
    plt.title(f"Plot {plot_num}: Goal Rate")
    plt.show()
    save_log_figure(fig, 'goal_rate', plot_num, experiment)

def prepare_goal_rate(y_vals, y_pred):
    # Data preparation logic for goal rate plot
    # ...
    pass

# Adjust labels and grid for plots
def adjust_plot_labels():
    plt.yticks(np.arange(0, 1.05, 0.1))
    plt.xticks(np.arange(0, 101, 10))
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend(loc='lower right')

# Function for Calibration plot
def plot_calibration(y_vals, y_preds, model_names, plot_num, experiment=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    for idx, y_pred in enumerate(y_preds):
        CalibrationDisplay.from_predictions(y_vals, y_pred, label=model_names[idx], ax=ax)
    plt.title(f"Plot {plot_num}: Calibration")
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend(loc="center right")
    plt.show()
    save_log_figure(fig, 'calibration', plot_num, experiment)
