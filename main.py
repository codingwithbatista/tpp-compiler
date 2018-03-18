from lexical.automata.Automata import automaton
from lexical.structure.token.Token import token

def printToken(token):
    print("tokentype:", token.tokentype)
    print("tokenval:", token.tokenval)
    print("lexeme:", token.lexeme)


if __name__ == "__main__":
    dfa = automaton()
    source = ": vet[10]"
    result, j = dfa.getTokenProcess(source)
    print(result.tokentype)
    print(result.tokenval)
    print(result.lexeme)
    print(result.numberOfLine)
    print(result.numberOfColumn)
    print(j)

