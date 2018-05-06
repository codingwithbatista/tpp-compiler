from lexical.structure.token.TokenVal import TokenVal
from lexical.structure.token.Token import token
from anytree import Node, RenderTree, PreOrderIter, Walker, Resolver

class syntax_scanner(object):

    def __init__(self):
        self.errorFound = False
        self.current_node = None
        
        

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
    

    def __isPositiveNumber(self, tokenlist=[]):
        try:
            token = tokenlist[0]
            if token.tokenval == TokenVal.PLUS.value:
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
            isVar = self.isVar(tokenlist)
            isNegativeNumber = self.__IsNegativeNumber(tokenlist)
            isPositiveNumber = self.__isPositiveNumber(tokenlist)
            isFactorExpressionStatement = self.__isFactorExpressionStatement(tokenlist)
            isCallFunction = self.__isCallFunction(tokenlist)
                    
            if isFactorExpressionStatement[0]:
                return isFactorExpressionStatement

            elif isCallFunction[0]:
                return isCallFunction

            elif isVar[0]:
                return isVar

            elif self.__isNumber(token):
                return True, 1
            
            elif isNegativeNumber[0]:
                return isNegativeNumber

            elif isPositiveNumber[0]:
                return isPositiveNumber
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

    
    def __isVarIndexStatement(self, tokenlist=[]):
        try:
            token = tokenlist[0]

            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = 1
                isIndex = self.__isIndex(tokenlist[index:])
                if isIndex[0]:
                    index = index + isIndex[1]
                    return True, index
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isNegativeVarStatement(self, tokenlist=[]):
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
        isVarIndexStatement = self.__isVarIndexStatement(tokenlist)
        isNegativeVar = self.__isNegativeVarStatement(tokenlist)
        if isVarIndexStatement[0]:
            return isVarIndexStatement
        
        elif token.tokenval == TokenVal.IDENTIFICATOR.value:
            return True, 1
        
        elif isNegativeVar[0]:
            return isNegativeVar

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
                    print("In line", token.getNumberOfLine())
                    print("Error in additive expression")
                    self.errorFound = True
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
                    print("In line", token.getNumberOfLine())
                    print("Erro in relational expression")
                    self.errorFound = True
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
                    print("In line", token.getNumberOfLine())
                    print("Error in logic expression statement")
                    self.errorFound = True
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
            isAssignment = self.__isAssignment(tokenlist)

            if isAssignment[0]:
                return isAssignment

            elif isLogicExpression[0]:
                return isLogicExpression

            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __isIndex(self, tokenlist=[]):
        try:
            isIndexStatement = self.__isIndexStatement(tokenlist)
            index = 0
            if isIndexStatement[0]:
                while isIndexStatement[0]:
                    isIndexStatement = self.__isIndexStatement(tokenlist[index:])
                    if isIndexStatement[0]:
                        index = index + isIndexStatement[1]
                
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    
    # feito levantamento de erros
    def __isIndexStatement(self, tokenlist=[]):
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
                        if self.errorFound == False:
                            self.__printErrorFound("]", token.tokenval, token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Index", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __isAssignment(self, tokenlist=[]):
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
                        if self.errorFound == False:
                            self.__printErrorStatement("Assignment", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __isRead(self, tokenlist=[]):
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
                            if self.errorFound == False:
                                self.__printErrorFound(")", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                            return False, -1
                    else:
                        if self.errorFound == False:
                            self.__printErrorStatement("Variable", token.getNumberOfLine())
                        self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorFound("(", token.tokenval, token.getNumberOfLine())
                    self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __isWrite(self, tokenlist=[]):
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
                            if self.errorFound == False:
                                self.__printErrorFound(")", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                            return False, -1
                    else:
                        if self.errorFound == False:
                            self.__printErrorStatement("Expression", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1                        
                else:
                    if self.errorFound == False:
                        self.__printErrorFound("(", token.tokenval, token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __isReturn(self, tokenlist=[]):
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
                            if self.errorFound == False:
                                self.__printErrorFound(")", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                            return False, -1
                    else:
                        if self.errorFound == False:
                            self.__printErrorStatement("Expression", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorFound("(", token.tokenval, token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isArgumentStatement(self, tokenlist=[]):
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


    def __isArgumentList(self, tokenlist=[]):
        try:
            isExpression = self.isExpression(tokenlist)
            if isExpression[0]:
                index = isExpression[1]
                isArgumentStatement = self.__isArgumentStatement(tokenlist[index:])

                if isArgumentStatement[0]:
                    while isArgumentStatement[0]:
                        isArgumentStatement = self.__isArgumentStatement(tokenlist[index:])
                        if isArgumentStatement[0]:
                            index = index + isArgumentStatement[1]
                    return True, index
                else:
                    return isExpression
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    
    def __isCallFunctionWithoutArgumentsStatement(self, tokenlist=[]):
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


    def __isCallFunctionWithArgumentsStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isArgumentList = self.__isArgumentList(tokenlist[index:])
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


    def __isCallFunction(self, tokenlist=[]):
        try:
            isCallFunctionWithoutArgumentsStatement = self.__isCallFunctionWithoutArgumentsStatement(tokenlist)
            if isCallFunctionWithoutArgumentsStatement[0]:
                return isCallFunctionWithoutArgumentsStatement
              
            isCallFunctionWithArgumentsStatement = self.__isCallFunctionWithArgumentsStatement(tokenlist)
            
            if isCallFunctionWithArgumentsStatement[0]:
                return isCallFunctionWithArgumentsStatement
            
            else:
                return False, -1
        except:
            return False, -1
    
    # foi realizado o levantamento de erros
    def __isVarListStatement(self, tokenlist=[]):
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
                    if self.errorFound == False:
                        self.__printErrorFound("ID", token.tokenval, token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    # foi realizado o levantamento de erros
    def __isVarList(self, tokenlist=[]):
        try:
            isVar = self.isVar(tokenlist)
            if isVar[0]:
                index = isVar[1]
                isVarListStatement = self.__isVarListStatement(tokenlist[index:])
                while isVarListStatement[0]:
                    isVarListStatement = self.__isVarListStatement(tokenlist[index:])
                    if isVarListStatement[0]:
                        index = index + isVarListStatement[1]

                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def __isVarDeclare(self, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]

            if token.tokenval in types:
                index = index + 1
                token = tokenlist[index]
                
                if token.tokenval == TokenVal.TWO_DOTS.value:
                    index = index + 1
                    isVarList = self.__isVarList(tokenlist[index:])
                    if isVarList[0]:
                        index = index + isVarList[1]
                        return True, index
                    else:
                        if self.errorFound == False:
                            self.__printErrorStatement("Variable declarion", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1

        except:
            return False, -1
    

    def __isAction(self, tokenlist=[]):
        try:
            isVarDeclare = self.__isVarDeclare(tokenlist)
            if isVarDeclare[0]:
                return isVarDeclare
            
            isRead = self.__isRead(tokenlist)
            if isRead[0]:
                return isRead
            
            isWrite = self.__isWrite(tokenlist)
            if isWrite[0]:
                return isWrite
            
            isReturn = self.__isReturn(tokenlist)
            if isReturn[0]:
                return isReturn
            
            isConditional = self.__isConditional(tokenlist)
            if isConditional[0]:
                return isConditional
            
            isRepeat = self.__isRepeat(tokenlist)
            if isRepeat[0]:
                return isRepeat

            isExpression = self.isExpression(tokenlist)
            if isExpression[0]:
                return isExpression

            #self.errorHandler.errorActionStatement()
            return False, -1
        except IndexError:
            return False, -1
    

    def __isBody(self, tokenlist=[]):
        try:
            isAction = self.__isAction(tokenlist)
            if isAction[0]:
                index = isAction[1]
                while isAction[0]:
                    isAction = self.__isAction(tokenlist[index:])
                    if isAction[0]:
                        index = index + isAction[1]
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    

    def __isFirstConditionalStatement(self, tokenlist=[]):
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
                        isBody = self.__isBody(tokenlist[index:])
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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isSecondConditionalStatement(self, tokenlist=[]):
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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True                        
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1

            else:
                return False, -1
        except:
            return False, -1


    def __isThirdConditionalStatement(self, tokenlist=[]):
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
                        isBody = self.__isBody(tokenlist[index:])
                        
                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.ELSE.value:
                                index = index + 1
                                isBody = self.__isBody(tokenlist[index:])

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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True                       
                        return False, -1
                else: 
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    def __isFourthConditionalStatement(self, tokenlist=[]):
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
                            isBody = self.__isBody(tokenlist[index:])

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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isFifthConditionalStatement(self, tokenlist=[]):
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
                        isBody = self.__isBody(tokenlist[index:])

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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __isSixthConditionalStatement(self, tokenlist=[]):
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
                        if self.errorFound == False:
                                self.__printErrorFound("então", token.tokenval, token.getNumberOfLine())
                                self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Conditional", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

   
    def __isConditional(self, tokenlist):
          
        try:
            isFirstConditionalStatement = self.__isFirstConditionalStatement(tokenlist)
            if isFirstConditionalStatement[0]:
                return isFirstConditionalStatement
            
            isSecondConditionalStatement = self.__isSecondConditionalStatement(tokenlist)
            if isSecondConditionalStatement[0]:
                return isSecondConditionalStatement
            
            isThirdConditionalStatement = self.__isThirdConditionalStatement(tokenlist)
            if isThirdConditionalStatement[0]:
                return isThirdConditionalStatement

            isFourthConditionalStatement = self.__isFourthConditionalStatement(tokenlist)
            if isFourthConditionalStatement[0]:
                return isFourthConditionalStatement

            isFifthConditionalStatement = self.__isFifthConditionalStatement(tokenlist)
            if isFifthConditionalStatement[0]:
                return isFifthConditionalStatement
            
            isSixthConditionalStatement = self.__isSixthConditionalStatement(tokenlist)
            if isSixthConditionalStatement[0]:
                return isSixthConditionalStatement
            

            return False, -1
        except IndexError:
            return False, -1



    
    # foi realizado levantamento de erros
    def __isRepeatWithBodyStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.FOR.value:
                index = index + 1
                isBody = self.__isBody(tokenlist[index:])

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

                            if self.errorFound == False:
                                self.__printErrorStatement("Repeat", token.getNumberOfLine())
                                self.errorFound = True
                            return False, -1
                            
                    else:
                        if self.errorFound == False:
                            self.__printErrorFound("até", token.tokenval, token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        self.__printErrorStatement("Body", token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    # foi realizado levantamento de erros
    def __isRepeatWithoutBodyStatement(self, tokenlist=[]):
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
                        if self.errorFound == False:
                            self.__printErrorStatement("Repeat", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    if self.errorFound == False:
                        print("aqui")
                        self.__printErrorFound("até", token.tokenval, token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    # foi realizado levantamento de erros
    def __isRepeat(self, tokenlist=[]):
        try:
            isRepeatWithBodyStatement = self.__isRepeatWithBodyStatement(tokenlist)

            if isRepeatWithBodyStatement[0]:
                return isRepeatWithBodyStatement
            
            isRepeatWithoutBodyStatement = self.__isRepeatWithoutBodyStatement(tokenlist)

            if isRepeatWithoutBodyStatement[0]:
                return isRepeatWithoutBodyStatement
            return False, -1
        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def __isParameterStatement(self, tokenlist=[]):
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
                        if self.errorFound == False:
                            self.__printErrorStatement("Parameter", token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    return False, -1
            else:
                return True, -1

        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def __isUnidimensionalParameter(self, tokenlist=[]):
        try:
            isParameterStatement = self.__isParameterStatement(tokenlist)
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
                        if self.errorFound == False:
                            self.__printErrorFound("]", token.tokenval, token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1

                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    # foi realizado levantamento de erros
    def __isBidimensionalParameter(self, tokenlist=[]):
        try:
            isUnidimensional = self.__isUnidimensionalParameter(tokenlist)
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
                        if self.errorFound == False:
                            self.__printErrorFound("]", token.tokenval, token.getNumberOfLine())
                            self.errorFound = True
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    # foi realizado levantamento de erros
    def __isParameter(self, tokenlist=[]):
        try:
            isBidimensionalParameter = self.__isBidimensionalParameter(tokenlist)
            if isBidimensionalParameter[0]:
                return isBidimensionalParameter

            isUnidimensionalParameter = self.__isUnidimensionalParameter(tokenlist)
            if isUnidimensionalParameter[0]:
                return isUnidimensionalParameter
            
            isParameterStatement = self.__isParameterStatement(tokenlist)
            if isParameterStatement[0]:
                return isParameterStatement
            
            return False, -1
        except:
            return False, -1
    
    # foi realizado levantamento de erros
    def __isParameterListStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.COMMA.value:
                index = index + 1
                isParameter = self.__isParameter(tokenlist[index:])
                if isParameter[0]:
                    index = index + isParameter[1]
                    return True, index
                else:
                    if self.errorFound == False:
                        self.__printErrorFound("TYPE", token.tokenval, token.getNumberOfLine())
                        self.errorFound = True
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1

    # foi realizado levantamento de erros
    def __isParameterList(self, tokenlist=[]):
        try:
            isParameter = self.__isParameter(tokenlist)
            if isParameter[0]:
                index = isParameter[1]
                isParameterStatement = self.__isParameterStatement(tokenlist[index:])
                while isParameterStatement[0]:
                    isParameterStatement = self.__isParameterListStatement(tokenlist[index:])
                    if isParameterStatement[0]:
                        index = index + isParameterStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def __isFirstHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isParameterList = self.__isParameterList(tokenlist[index:])

                    if isParameterList[0]:
                        index = index + isParameterList[1]
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            index = index + 1
                            isBody = self.__isBody(tokenlist[index:])

                            if isBody[0]:
                                index = index + isBody[1]
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    index = index + 1
                                    return True, index
                                else:
                                    if self.errorFound == False:
                                        print("Near the statement that begins near line", token.getNumberOfLine())
                                        print("The statement needs an END token")
                                        self.errorFound = True
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
    

    def __isSecondHeaderStatement(self, tokenlist=[]):
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
                        isBody = self.__isBody(tokenlist[index:])

                        if isBody[0]:
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                index = index + 1
                                return True, index
                            else:
                                if self.errorFound == False:
                                    print("Near the statement that begins near line", token.getNumberOfLine())
                                    print("The statement needs an END token")
                                    self.errorFound = True
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
    

    def __isThirdHeaderStatement(self, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    index = index + 1
                    isParameterList = self.__isParameterList(tokenlist[index:])

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
                                if self.errorFound == False:
                                    print("Near the statement that begins near line", token.getNumberOfLine())
                                    print("The statement needs an END token")
                                    self.errorFound = True
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
    

    def __isFourthHeaderStatement(self, tokenlist=[]):
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
                            if self.errorFound == False:
                                    print("Near the statement that begins near line", token.getNumberOfLine())
                                    print("The statement needs an END token")
                                    self.errorFound = True
                            return False, -1
                    else:
                        return False, -1
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __isHeader(self, tokenlist=[]):
        try:
            isFirstHeaderStatement = self.__isFirstHeaderStatement(tokenlist)
            if isFirstHeaderStatement[0]:
                return isFirstHeaderStatement
            
            isSecondHeaderStatement = self.__isSecondHeaderStatement(tokenlist)
            if isSecondHeaderStatement[0]:
                return isSecondHeaderStatement

            isThirdHeaderStatement = self.__isThirdHeaderStatement(tokenlist)
            if isThirdHeaderStatement[0]:
                return isThirdHeaderStatement
            
            isFourthHeaderStatement = self.__isFourthHeaderStatement(tokenlist)
            if isFourthHeaderStatement[0]:
                return isFourthHeaderStatement
            
            return False, -1

        except IndexError:
            return False, -1


    def __isFunctionDeclaration(self, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]
            isHeader = self.__isHeader(tokenlist)
            if token.tokenval in types:
                index = index + 1
                isHeader = self.__isHeader(tokenlist[index:])

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
    def __isVarInitialization(self, tokenlist=[]):
        try:
            return self.__isAssignment(tokenlist)
        except IndexError:
            return False, -1


    def __isDeclaration(self, tokenlist=[]):
        try:
            isVarDeclare = self.__isVarDeclare(tokenlist)
  
            if isVarDeclare[0]:
                
                Node("VAR_DECLARE", parent=self.current_node, tokenval="VAR_DECLARE")
                return isVarDeclare

            isVarInitialization = self.__isVarInitialization(tokenlist)
            if isVarInitialization[0]:
                Node("VAR_INITIALIZATION", parent=self.current_node, tokenval="VAR_INITIALIZATION")
                return isVarInitialization
            
            isFunctionDeclaration = self.__isFunctionDeclaration(tokenlist)
            if isFunctionDeclaration[0]:
                Node("FUNCTION_DECLARATION", parent=self, tokenval="FUNCTION_DECLARATION")
                return isFunctionDeclaration
            
            return False, -1
        except IndexError:
            return False, -1
    

    def __isDeclarationsList(self, tokenlist=[]):
        try:
            isDeclaration = self.__isDeclaration(tokenlist)
            if isDeclaration[0]:
                index = isDeclaration[1]
                while isDeclaration[0]:
                    isDeclaration = self.__isDeclaration(tokenlist[index:])
                    if isDeclaration[0]:
                        index = index + isDeclaration[1]
                
                Node("DECLARATION_LIST", tokenval="DECLARATION_LIST", parent=self.st)
              

                return True, index
            
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isAProgram(self, tokenlist=[]):
        self.st = Node("PROGRAM",parent=None,tokenval="PROGRAM")
        #print(RenderTree(self.st))
        return self.__isDeclarationsList(tokenlist)


    def __printErrorFound(self, expected=str, received=str, line=int):
        print("In line", line)
        print("Expected", expected, ", but got a ", received)

    
    def __printErrorStatement(self, statement=str, line=int):
        print("Near line", line,":")
        print("The ", statement, " statement got errors" )

class syntax_process(object):

    def exec(self, tokenlist=[]):
        sr = syntax_scanner()
        process = sr.isAProgram(tokenlist)
        if process[0] == True and (len(tokenlist) == int(process[1])):
            print("successfull syntactic check")
        
        elif(len(tokenlist) > process[1] and process[1] > 0 and sr.errorFound == False):
            line = tokenlist[process[1] + 1].getNumberOfLine()
            print("Error near the statement that begins near line", line)
            print("near the token", tokenlist[process[1]].tokenval)
        
        print(RenderTree(sr.st))
        print(sr.st.descendants[0])
        #r = Resolver("name")
        #print(r.get(sr.st,"DECLARATION_LIST"))