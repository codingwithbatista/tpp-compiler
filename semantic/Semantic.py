from anytree import Node, PreOrderIter, PostOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.SymbolTable = []
        self.defineScopes()
        self.walking()
        #self.printTree()
        self.printTable(self.SymbolTable)
        

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
                variables.append(["var_declare",data_type,n.lexeme, n.scope, n.line])
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
            self.SymbolTable.append(p)


    def annotateVarTypes(self, varNode=Node):
        node = varNode.children[0]
        for line in self.SymbolTable:
            if line[0] == "var_declare" or line[0] == "parameter_func":
                if node.lexeme == line[2] and line[3] in node.scope:
                    node.data_type = line[1]


    def annotateExpressionTypes(self, exprNode=Node):
        for node in PreOrderIter(exprNode):
            if hasattr(node, 'data_type'):
                if node.data_type == "flutuante":
                    exprNode.data_type = "flutuante"
                    break
                elif node.data_type == "inteiro":
                    exprNode.data_type = "inteiro"
    
    
    def warningCastingTypes(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "ASSIGNMENT":
                leftNode = node.children[0].children[0]
                rightNode = node.children[1]
                if leftNode.data_type != rightNode.data_type:
                    print("===== WARNING =====\nIn line ", leftNode.line, " variable '", leftNode.lexeme,
                    "is ", leftNode.data_type, ", but received ", rightNode.data_type)

          
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


    def walking(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR_DECLARE":
                self.addVarDeclareSymbolTable(node)
            if node.tokenval == "NUMERO_INTEIRO":
                node.data_type = "inteiro"
            elif node.tokenval == "NUMERO_FLUTUANTE" :
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
        self.warningCastingTypes()
        self.isMainDeclared()


        









        