import unittest
import numpy as np
from ai.logistic_custom import LogisticRegressionCustom, accuracy, confusion_matrix

class TestLogisticRegressionCustom(unittest.TestCase):

    def setUp(self):
        self.X = np.array([[0], [1], [2], [3], [4], [5]])
        self.y = np.array([0, 0, 0, 1, 1, 1])
        self.model = LogisticRegressionCustom(n_iters=1000)
        self.model.fit(self.X, self.y)

    def test_prediction_accuracy(self):
        preds = self.model.predict(self.X)
        acc = accuracy(self.y, preds)
        self.assertGreaterEqual(acc, 0.8)  # Expect at least 80% accuracy

    def test_loss_output(self):
        proba = self.model.predict_proba(self.X)
        loss = self.model.loss(self.y, proba)
        self.assertLess(loss, 0.7)  # Expect loss below 0.7

    def test_confusion_matrix_keys(self):
        preds = self.model.predict(self.X)
        matrix = confusion_matrix(self.y, preds)
        self.assertIn('TP', matrix)
        self.assertIn('TN', matrix)
        self.assertIn('FP', matrix)
        self.assertIn('FN', matrix)

if __name__ == '__main__':
    unittest.main()
