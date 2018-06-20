from anytree import Node, PreOrderIter, PostOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.SymbolTable = []
        self.defineScopes()
        self.walking()
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
            and node.children[0].name != "VAR_INDEX_STMT" and node.children[0].name != "NEGATIVE_VAR"):
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
        for symbol in self.SymbolTable:
            if symbol[0] == "func_declare":
                hasError = True
                hasReturn = False
                for node in PreOrderIter(self.syntax_tree):
                    if (symbol[3] == node.scope and node.name == "EXPRESSION" 
                    and node.parent.name == "RETURN_STMT"):
                        if(symbol[1] == node.data_type):
                            hasError = False
                        else:
                            if(symbol[1] == "inteiro" and node.data_type == "flutuante"):
                                message = ("===== WARNING =====\nIn function " + symbol[2] + 
                                ": It should return inteiro, but "
                                + "It returns flutuante. The return value will be casted to inteiro")
                                print(message)
                            elif(symbol[1] == "flutuante" and node.data_type == "inteiro"):
                                message = ("===== WARNING =====\nIn function " + symbol[2] + ": It should return flutuante, but "
                                + "It returns inteiro. The return value will be casted to flutuante")
                                print(message)
                            elif (symbol[1] == "vazio" and node.data_type == "inteiro"):
                                message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return vazio, but "
                                + "It returns inteiro")
                                print(message)
                            elif(symbol[1] == "vazio" and node.data_type == "flutuante"):
                                message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return vazio, but "
                                + "It returns flutuante")
                                print(message)
                            hasReturn = True
                    if (symbol[3] in node.scope and symbol[3] != node.scope and node.name == "EXPRESSION" 
                    and node.parent.name == "RETURN_STMT"):
                        if(symbol[1] == "inteiro" and node.data_type == "flutuante"):
                            message = ("===== WARNING =====\nIn function " + symbol[2] + 
                            ": It should return inteiro, but "
                            + "It returns flutuante. The return value will be casted to inteiro. See line " + 
                            str(node.parent.children[0].line))
                            print(message)
                        elif(symbol[1] == "flutuante" and node.data_type == "inteiro"):
                            message = ("===== WARNING =====\nIn function " + symbol[2] + ": It should return flutuante, but "
                            + "It returns inteiro. The return value will be casted to flutuante. See line " 
                            + str(node.parent.children[0].line))
                            print(message)
                        elif (symbol[1] == "vazio" and node.data_type == "inteiro"):
                            message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return vazio, but "
                            + "It returns inteiro. See line " + str(node.parent.children[0].line))
                            print(message)
                        elif(symbol[1] == "vazio" and node.data_type == "flutuante"):
                            message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return vazio, but "
                            + "It returns flutuante. See line " + str(node.parent.children[0].line))
                            print(message)


                if(hasReturn == False and symbol[1] == "vazio"):
                        hasError = False
                if hasError:
                    
                    if(symbol[1] == "inteiro" and hasReturn == False):
                        message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return inteiro, but "
                        + "It returns vazio")
                        print(message)
                    elif(symbol[1] == "flutuante" and hasReturn == False):
                        message = ("===== ERROR =====\nIn function " + symbol[2] + ": It should return flutuante, but "
                        + "It returns vazio")
                        print(message)
                    

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
                if(nodeVar.name == "NEGATIVE_VAR"):
                    nodeVar = node.children[0].children[1]
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
                if len(node.children) == 1:
                    if node.children[0].name != "NEGATIVE_VAR":
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
        
     
    def cuttingLeafs(self, tree=Node):
        nodeName = ["RETURN","OPEN_PARENTHESES","CLOSE_PARENTHESES","TYPE","COMMA",
        "TWO_DOTS","END", "WRITE", "READ", "UNTIL", "FOR"]
        for node in PreOrderIter(tree):
            if node.name in nodeName:
                node.parent = None

        for node in PreOrderIter(tree):
            if "WRITE" in node.name:
                node.name = "WRITE"
            elif "READ" in node.name:
                node.name = "READ"
            

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
        nodeName = ["VAR", "FACTOR", "NOT_FACTOR", "UNARY_EXPRESSION"]
        for name in nodeName:
            for node in PreOrderIter(tree):
                if node.name == name and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(name):
                        self.cuttingVarNodes(self.syntax_tree)
                    else:
                        break
        nodeName = ["VAR_LIST","INDEX_STMT","VAR_INDEX_STMT"]
        for node in PreOrderIter(tree):
            if node.name in nodeName:
                for n in node.children:
                    parent = node.parent
                    n.parent = parent
                node.parent = None
                if self.treeHasElement(node.name):
                    self.cuttingVarNodes(self.syntax_tree)
                else:
                    break
        nodeName = ["OPEN_BRACKET","CLOSE_BRACKET", "NOT"]
        for node in PreOrderIter(tree):
            if node.name in nodeName:
                node.parent = None
            elif (node.name == "MINUS" and 
            (node.parent.name == "NEGATIVE_VAR" or node.parent.name == "NEGATIVE_NUMBER")):
                node.parent = None


    def cuttingExpressionStatementsNodes(self, tree=Node):
        nodeName = ["MULTIPLICATIVE_EXPRESSION_STMT","ADDITIVE_STATEMENT","ADDITIVE_EXPRESSION_STMT",
        "SIMPLE_EXPRESSION_STMT", "LOGIC_EXPRESSION_STMT","FACTOR_EXPRESSION_STMT","EXPRESSION",
        "ASSIGNMENT_STMT","ACTION_STMT"]
        for name in nodeName:
            for node in PreOrderIter(tree):
                if node.name == name  and len(node.children) == 1 and "CONDITIONAL" not in node.parent.name:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(name):
                        self.cuttingExpressionStatementsNodes(self.syntax_tree)
                    else:
                        break
                            

    def cuttingParameterStatementsNodes(self, tree=Node):
        nodeName = ["PARAMETER_STATEMENT_STMT","PARAMETER_STMT","PARAMETER_LIST_STMT"]
        for name in nodeName:
            for node in PreOrderIter(tree):
                if node.name == name and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(name):
                        self.cuttingParameterStatementsNodes(self.syntax_tree)
                    else:
                        break   
        
    
    def cuttingFunctionNodes(self, tree=Node):
            nodeName = ["HEADER", "FUNCTION_DECLARATION"]
            for name in nodeName:
                for node in PreOrderIter(tree):
                    if node.name == name and len(node.children) ==  1:
                        n = node.children[0]
                        self.cutting(n, node)
                        if self.treeHasElement(name):
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
            
            nodeName = "PARAMETER_LIST_STMT"
            for node in PreOrderIter(tree):
                if node.name == nodeName:
                    node.parent = None
            
            nodeName = "BODY_STMT"
            for node in PreOrderIter(tree):
                if node.name == nodeName:
                    parent = node.parent
                    for n in node.children:
                        n.parent = parent
                    node.parent = None
                    if self.treeHasElement(nodeName):
                        self.cuttingFunctionNodes(self.syntax_tree)
                    else:
                        break

            for node in PreOrderIter(tree):
                if "HEADER" in node.name:
                    node.name = "FUNCTION"
                elif "RETURN" in node.name:
                    node.name = "RETURN"
            
            for node in PreOrderIter(tree):
                if node.name == "FUNCTION" and node.children[0].name == "ID":
                        for n in node.children:
                            if n.name != "ID":
                                n.parent = node.children[0]
                        node.children[0].parent = node.parent
                        node.parent = None


    def cuttingCallFunctionNodes(self, tree=Node):
        nodeName = ["ARGUMENT_STATEMENT_STMT", "CALL_FUNCTION_STMT"]
        for name in nodeName:
            for node in PreOrderIter(tree):
                if node.name == name and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(name):
                        self.cuttingCallFunctionNodes(self.syntax_tree)
                    else:
                        break

        for node in PreOrderIter(tree):
            if node.name == "ARGUMENT_LIST_STMT":
                parent = node.parent
                for n in node.children:
                    n.parent = parent
                node.parent = None
                if self.treeHasElement("ARGUMENT_LIST_STMT"):
                    self.cuttingCallFunctionNodes(self.syntax_tree)
                else:
                    break
        for node in PreOrderIter(tree):
            if "CALL_FUNCTION" in node.name:
                node.name = "CALL_FUNCTION"
        
    
    def cuttingRepeatNodes(self, tree=Node):
        nodeName = ["REPEAT_STMT", "SIMPLE_STATEMENT"]
        for name in nodeName:
            for node in PreOrderIter(self.syntax_tree):
                if node.name == name and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n, node)
                    if self.treeHasElement(name):
                        self.cuttingRepeatNodes(self.syntax_tree)
                    else:
                        break
        for node in PreOrderIter(tree):
            if "REPEAT" in node.name:
                node.name = "REPEAT" 


    def cuttingConditionalNodes(self, tree=Node):
        nodeName = ["CONDITIONAL_STMT", "EXPRESSION", "THEN"]#,"EXPRESSION", "IF"
        for name in nodeName:
            for node in PreOrderIter(tree):
                if node.name == name and len(node.children) == 1:
                    n = node.children[0]
                    self.cutting(n,node)
                    if self.treeHasElement(name):
                        self.cuttingConditionalNodes(self.syntax_tree)
                    else:
                        break
        
        for node in PreOrderIter(tree):
            if node.name == "IF" or node.name == "THEN":
                node.parent = None
            elif "CONDITIONAL" in node.name:
                node.name = "CONDITIONAL" 
        
        for node in PreOrderIter(tree):
            if "CONDITIONAL" in node.name:
                node.name = "CONDITIONAL"



    def cuttingTree(self):
        tree = self.syntax_tree
        self.cuttingLeafs(tree)
        self.cuttingVarNodes(tree)
        self.cuttingExpressionStatementsNodes(tree)
        self.cuttingParameterStatementsNodes(tree)
        self.cuttingFunctionNodes(tree)
        self.cuttingCallFunctionNodes(tree)
        self.cuttingRepeatNodes(tree)
        self.cuttingConditionalNodes(tree)



       
        

                    
                



        









        