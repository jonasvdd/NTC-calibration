"""
    ******************
    SteinhartHart.py
    ******************
    
    Representation of the Steinhart-Hart equation.
    Wittholds 2 classes. 
"""
__author__ = 'Jonas Van Der Donckt'

import numpy as np
from formulas import Physical_Unit


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
    """
    Helper class to ease some calculations/readability
    """
    def __init__(self, T, R):
        self.T = T
        self.R = R
        self._dist = -1

    def calc_dist(self, minTR, maxTR):
        """
        Calculates the distance between The current TemperatureResistance
        and 2 other TemperatureResistances objects. 
                
        :return: The calculated distance
        :rtype: float
        """
        self._dist = np.sqrt(self.T - minTR.T) + np.sqrt(maxTR.T - self.T)
        return self._dist

    def __lt__(self, other):
        """
        Implement the **lesser than** operation to be able to sort instances
        """
        return self.T < other.T

    def __str__(self):
        return "{ T: %s, R: %s }" % (self.T, self.R)

    def __repr__(self):
        return self.__str__()


class SteinHart:
    """
    Object Oriented representation of the steinhart equation
    
    Has the nifty feature that it will use the **3 most distant**
    points to calculate the steinhart hart coefficients. 
    """

    def __init__(self, A=None, B=None, C=None):
        self.A, self.B, self.C = A, B, C
        self.calibrated = self.A is not None and self.B is not None and self.C is not None
        self.TR_values = []

    def calculateT(self, R):
        """
        Calculates the temperature in °C, based on the resistance of the NTC
        
        :param float R: The resistance of the NTC
        :return: The predicted temperature in °C if the system is calibrated, 
            otherwise None
        :rtype: float
        """
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
            # a = np.array(([1 , L1, L1**3],
            #              [1,  L2, L2**3],
            #              [1,  L3, L3**3]))


            Y1 = 1 / (self.TR_values[MIN_POS].T + K_OFFSET)
            Y2 = 1 / (self.TR_values[MID_POS].T + K_OFFSET)
            Y3 = 1 / (self.TR_values[MAX_POS].T + K_OFFSET)
            # b = np.array([Y1, Y2, Y3])
            # print("Y1: ", Y1, '\t', Y1.re)
            # print("Y2: ", Y2, '\t', Y2.re)
            # print("Y3: ", Y3, '\t', Y3.re)

            # result = np.linalg.solve(a, b)
            # print(result)

            y2_1 = (Y2 - Y1) / (L2 - L1)
            y3_1 = (Y3 - Y1) / (L3 - L1)
            print("Y2_1: ", y2_1,  '\t', y2_1.re)
            print("Y3_1: ", y3_1,  '\t', y3_1.re)


            self.C = (y3_1 - y2_1) / (L3 - L2) * 1 / (L1 + L2 + L3)
            self.B = y2_1 - self.C * (L1**2 + L1 * L2 + L2**2)
            self.A = Y1 - (self.B + L1**2 * self.C) * L1

            if type(self.A) is Physical_Unit:
                self.A = self.A.val
                self.B = self.B.val
                self.C = self.C.val

            self.calibrated = True
        else:
            print("Can't calibrate yet, feed me some more data ;)") 


    def feed(self, T, R):
        """
        Feeds new temperature values to the Steinhart Hart Equation.

        This function will only use the values to calibrate the values
        if they are "more distant" than the current values. 
                
        :param float T: The reference temperature in °C
        :param float R: The measured/calculated resistance of the thermistor
        """
        # create a new Temperature Resistance object
        new_TR = TemperatureResistance(T, R)

        if len(self.TR_values) < 3:
            threshold = 1       #         # threshold distance
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

    def save(self, filename=None):
        """
        Saves the current Steinhart Hart coefficients in .csv file.
        """
        if self.calibrated:
            with open(COEFF_FILE_CSV) as f:
                f.write("%s,%s,%s", self.A, self.B, self.C)
        else:
            print("Can't save the coefficients if they aren't calculated (╯°□°）╯︵ ┻━┻")

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

    def __str__(self):
        return str(self.TR_values) + "\nA: %s\tB: %s\tC: %s" % (self.A, self.B, self.C)


##############################
# For testing purposes:
##############################
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

