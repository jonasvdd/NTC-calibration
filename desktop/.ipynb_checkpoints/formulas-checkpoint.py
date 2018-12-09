from decimal import Decimal

import numpy as np
import math


class Physical_Unit:
    def __init__(self, unit_name,  symbol,  value, ae=None, re=None):
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
            # assert(self.sym.lower() == other.sym.lower())
            return Physical_Unit(self.un, self.sym, self.val + other.val, ae=self.ae + other.ae)
        else:
            raise NotImplementedError

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other);

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            return Physical_Unit(self.un, self.sym, self.val * other , ae=self.ae * other)
        elif type(other) is Physical_Unit:
            return Physical_Unit(self.un + ' * ' + other.un  , self.sym + ' * ' + other.sym, self.val * other.val, re=self.re + other.re)
        else:
            raise NotImplementedError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) is int or type(other) is float:
            return Physical_Unit(self.un, self.sym, self.val / other, re=self.re / other)
        elif type(other) is Physical_Unit:
            div_un, div_sim = self.un + ' / ' + other.un, self.sym + ' / ' + other.sym
            if (self.un == other.un):
                div_un = ""
                if (self.sym.lower() == other.sym.lower()):
                    div_sim =  ""
            return Physical_Unit(div_un, div_sim, self.val / other.val, re=self.re + other.re)
        else:
            raise NotImplementedError

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
        str_pow = '^(' + str(power) + ')'
        return Physical_Unit(self.un + str_pow, self.sym + str_pow, self.val**power, re=self.re * abs(power))
    
    def log(self):
        logval =  np.log(self.val)
        return Physical_Unit("ln(" + self.un + ")", "ln(" + self.sym + ")" , logval , ae=self.ae * logval / self.val)

    def exp(self):
        return Physical_Unit("e^(" + self.un + ")", "e^(" + self.sym + ")" , np.exp(self.val), ae=self.fout * self.val)

    def __str__(self):
        return "(" + str(self.val) + " ± " + str(self.ae) + ") " + self.sym

    def __repr__(self):
        return self.__repr__()

    def to_scientific(self):
        # round 2 time, if you have for example 981 --> roundval = -2 --> 1000
        # which mean that the roundval is actually -3 
        ae_roundval = -int(math.floor(math.log10(float(self.ae))))
        ae = round(self.ae, ae_roundval)
        ae_roundval = -int(math.floor(math.log10(float(self.ae))))
        
        val = float(round(self.val, ae_roundval))        
        return str("{:." + str(math.ceil(math.log10(val/ae)) -1) + 'E}').format(Decimal(val)) + " ± {:.0E}".format(Decimal(ae))


if __name__ == "__main__":
    from physical_units import *

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


    print('-'*40 + '\nTesting functionality 2\n' + '-'*40)
    a = Physical_Unit(LENGTH, METER, 3.5821e-2, ae=0.0000001)
    b = Physical_Unit(LENGTH, METER, 27.2, ae=0.3)
    c = Physical_Unit(LENGTH, METER, 3178, ae=1)

    sqr_a = a**2
    bxc = b*c
    sqr_a_plus_bxc = sqr_a + bxc
    adivb = a/b 
    one_adivb = -adivb+1
    sqrt_one_adivb = one_adivb**0.5
    result = sqr_a_plus_bxc / sqrt_one_adivb
    print("a       =\t", a)
    print("a**2    =\t", sqr_a)
    print("bc      =\t", bxc)
    print("a**2+bc =\t", sqr_a_plus_bxc)
    print("a/b     =\t", adivb)
    print("1-a/b   =\t", one_adivb)
    print("√(1-a/b)=\t", sqrt_one_adivb)
    print("(a**2+bc)/√(1-a/b)=", result)
    print("result: ", result.to_scientific())