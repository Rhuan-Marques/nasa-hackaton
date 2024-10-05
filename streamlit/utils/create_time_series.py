from models.time_series import TimeSeries
import pandas as pd

def create_time_series():
    """
    Create a mock of object TimeSeries.
    """
    timestamps = pd.date_range(start='2022-01-01', periods=100, freq='D')
    data = [i for i in range(100)]
    
    return TimeSeries(data=data, timestamps=timestamps)
