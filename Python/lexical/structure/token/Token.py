class token(object):

    
    def __init__(self, tokentype=None, tokenval=None, lexeme=None):
        self.tokentype = tokentype
        self.tokenval = tokenval
        self.lexeme = lexeme
        self.__setTerminal()


    def __setTerminal(self):
        if self.tokentype == None:
            self.terminal = False
        else:
            self.terminal = True

    def getTerminal(self):
        return self.terminal
    
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

    
    

    
   