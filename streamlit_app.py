#Mansoorali Amiri
import streamlit as st
import pandas as pd
import os
import sys
from client.ServingClient import ServingClient
from client.GameClient import GameClient
import json
import traceback

# Set up environment
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

# Initialize clients
serving_client = ServingClient(ip="0.0.0.0", port=8501)
game_client = GameClient()

# Utility functions
def download_model(workspace, model, version):
    serving_client.download_registry_model(workspace=workspace, model=model, version=version)
    st.write('Model Downloaded')

def process_game_data(game_id):
    try:
        filepath = game_client.get_game(game_id=game_id)
        return game_client.ping_game(filepath)
    except Exception as e:
        st.write("Error processing game data.")
        print(e)
        print(traceback.format_exc())

def display_game_info(game_id, model_df, last_event_df, new_dataframe_length):
    # Implement the logic for displaying game information
    pass

def display_predictions(model_df):
    # Implement the logic for displaying predictions
    pass

# Streamlit layout
st.title("Hockey Visualization App")

# Sidebar for model download
with st.sidebar:
    workspace = st.text_input('Workspace', 'Workspace x')
    model = st.text_input('Model', 'Model y')
    version = st.text_input('Version', 'Version z')
    if st.button('Get Model'):
        download_model(workspace, model, version)

# Main container for game data processing
with st.container():
    game_id = st.text_input('Game ID', '2022030411')
    if st.button('Ping game'):
        model_df, last_event_df, new_dataframe_length = process_game_data(game_id)
        display_game_info(game_id, model_df, last_event_df, new_dataframe_length)
        display_predictions(model_df)
