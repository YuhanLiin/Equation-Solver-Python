# Equation-Solver-Python
Polynomial_solver.py parses a polynomial expression, simplifies it, and prints both an expanded and factored version with all rational roots solved. Only the variable "x" is supported and non-integers must be entered as fractions in brackets (like (5/4)). Fractions.py and Term.py contain numerical classes for fractions and algebraic terms, which serve as the computational model for the algebra. Interpreter.py uses a grammar for parsing the algebraic expressions which is built upon assets from the Lexer_and_Parser repository. 

DISCLAIMER: 
-Since the '-' character denotes both subtraction and negatives, it must be placed within a set of brackets along with the value when used as a negative sign (such as (-5x) + 4).
-Putting expressions beside one another (like (5)(2x)) is synonomous with placing '*' in between them, so something like 5x/4x will be interpreted as (((5*x)/4)*x). 

Vector_adder.py is an unrelated extra program that adds 2-d vector values and outputs the sum.

