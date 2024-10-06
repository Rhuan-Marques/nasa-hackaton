import streamlit as st
from utils.create_time_series import create_time_series
import matplotlib.pyplot as plt
from models.multiple_linear_regression import MultipleLinearRegression
import numpy as np
def main():
    st.title("Data Analysis App with Time Series")
    serie = create_time_series()
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
