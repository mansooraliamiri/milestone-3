import streamlit as st
import pandas as pd
import numpy as np

st.title("Hockey Visualization App")

with st.sidebar:
    # Adding input for the sidebar
    workspace = st.selectbox('Workspace', ['Workspace 1', 'Workspace 2', 'Workspace 3'])
    model = st.selectbox('Model', ['Model 1', 'Model 2', 'Model 3'])
    version = st.selectbox('Version', ['Version 1', 'Version 2', 'Version 3'])
    st.button('Get model')

with st.container():
    # Adding Game ID input
    game_id = st.text_input('Game ID', '2021020329')
    st.button('Ping game')

with st.container():
    # Adding Game info and predictions
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

with st.container():
    # Adding data used for predictions
    st.subheader("Data used for predictions (and predictions)")
    data = np.random.rand(6, 8)  # Placeholder for the actual data
    df = pd.DataFrame(data, columns=[f'feature {i}' for i in range(8)])
    df['Event'] = [f'Event {i}' for i in range(6)]
    df = df.set_index('Event')
    st.dataframe(df)
