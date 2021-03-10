import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import webbrowser


# Helper function for the main page
def main():
    st.title('Sankey Diagram Web Application')
        
    link = '[View Source Code](https://github.com/Henry-Lim/SankeyDiagram)'
    st.markdown(link, unsafe_allow_html=True)
    
    file = st.file_uploader("Upload file", type=['txt', 'csv']) # Upload file
    
    if file is not None:
        df = pd.read_csv(file)

    if st.button('Plot'):
        
        label_names = df.label[df.label.notnull()].tolist()
        label_vals = np.zeros(len(label_names))
        label_dict = {}
        targsvals = df[['target', 'value']]
        for i in range(len(targsvals)):
            target, value = targsvals.iloc[i]
            label_vals[target] += value

        for i in range(len(label_names)):
            label_dict[label_names[i]] = label_vals[i]

        label_insert = [f"{name}:{label_dict[name]}" for name in label_dict]
        
        fig = go.Figure(go.Sankey(arrangement = "snap", 
                                  node = {"label": label_insert,
                                          "x": df.x,
                                          "y": df.y,
                                          "pad":10},  # 10 Pixels                          
                                  link = {"source": df.source,
                                          "target": df.target,
                                          "value": df.value}))
        st.write(fig)


if __name__ == "__main__": 
    main()