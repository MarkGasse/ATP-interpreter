import re
from typing import List, Tuple, Union

# -------------------------------------------
# Read file
# -------------------------------------------
def fileToStrings(fileName):
    with open(fileName, 'r') as file:
        return file.read();

# -------------------------------------------
# Token class
# -------------------------------------------
class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value
        # ADD line number

    def __repr__(self):
        return self.type
    
    def __str__(self):
        if self.value != '\n':
            return ("| TOKEN | type: " + self.type + " | value: " + self.value + " |")
        else: 
            return ("| TOKEN | type: " + self.type + " |")

# -------------------------------------------
# Token types
# -------------------------------------------
tokens = {
    'ADD': r'[+]',
    'SUB': r'[-]',
    'MUL': r'[*]',
    'DIV': r'[/]',
    'ASSIGN': r'[=]',
    'EQUAL': r'[is]',
    'EOL': r'[;]',
    'WHILE': r'[while]',
    'IF': r'[if]',
    'ELSE': r'[else]',
    'LESSER': r'[<]',
    'GREATER': r'[>]',
    'VAR': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INT': r'[0-9_]',  
}

# -------------------------------------------
# Lexer
# -------------------------------------------

# Check if string and token are equal
# checkToken:: str, str -> bool
def checkToken(token : str, string : str) -> bool:
    if re.match(token[1], string) is None:
        return False
    else:
        return True

# 
# matchToken :: str, str -> Union[Token, None]
def matchToken(string : str, tokens : str) -> Union[Token,None]:
    if len(tokens) == 0:
        return None
    else:
        head, *tail = tokens
        return Token(head[0], string) if checkToken(head, string) else matchToken(string, tail) 

#
# lexer :: str, str -> [Union[Token,None]]
def lexer(line : str, pattern : str = '') -> List[Union[Token,None]]:
    
    if len(line) == 0:
        return []

    head, *tail = line
    if str.isdigit(head) or str.isalpha(head):
        return lexer(tail, pattern + head)
    elif str.isspace(head) and pattern != '':
        return [matchToken(pattern,tokens.items())] + lexer(tail, '')
    elif not str.isspace(head): 
        if pattern != '':
            return [matchToken(pattern,tokens.items())] + [matchToken(head,tokens.items())] + lexer(tail, '')
        else:
            return [matchToken(head,tokens.items())] + lexer(tail, '')
    else: 
        return lexer(tail, '')

# -------------------------------------------
# Parser
# -------------------------------------------

class Number():
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return self.token

    def __str__(self):
        return ("Number(" + self.token.value + ")")

class Operator(Number): 
    pass

    def __str__(self):
        return ("Operator(" + self.token.value + ")")

class Node():
    def __init__(self, parent, Lchild, Rchild):
        self.parent = parent
        self.Lchild = Lchild
        self.Rchild = Rchild

    def __repr__(self):
        return self.parent
    
    def __str__(self):
        return (self.parent.token.type + "Operator("+ self.Lchild.__str__() + "," + self.parent.__str__() + "," + self.Rchild.__str__() + ")")

# Create AST of current line
# parseLine :: List[Token] -> Node
def parseLine( tokens : List[Token]) -> Node:
    if len(tokens) > 3: 
        Lchild, parent, *tail = tokens
        if re.match(r'[ASSIGN]', parent.type) != None: 
            return Node(Operator(parent), Lchild, parseOperators(tail))
        else:
            return []
    elif len(tokens) == 3: 
        Lchild, parent, Rchild = tokens
        return Node(Operator(parent), Lchild, Rchild)
    else: 
        return []

# Create AST of operators on current line
# parseOperators :: List[Token] -> Node
def parseOperators(tokens : List[Token]) -> Node: 
    if len(tokens) < 3:
        return tokens[0]

    Lchild, parent, *tail = tokens
    if re.match(r'[/^(MUL|DIV)$/]', parent.type) != None: 
        Rchild, *tail = tail
        tail.insert( 0,Node(Operator(parent), Lchild, Rchild))
        return parseOperators(tail)
    elif re.match(r'[/^(ADD|SUB)$/]', parent.type) != None:
        Rchild, *tail = tail
        if len(tail) >= 2:
            return parseOperators(lookAhead(tokens, tail))
        else: 
            tail.insert(0, Node(Operator(parent), Lchild, Rchild))
            return parseOperators(tail)

# Check if next operator has higher priority (if it should be executed first)
# lookAhead List[Token], List[Token] -> Node
def lookAhead(tokens : List[Token], currentTail : List[Token]) -> Node: 
    Lchild, parent, Rchild, parent2, Rchild2, *tail = tokens
    if re.match(r'[/^(MUL|DIV)$/]', parent2.type) != None: 
        tail.insert(0, Node(Operator(parent), Lchild, Node(Operator(parent2), Rchild, Rchild2)))
        return tail
    else: 
        currentTail.insert(0, Node(Operator(parent), Lchild, Rchild))
        return currentTail

# Create a List of Node from each line in txt file
# parser :: List[Token], List[Token] -> List[Node]
def parser(tokens : List[Token], Queue: List[Token] = []) -> List[Node]: 
    if len(tokens) == 0: 
        return []

    head, *tail = tokens
    if head.type != "EOL": 
        Queue.append(head)
        return parser(tail, Queue)
    else:
        return [parseLine(Queue)] + parser(tail, [])

# -------------------------------------------
# Run
# -------------------------------------------

def AddOperator( a: int, b: int) -> int: 
    return (int(a) + int(b))

def SubOperator( a: int, b: int) -> int: 
    return (int(a) - int(b))

def MulOperator( a: int, b: int) -> int: 
    return (int(a) * int(b))

def DivOperator( a: int, b: int) -> int: 
    return (int(a) / int(b))

def AssignOperator( a: int, b: int, vars: dict) -> int: 
    vars[a] = b
    return vars

def LesserThenOperator( a: int, b: int) -> bool: 
    return True if int(a) < int(b) else False 

def GreaterThenOperator( a: int, b: int) -> bool: 
    return True if int(a) > int(b) else False

def run(nodes: List[Node], vars: dict = {}):
    if len(nodes) == 0: 
        return vars
    head, *tail = nodes
    return run(tail, procesNodes(head, vars))

def procesNodes(node: Node, vars: dict): 
    if vars is None: 
        vars = {}
    if node.__class__ is Node:
        operator = node.parent.token.value
        if operator is '=': 
            return AssignOperator(node.Lchild.value, procesNodes(node.Rchild, vars), vars)
        elif operator is '*': 
            return MulOperator(procesNodes(node.Lchild, vars), procesNodes(node.Rchild, vars))
        elif operator is '/': 
            return DivOperator(procesNodes(node.Lchild, vars), procesNodes(node.Rchild, vars))
        elif operator is '+': 
            return AddOperator(procesNodes(node.Lchild, vars), procesNodes(node.Rchild, vars))
        elif operator is '-': 
            return SubOperator(procesNodes(node.Lchild, vars), procesNodes(node.Rchild, vars))
        else: 
            return 0
    else:
        if node.type is "VAR": 
            return vars.get(node.value)
        else:
            return node.value
    

    

# -------------------------------------------
# Debug / test functions
# -------------------------------------------

# Print list with tokens
#print(lexer(fileToStrings('File.txt')))

#print str of each token
#for i in lexer(fileToStrings('File.txt')): 
#    print(i)

#for x in parser(lexer(fileToStrings('File.txt'))):
#    print("PARSER: ",x)

print(run(parser(lexer(fileToStrings('File.txt')))))

