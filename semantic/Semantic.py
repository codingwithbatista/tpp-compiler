from anytree import Node, PreOrderIter, PostOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.table = []
        self.defineScopes()
        self.defineDataTypes()
        self.defineNumberDataType()
        #self.printVariableDefinedTable()
        self.verifyVariableNotDeclared()
        self.verifyVariableUses()
        self.verifyVariableAlreadyDefined()
        self.defineExpressionDataType()
        #self.printTree()
        self.verifyTypeAssignment()
        self.createDeclaredFunctionsTable()
        self.printFunctionsDefinedTable()
        self.verifyReturnType()
        #self.scope_definition()
        #self.declare_previous_verification()
        #self.print_simbol_table()
        #self.verify_semantic_errors()

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


    def printVariableDefinedTable(self):
        for line in self.definedVariableTable:
            print(line)


    def printFunctionsDefinedTable(self):
        for line in self.declaredFunctions:
            print(line)

    def defineScopes(self):
        scope = ""
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "PROGRAM":
                scope= "global"
                node.scope = scope
            
            elif node.name == "FUNCTION_DECLARATION":
                scope_name = node.children[1].children[0].children[0].lexeme
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
    

    def createDefinedVariableTable(self):
        table = []
        for node in PreOrderIter(self.syntax_tree):
            try:
                if node.op_type == "declaration" or node.op_type == "fnc_parameter":
                    table.append([node.number, node.scope, node.data_type, node.tokenval, node.lexeme, node.line, node.op_type])
            except AttributeError:
                pass

        self.definedVariableTable = table

    
    def delegateDataTypeToVarList(self, data_type=str, varListNode=Node):
        for node in PreOrderIter(varListNode):
            node.data_type = data_type
            node.op_type = "declaration"


    def delegateDataTypeToParameterFunction(self, data_type=str, varParameterNode=Node):
        varParameterNode.data_type = data_type
        varParameterNode.op_type = "fnc_parameter"
    
    def delegateDataTypeToDeclaredVariable(self, varNode):
        for line in self.definedVariableTable:
            if (line[1] in varNode.scope) and  (line[4] == varNode.lexeme):
                varNode.data_type = line[2]



    def defineDataTypes(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR_DECLARE" and node.children[2].children[0].children[0].name != "VAR_INDEX_STMT":
                data_type = node.children[0].lexeme
                self.delegateDataTypeToVarList(data_type, node.children[2])
            elif node.name == "PARAMETER_STATEMENT_STMT":
                data_type = node.children[0].lexeme
                self.delegateDataTypeToParameterFunction(data_type, node.children[2])
            #elif node.name == "VAR_INDEX_STMT":

            #    data_type = node.parent.parent.parent.children[0]

        self.createDefinedVariableTable()

        for node in PreOrderIter(self.syntax_tree):
            if node.name == "ID" and node.parent.parent.name != "VAR_LIST" and node.parent.name != "PARAMETER_STATEMENT_STMT":
                self.delegateDataTypeToDeclaredVariable(node)

    
    def isDeclaredVariable(self, nodeVar):
        if hasattr(nodeVar, 'data_type'):  
            return True
        return False

    
    def verifyVariableNotDeclared(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR" and node.children[0].name != "VAR_INDEX_STMT":
                
                isDeclaredVar = self.isDeclaredVariable(node.children[0])
                if isDeclaredVar == False:
                    print("In line ", node.children[0].line,":\n", "variable '", node.children[0].lexeme,"' is not declared", sep="")


    def isUsedVariable(self, line_variableDefinition):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR" and node.parent.name != "VAR_LIST" and node.children[0].name != "VAR_INDEX_STMT":
                varNode = node.children[0]
                if line_variableDefinition[1] in varNode.scope and line_variableDefinition[4] == varNode.lexeme:
                    return True
        return False


    def verifyVariableUses(self):
        for line in self.definedVariableTable:
            isUsed = self.isUsedVariable(line)
            if isUsed == False:
                print("In line ", line[5],":\n", "the variable '", line[4],"' is declared and unused", sep="")


    def verifyVariableAlreadyDefined(self):
        size = len(self.definedVariableTable)
        for i in range(size):
            for j in range(i+1, size):
                if (self.definedVariableTable[i][1] == self.definedVariableTable[i+1][1] and
                self.definedVariableTable[i][4]  == self.definedVariableTable[i+1][4]):
                    print("Variable '", self.definedVariableTable[i][4],"' is declared more than one time. See line ",
                    self.definedVariableTable[i][5]," and ",self.definedVariableTable[i+1][5], sep="")
    
        
    def defineNumberDataType(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "NUMBER":
                if node.tokenval == "NUMERO_INTEIRO":
                    node.data_type = "inteiro"
                elif node.tokenval == "NUMERO_FLUTUANTE":
                    node.data_type = "flutuante"
    
    
    def defineExpressionDataType(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "TIMES_OPERATOR" or node.name == "SUM_OPERATOR":
                node.data_type = self.verifyExpressionChildDataType(node)
        
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "EXPRESSION":
                node.data_type = self.verifyExpressionChildDataType(node)
    

    def verifyExpressionChildDataType(self, op_node=Node):
        for node in PreOrderIter(op_node):
            if hasattr(node, "data_type"):
                if node.data_type == "flutuante":
                    return "flutuante"
                elif node.data_type == "inteiro":
                    data_type = "inteiro"
        return data_type


    def verifyTypeAssignment(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "ASSIGNMENT":
                left = self.verifyExpressionChildDataType(node.children[0])
                right = self.verifyExpressionChildDataType(node.children[1])
                if (left == "inteiro" and right == "flutuante"):
                    print("warning: casting to inteiro, in line ", node.line, ":\nvariable '", node.children[0].children[0].lexeme,
                    "' is inteiro, but it receives flutuante data type.", sep="")
                elif (left == "flutuante" and right == "inteiro"):
                    print("warning: casting to flutuante, in line ", node.line, ":\nvariable '", node.children[0].children[0].lexeme,
                    "' is flutuante, but it receives inteiro data type.", sep="")
    

    def createDeclaredFunctionsTable(self):
        table = []
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "FUNCTION_DECLARATION":
                if node.children[0].name == "TYPE":
                    return_type = node.children[0].lexeme
                else:
                    return_type = "vazio"
                if node.children[1].children[0].children[0].name == "ID":
                    function_name = node.children[1].children[0].children[0].lexeme
                    scope = node.children[1].children[0].children[0].scope
                table.append([function_name, scope, return_type])
        self.declaredFunctions = table

    def verifyReturnType(self):
        for line in self.declaredFunctions:
            hasReturn = self.functionHasReturnType(line)
            if hasReturn[0] == False and line[2] != "vazio":
                print("deu aqui sem retorno")
            elif hasReturn[0] == True and line[2] != hasReturn[1]:
                print("Semantic Error in function '", line[0],"':\n", 
                "In line ", hasReturn[2], ", fuction should return ", line[2], " but it returns ",
                hasReturn[1],  sep="")
            

    

    def functionHasReturnType(self, functionDeclareLine=[]):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "RETURN_STMT" and node.scope == functionDeclareLine[1]:

                return True, node.children[2].data_type, node.children[0].line
        
        return False, "vazio"



        