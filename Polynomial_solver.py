from Interpreter import *

while True:    
    print "Enter a POLYNOMIAL function. No support for polynomial denominators or variable exponents"
    print "Use ^ for exponents and put negative values inside brackets."
    string = raw_input("Y = ")
    tokens = lex(string, lexer)
    ast = parse(grammar, {}, tokens, grammar['S'][0])
    pnmial = sorted(simplify(interpret(ast)), reverse=True)
    #print pnmial
    print 'Expanded: ', display_expanded(pnmial)
    print 'Roots: ', display_factored(factor(pnmial))
    print ''
            
            
