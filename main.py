from lexical.automata.Automata import automaton
from lexical.structure.token.Token import token

def printToken(token):
    print("tokentype:", token.tokentype)
    print("tokenval:", token.tokenval)
    print("lexeme:", token.lexeme)


if __name__ == "__main__":
    dfa = automaton()
    if dfa.getFloatNumberToken("12.\n") != None:
        token, line = dfa.getFloatNumberToken("12.23\n")
        printToken(token)
    source = "{comentatio aqui} resto da string"
    result = dfa.getTokenProcess(source)
    print(source)
    print(result)