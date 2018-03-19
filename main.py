#!/usr/bin/python3
import sys
from lexical.ScanLex import scanlex
from lexical.structure.token.Token import token


def printToken(token):
    print("<tokentype:", token.tokentype, "; tokenval:", token.tokenval,"; lexeme:", token.lexeme,"; line:", token.getNumberOfLine(),">")
  


def printTokenList(tokelist=[]):
    for token in tokenlist:
        printToken(token)

if __name__ == "__main__":


    lex = scanlex(sys.argv[1])
    tokenlist = lex.getTokenListProcess()
    printTokenList(tokenlist)
    

