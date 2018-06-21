from llvmlite import ir
from anytree import Node, PreOrderIter

class code_gen(object):

    def __init__(self, moduleName=str, abstract_tree=Node, symbolTable=[]):
        self.moduleName = moduleName
        self.ast = abstract_tree
        self.st = symbolTable
        self.module = ir.Module(moduleName + ".bc")
    
            
    
    def saveModule(self):
        with open(self.moduleName + ".ll", 'w') as file:
            file.write(str(self.module))
            file.close()
    
    

    def getVarType(self, nodeVar):
        dtype = None
        for sb in self.st:
            if (sb[0] == "var_declare" and sb[2] == nodeVar.lexeme and 
            sb[3] in nodeVar.scope and nodeVar.line >= sb[4]):
                dtype =  sb[1]
        
        return ir.IntType(64) if dtype == "inteiro" else ir.FloatType()


    def initializeGlobalVars(self, gVar):
        if gVar.value_type == ir.IntType(64):
            gVar.initializer = ir.Constant(ir.IntType(64), 0)
        else:
            gVar.initializer = ir.Constant(ir.FloatType(), 0.0)
        gVar.linkage = "common"
        gVar.align = 8

    def declareGlobalVariables(self, node=Node):
        self.globalVars = []
        for n in node.children:
            dtype = self.getVarType(n)
            gVar = ir.GlobalVariable(self.module, dtype, name=n.lexeme)
            self.initializeGlobalVars(gVar)
            self.globalVars.append(gVar)
    
    def getType(self,dtype=str):
        if dtype == "flutuante":
            return ir.FloatType()
        elif dtype == "inteiro":
            return ir.IntType(64)
        elif dtype == "vazio":
            return ir.VoidType()
        else:
            return None

   
    def declareFuncHeader(self, nodeFunc=Node):
        for sb in self.st:
            if (sb[0] == "func_declare" and sb[2] == nodeFunc.lexeme and  sb[3] == nodeFunc.scope):
                dtype_r = sb[1]
                
                if len(sb[5]) == 0:
                    param = None
                else:
                    param = []
                    for p in sb[5]:
                        param.append(self.getType(p))
                dtype_r = self.getType(dtype_r)
                if param != None:
                    fnty = ir.FunctionType(dtype_r,param)
                else:
                    fnty = ir.FunctionType(dtype_r,())
                func = ir.Function(self.module,fnty,name=nodeFunc.lexeme)
                return func
    
    
    def declareVar(self, varDeclareNode=Node, builder=ir.IRBuilder):
        for n in varDeclareNode.children:
            dtype = self.getVarType(n)
            builder.alloca(dtype, n.lexeme)
    

    def doAssignment(self, assignNode=Node, builder=ir.IRBuilder):
        pass


    def declareFunctionsBlock(self, nodeFunc=Node):
        func = self.declareFuncHeader(nodeFunc)
        entryBlock = func.append_basic_block('entry')
        endBasicBlock = func.append_basic_block('exit')
        builder = ir.IRBuilder(entryBlock)
        for node in PreOrderIter(nodeFunc):
            if node.name == "VAR_DECLARE":
                self.declareVar(node, builder)



    
    def walking(self):
        for node in PreOrderIter(self.ast):
            if node.name == "VAR_DECLARE" and node.parent.name == "PROGRAM":
                self.declareGlobalVariables(node)
            elif node.name == "ID" and node.parent.name == "PROGRAM":
                self.declareFunctionsBlock(node)

        

