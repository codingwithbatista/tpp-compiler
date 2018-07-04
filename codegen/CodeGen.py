from llvmlite import ir
from anytree import Node, PreOrderIter

class code_gen(object):

    def __init__(self, moduleName=str, abstract_tree=Node, symbolTable=[]):
        
        self.moduleName = moduleName
        self.ast = abstract_tree
        self.st = symbolTable
        self.cond = 0
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
                funcName = "main" if nodeFunc.lexeme == "principal" else nodeFunc.lexeme
                func = ir.Function(self.module,fnty,name=funcName)
                return func
    
    
    def declareVar(self, varDeclareNode=Node, builder=ir.IRBuilder):
        var = []
        for n in varDeclareNode.children:
            dtype = self.getVarType(n)
            v = builder.alloca(dtype, name=n.lexeme)
            v.scope = varDeclareNode.scope
            var.append(v)
        return var

    def doAssignment(self, assignNode=Node, fvars=[],builder=ir.IRBuilder):
        if len(assignNode.children) == 2:
            if assignNode.children[1].name == "NUMBER":
                nodeNumber = assignNode.children[1]
                var = 0
                dtype = ir.IntType(64) if assignNode.children[0].data_type == "inteiro" else ir.FloatType()
                numVal = int(nodeNumber.lexeme) if assignNode.children[0].data_type == "inteiro" else float(nodeNumber.lexeme)
                for v in fvars:
                    if v.name == assignNode.children[0].lexeme and v.scope in assignNode.scope:
                        var = v
                if var:
            
                    builder.store(ir.Constant(dtype, numVal), var)
                else: 
                    for var in self.globalVars:
                        if var._name == assignNode.children[0].lexeme:
                            builder.store(ir.Constant(dtype, numVal), var)
            elif assignNode.children[1].name == "ID":
                print("aqui")
                dtype = ir.IntType(64) if assignNode.children[0].data_type == "inteiro" else ir.FloatType()
                var = 0
                var2  = 0
                for v in fvars:
                    if v.name == assignNode.children[0].lexeme and v.scope in assignNode.scope:
                        var = v
                    if v.name == assignNode.children[1].lexeme and v.scope in assignNode.scope:
                        var2 = v
                if var == 0:
                    for v in self.globalVars:
                        if v._name == assignNode.children[0].lexeme:
                            var = v
                if var2 == 0:
                    for v in self.globalVars:
                        if v._name == assignNode.children[1].lexeme:
                            var2 = v
                print("aqui")
                print(var2)
                var_tmp = builder.load(var2,"")
                builder.store(var_tmp,var)

                
    def doReturn(self, returnNode=Node, fvars=[], builder=ir.IRBuilder,  endBasicBlock=ir.Block):
        #builder.position_at_end(endBasicBlock)
        #builder.branch(endBasicBlock)
        builder.branch(endBasicBlock)
        builder = ir.IRBuilder(endBasicBlock)
        for v in fvars:
            print(v._name)
        if returnNode.children[0].lexeme == '0':
            returnVal = builder.alloca(ir.IntType(64), name='retorno')
            Zero64 = ir.Constant(ir.IntType(64), 0)
            builder.store(Zero64, returnVal)
            returnVal_tmp = builder.load(returnVal, name='', align=8)
            builder.ret(returnVal_tmp)
        elif returnNode.children[0].name == "ID":
            for v in fvars:
                if v._name == returnNode.children[0].lexeme:
                    var = v
            builder.ret(builder.load(var, ""))

    

    def getVar(self, nodeVar=Node, fvars=[]):
        var = 0
        for v in fvars:
            if v.name == nodeVar.lexeme and v.scope in nodeVar.scope:
                var = v
        if var == 0:
            for v in self.globalVars:
                if v.name == nodeVar.lexeme:
                    var = v
        
        dtype = ir.IntType(64) if nodeVar.data_type == "inteiro" else ir.FloatType()
        return var, dtype


    def doConditional(self, func, conditionalNode=Node, fvars=[], builder = ir.IRBuilder):
        iftru = func.append_basic_block('iftru_' + str(self.cond))
        iffalse = func.append_basic_block('iffalse_' + str(self.cond))
        #ifend = func.append_basic_block('ifend_' + str(self.cond))

        for node in conditionalNode.children:
            if node.name == "RELATIONAL_OPERATOR":
                relationalNode = node
            elif node.name == "ELSE":
                elseNode = node

        if relationalNode.children[0].name == "ID":
            var = self.getVar(relationalNode.children[0])[0]
            
            varA_cmp = builder.load(var,"varA_cmp", align=8)

        if relationalNode.children[1].name == "NUMBER":
            dtype = ir.IntType(64) if relationalNode.children[1].data_type == "inteiro" else ir.FloatType
            numVal = int(relationalNode.children[1].lexeme) if relationalNode.children[1].data_type == "inteiro" else float(node.lexeme)
            constB = ir.Constant(dtype, numVal)
            condName = "if_test_" + str(self.cond)
            
            if_cmp = builder.icmp_signed(relationalNode.lexeme, varA_cmp, constB, name=condName)
            
            builder.cbranch(if_cmp, iftru, iffalse)
            builder.position_at_end(iftru)
            for node in conditionalNode.children:
                if node.number < elseNode.number:
                    if node.name == "ASSIGNMENT":
                        self.doAssignment(node, fvars, builder)
            #builder.branch(ifend)
            
            #builder.position_at_end(iffalse)
            for node in conditionalNode.children:
                if node.number > elseNode.number:
                    if node.name == "ASSIGNMENT":
                        self.doAssignment(node, fvars, builder)
            #builder.branch(ifend)
            #builder.position_at_end(ifend)
        self.cond += 1



            
    

    def declareFunctionsBlock(self, nodeFunc=Node):
        func = self.declareFuncHeader(nodeFunc)
        entryBlock = func.append_basic_block('entry')
        endBasicBlock = func.append_basic_block('exit')
        builder = ir.IRBuilder(entryBlock)
        fvars = []
        for node in PreOrderIter(nodeFunc):
            if node.name == "VAR_DECLARE":
                var = self.declareVar(node, builder)
                for v in var:
                    fvars.append(v)
            elif node.name == "ASSIGNMENT":
                self.doAssignment(node, fvars, builder)
            elif node.name == "RETURN":
                self.doReturn(node, fvars, builder, endBasicBlock)
            elif node.name == "CONDITIONAL":
                self.doConditional(func, node, fvars, builder)
                



    
    def walking(self):
        for node in PreOrderIter(self.ast):
            if node.name == "VAR_DECLARE" and node.parent.name == "PROGRAM":
                self.declareGlobalVariables(node)
            elif node.name == "ID" and node.parent.name == "PROGRAM":
                self.declareFunctionsBlock(node)

        

