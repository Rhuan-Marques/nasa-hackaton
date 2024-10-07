import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from .table_class import Table
class MultipleLinearRegression:
    def __init__(self, X: np.array, Y: np.array):
        if X.ndim != 2:
            raise ValueError("Predictor matrix X must be a 2D array.")
        
        if Y.ndim != 2:
            raise ValueError("Response matrix Y must be a 2D array.")
        
        # if X.shape[0] != Y.shape[0]:
        #     raise ValueError("The number of samples in X and Y must be the same.")
        
        self.X = X
        self.Y = Y
        self.coefficients = None
        self.intercept = None
        self.fitted = False
        self.errors = None
        self.squared_errors = None

    def fit(self):
        X_with_intercept = self.X
        self.coefficients = np.linalg.pinv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ self.Y
        self.intercept = self.coefficients[0]
        self.coefficients = self.coefficients[1:]
        self.fitted = True

    def predict(self, X_new):
        if not self.fitted:
            raise ValueError("The model has not been fitted yet.")
        
        return self.intercept + X_new[:, 1:] @ self.coefficients

    def calculate_errors(self):
        predictions = self.predict(self.X)
        self.errors = self.Y - predictions
        self.squared_errors = self.errors ** 2
        self.std_dev_error = np.std(self.errors, axis=0)

    def plot(self):
        """
        Plots a simple actual vs. predicted values for each response variable.
        """
        if not self.fitted:
            raise ValueError("The model must be fitted before plotting.")
        
        predictions = self.predict(self.X)
        plt.figure(figsize=(10, 5))
        plt.plot(self.Y, label='Actual', marker='o')
        plt.plot(predictions, label='Predicted', linestyle='--', marker='x')
        plt.title('Actual vs Predicted')
        plt.xlabel('Sample')
        plt.ylabel('Response Variable')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_residuals(self):
        if self.errors is None:
            self.calculate_errors()
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.errors, label='Residuals')
        plt.axhline(0, color='red', linestyle='--')
        plt.title('Residuals')
        plt.xlabel('Sample')
        plt.ylabel('Residuals')
        plt.grid(True)
        plt.show()

    def QQ_plot(self):
        if self.errors is None:
            self.calculate_errors()
        
        plt.figure(figsize=(10, 5))
        stats.probplot(self.errors.flatten(), dist="norm", plot=plt)
        plt.title('QQ Plot: Residuals')
        plt.grid(True)
        plt.show()

    def general_report(self):
        """
        Generates important plots and shows basic statistics for the analysis:
        - Actual vs Predicted values
        - Residuals plot
        - QQ plot of residuals
        - Displays the intercept and coefficients
        """
        print("Generating General Report...\n")
        
        try:
            self.fit()
        except Exception as e:
            print(f"Error fitting the model: {e}")
            return
        
        try: 
            self.plot()
        except Exception as e:
            print(f"Error plotting actual vs predicted: {e}")
        
        try:
            self.plot_residuals()
        except Exception as e:
            print(f"Error plotting residuals: {e}")
        
        try:
            self.QQ_plot()
        except Exception as e:
            print(f"Error plotting QQ plot: {e}")

        

    @classmethod
    def from_table(cls, table: Table, columns_x: list[str], columns_y: list[str]) -> 'MultipleLinearRegression':
        if not all([column in table.numeric_columns for column in columns_x]):
            raise ValueError("All columns in X must be numeric.")
        if not all([column in table.numeric_columns for column in columns_y]):
            raise ValueError("All columns in Y must be numeric.")
        x = np.array([table.column_dict[column].values for column in columns_x])
        y = np.array([table.column_dict[column].values for column in columns_y])
        return cls(X=x, Y=y)
