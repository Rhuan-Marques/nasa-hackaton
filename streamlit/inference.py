import pandas as pd
import streamlit as st
import seaborn as sns  # Adicione esta linha

def make_inferences(df):
    """
    Make inferences about the DataFrame.

    Parameters:
    df: DataFrame containing the data
    """
    st.subheader("Data Inferences")

    # Basic Statistics
    st.write("### Basic Statistics")
    st.write(df.describe(include='all'))

    # Sample Count by Sex
    if 'Sex' in df.columns:
        sex_counts = df['Sex'].value_counts()
        st.write("### Sample Count by Sex")
        st.bar_chart(sex_counts)
    else:
        st.warning("Column 'Sex' not found in the DataFrame.")

    # Sample Count by Space Travel
    if 'Space Travel' in df.columns:
        travel_counts = df['Space Travel'].value_counts()
        st.write("### Sample Count by Space Travel")
        st.bar_chart(travel_counts)
    else:
        st.warning("Column 'Space Travel' not found in the DataFrame.")

    # Correlation Matrix
    st.write("### Correlation Matrix")
    correlation_matrix = df.corr(numeric_only=True)  # Ensure only numeric columns are included
    st.write(correlation_matrix)
    st.write("### Correlation Heatmap")
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    st.pyplot()
