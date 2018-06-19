#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from lexical.ScanLex import scanlex
from lexical.structure.token.Token import token
from syntax.Syntax import syntax_process
from render.Render import tree_render
from semantic.Semantic import semantic_module


def printToken(token, option):
    if "txt" == option:     
        print("<tokentype:", token.tokentype, "; tokenval:", token.tokenval,"; lexeme:", token.lexeme,"; line:", token.getNumberOfLine(),">")
    elif "csv" == option:
        print(token.tokentype,",",token.tokenval,",",token.lexeme,",",token.getNumberOfLine())
  


def printTokenList(option, tokenlist=[]):
    for token in tokenlist:
        printToken(token, option)


def main():
    lex = scanlex(sys.argv[1])
    analise = sys.argv[2]
    
    #sm = semantic_module(syntax_tree)
    #sm.walking_syntaxtree()    

    if analise == "lexical":
        out_type = sys.argv[3]
        if (out_type != "txt") and (out_type != "csv"):
            print("Output file format is invalid. Please choose between txt or csv.")
        else:
            pass
            #printTokenList(out_type, tokenlist)
    elif analise == "syntax":
        tokenlist = lex.getTokenListProcess()
        syntax = syntax_process()
        syntax_tree = syntax.exec(tokenlist)
        if syntax_tree is not None:
            try:
                export = sys.argv[3]
                render = tree_render()
                out_name = sys.argv[4]
                if export == "img":             
                    render.exporToDotFile(syntax_tree, out_name)   
                    render.compileDotFile(out_name)

                    print("it was exported to dot file and compiled to png image file format")
                    
                elif export == "txt":
                    render.exportToTxtFile(syntax_tree, out_name)
                    print("it was exported to txt file")

                else:
                    print("invalid export option")
            except IndexError:
                if len(sys.argv) == 3:
                    render = tree_render()
                    render.renderTXT(syntax_tree)
                else:
                    print("too few arguments.")
    elif analise == "semantic":
        tokenlist = lex.getTokenListProcess()
        syntax = syntax_process()
        syntax_tree = syntax.exec(tokenlist)
        sm = semantic_module(syntax_tree)
        tree = sm.syntax_tree
        render = tree_render()
        render.exporToDotFile(tree, "out")   
        render.compileDotFile("out")

    else:
        print("Invalid analise option")

        


if __name__ == "__main__": main()

 

    

