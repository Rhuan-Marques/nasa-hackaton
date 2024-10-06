import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

class SupportVectorRegression3D:
    def __init__(self, X: np.array, Y: np.array, kernel='linear', C=1.0, epsilon=0.1):
        if X.ndim != 2:
            raise ValueError("Predictor matrix X must be a 2D array.")
        
        if Y.ndim != 1:
            raise ValueError("Response vector Y must be a 1D array.")
        
        if X.shape[0] != Y.shape[0]:
            raise ValueError("The number of samples in X and Y must be the same.")
        self.X = X
        self.Y = Y
        self.kernel = kernel
        self.C = C
        self.epsilon = epsilon
        self.model = None
        self.fitted = False
        self.predictions = None
        self.errors = None
    
    def fit(self):
        from sklearn.svm import SVR
        self.model = SVR(kernel=self.kernel, C=self.C, epsilon=self.epsilon)
        self.model.fit(self.X, self.Y)
        self.fitted = True
    
    def predict(self, X_new):
        if not self.fitted:
            raise ValueError("The model has not been fitted yet.")
        
        self.predictions = self.model.predict(X_new)
        return self.predictions
    
    def plot_3d(self):
        """
        Plota os dados reais e a superfície de regressão para duas variáveis independentes.
        """
        if self.X.shape[1] != 2:
            raise ValueError("Only 2 predictors are supported for 3D plotting.")
        
        if not self.fitted:
            raise ValueError("The model has not been fitted yet.")
        
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        # Dados reais
        ax.scatter(self.X[:, 0], self.X[:, 1], self.Y, color='blue', label='Real')

        # Previsões para a superfície de regressão
        X1, X2 = np.meshgrid(np.linspace(min(self.X[:, 0]), max(self.X[:, 0]), 100),
                             np.linspace(min(self.X[:, 1]), max(self.X[:, 1]), 100))
        Z = self.predict(np.column_stack((X1.ravel(), X2.ravel()))).reshape(X1.shape)
        
        # Superfície de regressão
        ax.plot_surface(X1, X2, Z, color='red', alpha=0.7, rstride=100, cstride=100)
        
        ax.set_xlabel('X1')
        ax.set_ylabel('X2')
        ax.set_zlabel('Y')
        plt.title('SVM: Superfície de Regressão')
        plt.show()