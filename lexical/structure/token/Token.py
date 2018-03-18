class token(object):

    
    def __init__(self, tokentype, tokenval, lexeme, numberOfLine, numberOfColumn, line):
        self.tokentype = tokentype
        self.tokenval = tokenval
        self.lexeme = lexeme
        self.numberOfLine = numberOfLine
        self.numberOfColumn = numberOfColumn
        self.line = line
    
   