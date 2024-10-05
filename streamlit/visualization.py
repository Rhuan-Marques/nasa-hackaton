import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_data(df):
    """
    Plot data from the DataFrame.

    Parameters:
    df: DataFrame containing the data
    """
    st.subheader("Data Distribution")
    
    if "Factor Value[Age]" in df.columns:
        plt.figure(figsize=(10, 5))
        sns.histplot(df["Factor Value[Age]"], bins=30, kde=True)
        plt.title("Histogram of Factor Value[Age]")
        st.pyplot(plt)
    else:
        st.warning("Column 'Factor Value[Age]' not found in the DataFrame.")
