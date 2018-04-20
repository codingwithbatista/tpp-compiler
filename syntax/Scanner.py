from syntax.SyntaxIdentifier import syntax_recognizer as sr

class syntax_scanner(object):

    def __init__(self):
        pass

    
    def scan(self, tokenlist=[]):
        while len(tokenlist) > 0:
            tokenlist = self.consumeNumber(tokenlist)
            

    

    def consumeNumber(self, tokenlist):
        if sr().isNumber(tokenlist[0]):
            return tokenlist[1:]
