import numpy as np
import matplotlib.pyplot as plt

class MultipleLinearRegression:
    def __init__(self, X, Y):
        """
        Initializes the MultipleLinearRegression model.
        
        Parameters:
        - X (2D np.array): Matrix of predictor variables with dimensions n x m (n samples, m features).
        - Y (2D np.array): Matrix of response variables with dimensions n x p (n samples, p response variables).
        """
        self.X = X
        self.Y = Y
        self.coefficients = None
        self.intercept = None
        self.fitted = False
        self.errors = None
        self.squared_errors = None
        self.std_dev_error = None
       

    def fit(self):
        """
        Fits the multiple linear regression model to the data.
        """
        # Add intercept column to X
        X_with_intercept = np.c_[np.ones(self.X.shape[0]), self.X]

        # Calculate coefficients using Normal Equation: (X'X)^-1 X'Y
        beta = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ self.Y

        # Separate intercept and coefficients
        self.intercept = beta[0, :]
        self.coefficients = beta[1:, :]

        # Calculate error metrics
        self.calculate_errors()

        self.fitted = True

    def predict(self, X_new):
        """
        Predicts values for new data based on the fitted model.
        
        Parameters:
        - X_new (2D np.array): New predictor variables with dimensions n x m.
        
        Returns:
        - predictions (2D np.array): The predicted values for the response variables.
        """
        if not self.fitted:
            raise ValueError("The model must be fitted before making predictions.")
        
        X_new = np.array(X_new)
        return self.intercept + X_new @ self.coefficients

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

    def get_error_metrics(self):
        """
        Returns the error metrics: error, squared error, and standard deviation of the error.
        
        Returns:
        - errors (2D np.array): The residuals for each response variable.
        - squared_errors (2D np.array): The squared residuals for each response variable.
        - std_dev_error (1D np.array): The standard deviation of the error for each response variable.
        """
        if self.errors is None:
            raise ValueError("The model must be fitted before accessing error metrics.")
        
        return {
            'errors': self.errors,
            'squared_errors': self.squared_errors,
            'std_dev_error': self.std_dev_error
        }

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
