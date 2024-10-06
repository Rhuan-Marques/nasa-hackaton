import streamlit as st
import pandas as pd
from scipy import stats

def make_inferences(df):
    """Gera inferências e análises estatísticas com base nos dados do DataFrame."""
    
    st.subheader("Inferences")
    st.write("Here are some potential inferences based on the data:")

    if not df.empty:
        # Número de amostras
        st.write(f"Number of samples: {len(df)}")
        
        # Estatísticas descritivas
        st.write("Summary statistics:")
        st.write(df.describe(include='all'))  # Inclui colunas não numéricas

        # Medidas de tendência central
        st.write("Measures of Central Tendency:")
        for column in df.select_dtypes(include=['float64', 'int64']).columns:
            mean = df[column].mean()
            median = df[column].median()
            mode_series = df[column].mode()
            mode = mode_series[0] if not mode_series.empty else 'No mode available'
            st.write(f"- **{column}:** Mean = {mean:.2f}, Median = {median:.2f}, Mode = {mode}")

            # Teste de normalidade com Shapiro-Wilk
            shapiro_test = stats.shapiro(df[column].dropna())
            st.write(f"  Normality Test (Shapiro-Wilk): p-value = {shapiro_test.pvalue:.5f}")

        # Identificação de valores ausentes
        missing_values = df.isnull().sum()
        if missing_values.any():
            st.write("Missing Values:")
            st.write(missing_values[missing_values > 0])

        # Correlações entre variáveis numéricas
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numeric_columns) > 0:
            correlation_matrix = df[numeric_columns].corr()
            st.write("Correlation Matrix:")
            st.write(correlation_matrix)
            st.line_chart(correlation_matrix)

        # Contagem de categorias para colunas categóricas
        categorical_columns = df.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            st.write("Counts of Categorical Variables:")
            for col in categorical_columns:
                counts = df[col].value_counts()
                st.write(f"- **{col}:**")
                st.write(counts)
    else:
        st.write("The DataFrame is empty, no inferences can be made.")
