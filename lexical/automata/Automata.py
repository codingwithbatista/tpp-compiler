
class automaton(object):


    def __init__(self):
        self.mathsymbols = ['*','/','+','-',':=']
        self.logicSymbols = ['=','<=','>=','<','>','&&','||']
        self.commonSymbols = [';',',','(',')','[',']','{','}']   
    

    def __getSymbols__(self):
        symbols = self.mathsymbols + self.logicSymbols + self.commonSymbols
        return symbols

    
    def __isIFLexeme__(self, lexeme):
        symbols = self.__getSymbols__()
        try:
            return lexeme[0:2] == "se" and lexeme[2] in symbols and True or False
        except IndexError:
            return lexeme[0:2] == "se" and len(lexeme) == 2 and True or False 
    

    def __isElseLexeme__(self, lexeme):
        symbols = self.__getSymbols__()
        try:
            return lexeme[0:5] == "senão" and lexeme[5] in symbols and True or False
        except IndexError:
            return lexeme[0:5] == "senão" and len(lexeme) == 5 and True or False
    

    def __isThenLexeme__(self, lexeme):
        symbols = self.__getSymbols__()
        try:
            return lexeme[0:5] == "então" and lexeme[5] in symbols and True or False
        except IndexError:
            return lexeme[0:5] == "então" and len(lexeme) == 5 and True or False
    

    def __isEndLexeme__(self, lexeme):
        symbols = self.__getSymbols__()        
        try:
            return lexeme[0:3] == "fim" and lexeme[3] in symbols and True or False
        except IndexError:
            return lexeme[0:3] == "fim" and len(lexeme) == 3 and True or False
    

    def __isWhileLexeme__(self, lexeme):
        symbols = self.__getSymbols__()        
        try:
            return lexeme[0:6] == "repita" and lexeme[6] in symbols and True or False
        except IndexError:
            return lexeme[0:6] == "repita" and len(lexeme) == 6 and True or False
    

    def __isFloatTypeLexeme__(self, lexeme):
        symbols = self.__getSymbols__()
        try:
            return lexeme[0:9] == "flutuante" and lexeme[9] in symbols and True or False
        except IndexError:
            return lexeme[0:9] == "flutuante" and len(lexeme) == 9 and True or False


    def __isReturnLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "retorna" and True or False
        except IndexError:
            return lexeme[0:7] == "retorna" and len(lexeme) == 7 and True or False
    

    def __isUntilLexeme__(self, lexeme):
        try:
            return lexeme[0:3] == "até" and True or False
        except IndexError:
            return lexeme[0:3] == "até" and len(lexeme) == 2 and True or False
    

    def __isReadLexeme__(self, lexeme):
        try:
            return lexeme[0:4] == "leia" and True or False
        except IndexError:
            return lexeme[0:4] == "leia" and len(lexeme) == 4 and True or False
    

    def __isWriteLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "escreve" and True or False
        except IndexError:
            return lexeme[0:7] == "escreve" and len(lexeme) == 7 and True or False
    

    def __isIntegerLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "inteiro" and True or False
        except IndexError:
            return lexeme[0:7] == "inteiro" and len(lexeme) == 7 and True or False
    

    def __isPlusLexeme__(self, lexeme):
        try:
            return lexeme[0] == "+" and True or False
        except IndexError:
            return False


    def __isMinusLexeme__(self, lexeme):
        try:
            return lexeme[0] == "-" and True or False
        except IndexError:
            return False


    def __isTimesLexeme__(self, lexeme):
        try:
            return lexeme[0] == "*" and True or False
        except IndexError:
            return False


    def __isDivisionLexeme__(self, lexeme):
        try:
            return lexeme[0] == "/" and True or False
        except IndexError:
            return False


    def __isAssignmentLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == ":=" and True or False
        except IndexError:
            return False


    def __isEqualityLexeme__(self, lexeme):
        try:
            return lexeme[0] == "=" and True or False
        except IndexError:
            return False


    def __isCommaLexeme__(self, lexeme):
        try:
            return lexeme[0] == "," and True or False
        except IndexError:
            return False


    def __isLessEqualsLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == "<=" and True or False
        except IndexError:
            return False


    def __isLessLexeme__(self, lexeme):
        try:
            return lexeme[0] == "<" and True or False
        except IndexError:
            return False


    def __isHigherEqualsLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == ">=" and True or False
        except IndexError:
            return False


    def __isHigherLexeme__(self, lexeme):
        try:
            return lexeme[0] == ">" and True or False
        except IndexError:
            return False
    

