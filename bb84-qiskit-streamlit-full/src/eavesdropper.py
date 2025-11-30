import numpy as np

class InterceptResend:
    def __init__(self, intercept_fraction=0.2, strategy='random'):
        self.intercept_fraction = intercept_fraction
        self.strategy = strategy

    def decide_intercept(self):
        return np.random.rand() < self.intercept_fraction
