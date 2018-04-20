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
    

    def __isLogicOperator(self, token):
        tokenvalues = [TokenVal.LOGIC_AND.value, TokenVal.LOGIC_OR.value]
        return self.__isOperator(token, tokenvalues)


    def __isNotLogicOperator(self, token):
        return self.__isOperator(token, [TokenVal.LOGIC_NOT.value])


    def __isFactorExpressionStatement(self, tokenlist):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                index = 1
                isExpression = self.isExpression(tokenlist[index:])
                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        index = index + 1
                        return True, index
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    def __IsNegativeNumber(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.MINUS.value:
                index = 1
                token = tokenlist[index]
                if self.__isNumber(token):
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    def __isFactor(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isVar = self.__isVar(tokenlist)
            isNegativeNumber = self.__IsNegativeNumber(tokenlist)
            isFactorExpressionStatement = self.__isFactorExpressionStatement(tokenlist)
            if isFactorExpressionStatement[0]:
                return isFactorExpressionStatement

            elif isVar[0]:
                return isVar

            elif self.__isNumber(token):
                return True, 1
            
            elif isNegativeNumber[0]:
                print("deu")
                return isNegativeNumber

            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __isNotFactor(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isNot = self.__isNotLogicOperator(token)
            isFactor = self.__isFactor(tokenlist)
            if isNot:
                index = 1
                isFactor = self.__isFactor(tokenlist[index:])
                if isFactor[0]:
                    index = index + isFactor[1]
                    return True, index
                else:
                    return False, -1
            elif isFactor[0]:
                return isFactor
            else:
                return False, -1
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
            isNotFactor = self.__isNotFactor(tokenlist)
            token = tokenlist[0]
            isSumOperator = self.__isSumOperator(token)
            
            if isNotFactor[0]:
                return isNotFactor

            elif isSumOperator:
                isNotFactor = self.__isNotFactor(tokenlist[1:])
                if isNotFactor[0]:
                    return True, (1 + isNotFactor[1])
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
    

    def __isSimpleExpression(self, tokenlist=[]):
        try:
            isAdditiveExpression = self.__isAdditiveExpression(tokenlist)
            if isAdditiveExpression[0]:
                index = isAdditiveExpression[1]
                isSimpleStatement = self.__isSimpleStatement(tokenlist[index:])
                while isSimpleStatement[0]:
                    isSimpleStatement = self.__isSimpleStatement(tokenlist[index:])
                    if isSimpleStatement[0]:
                        index = index + isSimpleStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isSimpleStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isRelationalOperator = self.__isRelationalOperator(token)
            if isRelationalOperator:
                index = 1
                isAdditiveExpression = self.__isAdditiveExpression(tokenlist[index:])
                if isAdditiveExpression[0]:
                    return True, (index + isAdditiveExpression[1])
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isLogicStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isLogicOperator = self.__isLogicOperator(token)
            if isLogicOperator:
                index = 1
                isSimpleExpression = self.__isSimpleExpression(tokenlist[index:])
                if isSimpleExpression[0]:
                    return True, (index + isSimpleExpression[1])
                else:
                    return False, -1
            else:
                return False,-1
        except IndexError:
            return False, -1


    def __isLogicExpression(self, tokenlist=[]):
        try:
            isSimpleExpression = self.__isSimpleExpression(tokenlist)
            if isSimpleExpression[0]:
                index = isSimpleExpression[1]
                isLogicStatement = self.__isLogicStatement(tokenlist[index:])
                while isLogicStatement[0]:
                    isLogicStatement = self.__isLogicStatement(tokenlist[index:])
                    if isLogicStatement[0]:
                        index = index + isLogicStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1
    

      
    def isExpression(self, tokenlist=[]):
        try:
            isLogicExpression = self.__isLogicExpression(tokenlist)

            if isLogicExpression[0]:
                return isLogicExpression
            else:
                return False, -1
        except IndexError:
            return False, -1



