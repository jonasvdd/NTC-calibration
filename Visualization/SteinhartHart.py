import numpy as np

class SteinHart:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def calculateT(self, R):
        return 1 / (self.A + self.B * np.log(R) + self.C * np.log(R)**3)

    def calibrate(T1, val1, T2, val2, T3, val3):
        