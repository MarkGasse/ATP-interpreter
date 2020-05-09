import re
from typing import List, Tuple, Union, Callable

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
def parseLine( tokens : List[Token]) -> Union[Node,List[Token]]:
    if len(tokens) >= 3: 
        Lchild, parent, *tail = tokens
        # if assign operator: create AST of current line
        if re.match(r'[ASSIGN]', parent.type) != None:
            # if 3 tokens create AST of tokens
            if len(tokens) == 3: 
                Rchild, *tail = tail
                return Node(Operator(parent), Lchild, Rchild)
            # if more then 3 tokens: first create AST of tokens in tail
            else:
                return Node(Operator(parent), Lchild, parseOperators(tail))
    # Not enough tokens to create AST: return tokens
    else: 
        return tokens

# Create AST of operators on current line
# parseOperators :: List[Token] -> Node
def parseOperators(tokens : List[Token]) -> Node: 
    if len(tokens) < 3:
        return tokens[0]

    Lchild, parent, *tail = tokens
    # Create Node of operator
    if re.match(r'[/^(MUL|DIV)$/]', parent.type) != None: 
        Rchild, *tail = tail
        tail.insert( 0,Node(Operator(parent), Lchild, Rchild))
        return parseOperators(tail)
    elif re.match(r'[/^(ADD|SUB)$/]', parent.type) != None:
        Rchild, *tail = tail
        # If their are more operators: check if next has higher priority
        if len(tail) >= 2:
            return parseOperators(lookAhead(tokens, tail))
        else: 
            tail.insert(0, Node(Operator(parent), Lchild, Rchild))
            return parseOperators(tail)
    # if token is condition: Create Node with Lchild is AST of operators on left side (Rchild vice versa)
    elif re.match(r'[/^(LESSER|GREATER|NOTEQUAL|EQUAL)$/]', parent.type) != None:
        return Node(Operator(parent), Lchild, parseOperators(tail))

# Check if next operator has higher priority (if "True", it should be executed first)
# lookAhead List[Token], List[Token] -> Node
def lookAhead(tokens : List[Token], currentTail : List[Token]) -> Node: 
    Lchild, parent, Rchild, parent2, Rchild2, *tail = tokens
    # If "True": add next operator node as Right child in current Node
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
        # Get AST of condition of statement
        statement = getStatementCondition(tail, [])
        # Split Tokens in list of tokens inside the statement and outside the statement
        tokensInCondition, tokensOutCondition = tokensInStatement(head.type, statement[1], 0, [])
        # return a AST containing the statement and the "parsed tokens" (statements) inside the statement
        # And continue to parsing tokens outside statement
        return [Node(Operator(head), parser(tokensInCondition, []), statement[0])] + parser(tokensOutCondition, [])
    # if end of line: Create AST of Queue and continue parsing tail
    elif head.type == "EOL": 
        return [parseLine(Queue)] + parser(tail, [])
    # Add token to Queue
    else:
        Queue.append(head)
        return parser(tail, Queue)

# Separate tokens in statement (if or while) from tail 
# Taking nested statements into account   
# tokensInStatement :: str, List[Token], int, List[Token] -> Tuple[List[Token], list[Token]]
def tokensInStatement(state: str,  tokens: List[Token],nested: int=0, Queue: List[Token] = []) -> Tuple[List[Token],List[Token]]: 
    if len(tokens) is 0: 
        return(Queue, tokens)
    head, *tail = tokens

    # Check if end of (if or while) statement
    if head.type is "ENDIF" and state is "IF" and nested is 0: 
        return(Queue, tail)
    elif head.type is "ENDWHILE" and state is "WHILE" and nested is 0: 
        return (Queue, tail)
    else:
        # If nested (while or if) update nested counter
        if (state is "IF" and head.type is "IF") or (state is "WHILE" and head.type is "WHILE"): 
            nested += 1
        elif (state is "IF" and head.type is "ENDIF") or (state is "WHILE" and head.type is "ENDWHILE"):
            nested -= 1
        # Add token to Queue
        Queue.append(head)
        return tokensInStatement(state, tail,nested, Queue)

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

# This decorator is called every assign operator (in executeStatement function)
# Prints line number and current variables of code
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

# Executes all statements in list
# run :: List[Node], dict -> dict 
def run(statements: List[Node], variables: dict ={}) -> dict:
    if variables is None: 
        variables = {}

    if len(statements) == 0: 
        return variables

    head, *tail = statements
    return run(tail, executeStatement(head, variables))

# Executes statement: variables are stored in the variables dict
# This can be used for the next statement
# executeStatement :: Node, dict -> dict
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

def showCurrentVariables(variables: dict, currentLine: str) -> List[print]:
    VariablesList = list(map(lambda x: "variable: " + str(x) + " = " +str(variables[x]), variables))
    VariablesList.insert(0, ("Current line number: " + str(currentLine)))
    VariablesList. append("\n")
    return list(map(lambda x: show(x), VariablesList))

def show(string: str) -> None: 
    print(string)

# -------------------------------------------
# Call functions
# -------------------------------------------

# Print list with tokens
Lexer = lexer(fileToStrings('File.txt'))
#print(Lexer)

#print str of each token
#for i in Lexer: 
#    print(i)

# parser
Parser = parser(Lexer)
#print(Parser)

#for x in Parser:
#    print(x , "\n")

# run
x = run(Parser)