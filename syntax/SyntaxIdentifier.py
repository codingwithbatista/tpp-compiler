from lexical.structure.token.TokenVal import TokenVal


class syntax_recognizer(object):

    def __init__(self):
        pass
    

    def __isNumber(self,token):
        number = [TokenVal.SCIENTIFIC_NOTATION.value, TokenVal.FLOAT_NUMBER.value
        , TokenVal.INTEGER_NUMBER.value]

        return (token.tokenval in number)
    

    def __isOperator(self, token, tokenvalues=[]):
        return (token.tokenval in tokenvalues)

    
    def __isSumOperator(self, token):
        tokenvalues = [TokenVal.PLUS.value, TokenVal.MINUS.value]
        return self.__isOperator(token, tokenvalues)
    

    def __isTimesOperator(self, token):
        tokenvalues = [TokenVal.TIMES.value, TokenVal.DIVISION.value]
        return self.__isOperator(token, tokenvalues)
    

    def __isRelationalOperator(self, token):
        tokenvalues = [TokenVal.HIGHER.value, TokenVal.LESS.value,
        TokenVal.HIGHER_EQUALS.value, TokenVal.LESS_EQUALS.value, TokenVal.LOGIC_EQUALS.value]
        return self.__isOperator(token, tokenvalues)
    

    def __isFactor(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isVar = self.__isVar(tokenlist)
            if isVar[0]:
                return isVar
            elif self.__isNumber(token):
                return True, 1
        except IndexError:
            return False, -1
    

    def __isVar(self, tokenlist=[]):
        token = tokenlist[0]
        if token.tokenval == TokenVal.IDENTIFICATOR.value:
            return True, 1
        else:
            return False, -1
        
    

    def __isUnaryExpression(self, tokenlist=[]):
        try:
            isFactor = self.__isFactor(tokenlist)
            token = tokenlist[0]
            isSumOperator = self.__isSumOperator(token)
            
            if isFactor[0]:
                return isFactor

            elif isSumOperator:
                isFactor = self.__isFactor(tokenlist[1:])
                if isFactor[0]:
                    return True, (1 + isFactor[1])
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __isMultiplicativeExpression(self, tokenlist=[]):
        try:
            isUnaryExpression = self.__isUnaryExpression(tokenlist)

            if isUnaryExpression[0]:
                index = isUnaryExpression[1]
                isMultiplicativeStatement = self.__isMultiplicativeStatement(tokenlist[index:])
                while isMultiplicativeStatement[0]:
                    isMultiplicativeStatement = self.__isMultiplicativeStatement(tokenlist[index:])
                    if isMultiplicativeStatement[0]:
                        index = index + isMultiplicativeStatement[1]
                return True, index
            else:
                return False, -1
                
        except IndexError:
            return False, -1
    

    def __isMultiplicativeStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if self.__isTimesOperator(token):
                isUnaryExpression = self.__isUnaryExpression(tokenlist[1:])
                if isUnaryExpression[0]:
                    return True, (isUnaryExpression[1] + 1)
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def __isAdditiveExpression(self, tokenlist=[]):
        try:
            isMultiplicativeExpression = self.__isMultiplicativeExpression(tokenlist)
            if isMultiplicativeExpression[0]:
                index = isMultiplicativeExpression[1]
                isAdditiveStatement = self.__isAdditiveStatement(tokenlist[index:])
                while isAdditiveStatement[0]:
                    isAdditiveStatement = self.__isAdditiveStatement(tokenlist[index:])
                    if isAdditiveStatement[0]:
                        index = index + isAdditiveStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isAdditiveStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isSumOperator = self.__isSumOperator(token)

            if isSumOperator:
                isMultiplicativeExpression = self.__isMultiplicativeExpression(tokenlist[1:])
                if isMultiplicativeExpression[0]:
                    return True, (1 + isMultiplicativeExpression[1])
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1