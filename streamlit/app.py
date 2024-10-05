import streamlit as st
from utils.create_time_series import create_time_series
import matplotlib.pyplot as plt

def main():
    st.title("Data Analysis App with Time Series")
    time_serie = create_time_series()
    time_serie.plot()
    st.pyplot()
    st.write(time_serie.describe())
    st.write(time_serie.cycle_analysis())
if __name__ == "__main__":
    main()
