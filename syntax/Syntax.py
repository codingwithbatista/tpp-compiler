from lexical.structure.token.TokenVal import TokenVal
from lexical.structure.token.Token import token
from syntax.Rules import syntax_rule
from anytree import Node, RenderTree, PreOrderIter, Walker, Resolver
from anytree.dotexport import DotExporter

class syntax_scanner(object):

    def __init__(self):
        self.errorFound = False
        self.current_node = None
        self.sr = syntax_rule()
        
        

    def __consumeNumber(self,node, token):
        number = [TokenVal.SCIENTIFIC_NOTATION.value, TokenVal.FLOAT_NUMBER.value
        , TokenVal.INTEGER_NUMBER.value]
        Node("NUMBER", tokenval = token.tokenval, tokentype = token.tokentype, line = token.getNumberOfLine(),
        lexeme = token.lexeme, parent = node)
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


    def __consumeFactorExpressionStatement(self, node, tokenlist):
        try:
            factor_node = Node("FACTOR_EXPRESSION_STMT", tokenval = "FACTOR_EXPRESSION_STMT", parent = node)
            token = tokenlist[0]
            if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                Node("OPEN_PARENTHESES", parent = factor_node, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())    
                index = 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(factor_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        Node("CLOSE_PARENTHESES", parent = factor_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, line = token.getNumberOfLine(),
                        lexeme = token.lexeme)
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


    def __consumeNegativeNumber(self, node, tokenlist=[]):
        try:
            negative_node = Node("NEGATIVE_NUMBER", parent = node, tokenval = "NEGATIVE_NUMBER")
            token = tokenlist[0]
            if token.tokenval == TokenVal.MINUS.value:
                Node("MINUS", tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine(), parent = negative_node)
                index = 1
                token = tokenlist[index]
                if self.sr.isNumber(token):
                    self.__consumeNumber(negative_node, token)
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __consumePositiveNumber(self, node, tokenlist=[]):
        try:
            positive_node = Node("POSITIVE_NUMBER", parent = node, tokenval = "POSITIVE_NUMBER")
            token = tokenlist[0]
            if token.tokenval == TokenVal.PLUS.value:
                Node("PLUS", parent = positive_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = 1
                token = tokenlist[index]
                if self.sr.isNumber(token):
                    self.__consumeNumber(positive_node, token)
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __consumeFactor(self, node, tokenlist=[]):
        try:
            factor_node = Node("FACTOR", parent = node, tokenval = "FACTOR")
            token = tokenlist[0]
            isVar = self.sr.isVar(tokenlist)
            isNegativeNumber = self.sr.IsNegativeNumber(tokenlist)
            isPositiveNumber = self.sr.isPositiveNumber(tokenlist)
            isFactorExpressionStatement = self.sr.isFactorExpressionStatement(tokenlist)
            isCallFunction = self.sr.isCallFunction(tokenlist)
                    
            if isFactorExpressionStatement[0]:
                self.__consumeFactorExpressionStatement(factor_node, tokenlist)
                return isFactorExpressionStatement

            elif isCallFunction[0]:
                self.__consumeCallFunction(factor_node, tokenlist)
                return isCallFunction

            elif isVar[0]:
                self.__consumeVar(factor_node, tokenlist)
                return isVar

            elif self.sr.isNumber(token):
                self.__consumeNumber(factor_node, token)
                return True, 1
            
            elif isNegativeNumber[0]:
                self.__consumeNegativeNumber(factor_node, tokenlist)
                return isNegativeNumber

            elif isPositiveNumber[0]:
                self.__consumePositiveNumber(factor_node, tokenlist)
                return isPositiveNumber
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __consumeNotFactor(self, node, tokenlist=[]):
        try:
            factor_node = Node("NOT_FACTOR", tokenval = "NOT_FACTOR", parent = node)
            token = tokenlist[0]
            isNot = self.sr.isNotLogicOperator(token)
            isFactor = self.sr.isFactor(tokenlist)
            if isNot:
                Node("NOT", parent = factor_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                line = token.getNumberOfLine(), lexeme = token.lexeme)
                index = 1
                isFactor = self.sr.isFactor(tokenlist[index:])
                if isFactor[0]:
                    self.__consumeFactor(factor_node, tokenlist[index:])
                    index = index + isFactor[1]
                    return True, index
                else:
                    return False, -1
            elif isFactor[0]:
                self.__consumeFactor(factor_node, tokenlist)
                return isFactor
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def __isVarIndexStatement(self, node, tokenlist=[]):
        try:
            token = tokenlist[0]
            new_node = Node("VAR_INDEX_STMT", parent=node, tokenval="VAR_INDEX_STMT")
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                index = 1
                #isIndex = self.__isIndex(tokenlist[index:])
                isIndex = self.sr.isIndex(tokenlist[index:])
                if isIndex[0]:
                    self.__consumeIndex(new_node, tokenlist[index:])
                    index = index + isIndex[1]
                    
                    return True, index
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __consumeNegativeVarStatement(self, node, tokenlist=[]):
        try:
            negative_node  = Node("NEGATIVE_VAR", tokenval = "NEGATIVE_VAR", parent = node)
            token = tokenlist[0]
            if token.tokenval == TokenVal.MINUS.value:
                Node("MINUS", parent = negative_node, tokenval = token.tokenval, 
                tokentype = token.tokentype, lexeme = token.lexeme,
                line = token.getNumberOfLine())
                token = tokenlist[1]
                if token.tokenval == TokenVal.IDENTIFICATOR.value:
                    Node("ID", parent = negative_node, tokenval = token.tokenval, 
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    return True, 2
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    def __consumeVar(self, node, tokenlist=[]):
        token = tokenlist[0]
        var_node = Node("VAR", parent=node, tokenval = "VAR")
        #isVarIndexStatement = self.__isVarIndexStatement(tokenlist)
        #isNegativeVar = self.__isNegativeVarStatement(tokenlist)
        isVarIndexStatement = self.sr.isVarIndexStatement(tokenlist)
        isNegativeVar = self.sr.isNegativeVarStatement(tokenlist)
        if isVarIndexStatement[0]:
            self.__isVarIndexStatement(var_node, tokenlist)
            return isVarIndexStatement
        
        elif token.tokenval == TokenVal.IDENTIFICATOR.value:
            Node("ID", parent=var_node, tokenval = token.tokenval, tokentype = token.tokentype,
            lexeme = token.lexeme, line = token.getNumberOfLine())
            return True, 1
        
        elif isNegativeVar[0]:
            self.__consumeNegativeVarStatement(var_node, tokenlist)
            return isNegativeVar

        else:
            return False, -1
    

    def __consumeUnaryExpression(self, node, tokenlist=[]):
        try:
            #isNotFactor = self.__isNotFactor(tokenlist)
            isNotFactor = self.sr.isNotFactor(tokenlist)
            token = tokenlist[0]
            #isSumOperator = self.__isSumOperator(token)
            isSumOperator = self.sr.isSumOperator(token)
            unary_node = Node("UNARY_EXPRESSION", parent = node, tokenval = "UNARY_EXPRESSION")
            if isNotFactor[0]:
                self.__consumeNotFactor(unary_node, tokenlist)
                return isNotFactor

            elif isSumOperator:
                isNotFactor = self.sr.isNotFactor(tokenlist[1:])
                if isNotFactor[0]:
                    self.__consumeNotFactor(unary_node, tokenlist[1:])
                    return True, (1 + isNotFactor[1])
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def __consumeMultiplicativeExpression(self, node, tokenlist=[]):
        try:
            mult_node = Node("MULTUPLICATIVE_EXPRESSION_STMT", parent = node, tokenval = "MULTIPLICATIVE_EXPRESSION_STMT")
            #isUnaryExpression = self.__isUnaryExpression(tokenlist)
            isUnaryExpression = self.sr.isUnaryExpression(tokenlist)

            if isUnaryExpression[0]:
                self.__consumeUnaryExpression(mult_node, tokenlist)
                index = isUnaryExpression[1]
                #isMultiplicativeStatement = self.__isMultiplicativeStatement(tokenlist[index:])
                isMultiplicativeStatement = self.sr.isMultiplicativeStatement(tokenlist[index:])
                while isMultiplicativeStatement[0]:
                    #isMultiplicativeStatement = self.__isMultiplicativeStatement(tokenlist[index:])
                    isMultiplicativeStatement = self.sr.isMultiplicativeStatement(tokenlist[index:])
                    if isMultiplicativeStatement[0]:
                        self.__consumeMultiplicativeStatement(mult_node, tokenlist[index:])
                        index = index + isMultiplicativeStatement[1]
                return True, index
            else:
                return False, -1
                
        except IndexError:
            return False, -1
    

    def __consumeMultiplicativeStatement(self, node, tokenlist=[]):
        try:
            token = tokenlist[0]
            if self.sr.isTimesOperator(token):
                children_nodes = node.children
                operator_node = Node("TIMES_OPERATOR", tokenval = token.tokenval,
                tokentype = token.tokentype,
                line = token.getNumberOfLine(), lexeme = token.lexeme)
                for n in children_nodes:
                    n.parent = operator_node
                operator_node.parent = node
                isUnaryExpression = self.sr.isUnaryExpression(tokenlist[1:])
                if isUnaryExpression[0]:
                    self.__consumeUnaryExpression(operator_node, tokenlist[1:])
                    return True, (isUnaryExpression[1] + 1)
                else:
                    return False, -1
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def __consumeAdditiveExpression(self, node, tokenlist=[]):
        try:
            # bug está aqui
            
            add_node = Node("ADDITIVE_EXPRESSION_STMT", parent = node, tokenval = "ADDITIVE_EXPRESSION_STMT")
            isMultiplicativeExpression = self.sr.isMultiplicativeExpression(tokenlist)
            if isMultiplicativeExpression[0]:
                self.__consumeMultiplicativeExpression(add_node, tokenlist)
                index = isMultiplicativeExpression[1]
                isAdditiveStatement = self.sr.isAdditiveStatement(tokenlist[index:])
                while isAdditiveStatement[0]:
                    isAdditiveStatement = self.sr.isAdditiveStatement(tokenlist[index:])
                    if isAdditiveStatement[0]:
                        self.__consumeAdditiveStatement(add_node, tokenlist[index:])
                        index = index + isAdditiveStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __consumeAdditiveStatement(self, node, tokenlist=[]):
        try:
            # VENDO SE O BUG NÃO TA AQUI
            #print(node.tokenval)
            
            #children = node.children
            add_node = Node("ADDITIVE_STATEMENT", tokenval = "ADDITIVE_STATEMENT")
            #children.parent = add_node
            add_node.parent = node
            token = tokenlist[0]
            isSumOperator = self.sr.isSumOperator(token)
            
            if isSumOperator:
                sum_node = Node("SUM_OPERATOR", parent = add_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                for n in node.children:
                    if n.tokenval == "MULTIPLICATIVE_EXPRESSION_STMT":
                        n.parent = sum_node
                #print(n.tokenval)
                #isMultiplicativeExpression = self.__isMultiplicativeExpression(tokenlist[1:])
                isMultiplicativeExpression = self.sr.isMultiplicativeExpression(tokenlist[1:])
                if isMultiplicativeExpression[0]:
                    self.__consumeMultiplicativeExpression(sum_node, tokenlist[1:])
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
    

    def __consumeSimpleExpression(self, node, tokenlist=[]):
        try:
            simple_node = Node("SIMPLE_EXPRESSION_STMT", parent = node, tokenval = "SIMPLE_EXPRESSION_STMT")
            #isAdditiveExpression = self.__isAdditiveExpression(tokenlist)
            isAdditiveExpression = self.sr.isAdditiveExpression(tokenlist)
            if isAdditiveExpression[0]:
                self.__consumeAdditiveExpression(simple_node, tokenlist)
                index = isAdditiveExpression[1]
                isSimpleStatement = self.sr.isSimpleStatement(tokenlist[index:])
                while isSimpleStatement[0]:
                    isSimpleStatement = self.sr.isSimpleStatement(tokenlist[index:])
                    if isSimpleStatement[0]:
                        self.__consumeSimpleStatement(simple_node, tokenlist[index:])
                        index = index + isSimpleStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1


    def __consumeSimpleStatement(self, node, tokenlist=[]):
        try:
            simple_node = Node("SIMPLE_STATEMENT", tokenval = "SIMPLE_STATEMENT", parent = node)
            token = tokenlist[0]
            isRelationalOperator = self.sr.isRelationalOperator(token)
            
            if isRelationalOperator:

                relational_node = Node("RELATIONAL_OPERATOR", parent = simple_node, tokenval = token.tokenval, 
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                #print(relational_node.parent.parent.tokenval,"1")    
                for n in relational_node.parent.parent.children:
                    if n.tokenval == "ADDITIVE_EXPRESSION_STMT":
                        n.parent = relational_node
                index = 1
                isAdditiveExpression = self.sr.isAdditiveExpression(tokenlist[index:])
                if isAdditiveExpression[0]:
                    self.__consumeAdditiveExpression(relational_node, tokenlist[index:])
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


    def __consumeLogicStatement(self, node, tokenlist=[]):
        try:
            #logic_node = Node("LOGIC_STATEMENT", tokanval = "LOGIC_STATEMENT", parent = node)
            token = tokenlist[0]
            #isLogicOperator = self.__isLogicOperator(token)
            isLogicOperator = self.sr.isLogicOperator(token)
            if isLogicOperator:
                operator_node = Node("LOGIC_OPERATOR", parent = node, tokenval = token.tokenval, 
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                #print(operator_node.parent.parent.tokenval)
                
                index = 1
                #isSimpleExpression = self.__isSimpleExpression(tokenlist[index:])
                
                isSimpleExpression = self.sr.isSimpleExpression(tokenlist[index:])
                if isSimpleExpression[0]:
                    print("deu mano")
                    for n in node.children:
                        if n.tokenval == "SIMPLE_EXPRESSION_STMT":
                            n.parent = operator_node
                    self.__consumeSimpleExpression(operator_node, tokenlist[index:])
                   

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


    def __consumeLogicExpression(self, node, tokenlist=[]):
        try:
            logic_node  = Node("LOGIC_EXPRESSION_STMT", parent = node, tokenval = "LOGIC_EXPRESSION_STMT")
            isSimpleExpression = self.sr.isSimpleExpression(tokenlist)
            if isSimpleExpression[0]:
                self.__consumeSimpleExpression(logic_node, tokenlist)
                index = isSimpleExpression[1]
                isLogicStatement = self.sr.isLogicStatement(tokenlist[index:])
                while isLogicStatement[0]:
                    isLogicStatement = self.sr.isLogicStatement(tokenlist[index:])
                    if isLogicStatement[0]:
                        self.__consumeLogicStatement(logic_node, tokenlist[index:])
                        index = index + isLogicStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    ####### << continuar a partir daqui >> #########
    def __consumeExpression(self, node, tokenlist=[]):
        try:
            exp_node = Node("EXPRESSION", parent=node, tokenval="EXPRESSION")
            #isLogicExpression = self.__isLogicExpression(tokenlist)
            isLogicExpression = self.sr.isLogicExpression(tokenlist)
            #isAssignment = self.__isAssignment(tokenlist)
            isAssignment = self.sr.isAssignment(tokenlist)
            if isAssignment[0]:
                self.__consumeAssignment(exp_node, tokenlist)
                return isAssignment

            elif isLogicExpression[0]:
                self.__consumeLogicExpression(exp_node, tokenlist)
                return isLogicExpression

            else:
                return False, -1
        except IndexError:
            return False, -1

    # feito levantamento de erros
    def __consumeIndex(self, node, tokenlist=[]):
        try:
            #isIndexStatement = self.__isIndexStatement(tokenlist)
            isIndexStatement = self.sr.isIndexStatement(tokenlist)
            index = 0
            if isIndexStatement[0]:            
                #self.__consumeIndexStatement(tokenlist)
                index_stmt = Node("INDEX_STMT", tokenval = "INDEX_STMT", parent=node)
                while isIndexStatement[0]:
                    #isIndexStatement = self.__isIndexStatement(tokenlist[index:])
                    isIndexStatement = self.sr.isIndexStatement(tokenlist[index:])
                    if isIndexStatement[0]:
                        self.__consumeIndexStatement(index_stmt, tokenlist)
                        index = index + isIndexStatement[1]
                
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    
    # feito levantamento de erros
    def __consumeIndexStatement(self, node, tokenlist=[]):
        try:
            token = tokenlist[0]
            new_node = Node("INDEX", parent=node, tokenval="INDEX")
            if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                Node("OPEN_BRACKET", parent=new_node, tokenval = token.tokenval,
                 tokentype= token.tokentype, lexeme=token.lexeme, line=token.getNumberOfLine())
                index = 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(new_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        Node("CLOSE_BRACKET", parent=new_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme= token.lexeme, line = token.getNumberOfLine())
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
    def __consumeAssignment(self, node, tokenlist=[]):
        try:
            assign_node = Node("ASSIGNMENT_STMT", tokenval="ASSIGNMENT_STMT", parent=node)
            isVar = self.sr.isVar(tokenlist)

            if isVar[0]:
                #self.__consumeVar(assign_node, tokenlist)
                index = isVar[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.ASSIGNMENT.value:
                    signal_node = Node("ASSIGNMENT", parent=assign_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, 
                    line = token.getNumberOfLine())
                    index = index + 1
                    #isExpression = self.isExpression(tokenlist[index:])
                    isExpression = self.sr.isExpression(tokenlist[index:])
                    if isExpression[0]:
                        self.__consumeVar(signal_node, tokenlist)
                        self.__consumeExpression(signal_node, tokenlist[index:])
                        
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
    def __consumeRead(self, node, tokenlist=[]):
        try:
            read_node = Node("READ_STMT", tokenval = "READ_STMT", parent = node)
            token = tokenlist[0]
            if token.tokenval == TokenVal.READ.value:
                Node("READ", parent = read_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = read_node, tokenval = token.tokenval, tokentype = token.tokentype,
                    lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = 2
                    isVar = self.sr.isVar(tokenlist[index:])
                    if isVar[0]:
                        self.__consumeVar(read_node, tokenlist[index:])
                        index = index + isVar[1]
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", parent = read_node, tokenval = token.tokenval,
                            tokentype = token.tokentype, lexeme = token.lexeme, 
                            line = token.getNumberOfLine())
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
    def __consumeWrite(self, node, tokenlist=[]):
        # continua aqui 3
        try:
            index = 0
            token = tokenlist[index]
            write_node = Node("WRITE_STMT", tokenval = "WRITE_STMT", parent = node)
            if token.tokenval == TokenVal.WRITE.value:
                Node("WRITE", parent = write_node, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = write_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    #isExpression = self.isExpression(tokenlist[index:])
                    isExpression = self.sr.isExpression(tokenlist[index:])
                    if isExpression[0]:
                        self.__consumeExpression(write_node, tokenlist[index:])
                        index = index + isExpression[1]
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", parent= write_node, tokenval = token.tokenval,
                            tokentype = token.tokentype, lexeme = token.lexeme,
                            line = token.getNumberOfLine())
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
    def __consumeReturn(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            return_node = Node("RETURN_STMT", parent = node, tokenval = "RETURN_STMT")
            if token.tokenval == TokenVal.RETURN.value:
                Node("RETURN", parent =  return_node, tokenval = token.tokenval, tokentype = token.tokentype,
                line = token.getNumberOfLine(), lexeme = token.lexeme)
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = return_node, tokenval = token.tokenval, tokentype = token.tokentype,
                    lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    #isExpression = self.isExpression(tokenlist[index:])
                    isExpression = self.sr.isExpression(tokenlist[index:])
                    if isExpression[0]:
                        self.__consumeExpression(tokenlist[index:])
                        index = index + isExpression[1]
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", parent = return_node, tokenval = token.tokenval, tokentype = token.tokentype,
                            lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeArgumentStatement(self, node, tokenlist=[]):
        try:
            argument_node = Node("ARGUMENT_STATEMENT_STMT", parent = node, 
            tokenval = "ARGUMENT_STATEMENT_STMT")
            token = tokenlist[0]
            if token.tokenval == TokenVal.COMMA.value:
                Node("COMMA", parent = argument_node, tokenval = token.tokenval, 
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(argument_node, tokenlist[index:])
                    index = index + isExpression[1]
                    return True, index
                else:
                    return False, -1
            else:
                return False, -1
        except:
            return False, -1


    def __consumeArgumentList(self, node, tokenlist=[]):
        try:
            #isExpression = self.isExpression(tokenlist)
            argument_list_node = Node("ARGUMENT_LIST_STMT", tokenval = "ARGUMENT_LIST_STMT", parent = node)
            isExpression = self.sr.isExpression(tokenlist)
            if isExpression[0]:
                self.__consumeExpression(argument_list_node, tokenlist)
                index = isExpression[1]
                #isArgumentStatement = self.__isArgumentStatement(tokenlist[index:])
                isArgumentStatement = self.sr.isArgumentStatement(tokenlist[index:])
                if isArgumentStatement[0]:
                    while isArgumentStatement[0]:
                        #isArgumentStatement = self.__isArgumentStatement(tokenlist[index:])
                        isArgumentStatement = self.sr.isArgumentStatement(tokenlist[index:])
                        if isArgumentStatement[0]:
                            self.__consumeArgumentStatement(argument_list_node, tokenlist[index:])
                            index = index + isArgumentStatement[1]
                    return True, index
                else:
                    return isExpression
            else:
                return False, -1
        except IndexError:
            return False, -1
    
    
    def __consumeCallFunctionWithoutArgumentsStatement(self, node, tokenlist=[]):
        try:
            call_function_node = Node("CALL_FUNCTION_WITHOUT_ARGUMENTS_STMT", tokenval = "CALL_FUNCTION_WITHOUT_ARGUMENTS_STMT",
            parent = node)
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent = call_function_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = call_function_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        Node("CLOSE_PARENTHESES", parent = call_function_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeCallFunctionWithArgumentsStatement(self, node, tokenlist=[]):
        try:
            call_function_node = Node("CALL_FUNCTION_WITH_ARGUMENTS_STMT", tokenval = "CALL_FUNCTION_WITH_ARGUMENTS_STMT",
            parent = node)
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent = call_function_node, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = call_function_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    #isArgumentList = self.__isArgumentList(tokenlist[index:])
                    isArgumentList = self.sr.isArgumentList(tokenlist[index:])
                    if isArgumentList[0]:
                        self.__consumeArgumentList(call_function_node, tokenlist[index:])
                        index = index + isArgumentList[1]
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", parent = call_function_node, tokenval = token.tokenval,
                            tokentype = token.tokentype, line = token.getNumberOfLine(),
                            lexeme = token.lexeme)
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


    def __consumeCallFunction(self, node, tokenlist=[]):
        try:
            call_function_node = Node("CALL_FUNCTION_STMT", tokenval = "CALL_FUNCTION_STMT", parent = node)
            isCallFunctionWithoutArgumentsStatement = self.sr.isCallFunctionWithoutArgumentsStatement(tokenlist)
            if isCallFunctionWithoutArgumentsStatement[0]:
                self.__consumeCallFunctionWithoutArgumentsStatement(call_function_node, tokenlist)
                return isCallFunctionWithoutArgumentsStatement
              
            isCallFunctionWithArgumentsStatement = self.sr.isCallFunctionWithArgumentsStatement(tokenlist)
            
            if isCallFunctionWithArgumentsStatement[0]:
                self.__consumeCallFunctionWithArgumentsStatement(call_function_node, tokenlist)
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
                #isVar = self.isVar(tokenlist[index:])
                isVar = self.sr.isVar(tokenlist[index:])
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
    def __consumeVarList(self, node, tokenlist=[]):
        try:
            #isVar = self.isVar(tokenlist)
            isVar = self.sr.isVar(tokenlist)
            new_node = Node("VAR_LIST", tokenval="VAR_LIST", parent = node)
            if isVar[0]:
                self.__consumeVar(new_node, tokenlist)
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
    def __consumeVarDeclare(self, node, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]

            if token.tokenval in types:
                index = index + 1
                token = tokenlist[index]
                
                if token.tokenval == TokenVal.TWO_DOTS.value:
                    index = index + 1
                    #isVarList = self.__isVarList(tokenlist[index:])
                    isVarList = self.sr.isVarList(tokenlist[index:])
                    if isVarList[0]:
                        new_node = Node("VAR_DECLARE", parent=node, tokenval="VAR_DECLARE")
                        self.__consumeVarList(new_node, tokenlist[index:])
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
    

    def __consumeAction(self, node, tokenlist=[]):
        try:
            action_node = Node("ACTION_STMT", parent = node, tokenval = "ACTION_STMT")
            isVarDeclare = self.sr.isVarDeclare(tokenlist)
            if isVarDeclare[0]:
                self.__consumeVarDeclare(action_node,tokenlist)
                return isVarDeclare
            
            
            isRead = self.sr.isRead(tokenlist)
            if isRead[0]:
                self.__consumeRead(action_node, tokenlist)
                return isRead
            
            #isWrite = self.__isWrite(tokenlist)
            isWrite = self.sr.isWrite(tokenlist)
            if isWrite[0]:
                self.__consumeWrite(action_node, tokenlist)
                return isWrite
            
            #isReturn = self.__isReturn(tokenlist)
            isReturn = self.sr.isReturn(tokenlist)
            if isReturn[0]:
                self.__consumeReturn(action_node, tokenlist)
                return isReturn
                
           
            isConditional = self.sr.isConditional(tokenlist)
            if isConditional[0]:
                self.__consumeConditional(action_node, tokenlist)
                return isConditional
            
            #isRepeat = self.__isRepeat(tokenlist)
            isRepeat = self.sr.isRepeat(tokenlist)
            if isRepeat[0]:
                self.__consumeRepeat(action_node, tokenlist)
                return isRepeat

            #isExpression = self.isExpression(tokenlist)
            isExpression = self.sr.isExpression(tokenlist)
            if isExpression[0]:
                self.__consumeExpression(action_node, tokenlist)
                return isExpression

            #self.errorHandler.errorActionStatement()
            return False, -1
        except IndexError:
            return False, -1
    

    def __consumeBody(self, node, tokenlist=[]):
        try:
            body_node = Node("BODY_STMT", parent=node, tokenval="BODY_STMT")
            #isAction = self.__isAction(tokenlist)
            isAction = self.sr.isAction(tokenlist)
            if isAction[0]:
                # parei aqui 2
                
                #index = isAction[1]
                index = 0
                while isAction[0]:
                    isAction = self.sr.isAction(tokenlist[index:])
                    if isAction[0]:
                        self.__consumeAction(body_node, tokenlist[index:])
                        index = index + isAction[1]
                return True, index
            else:
                return False, -1
        except:
            return False, -1
    

    def __consumeFirstConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            first_conditional_node = Node("FIRST_CONDITIONAL_STMT", parent = node, 
            tokenval = "FIRST_CONDITIONAL_STMT")
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = first_conditional_node, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])

                if isExpression[0]:
                    self.__consumeExpression(first_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = first_conditional_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        #isBody = self.__consumeBody(tokenlist[index:])
                        isBody = self.sr.isBody(tokenlist[index:])
                        if isBody[0]:
                            self.__consumeBody(first_conditional_node, tokenlist[index:])
                            index = index + isBody[1]
                            token = tokenlist[index]
                            if token.tokenval == TokenVal.END.value:
                                Node("END", parent = first_conditional_node, tokenval = token.tokenval,
                                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeSecondConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            second_conditional_node = Node("SECOND_CONDITIONAL_STMT", tokenval = "SECOND_CONDITIONAL_STMT", 
            parent = node)
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = second_conditional_node, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(second_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]
                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = second_conditional_node, tokentype = token.tokentype,
                        tokenval = token.tokenval, line = token.getNumberOfLine(), lexeme = token.lexeme)
                        index = index + 1
                        token = tokenlist[index]
                        if token.tokenval == TokenVal.END.value:
                            Node("END", parent = second_conditional_node, tokenval = token.tokenval,
                            tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeThirdConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            third_conditional_node = Node("THIRD_CONDITIONAL_STMT", parent = node, tokenval = "THIRD_CONDITIONAL_STMT")
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = third_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(third_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = third_conditional_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        isBody = self.sr.isBody(tokenlist[index:])
                        #self.__consumeBody(tokenlist[index:])
                        
                        if isBody[0]:
                            self.__consumeBody(third_conditional_node, tokenlist[index:])
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.ELSE.value:
                                Node("ELSE", parent = third_conditional_node, tokenval = token.tokenval,
                                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                                index = index + 1
                                
                                isBody = self.sr.isBody(tokenlist[index:])
                                #self.__consumeBody(tokenlist[index:])

                                if isBody[0]:
                                    self.__consumeBody(third_conditional_node, tokenlist[index:])
                                    index = index + isBody[1]
                                    token = tokenlist[index]

                                    if token.tokenval == TokenVal.END.value:
                                        Node("END", parent = third_conditional_node, tokenval = token.tokenval,
                                        tokentype = token.tokentype, lexeme = token.lexeme,
                                        line = token.getNumberOfLine())
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


    def __consumeFourthConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            fourth_conditional_node = Node("FOURTH_CONDITIONAL_STMT", parent = node, tokenval = "FOURTH_CONDITIONAL_STMT")
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = fourth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(fourth_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = fourth_conditional_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.ELSE.value:
                            Node("ELSE", parent = fourth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                            lexeme = token.lexeme, line = token.getNumberOfLine())
                            index = index + 1
                            isBody = self.sr.isBody(tokenlist[index:])
                            #self.__consumeBody(tokenlist[index:])

                            if isBody[0]:
                                self.__consumeBody(fourth_conditional_node, tokenlist[index:])
                                index = index + isBody[1]
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    Node("END", parent = fourth_conditional_node, tokentype = token.tokentype,
                                    tokenval = token.tokenval, lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeFifthConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            fifth_conditional_node = Node("FIFTH_CONDITIONAL_STMT", parent = node, tokenval = "FIFTH_CONDITIONAL_STMT")
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = fifth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(fifth_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = fifth_conditional_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        isBody = self.sr.isBody(tokenlist[index:])
                        #self.__consumeBody(tokenlist[index:])

                        if isBody[0]:
                            self.__consumeBody(fifth_conditional_node, tokenlist[index:])
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.ELSE.value:
                                Node("ELSE", parent = fifth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                                lexeme = token.lexeme, line = token.getNumberOfLine())
                                index = index + 1
                                token = tokenlist[index]

                                if token.tokenval == TokenVal.END.value:
                                    Node("END", parent = fifth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                                    lexeme = token.lexeme, line = token.getNumberOfLine())
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


    def __consumeSixthConditionalStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            sixth_conditional_node = Node("SIXTH_CONDITIONAL_STMT", parent = node, tokenval = "SIXTH_CONDITIONAL_STMT")
            if token.tokenval == TokenVal.IF.value:
                Node("IF", parent = sixth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isExpression = self.isExpression(tokenlist[index:])
                isExpression = self.sr.isExpression(tokenlist[index:])
                if isExpression[0]:
                    self.__consumeExpression(sixth_conditional_node, tokenlist[index:])
                    index = index + isExpression[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.THEN.value:
                        Node("THEN", parent = sixth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                        lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.ELSE.value:
                            Node("ELSE", parent = sixth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                            lexeme = token.lexeme, line = token.getNumberOfLine())
                            index = index + 1
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                Node("END", parent = sixth_conditional_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                                lexeme = token.lexeme, line = token.getNumberOfLine())
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

   
    def __consumeConditional(self, node, tokenlist=[]):
        print("aqui")
        try:
            #isFirstConditionalStatement = self.__isFirstConditionalStatement(tokenlist)
            conditional_node = Node("CONDITIONAL_STMT", parent = node, tokenval = "CONDITIONAL_STMT")

            isFirstConditionalStatement = self.sr.isFirstConditionalStatement(tokenlist)
            if isFirstConditionalStatement[0]:
                self.__consumeFirstConditionalStatement(conditional_node, tokenlist)
                return isFirstConditionalStatement
            
            #isSecondConditionalStatement = self.__isSecondConditionalStatement(tokenlist)
            isSecondConditionalStatement = self.sr.isSecondConditionalStatement(tokenlist)
            if isSecondConditionalStatement[0]:
                self.__consumeSecondConditionalStatement(conditional_node, tokenlist)
                return isSecondConditionalStatement
            
            #isThirdConditionalStatement = self.__isThirdConditionalStatement(tokenlist)
            isThirdConditionalStatement = self.sr.isThirdConditionalStatement(tokenlist)
            if isThirdConditionalStatement[0]:
                self.__consumeThirdConditionalStatement(conditional_node, tokenlist)
                return isThirdConditionalStatement

            #isFourthConditionalStatement = self.__isFourthConditionalStatement(tokenlist)
            isFourthConditionalStatement = self.sr.isFourthConditionalStatement(tokenlist)
            if isFourthConditionalStatement[0]:
                self.__consumeFourthConditionalStatement(conditional_node, tokenlist)
                return isFourthConditionalStatement

            #isFifthConditionalStatement = self.__isFifthConditionalStatement(tokenlist)
            isFifthConditionalStatement = self.sr.isFifthConditionalStatement(tokenlist)
            if isFifthConditionalStatement[0]:
                self.__consumeFifthConditionalStatement(conditional_node, tokenlist)
                return isFifthConditionalStatement
            
            #isSixthConditionalStatement = self.__isSixthConditionalStatement(tokenlist)
            isSixthConditionalStatement = self.sr.isSixthConditionalStatement(tokenlist)
            if isSixthConditionalStatement[0]:
                self.__consumeSixthConditionalStatement(conditional_node, tokenlist)
                return isSixthConditionalStatement
            

            return False, -1
        except IndexError:
            return False, -1



    
    # foi realizado levantamento de erros
    def __consumeRepeatWithBodyStatement(self, node, tokenlist=[]):
        try:
            repeat_node = Node("REPEAT_WITH_BODY_STMT", parent = node, tokenval = "REPEAT_WITH_BODY_STMT")
            index = 0
            token = tokenlist[index]

            if token.tokenval == TokenVal.FOR.value:
                Node("FOR", parent = repeat_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isBody = self.__consumeBody(tokenlist[index:])
                isBody = self.sr.isBody(tokenlist[index:])
                if isBody[0]:
                    self.__consumeBody(repeat_node, tokenlist[index:])
                    index = index + isBody[1]
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.UNTIL.value:
                        Node("UNTIL", parent = repeat_node, tokenval = token.tokenval, tokentype = token.tokentype,
                        lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        #isExpression = self.isExpression(tokenlist[index:])
                        isExpression = self.sr.isExpression(tokenlist[index:])
                        if isExpression[0]:
                            self.__consumeExpression(repeat_node, tokenlist[index:])
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
    def __consumeRepeatWithoutBodyStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            repeat_node = Node("REPEAT_WITHOUT_BODY_STMT", parent =  node, tokenval = "REPEAT_WITHOUT_BODY_STMT")
            if token.tokenval == TokenVal.FOR.value:
                Node("FOR", parent = repeat_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]
                
                if token.tokenval == TokenVal.UNTIL.value:
                    Node("UNTIL", parent = repeat_node, tokenval = token.tokenval, tokentype = token.tokentype,
                    lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    #isExpression = self.isExpression(tokenlist[index:])
                    isExpression = self.sr.isExpression(tokenlist[index:])
                    if isExpression[0]:
                        self.__consumeExpression(repeat_node, tokenlist[index:])
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
    def __consumeRepeat(self, node, tokenlist=[]):
        repeat_node = Node("REPEAT_STMT", parent = node, tokenval = "REPEAT_STMT")
        try:
            #isRepeatWithBodyStatement = self.__isRepeatWithBodyStatement(tokenlist)
            isRepeatWithBodyStatement = self.sr.isRepeatWithBodyStatement(tokenlist)

            if isRepeatWithBodyStatement[0]:
                self.__consumeRepeatWithBodyStatement(repeat_node, tokenlist)
                return isRepeatWithBodyStatement
            
            #isRepeatWithoutBodyStatement = self.__isRepeatWithoutBodyStatement(tokenlist)
            isRepeatWithoutBodyStatement = self.sr.isRepeatWithoutBodyStatement(tokenlist)

            if isRepeatWithoutBodyStatement[0]:
                self.__consumeRepeatWithoutBodyStatement(repeat_node, tokenlist)
                return isRepeatWithoutBodyStatement
            return False, -1
        except IndexError:
            return False, -1

    # foi realizado levantamento de erros
    def __consumeParameterStatement(self, node, tokenlist=[]):
        try:
            parameter_statement_node = Node("PARAMETER_STATEMENT_STMT", tokenval = "PARAMETER_STATEMENT_STMT", parent = node)
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]

            if token.tokenval in types:
                Node("TYPE", parent = parameter_statement_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.TWO_DOTS.value:
                    Node("TWO_DOTS", parent = parameter_statement_node, tokenval = token.tokenval, tokentype = token.tokentype,
                    lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.IDENTIFICATOR.value:
                        Node("ID", parent = parameter_statement_node, tokenval = token.tokenval, tokentype = token.tokentype, 
                        lexeme = token.lexeme, line = token.getNumberOfLine())
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
    def __consumeUnidimensionalParameter(self, node, tokenlist=[]):
        try:
            #isParameterStatement = self.__isParameterStatement(tokenlist)
            unidimensional_node = Node("UNIDIMENSIONAL_PARAMETER_STMT", tokenval = "UNIDIMENSIONAL_PARAMETER_STMT",
            parent = node)
            isParameterStatement = self.sr.isParameterStatement(tokenlist)
            index = 0
            if isParameterStatement[0]:
                self.__consumeParameterStatement(unidimensional_node, tokenlist)
                index = index + isParameterStatement[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                    Node("OPEN_BRACKETS", parent = unidimensional_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        Node("CLOSE_BRACKETS", parent = unidimensional_node, tokenval = token.tokenval, 
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
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
    def __consumeBidimensionalParameter(self, node, tokenlist=[]):
        try:
            bidimensional_parameter_node = Node("BIDIMENSIONAL_PARAMETER_STMT", parent = node, tokenval = "BIDIMENSIONAL_PARAMETER_STMT")
            #isUnidimensional = self.__isUnidimensionalParameter(tokenlist)
            isUnidimensional = self.sr.isUnidimensionalParameter(tokenlist)
            if isUnidimensional[0]:
                self.__consumeUnidimensionalParameter(bidimensional_parameter_node, tokenlist)
                index = isUnidimensional[1]
                token = tokenlist[index]
                if token.tokenval == TokenVal.OPEN_BRACKETS.value:
                    Node("OPEN_BRACKETS", parent = bidimensional_parameter_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_BRACKETS.value:
                        Node("CLOSE_BRACKETS", parent = bidimensional_parameter_node, tokenval = token.tokenval,
                        tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
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
    def __consumeParameter(self, node, tokenlist=[]):
        try:
            #isBidimensionalParameter = self.__isBidimensionalParameter(tokenlist)
            parameter_node = Node("PARAMETER_STMT", tokenval = "PARAMETER_STMT", parent = node)
            isBidimensionalParameter = self.sr.isBidimensionalParameter(tokenlist)
            if isBidimensionalParameter[0]:
                self.__consumeBidimensionalParameter(parameter_node, tokenlist)
                return isBidimensionalParameter

            #isUnidimensionalParameter = self.__isUnidimensionalParameter(tokenlist)
            isUnidimensionalParameter = self.sr.isUnidimensionalParameter(tokenlist)
            if isUnidimensionalParameter[0]:
                self.__consumeUnidimensionalParameter(parameter_node, tokenlist)
                return isUnidimensionalParameter
            
            #isParameterStatement = self.__isParameterStatement(tokenlist)
            isParameterStatement = self.sr.isParameterStatement(tokenlist)
            if isParameterStatement[0]:
                self.__consumeParameterStatement(parameter_node, tokenlist)
                return isParameterStatement
            
            return False, -1
        except:
            return False, -1
    
    # foi realizado levantamento de erros
    def __consumeParameterListStatement(self, node, tokenlist=[]):
        try:
            parameter_list_node = Node("PARAMETER_LIST_STMT", parent = node, tokenval = "PARAMETER_LIST_STMT")
            index = 0
            token = tokenlist[index]
            if token.tokenval == TokenVal.COMMA.value:
                Node("COMMA", parent = parameter_list_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isParameter = self.__isParameter(tokenlist[index:])
                isParameter = self.sr.isParameter(tokenlist[index:])
                if isParameter[0]:
                    self.__consumeParameter(parameter_list_node, tokenlist[index:])
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
    def __consumeParameterList(self, node, tokenlist=[]):
        try:
            parameter_list_stmt = Node("PARAMETER_LIST_STMT", parent=node, tokenval="PARAMETER_LIST_STMT")

            #isParameter = self.__Parameter(tokenlist)
            isParameter = self.sr.isParameter(tokenlist)
            if isParameter[0]:
                self.__consumeParameter(parameter_list_stmt, tokenlist)
                index = isParameter[1]
                #isParameterStatement = self.__isParameterStatement(tokenlist[index:])
                isParameterStatement  = self.sr.isParameterStatement(tokenlist[index:])
                while isParameterStatement[0]:
                    #isParameterStatement = self.__isParameterListStatement(tokenlist[index:])
                    isParameterStatement = self.sr.isParameterListStatement(tokenlist[index:])
                    if isParameterStatement[0]:
                        self.__consumeParameterStatement(parameter_list_stmt, tokenlist[index:])
                        index = index + isParameterStatement[1]
                return True, index
            else:
                return False, -1
        except IndexError:
            return False, -1

    
    def __consumeFirstHeaderStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            first_header_stmt = Node("FIRST_HEADER_STMT", parent=node, 
            tokenval = "FIRST_HEADER_STMT")
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent=first_header_stmt, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent=first_header_stmt, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    isParameterList = self.sr.isParameterList(tokenlist[index:])
                    #isParameterList = self.__isParameterList(tokenlist[index:])
                    
                    if isParameterList[0]:
                        self.__consumeParameterList(first_header_stmt, tokenlist[index:])
                        index = index + isParameterList[1]
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", parent=first_header_stmt, tokenval = token.tokenval,
                            tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                            index = index + 1
                            #isBody = self.__isBody(tokenlist[index:])
                            isBody = self.sr.isBody(tokenlist[index:])
                            # parei aqui
                            if isBody[0]:
                                self.__consumeBody(first_header_stmt, tokenlist[index:])
                                index = index + isBody[1]
                                token = tokenlist[index]
                                if token.tokenval == TokenVal.END.value:
                                    Node("END", parent=first_header_stmt, tokenval = token.tokenval, tokentype = token.tokentype,
                                    lexeme = token.lexeme, line = token.getNumberOfLine())
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
    

    def __consumeSecondHeaderStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            second_header_stmt = Node("SECOND_HEADER_STMT", parent=node, 
            tokenval = "SECOND_HEADER_STMT")
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent=second_header_stmt, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent=second_header_stmt, tokenval = token.tokenval,
                    tokentype = token.tokentype, line = token.getNumberOfLine(), lexeme = token.lexeme)
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        Node("CLOSE_PARENTHESES", parent=second_header_stmt, tokenval = token.tokenval,
                        tokentype = token.tokentype, line = token.getNumberOfLine(), lexeme = token.lexeme)
                        index = index + 1
                        
                        isBody = self.sr.isBody(tokenlist[index:])
                        if isBody[0]:
                            self.__consumeBody(second_header_stmt, tokenlist[index:])
                            index = index + isBody[1]
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                Node("END", parent=second_header_stmt, tokentype = token.tokentype,
                                tokenval = token.tokenval, lexeme = token.lexeme, line = token.getNumberOfLine())
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
    

    def __consumeThirdHeaderStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            third_header_node = Node("THIRD_HEADER_STMT", parent=node, tokenval="THIRD_HEADER_STMT")
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent=node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = third_header_node, tokenval = token.tokenval,
                    tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfline())
                    index = index + 1
                    #isParameterList = self.__ParameterList(tokenlist[index:])
                    isParameterList = self.sr.isParameterList(tokenlist[index:])
                    if isParameterList[0]:
                        self.__consumeParameterList(third_header_node, tokenlist[index:])
                        index = index + isParameterList[1]
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                            Node("CLOSE_PARENTHESES", tokenval = token.tokenval, parent =  third_header_node, 
                            lexeme = token.lexeme, tokentype = token.tokentype, line = token.getNumberOfLine())
                            index = index + 1
                            token = tokenlist[index]

                            if token.tokenval == TokenVal.END.value:
                                Node("END", parent = third_header_node, tokenval = token.tokentype, tokentype = token.tokentype,
                                lexeme = token.lexeme, line = token.getNumberOfLine())
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
    

    def __consumeFourthHeaderStatement(self, node, tokenlist=[]):
        try:
            index = 0
            token = tokenlist[index]
            fourth_header_node = Node("FOURTH_HEADER_STMT", parent =  node, 
            tokenval = "FOURTH_HEADER_STMT")
            if token.tokenval == TokenVal.IDENTIFICATOR.value:
                Node("ID", parent = fourth_header_node, tokenval = token.tokenval, tokentype = token.tokentype,
                lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                token = tokenlist[index]

                if token.tokenval == TokenVal.OPEN_PARENTHESES.value:
                    Node("OPEN_PARENTHESES", parent = fourth_header_node, tokenval = token.tokenval, tokentype = token.tokentype,
                    lexeme = token.lexeme, line = token.getNumberOfLine())
                    index = index + 1
                    token = tokenlist[index]

                    if token.tokenval == TokenVal.CLOSE_PARENTHESES.value:
                        Node("CLOSE_PARENTHESES", parent = fourth_header_node, tokenval = token.tokenval, tokentype = token.tokentype,
                        lexeme = token.lexeme, line = token.getNumberOfLine())
                        index = index + 1
                        token = tokenlist[index]

                        if token.tokenval == TokenVal.END.value:
                            Node("END", parent = fourth_header_node, tokenval = token.tokenval, tokentype = token.tokentype,
                            line = token.getNumberOfLine(), lexeme = token.lexeme)
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
    

    def __consumeHeader(self, node, tokenlist=[]):
        try:
            header_node = Node("HEADER", parent=node, tokenval = "HEADER")
            #isFirstHeaderStatement = self.__isFirstHeaderStatement(tokenlist)
            isFirstHeaderStatement = self.sr.isFirstHeaderStatement(tokenlist)
            if isFirstHeaderStatement[0]:
                # parei aqui
                self.__consumeFirstHeaderStatement(header_node, tokenlist)
                return isFirstHeaderStatement
            
            #isSecondHeaderStatement = self.__isSecondHeaderStatement(tokenlist)
            isSecondHeaderStatement = self.sr.isSecondHeaderStatement(tokenlist)
            if isSecondHeaderStatement[0]:
                self.__consumeSecondHeaderStatement(header_node, tokenlist)
                return isSecondHeaderStatement

            isThirdHeaderStatement = self.sr.isThirdHeaderStatement(tokenlist)
            if isThirdHeaderStatement[0]:
                self.__consumeThirdHeaderStatement(header_node,tokenlist)
                return isThirdHeaderStatement
            
            #isFourthHeaderStatement = self.__isFourthHeaderStatement(tokenlist)
            isFourthHeaderStatement = self.sr.isFourthHeaderStatement(tokenlist)
            if isFourthHeaderStatement[0]:
                self.__consumeFourthHeaderStatement(header_node, tokenlist)
                return isFourthHeaderStatement
            
            return False, -1

        except IndexError:
            return False, -1


    def __consumeFunctionDeclaration(self, node, tokenlist=[]):
        try:
            types = [TokenVal.INTEGER_TYPE.value, TokenVal.FLOAT_TYPE.value]
            index = 0
            token = tokenlist[index]
            #isHeader = self.__isHeader(tokenlist)
            func_dcl = Node("FUNCTION_DECLARATION", tokenval="FUNCTION_DECLARATION", parent=node)
            isHeader = self.sr.isHeader(tokenlist)
            if token.tokenval in types:
                Node("TYPE", parent=func_dcl, tokenval = token.tokenval,
                tokentype = token.tokentype, lexeme = token.lexeme, line = token.getNumberOfLine())
                index = index + 1
                #isHeader = self.__isHeader(tokenlist[index:])
                isHeader = self.sr.isHeader(tokenlist[index:])
                if isHeader[0]:
                    self.__consumeHeader(func_dcl, tokenlist[index:])
                    index = index + isHeader[1]
                    
                    return True, index
                else:
                    return False, -1

            elif isHeader[0]:
                self.__consumeHeader(func_dcl, tokenlist)
                return isHeader

            else:
                return False, -1

        except IndexError:
            return False, -1
    
    # levantamento de erros realizado
    def __consumeVarInitialization(self, node, tokenlist=[]):
        try:
            var_initialization = Node("VAR_INITIALIZATION", parent=node, tokenval="VAR_INITIALIZATION")
            self.__consumeAssignment(var_initialization, tokenlist)
            #return self.__Assignment(tokenlist)
            return self.sr.isAssignment(tokenlist)
        except IndexError:
            return False, -1


    def __consumeDeclaration(self, tokenlist=[]):
        try:
            isVarDeclare = self.sr.isVarDeclare(tokenlist)
            r = Resolver("name")
            node = r.get(self.st, "DECLARATION_LIST")
            if isVarDeclare[0]:
                self.__consumeVarDeclare(node, tokenlist)
                return isVarDeclare

            isVarInitialization = self.sr.isVarInitialization(tokenlist)
            if isVarInitialization[0]:
                self.__consumeVarInitialization(node, tokenlist)
                return isVarInitialization
            
            isFunctionDeclaration = self.sr.isFunctionDeclaration(tokenlist)
            if isFunctionDeclaration[0]:
                self.__consumeFunctionDeclaration(node,tokenlist)
                return isFunctionDeclaration
            
            return False, -1
        except IndexError:
            return False, -1
    

    def __isDeclarationsList(self, tokenlist=[]):
        try:
            isDeclaration = self.sr.isDeclaration(tokenlist)
            if isDeclaration[0]:
                Node("DECLARATION_LIST", parent=self.st, tokenval="DECLARATION_LIST")
                index = 0
                while isDeclaration[0]:
                    isDeclaration = self.sr.isDeclaration(tokenlist[index:])
                    if isDeclaration[0]:
                        self.__consumeDeclaration(tokenlist[index:])
                        index = index + isDeclaration[1] 

                return True, index
            
            else:
                return False, -1
        except IndexError:
            return False, -1
    

    def isAProgram(self, tokenlist=[]):
        self.st = Node("PROGRAM",parent=None,tokenval="PROGRAM")
        return self.__isDeclarationsList(tokenlist)


    def __printErrorFound(self, expected=str, received=str, line=int):
        print("In line", line)
        print("Expected", expected, ", but got a ", received)

    
    def __printErrorStatement(self, statement=str, line=int):
        print("Near line", line,":")
        print("The ", statement, " statement got errors" )

class syntax_process(object):
    
    
    
    def nodenamefunc(self, node):
        try:
            return '%s:%s\n%s\n%s' % (node.name, node.depth, node.tokentype, node.lexeme)
        except AttributeError:
            return '%s:%s' % (node.name, node.depth)
    
    
    def edgeattrfunc(self, node, child):
        return 'label="%s:%s"' % (node.name, child.name)
    
    
    def edgetypefunc(self, node, child):
        return '--'

    def exec(self, tokenlist=[]):
        sr = syntax_scanner()
        process = sr.isAProgram(tokenlist)
        if process[0] == True and (len(tokenlist) == int(process[1])):
            print("successfull syntactic check")
        
        elif(len(tokenlist) > process[1] and process[1] > 0 and sr.errorFound == False):
            line = tokenlist[process[1] + 1].getNumberOfLine()
            print("Error near the statement that begins near line", line)
            print("near the token", tokenlist[process[1]].tokenval)
        
        #print(RenderTree(sr.st))
        DotExporter(sr.st, graph="graph", nodenamefunc=self.nodenamefunc,
        nodeattrfunc=lambda node: "shape=box", edgeattrfunc=self.edgeattrfunc,
        edgetypefunc=self.edgetypefunc).to_dotfile("tree.dot")
        #print(sr.st.descendants[0])
        #r = Resolver("name")
        #print(r.get(sr.st,"DECLARATION_LIST"))