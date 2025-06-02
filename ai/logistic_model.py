import numpy as np

class LogisticRegressionCustom:
    def __init__(self, lr=0.01, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def fit(self, X, y):
        self.weights = np.zeros(X.shape[1])
        self.bias = 0
        for _ in range(self.n_iters):
            model = np.dot(X, self.weights) + self.bias
            preds = self.sigmoid(model)
            dw = (1 / len(y)) * np.dot(X.T, preds - y)
            db = (1 / len(y)) * np.sum(preds - y)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict(self, X):
        preds = self.sigmoid(np.dot(X, self.weights) + self.bias)
        return [1 if p > 0.5 else 0 for p in preds]

    def accuracy(self, y_true, y_pred):
        return np.mean(np.array(y_true) == np.array(y_pred))

    def confusion_matrix(self, y_true, y_pred):
        TP = sum((y_true[i] == 1 and y_pred[i] == 1) for i in range(len(y_true)))
        TN = sum((y_true[i] == 0 and y_pred[i] == 0) for i in range(len(y_true)))
        FP = sum((y_true[i] == 0 and y_pred[i] == 1) for i in range(len(y_true)))
        FN = sum((y_true[i] == 1 and y_pred[i] == 0) for i in range(len(y_true)))
        return {'TP': TP, 'TN': TN, 'FP': FP, 'FN': FN}