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
        
        self.X = X
        self.Y = Y
        self.coefficients = None
        self.intercept = None
        self.fitted = False
        self.errors = None
        self.squared_errors = None

    def fit(self):
        try:
            # Adiciona uma coluna de uns para o intercepto
            X_with_intercept = np.hstack((np.ones((self.X.shape[0], 1)), self.X))
            # Ajusta Y se necessário para que tenha a mesma quantidade de linhas de X
            if X_with_intercept.shape[0] != self.Y.shape[0]:
                min_len = min(X_with_intercept.shape[0], self.Y.shape[0])
                X_with_intercept = X_with_intercept[:min_len, :]
                self.Y = self.Y[:min_len, :]
            self.coefficients = np.linalg.pinv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ self.Y
            self.intercept = self.coefficients[0]
            self.coefficients = self.coefficients[1:]
            self.fitted = True
        except Exception as e:
            print(f"Error during fitting: {e}")

    def predict(self, X_new):
        if not self.fitted:
            raise ValueError("The model has not been fitted yet.")
        
        X_new_with_intercept = np.hstack((np.ones((X_new.shape[0], 1)), X_new))
        return X_new_with_intercept @ np.vstack([self.intercept, self.coefficients])

    def calculate_errors(self):
        predictions = self.predict(self.X)
        self.errors = self.Y - predictions
        self.squared_errors = self.errors ** 2
        self.std_dev_error = np.std(self.errors, axis=0)

    def plot(self, return_fig=False):
        """
        Plots actual vs. predicted values for each response variable.
        """
        if not self.fitted:
            raise ValueError("The model must be fitted before plotting.")
        
        predictions = self.predict(self.X)
        min_len = min(predictions.shape[0], self.Y.shape[0])
        predictions = predictions[:min_len]
        actual = self.Y[:min_len]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(actual, label='Actual', marker='o')
        ax.plot(predictions, label='Predicted', linestyle='--', marker='x')
        ax.set_title('Actual vs Predicted')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Response Variable')
        ax.legend()
        ax.grid(True)
        
        if return_fig:
            return fig
        else:
            plt.show()

    def plot_residuals(self, return_fig=False):
        if self.errors is None:
            self.calculate_errors()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(self.errors, label='Residuals')
        ax.axhline(0, color='red', linestyle='--')
        ax.set_title('Residuals')
        ax.set_xlabel('Sample')
        ax.set_ylabel('Residuals')
        ax.grid(True)

        if return_fig:
            return fig
        else:
            plt.show()
        
    def QQ_plot(self, return_fig=False):
        if self.errors is None:
            self.calculate_errors()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        stats.probplot(self.errors.flatten(), dist="norm", plot=ax)
        ax.set_title('QQ Plot: Residuals')
        ax.grid(True)
        
        if return_fig:
            return fig
        else:
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
        
        figs = []
        
        try: 
            fig1 = self.plot(return_fig=True)
            figs.append(fig1)
        except Exception as e:
            print(f"Error plotting actual vs predicted: {e}")
        
        try:
            fig2 = self.plot_residuals(return_fig=True)
            figs.append(fig2)
        except Exception as e:
            print(f"Error plotting residuals: {e}")
        
        try:
            fig3 = self.QQ_plot(return_fig=True)
            figs.append(fig3)
        except Exception as e:
            print(f"Error plotting QQ plot: {e}")
        
        return figs if figs else None  

    @classmethod
    def from_table(cls, table: Table, columns_x: list[str], columns_y: list[str]) -> 'MultipleLinearRegression':
        if not all([column in table.numeric_columns for column in columns_x]):
            raise ValueError("All columns in X must be numeric.")
        if not all([column in table.numeric_columns for column in columns_y]):
            raise ValueError("All columns in Y must be numeric.")
        x = np.array([table.column_dict[column].values for column in columns_x]).T
        y = np.array([table.column_dict[column].values for column in columns_y]).T
        return cls(X=x, Y=y)
