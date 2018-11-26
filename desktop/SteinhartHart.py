"""
    ******************
    SteinhartHart.py
    ******************
    
    Representation of the Steinhart-Hart equation.
    Wittholds 2 classes. 
"""
__author__ = 'Jonas Van Der Donckt'

import numpy as np


########################
#      CONSTANTS
########################
MIN_POS = 0
MID_POS = 1
MAX_POS = 2
K_OFFSET = 273.15

COEFF_FILE_TSV = 'coefficients.tsv'
COEFF_FILE_CSV = 'coefficients.tsv'

class TemperatureResistance:
        def __init__(self, T, R):
            self.T = T
            self.R = R
            self._dist = -1

        def __lt__(self, other):
            return self.T < other.T

        def __str__(self):
            return "{ T: %s, R: %s }" % (self.T, self.R)

        def __repr__(self):
            return self.__str__()

        def calc_dist(self, minRT, maxRT):
            self._dist = np.sqrt(self.T - minRT.T) + np.sqrt(maxRT.T - self.T)
            return self._dist

class SteinHart:
    def __init__(self, A=None, B=None, C=None):
        self.A, self.B, self.C = A, B, C
        # TODO CHECK WETHER THE VALUES ARE CORRECTLY CALIBRATED.
        self.calibrated = False
        self.TR_values = []

    def calculateT(self, R):
        if self.calibrated:
            return 1 / (self.A + self.B * np.log(R) + self.C * np.log(R)**3) - K_OFFSET
        else:
            print("Can't calibrate yet, feed me some more data ;)") 
            return None

    def _calibrate(self):
        """
        (Re)Calibrate the Steinhart-Hart coefficients
        
        `formulas <https://www.wikiwand.com/en/Steinhart%E2%80%93Hart_equation>`_ 
        """
        if (len(self.TR_values) == 3):
            L1 = np.log(self.TR_values[MIN_POS].R)
            L2 = np.log(self.TR_values[MID_POS].R)
            L3 = np.log(self.TR_values[MAX_POS].R)

            Y1 = 1 / (self.TR_values[MIN_POS].T + K_OFFSET)
            Y2 = 1 / (self.TR_values[MID_POS].T + K_OFFSET)
            Y3 = 1 / (self.TR_values[MAX_POS].T + K_OFFSET)

            y2_1 = (Y2 - Y1) / (L2 - L1)
            y3_1 = (Y3 - Y1) / (L3 - L1)

            self.C = (y3_1 - y2_1) / (L3 - L2) * 1 / (L1 + L2 + L3)
            self.B = y2_1 - self.C * (L1**2 + L1 * L2 + L2**2)
            self.A = Y1 - (self.B + L1**2 * self.C) * L1

            self.calibrated = True
        else:
            print("Can't calibrate yet, feed me some more data ;)") 


    def feed(self, T, R):
        # threshold distance
        # create a new Temperature Resistance object
        new_TR = TemperatureResistance(T, R)

        if len(self.TR_values) < 3:
            threshold = 1
            different = True

            for tr in self.TR_values:
                if (abs(tr.T - T) < threshold or abs(tr.R -R ) < threshold):
                    different = False
            
            if different:
                self.TR_values.append(new_TR)
                self.TR_values.sort()
                if len(self.TR_values) == 3:
                    self._calibrate()
            else:
                print("Data is not different enough!")
        else:   # more than 3 values
            # new minimum
            if new_TR.T < self.TR_values[MIN_POS].T:
                prev_min_TR = self.TR_values[MIN_POS]
                self.TR_values[MIN_POS] = new_TR
                new_TR = prev_min_TR
            
            # new maximum
            elif new_TR.T > self.TR_values[MAX_POS].T:
                prev_max_TR = self.TR_values[MAX_POS]
                self.TR_values[MAX_POS] = new_TR
                new_TR = prev_max_TR

            # calculate new distance since values could've been changed
            current_dist = self.TR_values[MID_POS].calc_dist(self.TR_values[MIN_POS], self.TR_values[MAX_POS])
            new_TR_dist = new_TR.calc_dist(self.TR_values[MIN_POS], self.TR_values[MAX_POS])
            
            if new_TR_dist > current_dist:
                self.TR_values[MID_POS] = new_TR
            
            # recalibrate
            self._calibrate()

    def save(self):
        if self.calibrated:
            with open(COEFF_FILE_CSV) as f:
                f.write("%s,%s,%s", self.A, self.B, self.C)
    
    def __str__(self):
        return str(self.TR_values) + "\nA: %s\tB: %s\tC: %s" % (self.A, self.B, self.C)

    @classmethod
    def from_csv(cls, file=COEFF_FILE_CSV):
        with open(file) as f:
            # todo check for whitespaces and stuff
            coeff = f.readline().split(',')
            return cls(A=coeff[0], B=coeff[1], C=coeff[2])

    @classmethod
    def from_tsv(cls, file=COEFF_FILE_TSV):
        with open(file) as f:
            coeff = f.readline().split('/t')
            return cls(A=coeff[0], B=coeff[1], C=coeff[2])


if __name__ == '__main__':
    sth = SteinHart()
    # testing whether it sorts correctly
    sth.feed(10, 1100)
    sth.feed(15, 30)
    print(sth)
    sth.calculateT(1300)
    
    print('-'*80)
    
    sth.feed(8, 110)
    print(sth)
    print("Calculation (R = %s ) T = %s" % (1300, round(sth.calculateT(1300), 4)))
    
    print('-'*80)
    
    # testing feeding it with some new values
    sth.feed(100, 10000)
    print(sth)
    print("Calculation (R = %s ) T = %s" % (1300, round(sth.calculateT(1300), 4)))

    print('-'*80)

    sth.feed(45, 3000)
    print(sth)
    print("Calculation (R = %s ) T = %s" % (1300, round(sth.calculateT(1300), 4)))

