import streamlit as st
import pandas as pd
import sweetviz as sv
import matplotlib.pyplot as plt
import seaborn as sns
from autoviz import AutoViz_Class
from servicos.data_loading import load_data
from servicos.csv_parser import check_delimiter_consistency
import re  # Para verificar links nas colunas
import tempfile  # Para trabalhar com arquivos temporários
import os  # Para verificar a existência de arquivos
from servicos.time_series import TimeSeries
from servicos.table_class import Table
from servicos.multiple_linear_regression import MultipleLinearRegression


def contains_link(series):
    """Verifica se uma série contém links."""
    url_pattern = r'(http|https|www)\S*'
    return series.astype(str).apply(lambda x: bool(re.search(url_pattern, x)))


def filter_columns_with_links(df):
    """Remove colunas que contêm links."""
    columns_with_links = [col for col in df.columns if contains_link(df[col]).any()]
    return df.drop(columns=columns_with_links), columns_with_links


def main():
    st.title("Data Analysis App")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Variável para armazenar o DataFrame
    df = None

    # Verifique se o relatório Sweetviz já foi gerado nesta sessão
    if "sweetviz_report_generated" not in st.session_state:
        st.session_state.sweetviz_report_generated = False

    if uploaded_file is not None:
        lines = uploaded_file.read().decode("utf-8").splitlines()
        if not check_delimiter_consistency(lines, ','):
            st.warning("CSV file has inconsistent delimiters.")
            return

        df = load_data(uploaded_file)
        
        if df is not None:
            st.write("Data Loaded:")
            st.write(df)

            # Filtra as colunas que contêm links
            df_filtered, columns_with_links = filter_columns_with_links(df)
            table = Table.from_dataframe(df_filtered)
            if columns_with_links:
                st.write(f"Columns removed due to links: {columns_with_links}")

            # Sweetviz - Relatório de análise
            if not st.session_state.sweetviz_report_generated:  # Gera o relatório apenas uma vez
                st.subheader("Sweetviz Report")
                report = sv.analyze(df_filtered)  # Usando o DataFrame filtrado
                report.show_html("sweetviz_report.html")
                st.session_state.sweetviz_report_generated = True  # Atualiza a variável

            # Carregar e exibir o relatório Sweetviz uma única vez
            with open("sweetviz_report.html", "r") as f:
                html_content = f.read()
                st.components.v1.html(html_content, height=1000)

            # Criar um arquivo temporário para AutoViz
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                df_filtered.to_csv(tmp.name, index=False)
                tmp_path = tmp.name

            # AutoViz
            st.subheader("AutoViz Report")
            AV = AutoViz_Class()
            dft = AV.AutoViz(tmp_path, sep=",")  # Gera gráficos automáticos usando o caminho do arquivo
            
            # Exibir os gráficos gerados pelo AutoViz
            for fig in plt.get_fignums():  # Itera sobre as figuras geradas pelo AutoViz
                fig_obj = plt.figure(fig)  # Obtém a figura específica
                st.pyplot(fig_obj)  # Exibe a figura no Streamlit

            # Seção para seleção de colunas e geração de gráficos   
            st.subheader("Plot Relationships Between Variables")

            # Obtenha a lista de colunas disponíveis
            columns = df_filtered.columns.tolist()
            selected_columns = st.multiselect("Select columns for plotting", columns)

            if len(selected_columns) == 2:
                # Cria o gráfico com base nas colunas selecionadas
                fig, ax = plt.subplots()
                if df_filtered[selected_columns[0]].dtype in ['int64', 'float64'] and df_filtered[selected_columns[1]].dtype in ['int64', 'float64']:
                    # Gráfico de dispersão para colunas numéricas
                    sns.scatterplot(data=df_filtered, x=selected_columns[0], y=selected_columns[1], ax=ax)
                    ax.set_title(f'Scatter Plot between {selected_columns[0]} and {selected_columns[1]}')
                else:
                    # Gráfico de barras se uma das colunas for categórica
                    sns.countplot(data=df_filtered, x=selected_columns[0], hue=selected_columns[1], ax=ax)
                    ax.set_title(f'Count Plot of {selected_columns[0]} by {selected_columns[1]}')

                st.pyplot(fig)
            elif len(selected_columns) > 2:
                st.warning("Please select only two columns for plotting.")
            else:
                st.warning("Please select two columns to visualize.")

            st.subheader("Plot time series data")

            time_column = st.selectbox("Select time column for time series", table.numeric_columns)
            time_series_value_columns = st.multiselect("Select value columns for time series", table.numeric_columns)

            frequency = st.number_input("Enter frequency of time series", value=1)

            if not time_series_value_columns or not time_column:
                st.warning("Please select time column and value columns for time series.")
            else:
                serie = TimeSeries.from_table(table, time_column, time_series_value_columns, frequency)
                st.write("Data:")
                st.write(serie.data)
                st.write("Timestamps:")
                st.write(serie.timestamps)
                st.write("Descriptive statistics:")
                st.write(serie.describe())
                st.write("Trend:")
                trend = serie.calculate_trend()
                st.write(trend)
                st.write("Seasonal decomposition:")
                trend, seasonal, residual = serie.seasonal_decompose()
                st.write("Trend:")
                st.write(trend)
                st.write("Seasonal:")
                st.write(seasonal)
                st.write("Residual:")
                st.write(residual)
                st.write("Plot:")
                serie.plot()
                st.pyplot()

            st.subheader("Plot multiple linear regression")

            # Verifica se há colunas numéricas para executar a regressão linear
            linear_regression_x = st.multiselect("Select x columns for linear regression", table.numeric_columns)
            linear_regression_y = st.multiselect("Select y columns for linear regression", table.numeric_columns)

            with_residuous = st.selectbox("Plot with residuous", ["No", "Simple", "QQPlot"])

            if not linear_regression_x or not linear_regression_y:
                st.warning("Please select x and y columns for linear regression.")
            else:
                mlr = MultipleLinearRegression.from_table(table, linear_regression_x, linear_regression_y)
                mlr.fit()
                if with_residuous == "Simple":
                    fig = mlr.plot_residuals()
                elif with_residuous == "QQPlot":
                    fig = mlr.QQ_plot()
                else:
                    fig = mlr.plot()
                st.pyplot(fig)

if __name__ == "__main__":
    main()
