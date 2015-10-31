from Fractions import *

class Term(object):
    def __init__(self, coeff, exp):
        #Assumes all variables are x.
        #Coefficients are all fractions. Exponents are ints
        self.coeff = coeff
        self.exp = exp

    def __cmp__(self, other):
        if type(other) != Term:
            return 1
        x = self.exp - other.exp
        if x == 0:
            return self.coeff - other.coeff
        return x

    def __neg__(self):
        return Term(-self.coeff, self.exp)

    def __pos__(self):
        return Term(abs(self.coeff), self.exp)

    def __add__(self, other):
        if self.exp == other.exp:
            t = Term(self.coeff+other.coeff, self.exp)
            return t

    def __sub__(self, other):
        if self.exp == other.exp:
            t = Term(self.coeff-other.coeff, self.exp)
            return t
        
    def __mul__(self, other):
        if type(other) == Term:
            t = Term(self.coeff*other.coeff, self.exp+other.exp)
            return t
        return Term(self.coeff*other, self.exp)

    def __div__(self, other):
        if type(other) == Term:
            t = Term(self.coeff/other.coeff, self.exp-other.exp)
            return t
        return Term(self.coeff/other, self.exp)

    __rmul__ = __mul__

    def __rdiv__(self, other):
        #Handles number divided by term
        newcoeff = other/self.coeff
        return Term(newcoeff, -self.exp)

    def __pow__(self, other):
        return Term(self.coeff**other, self.exp*other)

    def subval(self, x):
        return self.coeff * x**self.exp

    def __repr__(self):
        if self.exp == 1:
            return str(self.coeff)+'x'
        return str(self.coeff)+'x^'+str(self.exp)

    def __str__(self):
        if (self.coeff == 1 or self.coeff == -1) and self.exp == 1:
            return 'x'
        if self.exp == 0:
            return str(self.coeff)
        if self.coeff == 1:
            return 'x^'+str(self.exp)
        if self.exp == 1:
            return str(self.coeff)+'x'
        return str(self.coeff)+'x^'+str(self.exp)



def t(coeff, exp):
    return Term(coeff, exp)
