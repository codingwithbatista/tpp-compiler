from llvmlite import ir
from anytree import Node, PreOrderIter

class code_gen(object):

    def __init__(self, moduleName=str, abstract_tree=Node, symbolTable=[]):
        self.moduleName = moduleName
        self.ast = abstract_tree
        self.st = symbolTable
        self.funcs = []
        self.module = ir.Module(moduleName + ".bc")
    

    def create_types(self):
        self.flutuante = ir.DoubleType()
        self.inteiro = ir.IntType(64)
        self.vazio = ir.VoidType()


    def getArgumentNames(self,scope=str):
        args = []
        for symbol in self.st:
            if symbol[0] == "parameter_func" and  symbol[3] == scope:
                args.append(symbol[2])
        return args

    def getArgTypes(self, args=[]):
        arg_types = []
        for a in args:
            if a == "inteiro":
                arg_types.append(self.inteiro)
            elif a == "flutuante":
                arg_types.append(self.flutuante)
        return arg_types

    
    def declareFunctions(self, nodeFunc=Node):
        symbolTable = self.st
        for symbol in symbolTable:
            if symbol[0] == "func_declare" and symbol[2] == nodeFunc.lexeme and symbol[3] == nodeFunc.scope:
                if symbol[1] == "inteiro":
                    func_return = self.inteiro
                elif symbol[1] == "flutuante":
                    func_return = self.flutuante
                
                elif symbol[1] == "vazio":
                    func_return = self.vazio
                
                
                if len(symbol[5]) == 0:
                    fnty = ir.FunctionType(func_return, ())                  
                else:
                    arg_types = self.getArgTypes(symbol[5])
                    fnty = ir.FunctionType(func_return, arg_types)
                func = ir.Function(self.module, fnty, name = nodeFunc.lexeme)
                self.funcs.append(func)
            
                #print()
                #self.funcs.append(func)


    def searchTypeInSymbolTable(self, varLexeme=str, scope=str):
        for sb in self.st:
            if sb[0] == "var_declare" and sb[3] == scope and sb[2] == varLexeme:
                return self.inteiro if "inteiro" == sb[1] else self.flutuante


    def declareGlobalVariables(self, nodeVarDeclare=Node):
        self.globalVariables = []
        for child in nodeVarDeclare.children:
            dtype = self.searchTypeInSymbolTable(child.lexeme, child.scope)
            var = ir.GlobalVariable(self.module, dtype, child.lexeme)
            var.initializer = ir.Constant(dtype, 0)
            var.linkage = "common"
            var.align = 4
            self.globalVariables.append(var)


    def getFunction(self, name=str):
        for f in self.funcs:
            if f._get_name == name:
                return f


    def defineMainBlocks(self, mainNode=Node):
        main = self.getFunction("principal")
        entryBlock = main.append_basic_block('entry')
        #endBasicBlock = main.append_basic_block('exit')
        
        builder = ir.IRBuilder(entryBlock)
        for child in PreOrderIter(mainNode):
            # declarar variavel
            # atribuicao
            # retorno




    def exec_codeGeneration_process(self):
        ast = self.ast
        self.create_types()
        for node in PreOrderIter(ast):
            if node.name == "ID" and node.parent.name == "PROGRAM":
                self.declareFunctions(node)
            elif node.name == "VAR_DECLARE" and node.parent.name == "PROGRAM":
                self.declareGlobalVariables(node)

    def saveModule(self):
        with open(self.moduleName + ".ll", 'w') as file:
            file.write(str(self.module))
            file.close()
            print(file)
        

