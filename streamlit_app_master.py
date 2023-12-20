#Mansoorali Amiri
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
        print(game_id)
        print('**********')

        with st.container():
            
            try:
                json_data = GameClient.setup_game(game_id)
                print('LOADING DATA')
                st.subheader("Data used for predictions (and predictions)")
                # Accéder à une caractéristique spécifique
                game_id = json_data['id']
                game_date = json_data['gameDate']
                venue = json_data['venue']['default']

                print("Game ID:", game_id)
                print("Game Date:", game_date)
                print("Venue:", venue)

                # Accéder aux événements
                #if 'plays' in json_data:
                #    for event in json_data['plays']:
                #        event_id = event.get('eventId', None)
                #        period = event.get('period', None)
                #        event_type = event.get('typeDescKey', None)
                #        details = event.get('details', {})
                #data = np.random.rand(6, 8)  # Placeholder for the actual data
                #df = pd.DataFrame(data, columns=[f'feature {i}' for i in range(8)])
                #df['Event'] = [f'Event {i}' for i in range(6)]
                #df = df.set_index('Event')
                #st.dataframe(df)
                        
                events = json_data.get('plays', [])

                # Create a DataFrame for events
                data = []
                for event in events:
                    # Extracting event features
                    event_id = event.get('eventId')
                    period = event.get('period')
                    time_in_period = event.get('timeInPeriod')
                    time_remaining = event.get('timeRemaining')
                    situation_code = event.get('situationCode')
                    type_code = event.get('typeCode')
                    type_desc_key = event.get('typeDescKey')
                    details = event.get('details', {})
                    
                    # Adding to data list
                    data.append([event_id, period, time_in_period, time_remaining, situation_code, type_code, type_desc_key, json.dumps(details)])

                # Creating DataFrame
                df = pd.DataFrame(data, columns=[f'feature {i}' for i in range(8)])
                df['Event'] = [f'Event {i}' for i in range(len(data))]
                df = df.set_index('Event')
                st.dataframe(df)
                # Show a snippet of the DataFrame
                #df.head()
            except Exception as e:
                st.write("Une erreur s'est produite. Veuillez réessayer")
                print(e)
                #print(traceback.format_exc())
    

    


        


# Exécution principale
if __name__ == "__main__":
    app = HockeyApp()
    current_dir = setup_directory()
    print(current_dir)
    app.download_model()
    app.game_interaction()
