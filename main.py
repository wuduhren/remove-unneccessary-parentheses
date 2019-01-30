from utilities import *

#-------------------------------------------------------------------------------
#Problem
"""
Parentheses removal function.
Given a string containing an expression.
Return the expression with unnecessary parentheses removed.
For example:
f("1*(2+(3*(4+5)))") ===> "1*(2+3*(4+5))"
f("2+(3/-5)") ===> "2+3/-5"
f("x+(y+z)+(t+(v+w))") ===> "x+y+z+t+v+w"
Please write a function that removes unnecessary parenthesis for any given string.
You can write this in any language but please provide it in an executable format with instructions.
"""

#Solution
"""
1. Main idea is to convert the expression to postfix notation, to expression tree, then back to infix notation (with necessary parentheses).

2. Convert the expression into postfix. Because postfix don't need parentheses and postfix is easier to convert into expression tree.

3. In expression tree, we compare the priority of the operator from leaf(lower level) to the root(upper level).
If the operator from the lower level has higher priority, then it doesn't need parentheses.
If the operator from the lower level has lower priority, then it need parentheses.
There are two special cases.
First, if the right of the minus sign has + or - operator, then it need parentheses.
Second, if the right of the divided has * or / operator, then it need parentheses.

4. We use the rule above the reproduce infix, adding parentheses when necessary.

5. During the process, we use $ sign to differentiate minus and negative.
The look the same but minus is binary operator and negative is unary.
And negative has much higher priority.
There are two cases a minus sign is negative.
First, a minus sign at the very beginning of the expression.
Second, a minus sign after ( + - * $.
"""
#-------------------------------------------------------------------------------
def remove_parentheses(expr):
	#strip space
	expr = expr.replace(' ', '')
	check_valid(expr)

	expr = expression_encode(expr)
	postfix = to_postfix(expr)
	root = to_tree(postfix)
	infix = to_infix(root)
	expr = expression_decode(infix)
	return expr

def test(expression, expected=None):
	info = 'OK'
	try:
		result = remove_parentheses(expression)
		if expected and expected!=result:
			info = expression+' ==> '+result+' should be '+expected
	except ExpressionError:
		if expected!='ExpressionError':
			info = 'ExpressionError: '+expression
	print(info)
	return

#-------------------------------------------------------------------------------
#test cases
#normal test case
test('a+(b+c)-d', 'a+b+c-d')
test('8', '8')
test('3x', '3x')
test('(a*(b*c))', 'a*b*c')
test('(a*(b/c)*d)', 'a*b/c*d')
test('((x))', 'x')
test('((7+3)*(5-2))', '(7+3)*(5-2)')

#minus with Parentheses
test('a-(b+c)', 'a-(b+c)')
test('a-(b+c)-d', 'a-(b+c)-d')
test('a-(b+c)-((d-e)*(o+p))', 'a-(b+c)-(d-e)*(o+p)')
test('e*(a+b+c)-(f*u)', 'e*(a+b+c)-f*u')
test('1*(2+(3*(4+5)))', '1*(2+3*(4+5))')
test('((a+b)*f)-(i/j)', '(a+b)*f-i/j')

#negative value
test('-x', '-x')
test('-(x)', '-x')
test('((-x))', '-x')
test('a---b', 'a---b')
test('a/b/c/-d', 'a/b/c/-d')
test('-((b))', '-b')
test('-(a-(b+c))', '-(a-(b+c))')
test('2+(3/-5)', '2+3/-5')
test('-(-(a+b+c))', '--(a+b+c)')
test('-(a+b+c)', '-(a+b+c)')

#divided
test('(a*b)+c/(d*e)', 'a*b+c/(d*e)')
test('a+b/(c-d)', 'a+b/(c-d)')
test('a+b/(c*d)', 'a+b/(c*d)')
test('(a*b)/(c*d)', 'a*b/(c*d)')
test('a+b/(c-d)', 'a+b/(c-d)')
test('(a-b)/(c*d)', '(a-b)/(c*d)')
test('a/(b/c)', 'a/(b/c)')
test('(a/b)/c', 'a/b/c')
test('((a/(b/c))/d)', 'a/(b/c)/d')

#multiple char operand
test('(a*b)+4x/(3y*2z)', 'a*b+4x/(3y*2z)')
test('11*(22+(33*(44+55)))', '11*(22+33*(44+55))')

#ExpressionError
test('))', 'ExpressionError')
test('(a*b)+4x/(3y*+2z)', 'ExpressionError')
test('))((', 'ExpressionError')
test('()', 'ExpressionError')
test('(())', 'ExpressionError')
