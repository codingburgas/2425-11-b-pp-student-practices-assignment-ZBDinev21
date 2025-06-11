import numpy as np


def sigmoid(x):
    # Clip input to prevent overflow
    x = np.clip(x, -500, 500)
    return 1 / (1 + np.exp(-x))



def accuracy(y_true, y_pred):
    return np.mean(np.array(y_true) == np.array(y_pred))


def confusion_matrix(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    TP = np.sum((y_true == 1) & (y_pred == 1))
    TN = np.sum((y_true == 0) & (y_pred == 0))
    FP = np.sum((y_true == 0) & (y_pred == 1))
    FN = np.sum((y_true == 1) & (y_pred == 0))
    return {'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}


class LogisticRegressionCustom:
    def __init__(self, lr=0.01, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        self.bias = 0
        for _ in range(self.n_iters):
            model = np.dot(X, self.weights) + self.bias
            preds = sigmoid(model)
            dw = (1 / len(y)) * np.dot(X.T, preds - y)
            db = (1 / len(y)) * np.sum(preds - y)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X, threshold=0.5):
        preds = sigmoid(np.dot(X, self.weights) + self.bias)
        return [1 if p > threshold else 0 for p in preds]