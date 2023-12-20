# Importations et configurations initiales
import os
import sys
import json
import pandas as pd
import streamlit as st
from ift6758.ift6758.client.servingClient import ServingClient
from ift6758.ift6758.client.gameClient import GameClient

# Définition du répertoire courant et ajout au PATH
def setup_directory():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(current_dir)
    return current_dir

# Création d'une classe pour encapsuler les fonctionnalités de l'application
class HockeyApp:
    def __init__(self):
        self.setup_streamlit()
        self.sc = ServingClient(ip="0.0.0.0", port=8501)
        self.gc = GameClient()

    def setup_streamlit(self):
        st.title("Hockey Visualization App")

    def download_model(self):
        #workspace = st.selectbox('Workspace', ['Workspace x', 'Workspace y', 'Workspace z'])
        #model = st.selectbox('Model', ['Model x', 'Model y', 'Model z'])
        #version = st.selectbox('Version', ['Version x', 'Version y', 'Version z'])

        workspace = st.sidebar.selectbox('Version', ['Version x', 'Version y', 'Version z'])
        model = st.sidebar.selectbox('Model', ['Model x', 'Model y', 'Model z'])
        version = st.sidebar.text_input('Version', 'Version z')
        if st.sidebar.button('Get Model'):
            self.sc.download_registry_model(workspace, model, version)
            st.sidebar.write('Model Downloaded')

    def game_interaction(self):
        game_id = st.container().text_input('Game ID', '2021020329')
        if st.container().button('Ping game'):
            self.process_game_id(game_id)

    def process_game_id(self, game_id):
        # Le reste de la logique pour traiter l'ID de jeu
        # Cette partie comprendra la plupart du code de la fonction 'ping_game_id'
        pass

# Exécution principale
if __name__ == "__main__":
    app = HockeyApp()
    current_dir = setup_directory()
    print(current_dir)
    app.download_model()
    app.game_interaction()
