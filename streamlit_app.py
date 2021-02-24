import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd


# Helper function for the main page
def main():
    st.title('Sankey Diagram Web Application')
    
    file = st.file_uploader("Upload file", type=['txt', 'csv']) # Upload file
    
    if file is not None:
        df = pd.read_csv(file)

    if st.button('Plot'):
        fig = go.Figure(go.Sankey(arrangement = "snap", 
                                  node = {"label": df.label,
                                          "x": df.x,
                                          "y": df.y,
                                          "pad":10},  # 10 Pixels                          
                                  link = {"source": df.source,
                                          "target": df.target,
                                          "value": df.value}))
        st.write(fig)
    

if __name__ == "__main__": 
    main()