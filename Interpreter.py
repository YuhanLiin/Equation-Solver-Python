from Term import *
import sys
sys.path.append('/python/Parsing')
from Parser import *           

lexer = [temp('pl','\('),
         temp('pr','\)'),
         temp('int','[1-9][0-9]*',lambda a: int(a)),
         temp('space',' +',lambda a: None),
         temp('x','x'),
         temp('add','\+'),
         temp('minus','\-'),
         temp('div','/'),
         temp('times','\*'),
         temp('exp','\^'),]

grammar = {'S': [rule('S EXP', None, lambda p: p[1])],
           'EXP':[rule('EXP int','num',lambda p: (p[0],p[1])),
                  rule('EXP x','var',lambda p: (p[0],)),
                  rule('EXP EXP add EXP','+',lambda p: [p[0],p[1],p[3]],['times','div','exp','x','int','pl']),
		  rule('EXP EXP minus EXP','-',lambda p: [p[0],p[1],p[3]],['times','div','exp','x','int','pl']),
                  rule('EXP EXP times EXP','*',lambda p: [p[0],p[1],p[3]],['exp']),
                  rule('EXP EXP div EXP','/',lambda p: [p[0],p[1],p[3]],['exp']),
                  rule('EXP EXP EXP','*',lambda p: [p[0],p[1],p[2]],['exp']),
                  rule('EXP EXP exp EXP','^',lambda p: [p[0],p[1],p[3]]),
                  rule('EXP pl minus EXP pr','neg',lambda p: (p[0],p[3])),
                  rule('EXP pl EXP pr',None,lambda p: p[2])]}


def interpret(ast):
    name = ast[0]
    if name == 'num':
        return [t(f(int(ast[1]), 1), 0)]
    elif name == 'var':
        return [t(f(1,1), 1)]
    elif name == 'neg':
        return map(lambda x: -x, interpret(ast[1]))
    elif name == '*':
        return expand(simplify(interpret(ast[1])), simplify(interpret(ast[2])))
    elif name == '^':
        val = simplify(interpret(ast[1]))
        exp = simplify(interpret(ast[2]))
        if len(exp) > 1 or exp[0].exp > 0:
            raise Exception("Exponential functions not supported")
        exp = int(exp[0].coeff)
        if exp == 0:
            return t(f(1,1), 0)
        if exp < 0:
            raise Exception("Negative exponents not supported")
        return exponentiate(val, exp)
    elif name == '/':
        dividend = simplify(interpret(ast[1]))
        divisor = simplify(interpret(ast[2]))
        if len(dividend) == len(divisor) and sorted(dividend) == sorted(divisor):
            return [t(f(1,1), 0)]
        if len(divisor) > 1:
            raise Exception("Rational functions not supported")
        return map(lambda x: x/divisor[0], dividend)
    elif name == '+':
        val1 = interpret(ast[1])
        val2 = interpret(ast[2])
        for i in val2:
            val1.append(i)
        return val1
    elif name == '-':
        val1 = interpret(ast[1])
        val2 = interpret(ast[2])
        for i in val2:
            val1.append(-i)
        return val1

#To sort a polynomial, use the default sorted function with reverse as True.
def simplify(terms):
    degrees = {}
    reduced = []
    for term in terms:
        if term.exp not in degrees:
            degrees[term.exp] = 0
        degrees[term.exp] += term.coeff
    for d in degrees:
        if degrees[d] != 0:
            reduced.append(t(degrees[d], d))
    return reduced

def expand(exp1, exp2):
    ans = []
    for i in exp1:
        for j in exp2:
            ans.append(i*j)
    return ans

def rtheorem(x, pnmial):
    remainder = 0
    for term in pnmial:
        remainder += term.subval(x)
    return remainder

def is_root(pnmial):
    if len(pnmial) <= 1:
        return True
    if len(pnmial) == 2 and pnmial[0].exp == 1 and pnmial[1].exp == 0:
        return True
    return False

def longdiv(pnmial, bnmial):
    quotient = []
    fterm = pnmial[0]
    i = 1
    while i < len(pnmial):
        qterm = fterm/bnmial[0]
        quotient.append(qterm)
        if pnmial[i].exp != fterm.exp - 1:
            fterm = t(0, fterm.exp - 1) - bnmial[1]*qterm
        else:
            fterm = pnmial[i] - bnmial[1]*qterm
            i += 1
    return quotient
            
def factor(pnmial):
    #Takes in sorted polynomial and factors all rational roots
    if is_root(pnmial):
        return [pnmial]

    factors = []
    common = t(1, 0)
    if pnmial[-1].exp > 0:
        common *= t(1,pnmial[-1].exp)
        pnmial = map(lambda x: x/common, pnmial)

    first, last = pnmial[0].coeff, pnmial[-1].coeff
    A = int_factors(first.num * last.denom)
    B = int_factors(first.denom * last.num)
    pos_roots = []
    for a in A:
        for b in B:
            root = f(b,a)
            if root not in pos_roots:
                pos_roots.append(root)
            if -root not in pos_roots:
                pos_roots.append(-root)
                              
    for root in pos_roots:
        while rtheorem(root, pnmial) == 0: 
            a, b = root.denom, root.num
            bnmial = [t(f(a, 1), 1), t(f(-b, 1), 0)]
            pnmial = sorted(simplify(longdiv(pnmial, bnmial)), reverse=True)
            factors.append(bnmial)
        if is_root(pnmial):
            break

    if len(pnmial) != 0:
        top = reduce(lambda x, y: t(f(GCF(x.coeff.num, y.coeff.num), 1), 0), pnmial)
        bottom = reduce(lambda x, y: t(f(1, GCF(x.coeff.denom, y.coeff.denom)), 0), pnmial)
        avalue = f(top.coeff.num, bottom.coeff.denom)
        common *= avalue
        pnmial = map(lambda x: x/avalue, pnmial)
        if len(pnmial) > 1:
            factors.append(pnmial)
    if common.exp > 0 or common.coeff != 1:
        factors.append([common])
    return factors

def exponentiate(original, exp):
    #Solves exponent in nlogn by 'halving' it each time. Russian peasant's algorithm
    pnmial = [t(f(1,1), 0)]
    while exp != 0:
        if exp % 2 == 1:
            pnmial = simplify(expand(original, pnmial))
        exp /= 2
        original = simplify(expand(original,original))
    return pnmial

def display_expanded(equation):
    s = ''
    for term in equation:
        if term.coeff > 0:
            s += ' + '
        else:
            s += ' - '
        s += str(term)
    if s[1] == '-':
        return '-'+s[3:]
    return s[3:]

def display_factored(factors):
    s = ''
    for root in factors:
        s += '('+display_expanded(root)+') '
    return s
