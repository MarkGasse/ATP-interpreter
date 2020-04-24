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
        return ("| TOKEN: " + self.type + " | VALUE: " + self.value + " |")

# -------------------------------------------
# Token types
# -------------------------------------------
tokens = {
    'ADD': r'[+]',
    'SUB': r'[-]',
    'MUL': r'[*]',
    'DIV': r'[/]',
    'IS': r'[=]',
    'EQUAL': r'[=][=]',
    'VAR': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INT': r'[0-9_]'
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
def lexer(line : str, pattern : str) -> List[Union[Token,None]]:
    
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



# -------------------------------------------
# Run
# -------------------------------------------

# -------------------------------------------
# Debug / test functions
# -------------------------------------------

# Print list with tokens
print(lexer(fileToStrings('File.txt'), ''))

#print str of each token
for i in lexer(fileToStrings('File.txt'), ''): 
    print(i)









