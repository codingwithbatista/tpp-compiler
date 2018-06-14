from anytree import Node, PreOrderIter


class semantic_module(object):

    def __init__(self, syntax_tree=Node):
        self.syntax_tree = syntax_tree
        self.table = []
        self.scope_definition()
        self.declare_previous_verification()
        self.print_simbol_table()
        self.verify_semantic_errors()

    def printNode(self, node):
        if hasattr(node, 'lexeme'):
                print(node.name, node.lexeme, node.tokenval, node.scope)
        else:
            print(node.name, node.scope)


    def __defineScopeNode(self, node=Node, scope=str):
        for n in PreOrderIter(node):
            n.scope = scope


    def scope_definition(self):
        scope = "GLOBAL"
        local_scope_number = 1
        pre_scope = False
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "FUNCTION_DECLARATION":
                scope = "func" + str(local_scope_number)
                node.scope = scope
                local_scope_number += 1
            
            elif node.name == "CONDITIONAL_STMT":
                if hasattr(node, 'scope') == False:
                    scope = scope + ".conditional"
                    node.scope = scope
            
            elif node.name == "REPEAT_STMT":
                if hasattr(node, 'scope') == False:
                    scope = scope + ".repeat"
                    node.scope = scope
            
            elif node.name == "IF":
                if hasattr(node, 'scope') == False:
                    scope = scope + ".if"
                    node.scope = scope
            
            elif node.name == "UNTIL":
                if hasattr(node, 'scope') == False:
                    node.scope = scope
                    pre_scope = True

            elif node.name == "ELSE":
                if hasattr(node, 'scope') == False:
                    finalIndex = scope.rfind("if")
                    scope = scope[:finalIndex]
                    scope = scope + "else"
                    node.scope = scope
            
            elif node.name == "END":
                if hasattr(node, 'scope') == False:
                    node.scope = scope
                    finalIndex = scope.rfind(".")
                    scope = scope[:finalIndex]

            elif node.name == "EXPRESSION" and pre_scope:
                if hasattr(node, 'scope') == False:
                    node.scope = scope
                    finalIndex = scope.rfind(".")
                    self.__defineScopeNode(node, scope)
                    scope = scope[:finalIndex]
                    pre_scope = False
                
            else:
                if hasattr(node, 'scope') == False:
                    node.scope = scope


    def declareVariable_annotation_table(self, node=Node):
        scope = node.scope
        type_operation = "VAR_DECLARATION"
        for n in PreOrderIter(node):
            if n.name == "TYPE":
                data_type = n.tokenval
            elif n.name == "ID":
                variable = n.lexeme
                line = n.line
                self.table.append([type_operation, scope, data_type, variable, line])

    
    def declareFunction_annotation_table(self, node=Node):
        scope = node.scope
        type_operation = "FUNC_DECLARATION"
        for n in PreOrderIter(node, maxlevel=4):
            if n.name == "TYPE":
                func_type = n.tokenval
            elif n.name == "ID":
                func = n.lexeme
                line = n.line
                self.table.append([type_operation, scope, func_type, func, line])



    def declare_previous_verification(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR_DECLARE":
                self.declareVariable_annotation_table(node)
            
            elif node.name == "FUNCTION_DECLARATION":
                self.declareFunction_annotation_table(node)

    
    def verify_variable_declared(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name == "VAR":
                findVarDeclaration = False
                var_node = node.children[0]

                for line in self.table:
                    if hasattr(var_node, 'lexeme'):
                        if ((line[0] == "VAR_DECLARATION") and (line[3] == var_node.lexeme) and
                        ((line[1] in var_node.scope) or (line[1] == "GLOBAL"))):
                            findVarDeclaration = True
                if findVarDeclaration == False:
                    self.print_error_non_declared_var(var_node)

    
    def verify_function_declared(self):
        for node in PreOrderIter(self.syntax_tree):
            if node.name  == "CALL_FUNCTION_STMT":
                findFunctionDeclaration = False
                id_nome_func_node = node.children[0]
                id_nome_func_node = id_nome_func_node.children[0]

                for line in self.table:
                    if hasattr(id_nome_func_node, 'lexeme'):
                        if((line[0] == "FUNC_DECLARATION") and (line[3] == id_nome_func_node.lexeme)):
                            findFunctionDeclaration = True
                if findFunctionDeclaration == False:
                    self.print_error_non_declared_function(id_nome_func_node)


    def verify_semantic_errors(self):
        self.verify_variable_declared()
        self.verify_function_declared()


    def walking_syntaxtree(self):
        for node in PreOrderIter(self.syntax_tree):
            self.printNode(node)

    def print_simbol_table(self):
        for line in self.table:
            print(line)

    def print_error_non_declared_var(self, node=Node):
        print("In line ", node.line, ": variable '", node.lexeme,
        "' is not declared previously.", sep="")
    

    def print_error_non_declared_function(self, node=Node):
        print("In line", node.line, ": function '", node.lexeme,
        "' is not declared previously.", sep="")