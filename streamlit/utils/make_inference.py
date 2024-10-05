from models.time_series import TimeSeries
import pandas as pd
def make_inferences(df):
    timestamps = pd.date_range(start='2022-01-01', periods=len(df), freq='D')
    data = df.iloc[:, 0]  # Utilizando a primeira coluna como exemplo
    
    ts = TimeSeries(data=data, timestamps=timestamps)
    
    # Calculando tendência
    trend = ts.calculate_trend()
    print("Trend (Moving Average):", trend)
    
    # Decompondo a série temporal
    trend, seasonal, residual = ts.seasonal_decompose()
    print("Seasonal Decomposition:")
    print("Trend:", trend)
    print("Seasonal:", seasonal)
    print("Residual:", residual)
