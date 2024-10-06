import numpy as np
import matplotlib.pyplot as plt

class MultipleLinearRegression:
    def __init__(self, X: np.array, Y: np.array):
        # Verify that X is a 2D matrix
        if X.ndim != 2:
            raise ValueError("Predictor matrix X must be a 2D array.")
        
        # Verifica se Y é uma matriz 2D
        if Y.ndim != 2:
            raise ValueError("Response matrix Y must be a 2D array.")
        
        # verify that the number of samples in X and Y are the same
        if X.shape[0] != Y.shape[0]:
            raise ValueError("The number of samples in X and Y must be the same.")
        
        self.X = X
        self.Y = Y
        self.coefficients = None
        self.intercept = None
        self.fitted = False
        self.errors = None
        self.squared_errors = None

    def calculateErrors(self):
        """
        Calculates the residuals, squared residuals, and the standard deviation of the error.
        """
        predictions = self.predict(self.X)
        self.errors = self.Y - predictions
        self.squared_errors = self.errors ** 2
        self.std_dev_error = np.std(self.errors, axis=0)
    
    def fit(self):
        # add intercept to X matrix (column of 1s)
        X_with_intercept = self.X

        # calculate coefficients using the normal equation
        self.coefficients = np.linalg.pinv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ self.Y
        
        # split coefficients into intercept and feature coefficients
        self.intercept = self.coefficients[0]  # intercept is the first coefficient
        self.coefficients = self.coefficients[1:]  # remaining coefficients are the feature coefficients
        
        
        self.fitted = True
        
    def predict(self, X_new):
        if not self.fitted:
            raise ValueError("The model has not been fitted yet.")
        
        # retur the predicted values
        return self.intercept + X_new[:, 1:] @ self.coefficients

    def calculate_errors(self):
        """
        Calculates the residuals, squared residuals, and the standard deviation of the error.
        """
        predictions = self.predict(self.X)
        self.errors = self.Y - predictions
        self.squared_errors = self.errors ** 2
        self.std_dev_error = np.std(self.errors, axis=0)

    def get_coefficients(self):
        """
        Returns the intercept and coefficients of the fitted model.
        
        Returns:
        - intercept (1D np.array): The intercept for each response variable.
        - coefficients (2D np.array): The coefficients for each predictor for each response variable.
        """
        if not self.fitted:
            raise ValueError("The model must be fitted before accessing coefficients.")
        
        return self.intercept, self.coefficients
    def plot(self):
        """
        Plots the actual vs. predicted values for each response variable.
        """
        if not self.fitted:
            raise ValueError("The model must be fitted before plotting.")
        
        predictions = self.predict(self.X)
        num_plots = self.Y.shape[1]
        
        plt.figure(figsize=(10, 5 * num_plots))
        
        for i in range(num_plots):
            plt.subplot(num_plots, 1, i + 1)
            plt.plot(self.Y[:, i], label='Actual')
            plt.plot(predictions[:, i], label='Predicted', linestyle='--')
            plt.xlabel('Sample')
            plt.ylabel(f'Response Variable {i + 1}')
            plt.title(f'Response Variable {i + 1}: Actual vs Predicted')
            plt.legend()
        
        plt.tight_layout()
        plt.show()
    def plot_residuals(self):
        """
        Plots the residuals for each response variable.
        """
        if self.errors is None:
            self.calculate_errors()
        
        num_plots = self.errors.shape[1]
        
        plt.figure(figsize=(10, 5 * num_plots))
        
        for i in range(num_plots):
            plt.subplot(num_plots, 1, i + 1)
            plt.plot(self.errors[:, i])
            plt.axhline(0, color='red', linestyle='--')
            plt.xlabel('Sample')
            plt.ylabel(f'Residuals {i + 1}')
            plt.title(f'Residuals {i + 1}')
        
        plt.tight_layout()
        plt.show()
    def QQ_plot(self):
        """
        Generates a QQ plot of the residuals.
        """
        if self.errors is None:
            self.calculate_errors()
        
        import scipy.stats as stats
        
        num_plots = self.errors.shape[1]
        
        plt.figure(figsize=(10, 5 * num_plots))
        
        for i in range(num_plots):
            plt.subplot(num_plots, 1, i + 1)
            stats.probplot(self.errors[:, i], dist="norm", plot=plt)
            plt.title(f'QQ Plot: Residuals {i + 1}')
        
        plt.tight_layout()
        plt.show()