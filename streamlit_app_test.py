import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("Hockey Visualization App")

with st.sidebar:
    # Adding input for the sidebar
    workspace = st.selectbox('Workspace', ['Workspace x', 'Workspace y', 'Workspace z'])
    model = st.selectbox('Model', ['Model x', 'Model y', 'Model z'])
    version = st.selectbox('Version', ['Version x', 'Version y', 'Version z'])
    st.button('Get model')

# Function to simulate data loading
def load_data():
    time.sleep(5)  # Simulate a delay in loading data
    data = np.random.rand(6, 8)  # Placeholder for the actual data
    df = pd.DataFrame(data, columns=[f'feature {i}' for i in range(8)])
    df['Event'] = [f'Event {i}' for i in range(6)]
    return df.set_index('Event')

with st.container():
    # Adding Game ID input
    game_id = st.text_input('Game ID', '2021020329')
    if st.button('Ping game'):
        with st.spinner('Loading data...'):
            df = load_data()
            st.success('Data Loaded!')

        # Displaying Game info and predictions
        st.header(f"Game {game_id}: Canucks vs Avalanche")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Canucks xG (actual)")
            st.write("3.2 (3)")
            st.caption("↓0.2")
        with col2:
            st.subheader("Avalanche xG (actual)")
            st.write("1.4 (2)")
            st.caption("↑0.4")

        # Adding data used for predictions
        st.subheader("Data used for predictions (and predictions)")
        st.dataframe(df)
