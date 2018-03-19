class token(object):

    
    def __init__(self, tokentype, tokenval, lexeme):
        self.tokentype = tokentype
        self.tokenval = tokenval
        self.lexeme = lexeme

    
    def setNumberOfLine(self,  numberOfLine):
        self.numberOfLine = int(numberOfLine)
    

    def getNumberOfLine(self):
        return self.numberOfLine
    

    def setNumberOfColumn(self, numberOfColumn):
        self.numberOfColumn = numberOfColumn
    

    def getNumberOfColumn(self):
        return self.numberOfColumn
    

    def setLine(self, line):
        self.line = line
    

    def getLine(self):
        return self.line

    
    

    
   