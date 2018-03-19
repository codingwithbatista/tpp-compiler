from lexical.automata.Automata import automaton
from lexical.structure.token.Token import token


class scanlex(object):


    def __init__(self, filepath):
        self.filepath = filepath
    

    def getSourceCode(self):
        streamFile = open(self.filepath,'r',encoding="utf-8")
        return str(streamFile.read()).strip()
    

    def getTokenListProcess(self):
        dfa = automaton()
        streamFile = self.getSourceCode()
        return dfa.getTokenList(streamFile)