import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """
    Load the CSV data from the uploaded file.
    
    Parameters:
    uploaded_file: Uploaded CSV file

    Returns:
    DataFrame: Loaded DataFrame
    """
    try:
        # Tente diferentes delimitadores, por exemplo, ';' se o CSV estiver assim
        df = pd.read_csv(uploaded_file, sep=',')  # Altere ',' para ';' ou outro delimitador, se necessário
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
