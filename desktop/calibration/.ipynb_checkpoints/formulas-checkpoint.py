# -*- coding: utf-8 -*-
"""
    ************
    formulas.py
    ************
    
    Withholds the Physical_Unit class, which is used to perform calculations 
    on physical units with errors. 
"""
__author__ = 'Jonas Van Der Donckt'

from decimal import Decimal
import math

import numpy as np


class Physical_Unit:
    def __init__(self, unit_name,  symbol,  value, ae=None, re=None):
        """
        Creates an instance of a serial connection
        
        :param str unit_name: The unit name (e.g. 'Length')
        :param str symbol: The corresponding symbol of that unit (e.g. 'cm')
        :param float value: The value of that physical unit
        :param float ae: The value of the absolute error, defaults to None
        :param float re: The value of the relative error

        :raises NotImplementedError: if neither ea nor re are given. 
        """
        self.un = str(unit_name)
        self.sym = str(symbol)
        self.val = value

        if ae is None and re is not None:
            ae = re * value
        elif re is None:
            re = ae/value
        else:
            raise NotImplementedError

        self.ae = abs(ae)
        self.re = abs(re)

    def __neg__(self):
        return Physical_Unit(self.un, self.sym, -self.val, self.ae)

    def __add__(self, other):
        if type(other) is int or type(other) is float:
            return Physical_Unit(self.un, self.sym, self.val + other, ae=self.ae)
        elif type(other) is Physical_Unit:
            # this assertion assures that only physical units which the same symbol are added
            # assert(self.un.lower() == other.un.lower() and self.sym.lower() == other.sym.lower())
            
            # take the sum of both values, new ae = sum of both ae-s
            return Physical_Unit(self.un, self.sym, self.val + other.val, ae=self.ae + other.ae)
        else:
            raise NotImplementedError("Doesn't support addition operation with type: ", type(other))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Physical_Unit(self.un, self.sym, self.val * other , ae=self.ae * other)
        elif type(other) is Physical_Unit:
            # multiply both values, the new relative error is the sum of both its relative errors
            return Physical_Unit(self.un + ' * ' + other.un  , self.sym + ' * ' + other.sym,
                                 self.val * other.val, re=self.re + other.re)
        else:
            raise NotImplementedError("Doesn't support multiplication operation with type: ", type(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) is int or type(other) is float:
            return Physical_Unit(self.un, self.sym, self.val / other, re=self.re / other)
        elif type(other) is Physical_Unit:
            div_un, div_sym = self.un + ' / ' + other.un, self.sym + ' / ' + other.sym
            if other.sym == "":
                div_sym = self.sym
            if self.un == other.un:
                div_un = ""
                if self.sym.lower() == other.sym.lower():
                    div_sym = ""
            return Physical_Unit(div_un, div_sym, self.val / other.val, re=self.re + other.re)
        else:
            raise NotImplementedError("Doesn't support division operation with type: ", type(other))

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        return self.__truediv__(other)

    def __rtruediv__(self, other):
        return (self.__pow__(-1)).__mul__(other)

    def __rdiv__(self, other):
        return self.__rtruediv__(other)

    def __rdivmod__(self, other):
        return self.__rtruediv__(other)

    def __rfloordiv__(self, other):
        return self.__rtruediv__(other)

    def __lt__(self, other):
        """
        Implement the **lesser than** operation to be able to sort instances
        """
        if type(other) is int or type(other) is float:
            return self.val < other
        elif type(other) is Physical_Unit:
            return self.val < other.val
        else:
            raise NotImplementedError

    def __abs__(self):
        return Physical_Unit(self.un, self.sym, abs(self.val), re=self.re)

    def __pow__(self, power, modulo=None):
        str_pow = '^(' + str(power) + ')' if self.sym != "" else ""
        return Physical_Unit(self.un + str_pow, self.sym + str_pow, self.val**power, re=self.re * abs(power))
    
    def log(self):
        log_val = np.log(self.val)
        return Physical_Unit("ln(" + self.un + ")", "ln(" + self.sym + ")",  log_val, ae=self.ae * log_val / self.val )
        # return Physical_Unit("ln(" + self.un + ")", "ln(" + self.sym + ")" ,  logval , ae=self.re )

    def exp(self):
        return Physical_Unit("e^(" + self.un + ")", "e^(" + self.sym + ")", np.exp(self.val), ae=self.ae * self.val)

    def __str__(self):
        return "(" + str(self.val) + " ± " + str(self.ae) + ") " + self.sym

    def __repr__(self):
        return self.__str__()

    def to_scientific(self):
        """Converts the Physical unit to a scientific mode. 
        
        :return: [description]
        :rtype: [type]
        """

        # round 2 time, if you have for example 981 --> roundval = -2 --> 1000
        # which mean that the roundval is actually -3 
        ae_roundval = -int(math.floor(math.log10(float(self.ae))))
        ae = round(self.ae, ae_roundval)
        ae_roundval = -int(math.floor(math.log10(float(self.ae))))
        
        val = float(round(self.val, ae_roundval))        
        return str("{:." + str(math.ceil(math.log10(val/ae)) -1) + 'e}').format(Decimal(val)) + " ± {:.0e}".format(Decimal(ae))


if __name__ == "__main__":
    from calibration.physical_units import *
    
    # The first functional test
    print('-'*40 + '\nTesting functionality 1\n' + '-'*40)
    
    x = Physical_Unit(LENGTH, CENTIMETER, 12.13, ae=0.03)
    y = Physical_Unit(LENGTH, CENTIMETER, 12.5, ae=0.1)
    print("x:", x)
    print("y:", y)
    print("√(x)  =", x**0.5)
    print("x * y =", x*y)
    print("x / y =", x/y)
    print("x + y =", x + y)
    print("x - y =", x - y)
    print("y - x =", y - x)

    # The second functional test
    print('-'*40 + '\nTesting functionality 2\n' + '-'*40)
    a = Physical_Unit(LENGTH, METER, 3.5821e-2, ae=0.0000001)
    b = Physical_Unit(LENGTH, METER, 27.2, ae=0.3)
    c = Physical_Unit(LENGTH, METER, 3178, ae=1)
    print("a       =\t", a)
    print("b       =\t", b)
    print("c       =\t", c)


    sqr_a = a**2
    bxc = b*c
    sqr_a_plus_bxc = sqr_a + bxc
    adivb = a/b 
    one_adivb = -adivb+1
    sqrt_one_adivb = one_adivb**0.5
    result = sqr_a_plus_bxc / sqrt_one_adivb

    print("a**2    =\t", sqr_a)
    print("bc      =\t", bxc)
    print("a**2+bc =\t", sqr_a_plus_bxc)
    print("a/b     =\t", adivb)
    print("1-a/b   =\t", one_adivb)
    print("√(1-a/b)=\t", sqrt_one_adivb)
    print("(a**2+bc)/√(1-a/b)=", result)
    print("result: ", result.to_scientific())
