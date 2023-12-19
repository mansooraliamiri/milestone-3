#Mansoorali Amiri
import json
import requests
import pandas as pd
import logging
import os
import numpy as np
import math
import time
import sys
# Obtention du répertoire courant où se trouve le script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtention du répertoire parent
parent_dir = os.path.dirname(current_dir)


# Configuration du chemin pour l'importation des modules
#def setup_import_paths():
#    current_directory = os.path.dirname(os.path.abspath(__file__))
#    parent_directory = os.path.dirname(current_directory)
#    sys.path.append(parent_directory)

#setup_import_paths()

from featureLists import *

chemin_dossier_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(chemin_dossier_parent)
from data.load import NHLDataDownloader 


class GameClient:
    def setup_game( game_id):
        season_year = 2018
        nhl_downloader = NHLDataDownloader(season_year)
        season_data = nhl_downloader.load_data()
        
        game_id =  nhl_downloader.load_df_shots(game_id)
        return game_id

# Exécution principale
#if __name__ == "__main__":
#    test = GameClient.setup_game('2016')
#    print(test)


