from node import Node
import re

#-------------------------------------------------------------------------------
def check_valid(expr):
	#check continuous +*/
	#check char not a-z, A-Z, +-*/, $, ()
	#check no operand
	regex = r'[+*\/][+*\/]|[^a-zA-Z0-9+\-*\/$()]|^[^a-zA-Z0-9]*$'
	if re.search(regex, expr): raise ExpressionError

	#check invalid parentheses
	open_par = 0
	close_par = 0
	for i, c in enumerate(expr):
		if c=='(': open_par+=1
		elif c==')': close_par+=1
		if close_par>open_par: raise ExpressionError

	if open_par!=close_par: raise ExpressionError
	return

class ExpressionError(Exception):
	pass

#-------------------------------------------------------------------------------
#replace negative sign by $
def expression_encode(expr):
	for i, c in enumerate(expr):
		if c=='-':
			if i==0 or expr[i-1] in '+-*/($':
				#if minus is the first char or
				#minus is behind +-*/($
				#then the minus is a negative sign
				expr = expr[:i]+'$'+expr[i+1:]

	return expr

def expression_decode(expr):
	return expr.replace('$', '-')

#-------------------------------------------------------------------------------
#{operator: (ISP, ICP)}, $ as negative sign
#ISP: in-stack-priority
#ICP: in-coming-priority
OPERATOR = {
	'+':(1, 1),
	'-':(1, 1),
	'*':(2, 2),
	'/':(2, 2),
	'$':(3, 4),
	'(':(0, 4),
	')':(None, None)
}

def get_priority(operator, in_stack=False):
	if operator in OPERATOR:
		if in_stack: return OPERATOR[operator][0]
		else: return OPERATOR[operator][1]
	return 0

def is_operator(char):
	return char in OPERATOR

#-------------------------------------------------------------------------------
def to_postfix(infix):
	stack = []
	output = []
	operand = ''

	for i, c in enumerate(infix):
		if is_operator(c):
			if operand!='':
				output.append(operand)
				operand = ''

			if c=='(':
			    stack.append('(')
			elif c==')':
			    while stack and stack[-1]!='(':
			        output.append(stack.pop())
			    stack.pop() #pop (
			else:
			    while stack and stack[-1]!='(' and get_priority(c)<=get_priority(stack[-1], True):
			        output.append(stack.pop())
			    stack.append(c)
		else:
			operand+=c

	#leftover
	if operand!='': output.append(operand)
	while stack: output.append(stack.pop())
	return output

def to_tree(postfix):
	stack = []
	for c in postfix:
		node = Node(c)
		if is_operator(c):
			if len(stack)!=0:
				node.right = stack.pop()
			if len(stack)!=0 and c!='$': #negative is unary operator
				node.left = stack.pop()
		stack.append(node)			
	return stack.pop()

def to_infix(root, upper_priority=None):
	if root==None: return ''
	infix = ''
	
	if is_operator(root.value):
		priority = get_priority(root.value)
		right_expr = to_infix(root.right, priority)
		left_expr = to_infix(root.left, priority)

		if root.value=='-':
			if root.right.value in '+-':
				right_expr = '('+right_expr+')'
		elif root.value=='/':
			if root.right.value in '*/':
				right_expr = '('+right_expr+')'

		infix = left_expr+root.value+right_expr
		if upper_priority>priority:
			infix = '('+infix+')'
	else:
		infix = root.value
	return infix

