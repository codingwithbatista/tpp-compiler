from anytree import Node, PreOrderIter, PostOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.SymbolTable = []
        self.defineScopes()
        self.walking()
        #self.printTree()
        self.printTable(self.SymbolTable)
        self.cuttingTree()
    

    def printNode(self, node):
        if hasattr(node, 'lexeme'):
            if hasattr(node, 'data_type'):
                if hasattr(node, 'op_type'):
                    print("name:",node.name,"|", "lexeme:",node.lexeme,"|", "tokenval:",node.tokenval,"|", "scope:",node.scope,"|", "data_type:",node.data_type,"|",
                    "op_type:", node.op_type)
                else:
                    print("name:",node.name,"|", "lexeme:",node.lexeme,"|", "tokenval:",node.tokenval,"|", "scope:",node.scope,"|", "data_type:",node.data_type)

            else:
                print("name:",node.name,"|", "lexeme:",node.lexeme,"|", "tokenval:",node.tokenval,"|", "scope:",node.scope)
        else:
            if hasattr(node, "data_type"):
                print("name:",node.name,"|", "scope:",node.scope, "|", "data_type:", node.data_type)    
            else:
                print("name:",node.name,"|", "scope:",node.scope)


    def printTree(self):
        for node in PreOrderIter(self.syntax_tree):
            self.printNode(node)


    def printTable(self, table=[]):
        for t in table:
            print(t)


    def defineScopes(self):
        scope = ""
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "PROGRAM":
                scope= "global"
                node.scope = scope
            
            elif node.name == "FUNCTION_DECLARATION":
                try:
                    scope_name = node.children[1].children[0].children[0].lexeme
                    scope = scope + ".fnc_" + scope_name
                    node.scope = scope
                except IndexError:
                    scope_name = node.children[0].children[0].children[0].lexeme
                    scope = scope + ".fnc_" + scope_name
                    node.scope = scope
            
            elif node.name == "CONDITIONAL_STMT":
                scope = scope + ".conditional"
                node.scope = scope

            elif node.name == "IF":
                scope = scope + ".if"
                node.scope = scope
            
            elif node.name == "ELSE":
                finalIndex = scope.rfind(".if")
                scope = scope[:finalIndex]
                scope = scope + ".else"
                node.scope = scope
            
            elif node.name == "REPEAT_STMT":
                scope = scope + ".for"
                node.scope = scope

            elif node.name == "END":
                if node.parent.parent.name == "CONDITIONAL_STMT":
                    finalIndex = scope.rfind(".conditional")
                else:
                    finalIndex = scope.rfind(".")
                
                scope = scope[:finalIndex]
                node.scope = scope

            else:
                node.scope = scope
    

    def addVarDeclareSymbolTable(self, node=Node):
        variables = []
        for n in PreOrderIter(node):
            if n.name == "TYPE":
                data_type = n.lexeme
            elif n.name == "ID":
                index = []
                for i in PreOrderIter(n.parent):
                    if i.name == "NUMBER":
                        index.append(i.lexeme)
                if len(index) == 0:
                    variables.append(["var_declare",data_type,n.lexeme, n.scope, n.line])
                else:
                    variables.append(["var_declare",data_type,n.lexeme, n.scope, n.line, index])
        for v in variables:
            self.SymbolTable.append(v)
    
   
    def addParameterSymbolTable(self, node=Node):
        parameters = []
        for n in PreOrderIter(node):
            if n.name == "PARAMETER_STATEMENT_STMT":
                for p in PreOrderIter(n):
                    if p.name == "TYPE":
                        data_type = p.lexeme
                    elif p.name == "ID":
                        p.data_type = data_type
                        scope = p.scope
                        lexeme = p.lexeme
                        line = p.line
                        parameters.append(["parameter_func", data_type, lexeme, scope, line])
        for p in parameters:
            if p not in self.SymbolTable:
                self.SymbolTable.append(p)


    def annotateVarTypes(self, varNode=Node):
        node = varNode.children[0]
        for line in self.SymbolTable:
            if line[0] == "var_declare" or line[0] == "parameter_func":
                if node.name == "VAR_INDEX_STMT":
                    varNode = node.children[0]
                    if varNode.lexeme == line[2] and line[3] in node.scope:
                        varNode.data_type = line[1]

                elif node.lexeme == line[2] and line[3] in node.scope:
                    node.data_type = line[1]


    def annotateExpressionTypes(self, exprNode=Node):
        for node in PreOrderIter(exprNode):
            if node.name == "CALL_FUNCTION_STMT":
                func_name = node.children[0].children[0].lexeme
                for symbol in self.SymbolTable:
                    if symbol[0] == "func_declare" and func_name == symbol[2]:
                        exprNode.data_type = symbol[1]
                        return 
        for node in PreOrderIter(exprNode):
            if hasattr(node, 'data_type'):
                if node.data_type == "flutuante":
                    exprNode.data_type = "flutuante"
                    break
                elif node.data_type == "inteiro":
                    exprNode.data_type = "inteiro"
    
    
    def warningCastingTypes(self):
        try: 
            for node in PreOrderIter(self.syntax_tree):
                if node.name == "ASSIGNMENT":
                    if node.children[0].children[0] == "VAR_INDEX_STMT":
                        leftNode = node.children[0].children[0].children[0]
                    else:
                        leftNode = node.children[0].children[0]
                    rightNode = node.children[1]
                    if leftNode.data_type != rightNode.data_type:
                        print("===== WARNING =====\nIn line ", leftNode.line, " variable '", leftNode.lexeme,
                        "' is ", leftNode.data_type, ", but received ", rightNode.data_type, sep="")
                        print("The variable value will be casted to", leftNode.data_type)
        except AttributeError:
            pass

          
    def addFunctionDeclaredSymbolTable(self, node=Node):
        functions = []
        for node in PreOrderIter(node):
            if node.name == "FUNCTION_DECLARATION":
                if node.children[0].name == "TYPE":
                    data_type = node.children[0].lexeme
                    headerNode = node.children[1].children[0].children[0]
                else:
                    data_type = "vazio"
                    headerNode = node.children[0].children[0].children[0]
                if headerNode.name == "ID":
                    func_name = headerNode.lexeme
                    line = headerNode.line
                    scope = headerNode.scope
                    functions.append(["func_declare",data_type, func_name, scope, line])
    
        for f in functions:
            self.SymbolTable.append(f)


    def isMainDeclared(self):
        for line in self.SymbolTable:
            if line[0] == "func_declare" and line[2] == "principal":
                return True
        
        print("===== ERROR =====\n", "principal function was not declared", sep="")
        return False


    def isVarUnused(self, varSymbolTable=[]):
        for node in PreOrderIter(self.syntax_tree):
            if (node.name == "VAR" and node.parent.name != "VAR_LIST" 
            and node.children[0].name != "VAR_INDEX_STMT"):
                varNode = node.children[0]
                if varSymbolTable[3] in varNode.scope and varSymbolTable[2] == varNode.lexeme:
                    return True
            elif(node.name == "VAR" and node.parent.name != "VAR_LIST"
            and node.children[0].name == "VAR_INDEX_STMT"):
                varNode = node.children[0].children[0]
                if varSymbolTable[3] in varNode.scope and varSymbolTable[2] == varNode.lexeme:
                    return True
        
        return False

    
    def warningUnusedVars(self):
        for symbol in self.SymbolTable:
            if symbol[0] == "var_declare":
                isUsed = self.isVarUnused(symbol)
                if isUsed == False:
                    print("===== WARNING =====\nthe declared variable '", symbol[2],"' is unused"
                    ,sep="")


    def hasIndexError(self):
        hasError = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "INDEX":
                for i in PreOrderIter(node):
                    if hasattr(i, 'data_type') and hasattr(i, 'line'):
                        if i.data_type == "flutuante":
                            print("===== ERROR =====\n", "In line ", i.line, ", index cannot be flutuante",
                            sep="" )
                            hasError = True
        return hasError


    def hasReturnError(self):
        hasError = False
        errorMessages = []
        for symbol in self.SymbolTable:
            if symbol[0] == "func_declare":
                hasReturn = False
                for node in PreOrderIter(self.syntax_tree):
                    if node.name == "RETURN_STMT":
                        returnNode = node.children[2]
                        if hasattr(returnNode, "data_type"):
                            data_type = returnNode.data_type
                            scope = returnNode.scope
                        else:
                            return hasError
                        if scope == symbol[3]:
                            hasReturn = True
                        if data_type != symbol[1] and scope == symbol[3]:
                            hasError = True
                            print("===== ERROR =====\nIn function ", symbol[2]," (line ",
                            node.children[0].line,") : it returns ",data_type,
                            ", but should return ", symbol[1], sep="")
                if symbol[1] != "vazio" and hasReturn == False:
                    hasError = True
                    message = ("===== ERROR =====\nIn function " + symbol[2] + 
                    ": it returns vazio, but should return " + symbol[1])
                    if message not in errorMessages:
                        errorMessages.append(message)
                        print(message)
                for node in PreOrderIter(self.syntax_tree):
                    if node.name == "RETURN_STMT":
                        returnNode = node.children[2]
                        data_type = returnNode.data_type
                        scope = returnNode.scope
                        if data_type != symbol[1] and symbol[3] in scope and symbol[3] != scope:
                            hasError = True
                            message = ("===== ERROR =====\nIn function " + symbol[2] + " (line " +
                            str(node.children[0].line) + ") : it returns " + data_type +", but should return " + symbol[1])
                            if message not in errorMessages:
                                print(message)
                                errorMessages.append(message)

        return hasError


    def hasUndeclaredFunction(self):
        hasError = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "CALL_FUNCTION_STMT":
                defined = False
                for symbol in self.SymbolTable:
                    funcNameNode = node.children[0].children[0]
                    if (symbol[0] == "func_declare" and symbol[2] == funcNameNode.lexeme
                    and symbol[3] == "global.fnc_" + funcNameNode.lexeme):
                        defined = True
                if defined == False:
                    line = funcNameNode.line
                    funcName = funcNameNode.lexeme
                    hasError = True
                    print("===== ERROR =====\nIn line ", line, ": function '",funcName,
                    "' wasn't defined", sep="")
        return hasError

                    
    def hasErrorNumberParametersCallFunction(self):
        hasError = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "CALL_FUNCTION_STMT":
                funcNameNode = node.children[0].children[0]
                line = node.children[0].children[0].line
                parameterNumber = 0
                for symbol in self.SymbolTable:
                    funcScope = "global.fnc_" + funcNameNode.lexeme
                    if symbol[0] == "parameter_func" and symbol[3] == funcScope:
                        parameterNumber += 1
                callParameterNumber = 0
                if node.children[0].name == "CALL_FUNCTION_WITH_ARGUMENTS_STMT":
                    callParameterNumber = len(node.children[0].children[2].children)
                    
                if callParameterNumber != parameterNumber:
                    hasError = True
                    print("===== ERROR =====\nIn call function '", funcNameNode.lexeme,"': function expect ", parameterNumber,
                    " parameters, but received ", callParameterNumber,". See line ", line, sep="")
        return hasError


    def warningVariableDeclaredMoreThanOneTime(self):
        symbol = self.SymbolTable
        for i in range(len(self.SymbolTable)):
            for j in range(i+1, len(self.SymbolTable)):
                if symbol[i][0] == symbol[j][0] and symbol[i][0] == "var_declare":
                    if symbol[i][2] == symbol[j][2] and symbol[i][3] == symbol[j][3]:
                        print("===== WARNING =====\nIn line ", symbol[j][4], ": variable '", symbol[i][2],
                        "' is defined in line ", symbol[i][4], " already", sep="")


    def hasErrorUndefinedVariable(self):
        hasError = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR" and node.parent.name == "FACTOR":
                defined = False
                nodeVar = node.children[0]
                for symbol in self.SymbolTable:
                    if symbol[0] == "var_declare" or symbol[0] == "parameter_func":
                        if symbol[2] == nodeVar.lexeme and symbol[3] in nodeVar.scope:
                            defined = True
                if defined == False:
                    hasError = True
                    print("===== ERROR =====\nIn line ", nodeVar.line, " variable '", nodeVar.lexeme,
                    "' isn't declared previously", sep="" )
        return hasError

    
    def warningNonInitializedVariable(self):
        initializedVars = []
        try:
            for node in PreOrderIter(self.syntax_tree):
                if node.name == "VAR" and node.parent.name == "ASSIGNMENT":
                    nodeVar = node.children[0]
                    initializedVars.append([nodeVar.data_type, nodeVar.lexeme, nodeVar.scope])
                elif node.name == "PARAMETER_STATEMENT_STMT":
                    nodeVar = node.children[2]
                    initializedVars.append([nodeVar.data_type, nodeVar.lexeme, nodeVar.scope])
                elif node.name == "VAR" and node.parent.name == "FACTOR":
                    nodeElement = node.children[0]
                    initialized = False
                    for var in initializedVars:
                        if (nodeElement.lexeme == var[1] and  nodeElement.data_type == var[0]
                        and var[2] in nodeElement.scope):
                            initialized = True
                    if initialized == False:
                        print("===== WARNING =====\nIn line ", nodeElement.line,": variable '",
                        nodeElement.lexeme,"' wasn't initilized before", sep="")
        except AttributeError:
            pass



    def hasCallMainError(self):
        hasError = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "CALL_FUNCTION_STMT":
                callNode = node.children[0].children[0]
                if callNode.lexeme == "principal" and "global.fnc_principal" not in callNode.scope:
                    print("===== ERROR =====\nIn line ", callNode.line,
                    ": a call to principal function was made. It cannot be made.", sep="")
                    hasError = True
                elif callNode.lexeme == "principal" and "global.fnc_principal" in callNode.scope:
                    print("===== WARNING =====\nIn line ", callNode.line,
                    ": a recursive call to principal function was made.", sep="")
        return hasError
    

    def warningUnusedDefinedFunction(self):
        for symbol in self.SymbolTable:
            if symbol[0] == "func_declare" and symbol[2] != "principal":
                warning = True
                for node in PreOrderIter(self.syntax_tree):
                    if node.name == "CALL_FUNCTION_STMT":
                        funcNameNode = node.children[0].children[0]
                        if (symbol[2] == funcNameNode.lexeme):
                            warning = False
                if warning == True:
                    print("===== WARNING =====\nFunction '", symbol[2], "' was define in line ", symbol[4],
                    ", but it's unused", sep="")


    def warningParameterTypes(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "HEADER":
                func_name = node.children[0].children[0].lexeme
                scope = node.children[0].children[0].scope
                parameters = []
                for n in PreOrderIter(node):
                    if n.name == "TYPE" and n.parent.name == "PARAMETER_STATEMENT_STMT":
                        parameters.append(n.lexeme)
                for symbol in self.SymbolTable:
                    if (symbol[0] == "func_declare" and symbol[2] == func_name and
                    scope == symbol[3]):
                        symbol.append(parameters)
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "CALL_FUNCTION_STMT":
                func_name = node.children[0].children[0].lexeme
                line = node.children[0].children[0].line
                call_parameters = []
                if node.children[0].name == "CALL_FUNCTION_WITH_ARGUMENTS_STMT":
                    argNode = node.children[0].children[2]
                    call_parameters.append(argNode.children[0].data_type)
                    for n in argNode.children:
                        if n.name == "ARGUMENT_STATEMENT_STMT":
                            call_parameters.append(n.children[1].data_type)
                
                for symbol in self.SymbolTable:
                    if (symbol[0] == "func_declare" and symbol[2] == func_name):
                        if symbol[5] != call_parameters:
                            print("===== WARNING =====\nIn call function '", func_name,"', it's expected ",
                            symbol[5],", but received ", call_parameters,". See line ", line, sep="")


    def walking(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR_DECLARE":
                self.addVarDeclareSymbolTable(node)
            if node.tokenval == "NUMERO_INTEIRO":
                node.data_type = "inteiro"
            elif node.tokenval == "NUMERO_FLUTUANTE" :
                node.data_type = "flutuante"
            elif node.tokenval == "NOTACAO_CIENTIFICA":
                node.data_type = "flutuante"
            elif node.name == "VAR" and node.parent.name != "VAR_LIST":
                self.annotateVarTypes(node)
            elif node.name == "PARAMETER_LIST_STMT":
                self.addParameterSymbolTable(node)
            elif node.name == "FUNCTION_DECLARATION":
                self.addFunctionDeclaredSymbolTable(node)

        for node in PostOrderIter(self.syntax_tree):
            if node.name == "EXPRESSION":
                self.annotateExpressionTypes(node)
        self.hasIndexError()
        self.hasReturnError()
        self.hasUndeclaredFunction()
        self.hasErrorNumberParametersCallFunction()
        self.hasErrorUndefinedVariable()
        self.isMainDeclared()
        self.warningCastingTypes()
        self.warningUnusedVars()
        self.warningVariableDeclaredMoreThanOneTime()
        self.warningNonInitializedVariable()
        self.hasCallMainError()
        self.warningUnusedDefinedFunction()
        self.warningParameterTypes()
        
    
    


    def removeVariableDeclarations(self, tree=Node):
        for node in PreOrderIter(tree):
            if node.name == "ACTION_STMT" and node.children[0].name == "VAR_DECLARE":
                node.parent = None
            elif node.name == "VAR_DECLARE":
                node.parent = None
    

    
    def cuttingLeafs(self, tree=Node):
        for node in PreOrderIter(tree):
            if node.name == "RETURN":
                node.parent = None
            elif node.name == "OPEN_PARENTHESES" or node.name == "CLOSE_PARENTHESES":
                node.parent = None
            elif node.name == "TYPE":
                node.parent = None
            elif node.name == "COMMA":
                node.parent = None
            elif node.name == "TWO_DOTS":
                node.parent = None
            elif node.name == "END":
                node.parent = None
            

    def treeHasElement(self, element=str):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == element:
                return True
        return False


    def cutting(self, node, subtree):
        node.parent = None
        parent = subtree.parent
        node.parent = parent
        subtree.parent = None


    def cuttingVarNodes(self, tree=Node):
        nodeName = "VAR"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingVarNodes(self.syntax_tree)
                else:
                    break
        nodeName = "FACTOR"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingVarNodes(self.syntax_tree)
                else:
                    break
        nodeName = "NOT_FACTOR"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingVarNodes(self.syntax_tree)
                else:
                    break
        nodeName = "UNARY_EXPRESSION"
        for node in PreOrderIter(tree):
            if node.name ==  nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                   self.cuttingVarNodes(self.syntax_tree)
                else:
                    break


    def cuttingExpressionStatementsNodes(self, tree=Node):
        nodeName = "MULTIPLICATIVE_EXPRESSION_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName  and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "ADDITIVE_STATEMENT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "ADDITIVE_EXPRESSION_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "SIMPLE_EXPRESSION_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "LOGIC_EXPRESSION_STMT"
        for node in PreOrderIter(tree): 
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "FACTOR_EXPRESSION_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "EXPRESSION"
        for node in PreOrderIter(tree):      
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "ASSIGNMENT_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "ACTION_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingExpressionStatementsNodes(self.syntax_tree)
                else:
                    break
                            

    def cuttingParameterStatementsNodes(self, tree=Node):
        nodeName = "PARAMETER_STATEMENT_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingParameterStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "PARAMETER_STMT"
        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                n = node.children[0]
                self.cutting(n, node)
                if self.treeHasElement(nodeName):
                    self.cuttingParameterStatementsNodes(self.syntax_tree)
                else:
                    break
        nodeName = "PARAMETER_LIST_STMT"

        for node in PreOrderIter(tree):
            if node.name == nodeName and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(nodeName):
                        self.cuttingParameterStatementsNodes(self.syntax_tree)
                    else:
                        break


    
    def cuttingFunctionNodes(self, tree=Node):
            # remover header
            nodeName = "HEADER"
            for node in PreOrderIter(tree):
                if node.name == nodeName and len(node.children) ==  1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(nodeName):
                        self.cuttingFunctionNodes(self.syntax_tree)
                    else:
                        break
            nodeName = "FUNCTION_DECLARATION"
            for node in PreOrderIter(tree):
                if node.name == nodeName and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(nodeName):
                        self.cuttingFunctionNodes(self.syntax_tree)
                    else:
                        break
            nodeName = "DECLARATION_LIST"
            for node in PreOrderIter(tree):
                if node.name == nodeName:
                    for n in node.children:
                        parent = node.parent
                        n.parent = parent
                    node.parent = None
                    break

            for node in PreOrderIter(tree):
                if "HEADER" in node.name:
                    node.name = "FUNCTION"
                elif "PARAMETER" in node.name:
                    node.name = "PARAMETERS"
                elif "RETURN" in node.name:
                    node.name = "RETURN"
                elif "BODY" in node.name:
                    node.name = "BODY"

    '''
    ================== To Do ======================
            # remover function_declaration
            # remover declaration_list
    def cuttingCallFunctionNodes(self, tree=Node):
        # remover Call_function
        # remover argument_statement
    ==============================================='''

    def cuttingTree(self):
        tree = self.syntax_tree

        self.removeVariableDeclarations(tree)
        self.cuttingLeafs(tree)
        self.cuttingVarNodes(tree)
        self.cuttingExpressionStatementsNodes(tree)
        self.cuttingParameterStatementsNodes(tree)
        self.cuttingFunctionNodes(tree)
        #self.cuttingExpression(tree)



       
        

                    
                



        









        