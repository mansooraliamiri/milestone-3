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
import pkgutil
# Obtention du répertoire courant où se trouve le script

# Obtention du répertoire parent
#parent_dir = os.path.dirname(current_dir)


# Configuration du chemin pour l'importation des modules
#def setup_import_paths():
#    current_directory = os.path.dirname(os.path.abspath(__file__))
#    parent_directory = os.path.dirname(current_directory)
#    sys.path.append(parent_directory)


#from client.featureLists import *


# source usagé: https://blog.enterprisedna.co/python-import-from-parent-directory/
# source usagé: https://stackoverflow.com/questions/1054271/how-to-import-a-python-class-that-is-in-a-directory-above

#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

#sys.path.append('..')


#path_to_directory = '/code/ift6758/ift6758/'
# Change the current working directory to the specified path
#os.chdir(path_to_directory)

# Optionally, add the directory path to sys.path if you plan to import these modules
#if path_to_directory not in sys.path:
#    sys.path.append(path_to_directory)

# List all modules in the current directory
#os.chdir(path_to_directory)

# List all importable modules in the current directory
#print("Modules available in the current directory:")
#for module in pkgutil.iter_modules():
#    print(module.name)

# Add this path to sys.path
#if path_to_directory not in sys.path:
#    sys.path.append(path_to_directory)
#print('path:=== ',sys.path)
#from data.load import NHLDataDownloader , load_game
#sys.path.append('..')
#from data.load import NHLDataDownloader , load_game
from ..data import load



class GameClient:
    def setup_game( game_id ):
        
        #season_year = 2016
        #nhl_downloader = NHLDataDownloader(season_year)
        #season_data = nhl_downloader.load_data()
        data_game = load.load_game(game_id)
        #nhl_downloader.load_processed_data()
        #game_id =  nhl_downloader.load_df_shots(game_id)
        print('data_game ===> ',data_game)
        return data_game


# Exécution principale
if __name__ == "__main__":
    test = GameClient.setup_game('2016')
    print(test)


