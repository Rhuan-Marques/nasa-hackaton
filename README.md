# DataSage - Facilitated Data Analysis

## Overview

**DataSage** is a web application developed using Streamlit that facilitates data analysis for researchers and analysts. The application allows users to upload CSV files and perform various analyses, including generating reports using Sweetviz and AutoViz, visualizing relationships between variables, and performing time series analysis and multiple linear regression.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)

## Features

- **CSV File Upload:** Users can upload CSV files for analysis.
- **Sweetviz Reports:** Automatically generates interactive visual reports to understand data features.
- **AutoViz Reports:** Quickly visualizes data relationships and distributions.
- **Data Visualization:** Offers scatter plots and count plots to visualize relationships between variables.
- **Time Series Analysis:** Performs time series analysis based on user-selected time and value columns.
- **Multiple Linear Regression:** Provides regression analysis and visualizations.

## Technologies Used

- **Python**
- **Streamlit**: For building the web application interface.
- **Pandas**: For data manipulation and analysis.
- **Sweetviz**: For generating visual reports.
- **AutoViz**: For automatic data visualization.
- **Matplotlib** and **Seaborn**: For creating static, animated, and interactive visualizations.
- **Custom Services**: Includes additional functionality like time series analysis and regression analysis.

## How to Use

1. Clone the repository or download the project files.
2. Install Poetry (if you haven't already):
```curl -sSL https://install.python-poetry.org | python3 -```
3. Install project dependencies
``` poetry install ```
5. Run the Streamlit app:
```streamlit run app_base/main.py```
7. Upload your CSV file using the file uploader.
8. Select the analysis option from the sidebar to start exploring your data.

## Project Structure
app_base/
│
├── parser/
├── services/
│   ├── csv_parser.py
|   ├── data_loading.py
│   ├── multiple_linear_regression.py
|   ├── process.py
|   ├── SupportVectorMachine.py
│   ├── table_class.py
│   └── time_series.py
|   ├── visualization.py
│
├── main.py
├── requirements.txt
└── README.md
