import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

class TimeSeries:
    def __init__(self, data, timestamps, frequency=None):
        self.data = data
        self.timestamps = timestamps
        self.frequency = frequency
        
        # Calculate error attributes during initialization
        self.error = self.calculate_error()
        self.squared_error = self.calculate_squared_error()
        self.error_std_dev = self.calculate_error_std_dev()

    def forecast(self, steps):
        """Forecast future values based on the time series data using simple mean."""
        forecast_value = np.mean(self.data)
        return [forecast_value] * steps

    def normalize(self):
        """Normalize the time series data to a range of 0 to 1."""
        min_val = np.min(self.data)
        max_val = np.max(self.data)
        self.data = [(x - min_val) / (max_val - min_val) for x in self.data]

    def cycle_analysis(self):
        """Identify cycles in the time series data."""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(self.data)
        troughs, _ = find_peaks(-np.array(self.data))
        return peaks, troughs

    def describe(self):
        """Return descriptive statistics of the time series data."""
        return {
            'mean': np.mean(self.data),
            'median': np.median(self.data),
            'std_dev': np.std(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data),
            'count': len(self.data)
        }

    def calculate_trend(self):
        """Calculate and return the trend using a simple moving average."""
        window_size = 5
        trend = np.convolve(self.data, np.ones(window_size) / window_size, mode='valid')
        return trend

    def seasonal_decompose(self):
        """Decompose the time series into trend, seasonal, and residual components."""
        df = pd.DataFrame({'data': self.data}, index=pd.to_datetime(self.timestamps))
        decomposition = seasonal_decompose(df['data'], model='additive')
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        return trend, seasonal, residual

    def plot(self):
        """Plot the time series data."""
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 5))
        plt.plot(self.timestamps, self.data, marker='o')
        plt.title('Time Series Plot')
        plt.xlabel('Timestamps')
        plt.ylabel('Values')
        plt.grid()
        plt.show()
    
    def calculate_error(self):
        """
        Calculate the error between the actual values and the adjusted trend using a moving average.
        """
        trend = self.calculate_trend()
        adjusted_trend = np.concatenate((np.full(len(self.data) - len(trend), np.nan), trend))
        error = np.array(self.data) - adjusted_trend
        return error

    def calculate_squared_error(self):
        """
        Calculate the squared error.
        """
        return self.calculate_error() ** 2

    def calculate_error_std_dev(self):
        """
        Calculate the standard deviation of the error, ignoring NaN values.
        """
        valid_error = self.calculate_error()[~np.isnan(self.calculate_error())]
        error_std_dev = np.std(valid_error)
        return error_std_dev
