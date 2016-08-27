import math

def int_factors(x):
    x = abs(x)
    root = int(math.sqrt(x))
    l = []
    for i in xrange(1,root+1):
        j = x / i
        if x%j == 0:
            l.append(j)
    for i in xrange(root,0,-1):
        if x%i == 0:
            l.append(i)
    return l

def GCF(x, y):
    smaller = min(x,y)
    for f in int_factors(smaller):
        if x%f == 0 and y%f == 0:
            return f
    return 1

class Fraction(object):
    def __init__(self, num, denom):
        #These must be ints
        assert denom != 0
        self.num = num
        self.denom = denom
        self.simplify()

    def simplify(self):
        if self.denom == 1 or self.num == 1:
            return
        factor = GCF(self.denom, self.num)
        self.denom /= factor
        self.num /= factor
        if self.denom < 0:
            self.denom = abs(self.denom)
            self.num = self.num*-1

    def recip(self):
        return Fraction(self.denom, self.num)
    
    def __neg__(self):
        return Fraction(-self.num, self.denom)

    def __pos__(self):
        return Fraction(abs(self.num), self.denom)
    
    def __float__(self):
        return self.num*1.0/self.denom

    def __int__(self):
        if self.num % self.denom == 0:
            return self.num/self.denom

    def __cmp__(self, other):
        if other == None:
            return 1
        if float(self) - float(other) > 0:
            return 1
        elif float(self) - float(other) < 0:
            return -1
        else:
            return 0

    def __add__(self, other):
        if type(other) == Fraction:
            f = Fraction(self.num*other.denom + other.num*self.denom, other.denom*self.denom)
            return f
        else:
            f = Fraction(self.num + other*self.denom, self.denom)
            return f

    def __sub__(self, other):
        if type(other) == Fraction:
            f = Fraction(self.num*other.denom - other.num*self.denom, other.denom*self.denom)
            return f
        else:
            f = Fraction(self.num - other*self.denom, self.denom)
            return f

    def __mul__(self, other):
        if type(other) == Fraction:
            f = Fraction(self.num*other.num, self.denom*other.denom)
            return f
        elif type(other) == int:
            f = Fraction(self.num*other, self.denom)
            return f
        else:
            #Give the operation to the Term __mul__ method
            return other * self
        
    def __div__(self, other):
        if type(other) == Fraction:
            f = Fraction(self.num*other.denom, self.denom*other.num)
            return f
        else:
            f = Fraction(self.num, self.denom*other)
            return f
        
    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        f = Fraction(other*self.denom - self.num, self.denom)
        return f

    def __rdiv__(self, other):
        f = Fraction(self.denom*other, self.num)
        return f
    
    def __pow__(self, other):
        if other > 0:
            f = Fraction(self.num**other, self.denom**other)
        elif other < 0:
            f = Fraction(self.denom**abs(other), self.num**abs(other))
        else:
            f = Fraction(1,1)
        return f

    def __repr__(self):
        return '('+str(self.num)+'/'+str(self.denom)+')'

    def __str__(self):
        if self.num == 0:
            return '0'
        if self.denom == 1:
            return str(abs(self.num))
        #Doesn't print negative sign for display purposes
        return '('+str(abs(self.num))+'/'+str(self.denom)+')'

def f(num, denom):
    return Fraction(num, denom)

