from lexical.structure.token.Token import token
from lexical.structure.token.TokenType import TokenType
from lexical.structure.token.TokenVal import TokenVal
from lexical.structure.Stack import stack
import copy


class automaton(object):


    def __init__(self):
        self.mathsymbols = ['*','/','+','-',':=']
        self.logicSymbols = ['=','<=','>=','<','>','&&','||']
        self.commonSymbols = [':',';',',','(',')','[',']','{','}']   
        self.naturalDigits = ['0','1','2','3','4','5','6','7','8','9']
        self.lowercaseLetters = ['a','b','c','ç','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','w','y','z','_']
        self.uppercaseLetters = ['A','B','C','Ç','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','W','Y','Z','_']
        self.specialLowerCases = ['á','é','í','ó','ú','à','è','ì','ò','ù','â','ê','î','ô','û','ã','ẽ','ĩ','õ','ũ','ä','ë','ï','ö','ü']
        self.specialUpperCases = ['Á','É','Í','Ó','Ú','À','È','Ì','Ò','Ù','Â','Ê','Î','Ô','Û','Ã','Ẽ','Ĩ','Õ','Ũ','Ä','Ë','Ï','Ö','Ü']
        self.numberOfCurrentLine = 1
        self.numberOfCurrentColumn = 1

    def __getSymbols__(self):
        symbols = self.mathsymbols + self.logicSymbols + self.commonSymbols
        return symbols

    
    def __isIFLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == "se" and self.__isLetter__(lexeme[2]) == False and True or False
        except IndexError:
            return lexeme[0:2] == "se" and len(lexeme) == 2 and True or False 
    

    def __isElseLexeme__(self, lexeme):
        try:
            return lexeme[0:5] == "senão" and self.__isLetter__(lexeme[5]) == False and True or False
        except IndexError:
            return lexeme[0:5] == "senão" and len(lexeme) == 5 and True or False
    

    def __isThenLexeme__(self, lexeme):
        try:
            return lexeme[0:5] == "então" and self.__isLetter__(lexeme[5]) == False and True or False
        except IndexError:
            return lexeme[0:5] == "então" and len(lexeme) == 5 and True or False
    

    def __isEndLexeme__(self, lexeme):     
        try:
            return lexeme[0:3] == "fim" and self.__isLetter__(lexeme[3]) == False and True or False
        except IndexError:
            return lexeme[0:3] == "fim" and len(lexeme) == 3 and True or False
    

    def __isForLexeme__(self, lexeme):
        try:
            return lexeme[0:6] == "repita" and self.__isLetter__(lexeme[6]) == False and True or False
        except IndexError:
            return lexeme[0:6] == "repita" and len(lexeme) == 6 and True or False
    

    def __isFloatTypeLexeme__(self, lexeme):
        try:
            return lexeme[0:9] == "flutuante" and self.__isLetter__(lexeme[9]) == False and True or False
        except IndexError:
            return lexeme[0:9] == "flutuante" and len(lexeme) == 9 and True or False


    def __isReturnLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "retorna" and self.__isLetter__(lexeme[7]) == False and True or False
        except IndexError:
            return lexeme[0:7] == "retorna" and len(lexeme) == 7 and True or False
    

    def __isUntilLexeme__(self, lexeme):
        try:
            return lexeme[0:3] == "até" and self.__isLetter__(lexeme[3]) == False and True or False
        except IndexError:
            return lexeme[0:3] == "até" and len(lexeme) == 2 and True or False
    

    def __isReadLexeme__(self, lexeme):
        try:
            return lexeme[0:4] == "leia" and self.__isLetter__(lexeme[4]) == False and True or False
        except IndexError:
            return lexeme[0:4] == "leia" and len(lexeme) == 4 and True or False
    

    def __isWriteLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "escreve" and self.__isLetter__(lexeme[7]) == False and True or False
        except IndexError:
            return lexeme[0:7] == "escreve" and len(lexeme) == 7 and True or False
    

    def __isIntegerTypeLexeme__(self, lexeme):
        try:
            return lexeme[0:7] == "inteiro" and self.__isLetter__(lexeme[7]) == False and True or False
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
    

    def __isOPenParenthesesLexeme__(self, lexeme):
        try:
            return lexeme[0] == "(" and True or False
        except IndexError:
            return False


    def __isCloseParenthesesLexeme__(self, lexeme):
        try:
            return lexeme[0] == ")" and True or False
        except IndexError:
            return 
            

    def __isTwoDotsLexeme_(self, lexeme):
        try:
            return lexeme[0] == ":" and True or False
        except IndexError:
            return False


    def __isOpenBracketsLexeme__(self, lexeme):
        try:
            return lexeme[0] == "[" and True or False
        except IndexError:
            return False


    def __isCloseBracketsLexeme__(self, lexeme):
        try:
            return lexeme[0] == "]" and True or False
        except IndexError:
            return False


    def __isLogicAndLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == "&&" and True or False
        except IndexError:
            return False


    def __isLogicOrLexeme__(self, lexeme):
        try:
            return lexeme[0:2] == "||" and True or False
        except IndexError:
            return False


    def __isNotLexeme__(self, lexeme):
        try:
            return lexeme[0] == "!" and True or False
        except IndexError:
            return False
    

    def __isNumber__(self, lexeme):
        try:
            return lexeme[0] in self.naturalDigits and True or False
        except IndexError:
            return False
    

    def __discardComment__(self, lexeme):
        if lexeme[0] == "{":
            try:
                stk = stack()
                for i in range(len(lexeme)):
                    if lexeme[i] == "{":
                        stk.push("{")
                    elif lexeme[i] == "}":
                        stk.pop()
                    elif self.__isBreakLine__(lexeme[i]):
                        self.numberOfCurrentLine = self.numberOfCurrentLine + 1
                        self.numberOfCurrentColumn = 1
                    if stk.isEmpty():
                        index = i + 1
                        return lexeme[index:]
                        
            except IndexError:
                return None
        else:
            return None
    

    def __discardSpace__(self, lexeme):
        try:
            if lexeme[0] == " ":
                self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
                return lexeme[1:]
            else :
                return None
        except IndexError:
            return None
    

    def __discardBreakLine__(self, lexeme):
        try:
            if lexeme[0] == "\n":
                self.numberOfCurrentLine = self.numberOfCurrentLine + 1
                self.numberOfCurrentColumn = 1
                return lexeme[1:]
            else:
                return None
        except IndexError:
            return None

    
    def __isBreakLine__(self, lexeme):
        return lexeme[0] == "\n" and True or False
    

    def __isSpace__(self, lexeme):
        return lexeme[0] == " " and True or False

    def __isLetter__(self, lexeme):
        if lexeme[0] in self.lowercaseLetters:
            return True
        elif lexeme[0] in self.uppercaseLetters:
            return True
        elif lexeme[0] in self.specialLowerCases:
            return True
        elif lexeme[0] in self.specialUpperCases:
            return True
        else:
            return False


    def getCurrentLine(self, sourceCode):
        try:
            currentLine = str(sourceCode).split("\n")[0]
            return currentLine
        except IndexError:
            return ""


    def getIfToken(self, sourceCode):
        if self.__isIFLexeme__(sourceCode):
            tokentype = TokenType.IF
            tokenval = TokenVal.IF
            lexeme = "se"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None
    

    def getElseToken(self, sourceCode):
        if self.__isElseLexeme__(sourceCode):
            tokentype = TokenType.ELSE
            tokenval = TokenVal.ELSE
            lexeme = "senão"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[5:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 5
            return tk, slicedSourceCode
        else:
            return None
    

    def getThenToken(self, sourceCode):
        if self.__isThenLexeme__(sourceCode):
            tokentype = TokenType.THEN
            tokenval = TokenVal.THEN
            lexeme = "então"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[5:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 5
            return tk, slicedSourceCode
        else:
            return None


    def getEndToken(self, sourceCode):
        if self.__isEndLexeme__(sourceCode):
            tokentype = TokenType.END
            tokenval = TokenVal.END
            lexeme = "fim"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[3:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 3
            return tk, slicedSourceCode
        else:
            return None
    

    def getForToken(self, sourceCode):
        if self.__isForLexeme__(sourceCode):
            tokentype = TokenType.FOR
            tokenval = TokenVal.FOR
            lexeme = "repita"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[6:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 6
            return tk, slicedSourceCode
        else:
            return None
    

    def getReturnToken(self, sourceCode):
        if self.__isReturnLexeme__(sourceCode):
            tokentype = TokenType.RETURN
            tokenval = TokenVal.RETURN
            lexeme = "retorna"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[7:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 7
            return tk, slicedSourceCode
        else:
            return None
    

    def getUntilToken(self, sourceCode):
        if self.__isUntilLexeme__(sourceCode):
            tokentype = TokenType.UNTIL
            tokenval = TokenVal.UNTIL
            lexeme = "até"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[3:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 3
            return tk, slicedSourceCode
        else:
            return None
    

    def getReadToken(self, sourceCode):
        if self.__isReadLexeme__(sourceCode):
            tokentype = TokenType.READ
            tokenval = TokenVal.READ
            lexeme = "leia"
            numberOfCurrentLine = self.numberOfCurrentLine
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[4:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 4
            return tk, slicedSourceCode
        else:
            return None
    

    def getWriteToken(self, sourceCode):
        if self.__isWriteLexeme__(sourceCode):
            tokentype = TokenType.WRITE
            tokenval = TokenVal.WRITE
            lexeme = "escreve"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[7:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 7
            return tk, slicedSourceCode
        else:
            return None
    

    def getIntegerTypeToken(self, sourceCode):
        if self.__isIntegerTypeLexeme__(sourceCode):
            tokentype = TokenType.INTEGER_TYPE
            tokenval = TokenVal.INTEGER_TYPE
            lexeme = "inteiro"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[7:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 7
            return tk, slicedSourceCode
        else:
            return None
    

    def getFloatTypeToken(self, sourceCode):
        if self.__isFloatTypeLexeme__(sourceCode):
            tokentype = TokenType.FLOAT_TYPE
            tokenval = TokenVal.FLOAT_TYPE
            lexeme = "flutuante"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[9:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 9
            return tk, slicedSourceCode
        else:
            return None


    def getPlusToken(self, sourceCode):
        if self.__isPlusLexeme__(sourceCode):
            tokentype = TokenType.PLUS
            tokenval = TokenVal.PLUS
            lexeme = "+"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getMinusToken(self, sourceCode):
        if self.__isMinusLexeme__(sourceCode):
            tokentype = TokenType.MINUS
            tokenval = TokenVal.MINUS
            lexeme = "-"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getTimesToken(self, sourceCode):
        if self.__isTimesLexeme__(sourceCode):
            tokentype = TokenType.TIMES
            tokenval = TokenVal.TIMES
            lexeme = "*"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getDivisionToken(self, sourceCode):
        if self.__isDivisionLexeme__(sourceCode):
            tokentype = TokenType.DIVISION
            tokenval = TokenVal.DIVISION
            lexeme = "/"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getLogicEqualsToken(self, sourceCode):
        if self.__isEqualityLexeme__(sourceCode):
            tokentype = TokenType.LOGIC_EQUALS
            tokenval = TokenVal.LOGIC_EQUALS
            lexeme = "="
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getCommaToken(self, sourceCode):
        if self.__isCommaLexeme__(sourceCode):
            tokentype = TokenType.COMMA
            tokenval = TokenVal.COMMA
            lexeme = ","
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getAssignmentToken(self, sourceCode):
        if self.__isAssignmentLexeme__(sourceCode):
            tokentype = TokenType.ASSIGNMENT
            tokenval = TokenVal.ASSIGNMENT
            lexeme = ":="
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None
    

    def getLessToken(self, sourceCode):
        if self.__isLessLexeme__(sourceCode):
            tokentype = TokenType.LESS
            tokenval = TokenVal.LESS
            lexeme = "<"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getHigherToken(self, sourceCode):
        if self.__isHigherLexeme__(sourceCode):
            tokentype = TokenType.HIGHER
            tokenval = TokenVal.HIGHER
            lexeme = ">"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getLessEqualsToken(self, sourceCode):
        if self.__isLessEqualsLexeme__(sourceCode):
            tokentype = TokenType.LESS_EQUALS
            tokenval = TokenVal.LESS_EQUALS
            lexeme = "<="
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None


    def getHigherEqualsToken(self, sourceCode):
        if self.__isHigherEqualsLexeme__(sourceCode):
            tokentype = TokenType.HIGHER_EQUALS
            tokenval = TokenVal.HIGHER_EQUALS
            lexeme = ">="
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None
    

    def getOpenParethesesToken(self, sourceCode):
        if self.__isOPenParenthesesLexeme__(sourceCode):
            tokentype = TokenType.OPEN_PARENTHESES
            tokenval = TokenVal.OPEN_PARENTHESES
            lexeme = "("
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getCloseParenthesesToken(self, sourceCode):
        if self.__isCloseParenthesesLexeme__(sourceCode):
            tokentype = TokenType.CLOSE_PARENTHESES
            tokenval = TokenVal.CLOSE_PARENTHESES
            lexeme = ")"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getTwoDotsToken(self, sourceCode):
        if self.__isTwoDotsLexeme_(sourceCode):
            tokentype = TokenType.TWO_DOTS
            tokenval = TokenVal.TWO_DOTS
            lexeme = ":"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    
    
    def getOpenBracketsToken(self, sourceCode):
        if self.__isOpenBracketsLexeme__(sourceCode):
            tokentype = TokenType.OPEN_BRACKETS
            tokenval = TokenVal.OPEN_BRACKETS
            lexeme = "["
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getCloseBracketsToken(self, sourceCode):
        if self.__isCloseBracketsLexeme__(sourceCode):
            tokentype = TokenType.CLOSE_BRACKETS
            tokenval = TokenVal.CLOSE_BRACKETS
            lexeme = "]"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getLogicAndToken(self, sourceCode):
        if self.__isLogicAndLexeme__(sourceCode):
            tokentype = TokenType.LOGIC_AND
            tokenval = TokenVal.LOGIC_AND
            lexeme = "&&"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None
    
    def getLogicOrToken(self, sourceCode):
        if self.__isLogicOrLexeme__(sourceCode):
            tokentype = TokenType.LOGIC_OR
            tokenval = TokenVal.LOGIC_OR
            lexeme = "||"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[2:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 2
            return tk, slicedSourceCode
        else:
            return None
    
    
    def getLogicNotToken(self, sourceCode):
        if self.__isNotLexeme__(sourceCode):
            tokentype = TokenType.LOGIC_NOT
            tokenval = TokenVal.LOGIC_NOT
            lexeme = "!"
            currentLine = self.getCurrentLine(sourceCode)
            numberOfCurrentLine = self.numberOfCurrentLine
            numberOfCurrentColumn = self.numberOfCurrentColumn
            tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
            slicedSourceCode = sourceCode[1:]
            self.numberOfCurrentColumn = self.numberOfCurrentColumn + 1
            return tk, slicedSourceCode
        else:
            return None
    

    def getIntegerNumberToken(self, sourceCode):
        if self.__isNumber__(sourceCode):
            try:
                index = 0
                for i in range(len(sourceCode)):
                    if self.__isNumber__(sourceCode[i]):
                        index = i
                    else:
                        break
                index = index + 1
                
                tokentype = TokenType.INTEGER_NUMBER
                tokenval = TokenVal.INTEGER_NUMBER
                lexeme = sourceCode[0:index]
                currentLine = self.getCurrentLine(sourceCode)
                numberOfCurrentLine = self.numberOfCurrentLine
                numberOfCurrentColumn = self.numberOfCurrentColumn
                tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
                slicedSourceCode = sourceCode[index:]
                self.numberOfCurrentColumn = self.numberOfCurrentColumn + index
                return tk, slicedSourceCode
            except IndexError:
                return None
        else:
            return None
    

    def getFloatNumberToken(self, sourceCode):
        if self.__isNumber__(sourceCode):
            try:
                index = 0
                for i in range(len(sourceCode)):
                    if self.__isNumber__(sourceCode[i]):
                        index = i
                    else:
                            break
                index = index + 1
                if sourceCode[index] == ".":
                    newIndex = index + 1
                    if newIndex > len(sourceCode):
                        index = newIndex
                    else:    
                        for j in range(newIndex, len(sourceCode)):
                            if self.__isNumber__(sourceCode[j]):
                                index = j
                            else:
                                break
                    index = index + 1
                    if index > len(sourceCode):
                        index = len(sourceCode) - 1
                    tokentype = TokenType.FLOAT_NUMBER
                    tokenval = TokenVal.FLOAT_NUMBER
                    lexeme = sourceCode[0:index]
                    numberOfCurrentLine = self.numberOfCurrentLine
                    currentLine = self.getCurrentLine(sourceCode)
                    numberOfCurrentColumn = self.numberOfCurrentColumn
                    tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine)
                    slicedSourceCode = sourceCode[index:]
                    self.numberOfCurrentColumn = self.numberOfCurrentColumn + index
                    return tk, slicedSourceCode
            except IndexError:
                return None
            else:
                return None
    

    def getIdToken(self, sourceCode):
        letters = self.uppercaseLetters + self.lowercaseLetters + self.specialUpperCases + self.specialLowerCases
        lettersAndDigits = letters + self.naturalDigits
        try:
            if sourceCode[0] not in letters:
                return None
            index = 0
            for i in range(len(sourceCode)):
                if sourceCode[i] in lettersAndDigits:
                    index = i
                else:
                    index = index + 1
                    tokentype = TokenType.IDENTIFICATOR.value
                    tokenval = TokenVal.IDENTIFICATOR.value
                    lexeme = sourceCode[0:index]
                    currentLine = self.getCurrentLine(sourceCode)
                    numberOfCurrentLine = self.numberOfCurrentLine
                    numberOfCurrentColumn = self.numberOfCurrentColumn
                    tk = token(tokentype.value, tokenval.value, lexeme, numberOfCurrentLine, numberOfCurrentColumn,currentLine) 
                    slicedSourceCode = sourceCode[index:]
                    self.numberOfCurrentColumn = self.numberOfCurrentColumn + index
                    return tk, slicedSourceCode            
        except IndexError:
            return None
    
   

    def getScientificNotationToken(self, sourceCode):
        fixedNumberOfCurrentColumn = copy.deepcopy(self.numberOfCurrentColumn)
        try:
            if self.getFloatNumberToken(sourceCode) != None:
                floatTK = self.getFloatNumberToken(sourceCode)[0]
                index = len(floatTK.lexeme)
                if sourceCode[index] == 'e' or sourceCode[index] == 'E':
                    index = index + 1
                    if sourceCode[index] == "+" or sourceCode[index] == "-":
                        index = index + 1
                
                    if self.getFloatNumberToken(sourceCode[index:]) != None:
                        floatTK = self.getFloatNumberToken(sourceCode[index:])[0]
                        totalIndex = index + len(floatTK.lexeme)
                        tokenval = TokenVal.SCIENTIFIC_NOTATION.value
                        tokentype = TokenType.SCIENTIFIC_NOTATION.value
                        numberOfCurrentLine = self.numberOfCurrentLine
                        lexeme = sourceCode[0:totalIndex]
                        numberOfCurrentColumn = fixedNumberOfCurrentColumn + len(lexeme)
                        currentLine = self.getCurrentLine(sourceCode)
                        tk = token(tokentype, tokenval, lexeme, numberOfCurrentLine, numberOfCurrentColumn, currentLine)
                        slicedSourceCode = sourceCode[totalIndex:]
                        self.numberOfCurrentColumn = fixedNumberOfCurrentColumn + totalIndex
                        return tk, slicedSourceCode
                    elif self.getIntegerNumberToken(sourceCode[index:]) != None:
                        intTK = self.getIntegerNumberToken(sourceCode[index:])[0]
                        totalIndex = index + len(intTK.lexeme)
                        tokenval = TokenVal.SCIENTIFIC_NOTATION.value
                        tokentype = TokenType.SCIENTIFIC_NOTATION.value
                        numberOfCurrentLine = self.numberOfCurrentLine
                        lexeme = sourceCode[0:totalIndex]
                        numberOfCurrentColumn = fixedNumberOfCurrentColumn + len(lexeme)
                        currentLine = self.getCurrentLine(sourceCode)
                        tk = token(tokentype, tokenval, lexeme, numberOfCurrentLine, numberOfCurrentColumn, currentLine)
                        slicedSourceCode = sourceCode[totalIndex:]
                        self.numberOfCurrentColumn = fixedNumberOfCurrentColumn + totalIndex
                        return tk, slicedSourceCode

            elif self.getIntegerNumberToken(sourceCode) != None:
                intTK = self.getIntegerNumberToken(sourceCode)[0]
                index = len(intTK.lexeme)
                if sourceCode[index] == 'e' or sourceCode[index] == 'E':
                    index = index + 1
                    if sourceCode[index] == "+" or sourceCode[index] == "-":
                        index = index + 1
                
                    if self.getFloatNumberToken(sourceCode[index:]) != None:
                        floatTK = self.getFloatNumberToken(sourceCode[index:])[0]
                        totalIndex = index + len(floatTK.lexeme)
                        tokenval = TokenVal.SCIENTIFIC_NOTATION.value
                        tokentype = TokenType.SCIENTIFIC_NOTATION.value
                        numberOfCurrentLine = self.numberOfCurrentLine
                        lexeme = sourceCode[0:totalIndex]
                        numberOfCurrentColumn = fixedNumberOfCurrentColumn + len(lexeme)
                        currentLine = self.getCurrentLine(sourceCode)
                        tk = token(tokentype, tokenval, lexeme, numberOfCurrentLine, numberOfCurrentColumn, currentLine)
                        slicedSourceCode = sourceCode[totalIndex:]
                        self.numberOfCurrentColumn = fixedNumberOfCurrentColumn + totalIndex
                        return tk, slicedSourceCode
                    elif self.getIntegerNumberToken(sourceCode[index:]) != None:
                        intTK = self.getIntegerNumberToken(sourceCode[index:])[0]
                        totalIndex = index + len(intTK.lexeme)
                        tokenval = TokenVal.SCIENTIFIC_NOTATION.value
                        tokentype = TokenType.SCIENTIFIC_NOTATION.value
                        numberOfCurrentLine = self.numberOfCurrentLine
                        lexeme = sourceCode[0:totalIndex]
                        numberOfCurrentColumn = fixedNumberOfCurrentColumn + len(lexeme)
                        currentLine = self.getCurrentLine(sourceCode)
                        tk = token(tokentype, tokenval, lexeme, numberOfCurrentLine, numberOfCurrentColumn, currentLine)
                        slicedSourceCode = sourceCode[totalIndex:]
                        self.numberOfCurrentColumn = fixedNumberOfCurrentColumn + totalIndex
                        return tk, slicedSourceCode
            else:
                return None
        except IndexError:
            return None
        
   

    def getTokenProcess(self, sourceCode):
        if self.__isElseLexeme__(sourceCode):
            return self.getElseToken(sourceCode)

        elif self.__isIFLexeme__(sourceCode):
            return self.getIfToken(sourceCode)

        elif self.__isThenLexeme__(sourceCode):
            return self.getThenToken(sourceCode)

        elif self.__isEndLexeme__(sourceCode):
            return self.getEndToken(sourceCode)

        elif self.__isForLexeme__(sourceCode):
            return self.getForToken(sourceCode)

        elif self.__isUntilLexeme__(sourceCode):
            return self.getUntilToken(sourceCode)

        elif self.__isFloatTypeLexeme__(sourceCode):
            return self.getFloatTypeToken(sourceCode)

        elif self.__isReturnLexeme__(sourceCode):
            return self.getFloatTypeToken(sourceCode)

        elif self.__isReadLexeme__(sourceCode):
            return self.getReadToken(sourceCode)

        elif self.__isWriteLexeme__(sourceCode):
            return self.getWriteToken(sourceCode)
        
        elif self.__isIntegerTypeLexeme__(sourceCode):
            return self.getIntegerTypeToken(sourceCode)
        
        elif self.__isPlusLexeme__(sourceCode):
            return self.getPlusToken(sourceCode)
        
        elif self.__isMinusLexeme__(sourceCode):
            return self.getMinusToken(sourceCode)
        
        elif self.__isTimesLexeme__(sourceCode):
            return self.getTimesToken(sourceCode)

        elif self.__isDivisionLexeme__(sourceCode):
            return self.getDivisionToken(sourceCode)
        
        elif self.__isAssignmentLexeme__(sourceCode):
            return self.getAssignmentToken(sourceCode)
        
        elif self.__isEqualityLexeme__(sourceCode):
            return self.getLogicEqualsToken(sourceCode)
        
        elif self.__isCommaLexeme__(sourceCode):
            return self.getCommaToken(sourceCode)
        
        elif self.__isAssignmentLexeme__(sourceCode):
            return self.getAssignmentToken(sourceCode)
        
        elif self.__isTwoDotsLexeme_(sourceCode):
            return self.getTwoDotsToken(sourceCode)
        
        elif self.__isLessEqualsLexeme__(sourceCode):
            return self.getLessEqualsToken(sourceCode)
        
        elif self.__isLessLexeme__(sourceCode):
            return self.getLessToken(sourceCode)
        
        elif self.__isHigherEqualsLexeme__(sourceCode):
            return self.getHigherEqualsToken(sourceCode)
        
        elif self.__isHigherLexeme__(sourceCode):
            return self.getHigherToken(sourceCode)
        
        elif self.__isOPenParenthesesLexeme__(sourceCode):
            return self.getOpenParethesesToken(sourceCode)
        
        elif self.__isCloseParenthesesLexeme__(sourceCode):
            return self.getCloseParenthesesToken(sourceCode)
        
        elif self.__isOpenBracketsLexeme__(sourceCode):
            return self.getOpenBracketsToken(sourceCode)
        
        elif self.__isCloseBracketsLexeme__(sourceCode):
            return self.getCloseBracketsToken(sourceCode)
        
        elif self.__isLogicAndLexeme__(sourceCode):
            return self.getLogicAndToken(sourceCode)
        
        elif self.__isLogicOrLexeme__(sourceCode):
            return self.getLogicOrToken(sourceCode)
        
        elif self.__isNotLexeme__(sourceCode):
            return self.getLogicNotToken(sourceCode)
        
        elif self.__discardComment__(sourceCode) != None:
            self.__discardComment__(sourceCode)
        
        elif self.__discardSpace__(sourceCode) != None:
            self.__discardSpace__(sourceCode)
        
        elif self.__discardBreakLine__(sourceCode) != None:
            self.__discardBreakLine__(sourceCode)
        
        elif self.__isLetter__(sourceCode):
            return self.getIdToken(sourceCode)
        
        elif self.getScientificNotationToken(sourceCode) != None:
            return self.getScientificNotationToken(sourceCode)
        
        elif self.getFloatNumberToken(sourceCode) != None:
            return self.getFloatNumberToken(sourceCode)
        
        elif self.getIntegerNumberToken(sourceCode) != None:
            return self.getIntegerNumberToken(sourceCode)





        
    
    
    

    

    

            
