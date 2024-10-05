import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

class TimeSeries:
    def __init__(self, data, timestamps, frequency=None):
        self.data = data
        self.timestamps = timestamps
        self.frequency = frequency

    def forecast(self, steps):
        forecast_value = np.mean(self.data)
        return [forecast_value] * steps

    def normalize(self):
        min_val = np.min(self.data)
        max_val = np.max(self.data)
        self.data = [(x - min_val) / (max_val - min_val) for x in self.data]

    def cycle_analysis(self):
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(self.data)
        troughs, _ = find_peaks(-np.array(self.data))
        return peaks, troughs

    def describe(self):
        return {
            'mean': np.mean(self.data),
            'median': np.median(self.data),
            'std_dev': np.std(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data),
            'count': len(self.data)
        }

    def calculate_trend(self):
        window_size = 5
        trend = np.convolve(self.data, np.ones(window_size) / window_size, mode='valid')
        return trend

    def seasonal_decompose(self):
        df = pd.DataFrame({'data': self.data}, index=pd.to_datetime(self.timestamps))
        decomposition = seasonal_decompose(df['data'], model='additive')
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        return trend, seasonal, residual

    def plot(self):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.plot(self.timestamps, self.data, marker='o')
        plt.title('Time Series Plot')
        plt.xlabel('Timestamps')
        plt.ylabel('Values')
        plt.grid()
        plt.show()
