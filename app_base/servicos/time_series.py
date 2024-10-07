import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from .table_class import ColumnType, Table
import matplotlib.pyplot as plt
class TimeSeries:
    def __init__(self, data, timestamps, frequency=None):
        self.data = np.array(data)  # Garantir que os dados sejam convertidos para NumPy array
        self.timestamps = pd.to_datetime(timestamps)  # Garantir que os timestamps sejam convertidos para datetime
        self.frequency = frequency

        # Verificar dimensões dos dados
        if self.data.ndim not in [1, 2]:
            raise ValueError("Data should be either 1D or 2D.")

        # Calcular atributos de erro durante a inicialização
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
        self.data = (self.data - min_val) / (max_val - min_val)

    def cycle_analysis(self):
        """Identify cycles in the time series data."""
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(self.data)
        troughs, _ = find_peaks(-self.data)
        return peaks, troughs

    def describe(self):
        """Return descriptive statistics of the time series data."""
        return {
            'mean': np.mean(self.data),
            'median': np.median(self.data),
            'std_dev': np.std(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data),
            'count': self.data.shape[0]
        }

    def calculate_trend(self):
        """Calculate and return the trend using a simple moving average."""
        window_size = 5

        if self.data.ndim == 1:
            # Unidimensional: aplicar média móvel diretamente
            trend = np.convolve(self.data, np.ones(window_size) / window_size, mode='same')
        else:
            # Multidimensional: aplicar média móvel em cada coluna
            trend = np.apply_along_axis(
                lambda x: np.convolve(x, np.ones(window_size) / window_size, mode='same'),
                axis=0,
                arr=self.data
            )
        return trend

    def calculate_error(self):
        """
        Calculate the error between the actual values and the adjusted trend using a moving average.
        Handles both unidimensional and multidimensional data.
        """
        trend = self.calculate_trend()

        if self.data.ndim == 1:
            # Garantir que não haja tamanho negativo
            padding_size = max(0, len(self.data) - len(trend))
            adjusted_trend = np.concatenate((np.full(padding_size, np.nan), trend))
        else:
            # Multidimensional: Ajustar cada coluna separadamente
            def adjust_trend_for_series(x, trend_series):
                padding_size = max(0, len(x) - len(trend_series))
                return np.concatenate((np.full(padding_size, np.nan), trend_series))
            
            adjusted_trend = np.apply_along_axis(
                lambda x: adjust_trend_for_series(x, trend[:, 0]),
                axis=0,
                arr=self.data
            )

        error = self.data - adjusted_trend
        return error

    def calculate_squared_error(self):
        """Calculate the squared error."""
        return self.calculate_error() ** 2

    def calculate_error_std_dev(self):
        """Calculate the standard deviation of the error, ignoring NaN values."""
        error = self.calculate_error()
        valid_error = error[~np.isnan(error)]
        return np.std(valid_error)

    def __init__(self, data, timestamps, frequency):
        self.data = data
        self.timestamps = timestamps
        self.frequency = frequency

    def seasonal_decompose(self):
        """Decompose the time series into trend, seasonal, and residual components."""
        if self.data.ndim != 1:
            # Chama o método de decomposição especial se os dados não forem unidimensionais
            return self.special_decompose()
        
        df = pd.DataFrame({'data': self.data}, index=self.timestamps)
        decomposition = seasonal_decompose(df['data'], model='additive', period=self.frequency)
        return decomposition.trend, decomposition.seasonal, decomposition.resid

    def special_decompose(self):
        """Handle the case where data is multidimensional."""
        if self.data.ndim < 2:
            raise ValueError("Data must be at least two-dimensional for special decomposition.")

        trends, seasonals, residuals = [], [], []
        
        # Itera sobre cada coluna de dados
        for i in range(self.data.shape[1]):
            df = pd.DataFrame({'data': self.data[:, i]}, index=self.timestamps)
            decomposition = seasonal_decompose(df['data'], model='additive', period=self.frequency)
            
            # Renomear as colunas para evitar duplicatas
            trends.append(decomposition.trend.rename(f'trend_{i}'))
            seasonals.append(decomposition.seasonal.rename(f'seasonal_{i}'))
            residuals.append(decomposition.resid.rename(f'residual_{i}'))

        # Converte as listas em arrays numpy
        return (
            pd.concat(trends, axis=1),
            pd.concat(seasonals, axis=1),
            pd.concat(residuals, axis=1)
        )
        
        # Itera sobre cada coluna de dados
        for i in range(self.data.shape[1]):
            df = pd.DataFrame({'data': self.data[:, i]}, index=self.timestamps)
            decomposition = seasonal_decompose(df['data'], model='additive', period=self.frequency)
            trends.append(decomposition.trend)
            seasonals.append(decomposition.seasonal)
            residuals.append(decomposition.resid)

        # Converte as listas em arrays numpy
        return (
            pd.concat(trends, axis=1),
            pd.concat(seasonals, axis=1),
            pd.concat(residuals, axis=1)
        )

    def plot_decompose(self):
        """Plot the seasonal decomposition of the time series data."""
        trend, seasonal, residual = self.seasonal_decompose()
        plt.figure(figsize=(10, 7))
        plt.subplot(311)
        plt.plot(trend)
        plt.title('Trend')
        plt.subplot(312)
        plt.plot(seasonal)
        plt.title('Seasonal')
        plt.subplot(313)
        plt.plot(residual)
        plt.title('Residual')
        plt.tight_layout()
        plt.show()
    
    def plot(self) :
        """Plot the time series data."""
        fig = plt.figure(figsize=(10, 5))
        plt.plot(self.timestamps, self.data, marker='o', linestyle='-')
        plt.title('Time Series Plot')
        plt.xlabel('Timestamps')
        plt.ylabel('Values')
        plt.grid(True)
        plt.show()
        return fig

    @classmethod
    def from_table(cls, table: Table, time_field: str, value_fields: list[str], frequency: int):
        """Create a TimeSeries instance from a Table object."""
        if time_field not in table.numeric_columns:
            raise ValueError(f"Time field {time_field} not found in table's numeric columns.")
        if not all([field in table.numeric_columns for field in value_fields]):
            raise ValueError("One or more value fields not found in table's numeric columns.")
        if table.column_dict[time_field].value_type not in [ColumnType.Int, ColumnType.Float]:
            raise ValueError("Time field must be numeric.")
        if not all([table.column_dict[field].value_type in [ColumnType.Int, ColumnType.Float] for field in value_fields]):
            raise ValueError("Value fields must be numeric to be used in time series.")
        
        timestamps = np.array(table.column_dict[time_field].values)
        values = np.array([table.column_dict[field].values for field in value_fields])

        # Verificar se os valores são unidimensionais ou multidimensionais
        if len(values.shape) == 2:
            values = values.T  # Transpor se necessário

        return cls(timestamps=timestamps, data=values, frequency=frequency)
