import streamlit as st
from utils.create_time_series import create_time_series
import matplotlib.pyplot as plt
from models.multiple_linear_regression import MultipleLinearRegression
import numpy as np
from data_loading import load_data
from visualization import plot_data
from inference import make_inferences

def main():
    st.title("Data Analysis App with Time Series")

    st.title("Data Analysis App")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.write("Data Loaded:")
            st.write(df)

            st.write("Plot Data:")
            plot_data(df)

            st.write("Inferences:")
            make_inferences(df)

            st.write("Time Series:")
            time_field = st.text_input("Enter the timestamp field")
            value_fields = st.text_input("Enter the value fields")
            values = value_fields.split(",")
            frequency = st.number_input("Enter the frequency", value=1)
            serie = TimeSeries.from_table(Table.from_dataframe(df), time_field, values, frequency)
            
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

if __name__ == "__main__":
    main()
