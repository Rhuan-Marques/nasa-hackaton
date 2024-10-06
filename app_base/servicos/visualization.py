import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from autoviz.AutoViz_Class import AutoViz_Class
from ydata_profiling import ProfileReport  # Alterado para ydata_profiling
import re  # Para verificar links nas colunas


def contains_link(series):
    """Verifica se uma série contém links."""
    url_pattern = r'(http|https|www)\S*'
    return series.astype(str).apply(lambda x: bool(re.search(url_pattern, x)))


def filter_columns_with_links(df):
    """Remove colunas que contêm links."""
    columns_with_links = [col for col in df.columns if contains_link(df[col]).any()]
    return df.drop(columns=columns_with_links)


def analyze_data(df):
    """Analisa as colunas e retorna os tipos de dados."""
    column_types = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            column_types[column] = 'numerical'
        elif pd.api.types.is_categorical_dtype(df[column]) or pd.api.types.is_object_dtype(df[column]):
            column_types[column] = 'categorical'
        else:
            column_types[column] = 'other'
    return column_types


def plot_numerical_data(df, column):
    """Plota dados numéricos."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], bins=20, kde=True)
    plt.title(f'Distribuição de {column}')
    plt.xlabel(column)
    plt.ylabel('Frequência')
    st.pyplot(plt)


def plot_categorical_data(df, column):
    """Plota dados categóricos."""
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x=column, palette='pastel')
    plt.title(f'Contagem de Amostras por {column}')
    plt.xlabel(column)
    plt.ylabel('Contagem')
    st.pyplot(plt)


def plot_data(df):
    """Chama as funções de AutoViz."""
    st.subheader("AutoViz Analysis")
    AV = AutoViz_Class()
    AV.AutoViz('', dfte=df)  # Gera gráficos automáticos


def generate_profile_report(df):
    """Gera um relatório completo com YData Profiling."""
    st.subheader("YData Profiling Report")
    profile = ProfileReport(df, title="YData Profiling Report", explorative=True)
    st.components.v1.html(profile.to_html(), height=1000)  # Exibir o relatório no Streamlit


def main(df):
    """Função principal para gerar visualizações e relatórios."""
    st.title("Data Analysis and Visualization")

    # Aplicar o filtro de colunas com links
    df_filtered = filter_columns_with_links(df)
    if df_filtered.shape[1] < df.shape[1]:
        st.write("Colunas com links foram removidas da análise.")

    # Opção para visualizações tradicionais e AutoViz
    if st.checkbox("Gerar visualizações automaticamente com AutoViz"):
        plot_data(df_filtered)

    # Opção para relatório completo com YData Profiling
    if st.checkbox("Gerar relatório completo com YData Profiling"):
        generate_profile_report(df_filtered)
