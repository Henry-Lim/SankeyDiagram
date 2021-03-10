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
    
    #Once the file uploader detects the file
    if file is not None:
        df = pd.read_csv(file)
        
    #Once the button to plot is pressed
    if st.button('Plot'):
        
        #TO DO: place a Streamlit (app) checkbox to mark if numeric is true or not
        #Numeric in this sense means if the source and target nodes represent positions down the label
        #Say if labels are 'A', 'B', 'C' - these labels are represented as 0, 1, 2 in numeric representation
        numeric = True
        
        #if target/source not in numeric mode":
        
        #get label names for diagram
        label_names = df.label[df.label.notnull()].tolist()
        
        #initialise label values to append to labels for diagram nodes
        label_vals = np.zeros(len(label_names))
        
        #initialise label dictionary to correspond above two
        label_dict = {}
        
        #Implement numeric check
        if numeric:
            #check for nodes with zero incoming flow - 'proper' sources
            #this actually avoids these nodes' label values from being zero
            for i in range(len(df.label)):
                if i not in df.target.tolist() and pd.isnull(df.values[i]).any() == False:
                    #gets values from where the nodes in question are on the source side,
                    #not the target side
                    for j in np.where(df.source.to_numpy() == i):
                        label_vals[i] += df.value[j]
                        
            targsvals = df[['source','target', 'value']]
            
            #adds values to nodes such that their value represents the total incoming flow
            for i in range(len(targsvals)):
                source, target, value = targsvals.iloc[i]
                label_vals[target] += value
            target = df.target
            source = df.source
        else:
            #TO DO: what if the source and target nodes are not numbered, but instead are label names?
            pass
        
        
        #Adds values and label names to a dictionary, which makes the next step easier
        for i in range(len(label_names)):
            label_dict[label_names[i]] = label_vals[i]
        
        #Place a 'label list' where the values and label names can be together
        label_insert = [f"{name}:{label_dict[name]}" for name in label_dict]
        
        #Plot figure
        fig = go.Figure(go.Sankey(arrangement = "snap", 
                                  node = {"label": label_insert,
                                          "pad":10},  # 10 Pixels                          
                                  link = {"source": source,
                                          "target": target,
                                          "value": df.value}))
        st.write(fig)


if __name__ == "__main__": 
    main()