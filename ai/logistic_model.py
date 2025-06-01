import numpy as np

class LogisticRegressionCustom:
    def __init__(self, learning_rate=0.01, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            linear_model = np.dot(X, self.weights) + self.bias
            predictions = self.sigmoid(linear_model)

            dw = (1 / n_samples) * np.dot(X.T, (predictions - y))
            db = (1 / n_samples) * np.sum(predictions - y)

            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        return self.sigmoid(linear_model)

    def predict(self, X):
        proba = self.predict_proba(X)
        return [1 if p >= 0.5 else 0 for p in proba]

    def accuracy(self, y_true, y_pred):
        return np.mean(y_true == y_pred)

    def loss(self, y_true, y_pred_proba):
        return -np.mean(y_true * np.log(y_pred_proba + 1e-9) + (1 - y_true) * np.log(1 - y_pred_proba + 1e-9))

    def confusion_matrix(self, y_true, y_pred):
        TP = sum((y_true == 1) & (y_pred == 1))
        TN = sum((y_true == 0) & (y_pred == 0))
        FP = sum((y_true == 0) & (y_pred == 1))
        FN = sum((y_true == 1) & (y_pred == 0))
        return {'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}