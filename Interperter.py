import re
from typing import List, Tuple, Union, Callable
from functools import reduce

# -------------------------------------------
# Read file
# -------------------------------------------

# Returns str of characters in fileName
def fileToStrings(fileName):
    with open(fileName, 'r') as file:
        return file.read();

# -------------------------------------------
# Token class
# -------------------------------------------

# Token object containing: 
# type, value of token and line number of location in txt file
class Token():
    def __init__(self, type, value, lineNumber):
        self.type = type
        self.value = value
        self.lineNumber = lineNumber

    def __repr__(self):
        return self.type
    
    def __str__(self):
            return ("Line: "+ str(self.lineNumber) +"| TOKEN | type: " + self.type + " | value: " + self.value + " |")

# -------------------------------------------
# Token types
# -------------------------------------------

# Dict of supported tokens
tokens = {
    'ADD': r'(adde)',
    'SUB': r'(minuas)',
    'MUL': r'(pullulate)',
    'DIV': r'(divisa)',
    'ASSIGN': r'(assignato)',
    'EQUAL': r'(par)',
    'NOTEQUAL': r'(dispar)',
    'EOL': r'(semicolon)',
    'EOC': r'(tum)',
    'WHILE': r'(dum)',
    'ENDWHILE': r'(finisdum)',
    'IF': r'(si)',
    'ENDIF': r'(finissi)',
    'LESSER': r'(minor)',
    'GREATER': r'(major)',
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

# Creates a token of string
# matchToken :: str, str, int -> Token
def matchToken(string : str, tokens : str, lineNumber: int) -> Token:
    return Token(next(filter(lambda currentToken: checkToken(currentToken, string), tokens))[0], string, lineNumber)

# Creates a list of tokens
# lexer :: str, str -> [Token]
def lexer(stringOfChars : str, lineNumber: int=1, Queue : str = '') -> List[Token]:
    if len(stringOfChars) == 0:
        return []

    head, *tail = stringOfChars
    # Increase line number if char is "\n"
    if head is '\n': 
        lineNumber += 1

    # Add char to Queue if char is alpha or a digit
    if str.isdigit(head) or str.isalpha(head):
        return lexer(tail,lineNumber, Queue + head)
    # If Queue is variable or statement
    # Create token of current Queue and continue creating tokens out with the tail
    elif str.isspace(head) and Queue != '':
        return [matchToken(Queue,tokens.items(),lineNumber)] + lexer(tail,lineNumber, '')
    # if head is an operator
    elif not str.isspace(head): 
        # if Queue is not empty: create token of Queue and operator (head) and continue with tail
        # Else create token from operator (head) and continue with tail
        if Queue != '':
            return [matchToken(Queue,tokens.items(),lineNumber)] + [matchToken(head,tokens.items(),lineNumber)] + lexer(tail,lineNumber, '')
        else:
            return [matchToken(head,tokens.items(),lineNumber)] + lexer(tail,lineNumber, '')
    # If none of the above, continue tail and clear Queue (aka ignore empty space)
    else: 
       return lexer(tail,lineNumber, '')

# -------------------------------------------
# Classes
# -------------------------------------------

class base(): 
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return self.token

class Operator(base): 
    pass

    def __str__(self):
        return ("Operator(" + self.token.value + ")")

class Node():
    def __init__(self, parent, Lchild, Rchild):
        self.parent = parent
        self.Lchild = Lchild
        self.Rchild = Rchild

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return (str(self.parent.token.type) + "Operator("+ self.Lchild.__str__() + "," + self.parent.__str__() + "," + self.Rchild.__str__() + ")")

# -------------------------------------------
# Parser
# -------------------------------------------

# Create AST of current line
# parseLine :: List[Token] -> Node
def parseLine( tokens : List[Token]) -> Node:
    if len(tokens) >= 3: 
        Lchild, parent, *tail = tokens
        if re.match(r'[ASSIGN]', parent.type) != None: 
            if len(tokens) == 3: 
                Rchild, *tail = tail
                return Node(Operator(parent), Lchild, Rchild)
            else:
                return Node(Operator(parent), Lchild, parseOperators(tail))
        else:
            return []
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
    elif re.match(r'[/^(LESSER|GREATER|NOTEQUAL|EQUAL)$/]', parent.type) != None:
        return Node(Operator(parent), Lchild, parseOperators(tail))

# Check if next operator has higher priority (if "True", it should be executed first)
# lookAhead List[Token], List[Token] -> Node
def lookAhead(tokens : List[Token], currentTail : List[Token]) -> Node: 
    Lchild, parent, Rchild, parent2, Rchild2, *tail = tokens
    if re.match(r'[/^(MUL|DIV)$/]', parent2.type) != None: 
        tail.insert(0, Node(Operator(parent), Lchild, Node(Operator(parent2), Rchild, Rchild2)))
        return tail
    else: 
        currentTail.insert(0, Node(Operator(parent), Lchild, Rchild))
        return currentTail

# Create a List of AST from each line in txt file
# parser :: List[Token], List[Token] -> List[Node]
def parser(tokens : List[Token], Queue: List[Token] = []) -> List[Node]: 
    if len(tokens) == 0: 
        return []

    head, *tail = tokens
    if head.type is "IF" or head.type is "WHILE":
        statement = getStatementCondition(tail, [])
        statementsInCondition, statementsOutCondition = StatementsInStatement(head.type, statement[1], 0, [])
        return [Node(Operator(head), parser(statementsInCondition, []), statement[0])] + parser(statementsOutCondition, [])
    elif head.type == "EOL": 
        if len(Queue) < 2: 
            return []
        else:
            return [parseLine(Queue)] + parser(tail, [])
    else:
        Queue.append(head)
        return parser(tail, Queue)

# Separate tokens in statement (if or while) from tail 
# Taking nested statements into account   
# StatementsInStatement :: str, List[Token], int, List[Token] -> Tuple[List[Token], list[Token]]
def StatementsInStatement(state: str,  tokens: List[Token],nested: int=0, Queue: List[Token] = []) -> Tuple[List[Token], list[Token]]: 
    if len(tokens) is 0: 
        return(Queue, tokens)
    head, *tail = tokens
    if head.type is "ENDIF" and state is "IF" and nested is 0: 
        return(Queue, tail)
    if head.type is "ENDWHILE" and state is "WHILE" and nested is 0: 
        return(Queue, tail)
    else: 
        if (state is "IF" and head.type is "IF") or (state is "WHILE" and head.type is "WHILE"): 
            nested += 1
        elif (state is "IF" and head.type is "ENDIF") or (state is "WHILE" and head.type is "ENDWHILE"):
            nested -= 1
        Queue.append(head)
        return StatementsInStatement(state, tail,nested, Queue)

# Separate tokens of the condition from (if or while statement) from tail
# return a tuple of: condition of the statement (AST) and tail with other tokens
# getStatementCondition :: List[Token], List[Token] -> Tuple[List[Node],List[Token]]
def getStatementCondition(tokens: List[Token], Queue: List[Token] = []) -> Tuple[List[Node],List[Token]]: 
    head, *tail = tokens 
    if head.type is "EOC": 
        return (parseOperators(Queue), tail)
    else: 
        Queue.append(head)
        return getStatementCondition(tail, Queue)

# -------------------------------------------
# Decorator
# -------------------------------------------

#
# VariableChanges :: Callable[[str, int], dict], str -> Callable[[str, int], dict]
def VariableChanges(func: Callable[[str, int], dict], lineNumber: str) -> Callable[[str, int], dict]:
    # Print current existing variables
    showCurrentVariables(func, lineNumber)
    # return function
    return func

# -------------------------------------------
# Operator functions
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

def IsEqualOperator(a: int, b: int) -> bool: 
    return True if int(a) == int(b) else False

def IsNotEqualOperator(a: int, b: int) -> bool: 
    return True if int(a) != int(b) else False

# -------------------------------------------
# Run
# -------------------------------------------

def run(statements: List[Node], variables: dict ={}) ->dict:
    if variables is None: 
        variables = {}

    if len(statements) == 0: 
        return variables

    head, *tail = statements
    return run(tail, executeStatement(head, variables))

def executeStatement(statement: Node, variables: dict) -> dict: 
    if statement.__class__ is Node:
        operator = statement.parent.token.type
        if operator is 'ASSIGN': 
            return VariableChanges(AssignOperator(statement.Lchild.value, executeStatement(statement.Rchild, variables), variables), statement.parent.token.lineNumber)
        elif operator is 'MUL': 
            return MulOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'DIV': 
            return DivOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'ADD': 
            return AddOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'SUB': 
            return SubOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'IF': 
            if executeStatement(statement.Rchild, variables): 
               return run(statement.Lchild, variables)
            return(variables)
        elif operator is 'WHILE': 
            if executeStatement(statement.Rchild, variables): 
                return executeStatement(statement, run(statement.Lchild, variables))
            return(variables)
        elif operator is 'NOTEQUAL': 
            return IsNotEqualOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))  
        elif operator is 'EQUAL': 
            return IsEqualOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'LESSER': 
            return LesserThenOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
        elif operator is 'GREATER': 
            return GreaterThenOperator(executeStatement(statement.Lchild, variables), executeStatement(statement.Rchild, variables))
    else:
        if statement.type is "VAR": 
            return variables.get(statement.value)
        else:
            return statement.value

# -------------------------------------------
# Visualization 
# -------------------------------------------

def showCurrentVariables(variables: dict, currentLine: str):
    VariablesList = list(map(lambda x: "variable: " + str(x) + " = " +str(variables[x]), variables))
    VariablesList.insert(0, ("Current line number: " + str(currentLine)))
    VariablesList. append("\n")
    return list(map(lambda x: show(x), VariablesList))

def show(string: str) -> None: 
    print(string)

# -------------------------------------------
# Debug / test functions
# -------------------------------------------

# Print list with tokens
#print(lexer(fileToStrings('File.txt')))

#print str of each token
#for i in lexer(fileToStrings('File.txt')): 
#    print(i)

#parser
#for x in parser(lexer(fileToStrings('File.txt'))):
#    print("PARSER: ",x)

#run
x = run(parser(lexer(fileToStrings('File.txt'))))