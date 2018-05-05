#!/home/costa/.anaconda3/bin/python3.6.4
import sys
from lexical.ScanLex import scanlex
from lexical.structure.token.Token import token
from syntax.Syntax import syntax_scanner

def printToken(token, option):
    if "txt" == option:     
        print("<tokentype:", token.tokentype, "; tokenval:", token.tokenval,"; lexeme:", token.lexeme,"; line:", token.getNumberOfLine(),">")
    elif "csv" == option:
        print(token.tokentype,",",token.tokenval,",",token.lexeme,",",token.getNumberOfLine())
  


def printTokenList(option, tokenlist=[]):
    for token in tokenlist:
        printToken(token, option)

if __name__ == "__main__":

    lex = scanlex(sys.argv[1])
    option = sys.argv[2]
    
    tokenlist = lex.getTokenListProcess()
    printTokenList(option, tokenlist)

    syntax = syntax_scanner()

    print(syntax.isAProgram(tokenlist))

    

