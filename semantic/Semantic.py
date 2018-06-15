from anytree import Node, PreOrderIter, PostOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.table = []
        self.defineScopes()
        self.defineDataTypes()
        
        self.printVariableDefinedTable()
        self.verifyVariableNotDeclared()
        self.verifyVariableUses()
        self.verifyVariableAlreadyDefined()
        self.defineExpressionDataType()
        self.printTree()
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
            print("name:",node.name,"|", "scope:",node.scope)


    def printTree(self):
        for node in PreOrderIter(self.syntax_tree):
            self.printNode(node)


    def printVariableDefinedTable(self):
        for line in self.definedVariableTable:
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
    
    def defineExpressionDataType(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "SUM_OPERATOR":
                node.data_type = self.defineSumDataType(node)
                print(node.data_type)
    

    def defineSumDataType(self, sumNode=Node):
        childA = sumNode.children[0]
        childB = sumNode.children[1]
        data_typeA = ""
        for node in PreOrderIter(childA):
            if node.name == "ID":
                data_typeA = node.data_type
        
        for node in PreOrderIter(childB):
            if node.name == "ID":
                data_typeB = node.data_type
        
        if(data_typeA == "flutuante" or data_typeB == "flutuante"):
            sum_datatype = "flutuante"
        else:
            sum_datatype = "inteiro"
        
        return sum_datatype



        