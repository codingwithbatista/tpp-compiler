
class syntaxErrorHandler(object):

    def __init__(self):
        self.currentStatement = ""

   
    def errorActionStatement(self):
        token = self.currentToken
        print("syntax error in line", token.getNumberOfLine(),".")
        #print("statement: ", self.currentStatement)
        print("unexpected", token.lexeme,", but was expected", self.expectedToken)
        
    

    def setCurrentToken(self, token):
        self.currentToken = token


    def setExpectedToken(self, expectedToken=str):
        self.expectedToken = expectedToken
