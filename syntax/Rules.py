from lexical.structure.token.Token import token
from lexical.structure.token.TokenType import TokenType
from lexical.structure.token.TokenVal import TokenVal


class syntax_rule(object):


    
    def isNumber(self,token):
        number = [TokenVal.SCIENTIFIC_NOTATION.value, TokenVal.FLOAT_NUMBER.value
        , TokenVal.INTEGER_NUMBER.value]

        return (token.tokenval in number)
    

    def isOperator(self, token, tokenvalues=[]):
        return (token.tokenval in tokenvalues)

    
    def isSumOperator(self, token):
        tokenvalues = [TokenVal.PLUS.value, TokenVal.MINUS.value]
        return self.isOperator(token, tokenvalues)
    

    def isTimesOperator(self, token):
        tokenvalues = [TokenVal.TIMES.value, TokenVal.DIVISION.value]
        return self.isOperator(token, tokenvalues)
    

    def isRelationalOperator(self, token):
        tokenvalues = [TokenVal.HIGHER.value, TokenVal.LESS.value,
        TokenVal.HIGHER_EQUALS.value, TokenVal.LESS_EQUALS.value, TokenVal.LOGIC_EQUALS.value]
        return self.isOperator(token, tokenvalues)
    

    def isLogicOperator(self, token):
        tokenvalues = [TokenVal.LOGIC_AND.value, TokenVal.LOGIC_OR.value]
        return self.isOperator(token, tokenvalues)


    def isNotLogicOperator(self, token):
        return self.isOperator(token, [TokenVal.LOGIC_NOT.value])


    def isFactorExpressionStatement(self, tokenlist):
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


    def IsNegativeNumber(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.MINUS.value:
                index = 1
                token = tokenlist[index]
                if self.isNumber(token):
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isPositiveNumber(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.PLUS.value:
                index = 1
                token = tokenlist[index]
                if self.isNumber(token):
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isFactor(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isVar = self.isVar(tokenlist)
            isNegativeNumber = self.IsNegativeNumber(tokenlist)
            isPositiveNumber = self.isPositiveNumber(tokenlist)
            isFactorExpressionStatement = self.isFactorExpressionStatement(tokenlist)
            isCallFunction = self.isCallFunction(tokenlist)
                    
            if isFactorExpressionStatement[0]:
                return isFactorExpressionStatement

            elif isCallFunction[0]:
                return isCallFunction

            elif isVar[0]:
                return isVar

            elif self.isNumber(token):
                return True, 1
            
            elif isNegativeNumber[0]:
                return isNegativeNumber

            elif isPositiveNumber[0]:
                return isPositiveNumber
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isNotFactor(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isNot = self.isNotLogicOperator(token)
            isFactor = self.isFactor(tokenlist)
            if isNot:
                index = 1
                isFactor = self.isFactor(tokenlist[index:])
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

    
    def isVarIndexStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]

            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = 1
                isIndex = self.isIndex(tokenlist[index:])
                if isIndex[0]:
                    index = index + isIndex[1]
                    return True, index
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isNegativeVarStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.MINUS.value:
                token = tokenlist[1]
                if token.tokenval == TokenVal.IDENTIFICATOR.value:
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    def isVar(self, tokenlist=[]):
        token = tokenlist[0]
        isVarIndexStatement = self.isVarIndexStatement(tokenlist)
        isNegativeVar = self.isNegativeVarStatement(tokenlist)
        if isVarIndexStatement[0]:
            return isVarIndexStatement
        
        elif token.tokenval == TokenVal.IDENTIFICATOR.value:
            return True, 1
        
        elif isNegativeVar[0]:
            return isNegativeVar

        else:
            return False, -1
    

    def isUnaryExpression(self, tokenlist=[]):
        try:
            isNotFactor = self.isNotFactor(tokenlist)
            token = tokenlist[0]
            isSumOperator = self.isSumOperator(token)
            
            if isNotFactor[0]:
                return isNotFactor

            elif isSumOperator:
                isNotFactor = self.isNotFactor(tokenlist[1:])
                if isNotFactor[0]:
                    return True, (1 + isNotFactor[1])
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isMultiplicativeExpression(self, tokenlist=[]):
        try:
            isUnaryExpression = self.isUnaryExpression(tokenlist)

            if isUnaryExpression[0]:
                index = isUnaryExpression[1]
                isMultiplicativeStatement = self.isMultiplicativeStatement(tokenlist[index:])
                while isMultiplicativeStatement[0]:
                    isMultiplicativeStatement = self.isMultiplicativeStatement(tokenlist[index:])
                    if isMultiplicativeStatement[0]:
                        index = index + isMultiplicativeStatement[1]
                return True, index
            else:
                return False, -1
                
        except IndexError:
            return False, -1
    

    def isMultiplicativeStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if self.isTimesOperator(token):
                isUnaryExpression = self.isUnaryExpression(tokenlist[1:])
                if isUnaryExpression[0]:
                    return True, (isUnaryExpression[1] + 1)
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def isAdditiveExpression(self, tokenlist=[]):
        try:
            isMultiplicativeExpression = self.isMultiplicativeExpression(tokenlist)
            if isMultiplicativeExpression[0]:
                index = isMultiplicativeExpression[1]
                isAdditiveStatement = self.isAdditiveStatement(tokenlist[index:])
                while isAdditiveStatement[0]:
                    isAdditiveStatement = self.isAdditiveStatement(tokenlist[index:])
                    if isAdditiveStatement[0]:
                        index = index + isAdditiveStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isAdditiveStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isSumOperator = self.isSumOperator(token)

            if isSumOperator:
                isMultiplicativeExpression = self.isMultiplicativeExpression(tokenlist[1:])
                if isMultiplicativeExpression[0]:
                    return True, (1 + isMultiplicativeExpression[1])
                else:
                    
                    

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isSimpleExpression(self, tokenlist=[]):
        try:
            isAdditiveExpression = self.isAdditiveExpression(tokenlist)
            if isAdditiveExpression[0]:
                index = isAdditiveExpression[1]
                isSimpleStatement = self.isSimpleStatement(tokenlist[index:])
                while isSimpleStatement[0]:
                    isSimpleStatement = self.isSimpleStatement(tokenlist[index:])
                    if isSimpleStatement[0]:
                        index = index + isSimpleStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isSimpleStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isRelationalOperator = self.isRelationalOperator(token)
            if isRelationalOperator:
                index = 1
                isAdditiveExpression = self.isAdditiveExpression(tokenlist[index:])
                if isAdditiveExpression[0]:
                    return True, (index + isAdditiveExpression[1])
                else:
                    
                    

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isLogicStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            isLogicOperator = self.isLogicOperator(token)
            if isLogicOperator:
                index = 1
                isSimpleExpression = self.isSimpleExpression(tokenlist[index:])
                if isSimpleExpression[0]:
                    return True, (index + isSimpleExpression[1])
                else:
                    
                    

                    return False, -1
            else:
                return False,-1
        except IndexError:
            return False, -1


    def isLogicExpression(self, tokenlist=[]):
        try:
            isSimpleExpression = self.isSimpleExpression(tokenlist)
            if isSimpleExpression[0]:
                index = isSimpleExpression[1]
                isLogicStatement = self.isLogicStatement(tokenlist[index:])
                while isLogicStatement[0]:
                    isLogicStatement = self.isLogicStatement(tokenlist[index:])
                    if isLogicStatement[0]:
                        index = index + isLogicStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    
    def isExpression(self, tokenlist=[]):
        try:
            isLogicExpression = self.isLogicExpression(tokenlist)
            isAssignment = self.isAssignment(tokenlist)

            if isAssignment[0]:
                return isAssignment

            elif isLogicExpression[0]:
                return isLogicExpression

            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def isIndex(self, tokenlist=[]):
        try:
            isIndexStatement = self.isIndexStatement(tokenlist)
            index = 0
            if isIndexStatement[0]:
                while isIndexStatement[0]:
                    isIndexStatement = self.isIndexStatement(tokenlist[index:])
                    if isIndexStatement[0]:
                        index = index + isIndexStatement[1]
                
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    
    # feito levantamento de erros
    def isIndexStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                index = 1
                isExpression = self.isExpression(tokenlist[index:])
                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        index = index + 1
                        return True, index
                    else:

                            

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def isAssignment(self, tokenlist=[]):
        try:
            isVar = self.isVar(tokenlist)

            if isVar[0]:
                index = isVar[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.ASSIGNMENT.value:
                    index = index + 1
                    isExpression = self.isExpression(tokenlist[index:])
                    if isExpression[0]:
                        index = index + isExpression[1]
                        return True, index
                    else:

                            

                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def isRead(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.READ.value:
                index = 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = 2
                    isVar = self.isVar(tokenlist[index:])
                    if isVar[0]:
                        index = index + isVar[1]
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
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def isWrite(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.WRITE.value:
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
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
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def isReturn(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.RETURN.value:
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
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
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isArgumentStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.COMMA.value:
                index = 1
                isExpression = self.isExpression(tokenlist[index:])
                if isExpression[0]:
                    index = index + isExpression[1]
                    return True, index
                else:
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    def isArgumentList(self, tokenlist=[]):
        try:
            isExpression = self.isExpression(tokenlist)
            if isExpression[0]:
                index = isExpression[1]
                isArgumentStatement = self.isArgumentStatement(tokenlist[index:])

                if isArgumentStatement[0]:
                    while isArgumentStatement[0]:
                        isArgumentStatement = self.isArgumentStatement(tokenlist[index:])
                        if isArgumentStatement[0]:
                            index = index + isArgumentStatement[1]
                    return True, index
                else:
                    return isExpression
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    
    def isCallFunctionWithoutArgumentsStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
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
        except IndexError:
            return False, -1


    def isCallFunctionWithArgumentsStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isArgumentList = self.isArgumentList(tokenlist[index:])
                    if isArgumentList[0]:
                        index = index + isArgumentList[1]
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
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isCallFunction(self, tokenlist=[]):
        try:
            isCallFunctionWithoutArgumentsStatement = self.isCallFunctionWithoutArgumentsStatement(tokenlist)
            if isCallFunctionWithoutArgumentsStatement[0]:
                return isCallFunctionWithoutArgumentsStatement
              
            isCallFunctionWithArgumentsStatement = self.isCallFunctionWithArgumentsStatement(tokenlist)
            
            if isCallFunctionWithArgumentsStatement[0]:
                return isCallFunctionWithArgumentsStatement
            
            else:
                return False, -1
        except:
            return False, -1
    
    # foi realizado o levantamento de erros
    def isVarListStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.COMMA.value:
                index = index + 1
                isVar = self.isVar(tokenlist[index:])
                if isVar[0]:
                    index = index + isVar[1]
                    return True, index
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # foi realizado o levantamento de erros
    def isVarList(self, tokenlist=[]):
        try:
            isVar = self.isVar(tokenlist)
            if isVar[0]:
                index = isVar[1]
                isVarListStatement = self.isVarListStatement(tokenlist[index:])
                while isVarListStatement[0]:
                    isVarListStatement = self.isVarListStatement(tokenlist[index:])
                    if isVarListStatement[0]:
                        index = index + isVarListStatement[1]

                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def isVarDeclare(self, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]

            if token.tokenval in types:
                index = index + 1
                token = tokenlist[index]
                
                if token.tokenval == TokenVal.TWO_DOTS.value:
                    index = index + 1
                    isVarList = self.isVarList(tokenlist[index:])
                    if isVarList[0]:
                        index = index + isVarList[1]
                        return True, index
                    else:

                            

                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1

        except:
            return False, -1
    

    def isAction(self, tokenlist=[]):
        try:
            isVarDeclare = self.isVarDeclare(tokenlist)
            if isVarDeclare[0]:
                return isVarDeclare
            
            isRead = self.isRead(tokenlist)
            if isRead[0]:
                return isRead
            
            isWrite = self.isWrite(tokenlist)
            if isWrite[0]:
                return isWrite
            
            isReturn = self.isReturn(tokenlist)
            if isReturn[0]:
                return isReturn
            
            isConditional = self.isConditional(tokenlist)
            if isConditional[0]:
                return isConditional
            
            isRepeat = self.isRepeat(tokenlist)
            if isRepeat[0]:
                return isRepeat

            isExpression = self.isExpression(tokenlist)
            if isExpression[0]:
                return isExpression

            #self.errorHandler.errorActionStatement()
            return False, -1
        except IndexError:
            return False, -1
    

    def isBody(self, tokenlist=[]):
        try:
            isAction = self.isAction(tokenlist)
            if isAction[0]:
                index = isAction[1]
                while isAction[0]:
                    isAction = self.isAction(tokenlist[index:])
                    if isAction[0]:
                        index = index + isAction[1]
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    

    def isFirstConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.THEN.value:
                        index = index + 1
                        isBody = self.isBody(tokenlist[index:])
                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]
                            if token.tokenval == TokenVal.END.value:
                                index = index + 1
                                return True, index
                            else:
                                return False, -1
                        else:
                            
                            return False, -1
                    else:

                                

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isSecondConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.THEN.value:
                        
                        index = index + 1
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.END.value:
                            index = index + 1
                            return True, index
                        else:
                            return False, -1
                    else:

                                

                        return False, -1
                else:

                        

                    return False, -1

            else:
                return False, -1
        except:
            return False, -1


    def isThirdConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            
            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        index = index + 1
                        isBody = self.isBody(tokenlist[index:])
                        
                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.ELSE.value:
                                index = index + 1
                                isBody = self.isBody(tokenlist[index:])

                                if isBody[0]:
                                    index = index + isBody[1]
                                    token = tokenlist[index]

                                    if token.tokenval == TokenVal.END.value:
                                        index = index + 1
                                        return True, index
                                    else:
                                        return False, -1
                                else:
                                    return False, -1
                            else:
                                return False, -1
                        else:
                            return False, -1
                    else:

                                

                        return False, -1
                else: 

                        

                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    def isFourthConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.ELSE.value:
                            index = index + 1
                            isBody = self.isBody(tokenlist[index:])

                            if isBody[0]:
                                index = index + isBody[1]
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    index = index + 1
                                    return True, index
                                
                                else:
                                    return False, -1
                            else:
                                return False, -1
                        else:
                            return False, -1
                    else:

                                

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isFifthConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            
            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        index = index + 1
                        isBody = self.isBody(tokenlist[index:])

                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.ELSE.value:
                                index = index + 1
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    index = index + 1
                                    return True, index
                                else:
                                    return False, -1
                            else:
                                return False, -1
                        else:
                            return False, -1
                    else:

                                

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def isSixthConditionalStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.IF.value:
                index = index + 1
                isExpression = self.isExpression(tokenlist[index:])

                if isExpression[0]:
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.ELSE.value:
                            index = index + 1
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                index = index + 1
                                return True, index
                            else:
                            
                                return False, -1
                        else:
                            return False, -1
                    else:

                                

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

   
    def isConditional(self, tokenlist):
          
        try:
            isFirstConditionalStatement = self.isFirstConditionalStatement(tokenlist)
            if isFirstConditionalStatement[0]:
                return isFirstConditionalStatement
            
            isSecondConditionalStatement = self.isSecondConditionalStatement(tokenlist)
            if isSecondConditionalStatement[0]:
                return isSecondConditionalStatement
            
            isThirdConditionalStatement = self.isThirdConditionalStatement(tokenlist)
            if isThirdConditionalStatement[0]:
                return isThirdConditionalStatement

            isFourthConditionalStatement = self.isFourthConditionalStatement(tokenlist)
            if isFourthConditionalStatement[0]:
                return isFourthConditionalStatement

            isFifthConditionalStatement = self.isFifthConditionalStatement(tokenlist)
            if isFifthConditionalStatement[0]:
                return isFifthConditionalStatement
            
            isSixthConditionalStatement = self.isSixthConditionalStatement(tokenlist)
            if isSixthConditionalStatement[0]:
                return isSixthConditionalStatement
            

            return False, -1
        except IndexError:
            return False, -1



    
    # foi realizado levantamento de erros
    def isRepeatWithBodyStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.FOR.value:
                index = index + 1
                isBody = self.isBody(tokenlist[index:])

                if isBody[0]:
                    index = index + isBody[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.UNTIL.value:
                        index = index + 1
                        isExpression = self.isExpression(tokenlist[index:])

                        if isExpression[0]:
                            index = index + isExpression[1]
                            return True, index
                        else:


                                

                            return False, -1
                            
                    else:

                            

                        return False, -1
                else:

                        

                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    # foi realizado levantamento de erros
    def isRepeatWithoutBodyStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.FOR.value:
                index = index + 1
                token = tokenlist[index]
                
                if token.tokenval == TokenVal.UNTIL.value:
                    index = index + 1
                    isExpression = self.isExpression(tokenlist[index:])
                    
                    if isExpression[0]:
                        index = index + isExpression[1]
                        return True, index
                    else:

                            

                        return False, -1
                else:

                        
                        

                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    # foi realizado levantamento de erros
    def isRepeat(self, tokenlist=[]):
        try:
            isRepeatWithBodyStatement = self.isRepeatWithBodyStatement(tokenlist)

            if isRepeatWithBodyStatement[0]:
                return isRepeatWithBodyStatement
            
            isRepeatWithoutBodyStatement = self.isRepeatWithoutBodyStatement(tokenlist)

            if isRepeatWithoutBodyStatement[0]:
                return isRepeatWithoutBodyStatement
            return False, -1
        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def isParameterStatement(self, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]

            if token.tokenval in types:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.TWO_DOTS.value:
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.IDENTIFICATOR.value:
                        index = index + 1
                        return True, index
                    else:

                            

                        return False, -1
                else:
                    return False, -1
            else:
                return True, -1

        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def isUnidimensionalParameter(self, tokenlist=[]):
        try:
            isParameterStatement = self.isParameterStatement(tokenlist)
            index = 0
            if isParameterStatement[0]:
                index = index + isParameterStatement[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        index = index + 1
                        return True, index
                    else:

                            

                        return False, -1

                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    # foi realizado levantamento de erros
    def isBidimensionalParameter(self, tokenlist=[]):
        try:
            isUnidimensional = self.isUnidimensionalParameter(tokenlist)
            if isUnidimensional[0]:
                index = isUnidimensional[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        index = index + 1
                        return True, index
                    else:

                            

                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    # foi realizado levantamento de erros
    def isParameter(self, tokenlist=[]):
        try:
            isBidimensionalParameter = self.isBidimensionalParameter(tokenlist)
            if isBidimensionalParameter[0]:
                return isBidimensionalParameter

            isUnidimensionalParameter = self.isUnidimensionalParameter(tokenlist)
            if isUnidimensionalParameter[0]:
                return isUnidimensionalParameter
            
            isParameterStatement = self.isParameterStatement(tokenlist)
            if isParameterStatement[0]:
                return isParameterStatement
            
            return False, -1
        except:
            return False, -1
    
    # foi realizado levantamento de erros
    def isParameterListStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.COMMA.value:
                index = index + 1
                isParameter = self.isParameter(tokenlist[index:])
                if isParameter[0]:
                    index = index + isParameter[1]
                    return True, index
                else:

                        

                    return False, -1
            else:
                return False, -1
        except:
            return False, -1

    # foi realizado levantamento de erros
    def isParameterList(self, tokenlist=[]):
        try:
            isParameter = self.isParameter(tokenlist)
            if isParameter[0]:
                index = isParameter[1]
                isParameterStatement = self.isParameterStatement(tokenlist[index:])
                while isParameterStatement[0]:
                    isParameterStatement = self.isParameterListStatement(tokenlist[index:])
                    if isParameterStatement[0]:
                        index = index + isParameterStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def isFirstHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isParameterList = self.isParameterList(tokenlist[index:])

                    if isParameterList[0]:
                        index = index + isParameterList[1]
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            index = index + 1
                            isBody = self.isBody(tokenlist[index:])

                            if isBody[0]:
                                index = index + isBody[1]
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    index = index + 1
                                    return True, index
                                else:

                                        
                                        

                                    return False, -1
                            else:
                                return False, -1
                        else:
                            return False, -1
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isSecondHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        index = index + 1
                        isBody = self.isBody(tokenlist[index:])

                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                index = index + 1
                                return True, index
                            else:

                                    
                                    

                                return False, -1
                        else:
                            return False, -1
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isThirdHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isParameterList = self.isParameterList(tokenlist[index:])

                    if isParameterList[0]:
                        index = index + isParameterList[1]
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            index = index + 1
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                index = index + 1
                                return True, index
                            else:

                                    
                                    

                                return False, -1
                        else:
                            return False, -1
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1
    

    def isFourthHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.END.value:
                            index = index + 1
                            return True, index
                        else:

                                    
                                    

                            return False, -1
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isHeader(self, tokenlist=[]):
        try:
            isFirstHeaderStatement = self.isFirstHeaderStatement(tokenlist)
            if isFirstHeaderStatement[0]:
                return isFirstHeaderStatement
            
            isSecondHeaderStatement = self.isSecondHeaderStatement(tokenlist)
            if isSecondHeaderStatement[0]:
                return isSecondHeaderStatement

            isThirdHeaderStatement = self.isThirdHeaderStatement(tokenlist)
            if isThirdHeaderStatement[0]:
                return isThirdHeaderStatement
            
            isFourthHeaderStatement = self.isFourthHeaderStatement(tokenlist)
            if isFourthHeaderStatement[0]:
                return isFourthHeaderStatement
            
            return False, -1

        except IndexError:
            return False, -1


    def isFunctionDeclaration(self, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]
            isHeader = self.isHeader(tokenlist)
            if token.tokenval in types:
                index = index + 1
                isHeader = self.isHeader(tokenlist[index:])

                if isHeader[0]:
                    index = index + isHeader[1]
                    return True, index
                else:
                    return False, -1

            elif isHeader[0]:
                return isHeader

            else:
                return False, -1

        except IndexError:
            return False, -1
    
    # levantamento de erros realizado
    def isVarInitialization(self, tokenlist=[]):
        try:
            return self.isAssignment(tokenlist)
        except IndexError:
            return False, -1


    def isDeclaration(self, tokenlist=[]):
        try:
            isVarDeclare = self.isVarDeclare(tokenlist)
  
            if isVarDeclare[0]:
                
                return isVarDeclare

            isVarInitialization = self.isVarInitialization(tokenlist)
            if isVarInitialization[0]:

                return isVarInitialization
            
            isFunctionDeclaration = self.isFunctionDeclaration(tokenlist)
            if isFunctionDeclaration[0]:
                return isFunctionDeclaration
            
            return False, -1
        except IndexError:
            return False, -1
    

    def isDeclarationsList(self, tokenlist=[]):
        try:
            isDeclaration = self.isDeclaration(tokenlist)
            if isDeclaration[0]:
                index = isDeclaration[1]
                while isDeclaration[0]:
                    isDeclaration = self.isDeclaration(tokenlist[index:])
                    if isDeclaration[0]:
                        index = index + isDeclaration[1]
              

                return True, index
            
            else:
                return False, -1
        except IndexError:
            return False, -1