# -*- coding: utf-8 -*-
class lex(object):

    def getToken(self, stream=str):
        if self.__isEndStopword(stream):
            print("é fim")
        elif self.__isFloatStopword(stream):
            print("é frutuante")
    
        
    def __isEndStopword(self, stream=str):
        try:
            if stream[0:3]:
                if len(stream) == 3:
                    return True
                else:
                    return True if (stream[3] == ' ' or stream[3] == '\n') else False
            else:
                return False
        except IndexError:
            return False


    def __isFloatStopword(self, stream=str):
        try:
            if stream[0:9] == "flutuante":
                if len(stream) == 9:
                    return True
                else:
                    return True if (stream[9] == ' ' or stream[9] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    

    def __isIntStopword(self, stream=str):
        try:
            if stream[0:7] == "inteiro":
                if len(stream) == 7:
                    return True
                else:
                    return True if (stream[7] == ' ' or stream[7] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    
    
    def __isThenStopword(self, stream=str):
        try:
            if stream[0:5] == "então":
                if len(stream) == 5:
                    return True
                else:
                    return True if (stream[5] == ' ' or stream[5] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    

    def __isIfStopword(self, stream=str):
        try:
            if stream[0:2] == "se":
                if len(stream) == 2:
                    return True
                else:
                    return True if (stream[2] == ' ' or stream[2] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    
    
    def __isElseStopword(self, stream=str):
        try:
            if stream[0:5] == "senão":
                if len(stream) == 5:
                    return True
                else:
                    return True if (stream[5] == ' ' or stream[5] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    

    def __isForStopword(self, stream=str):
        try:
            if stream[0:6] == "repita":
                if len(stream) == 6:
                    return True
                else:
                    return True if (stream[6] == ' ' or stream[6] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    

    def __isUntilStopword(self, stream=str):
        try:
            if stream[0:3] == "até":
                if len(stream) == 3:
                    return True
                else:
                    return True if (stream[3] == ' ' or stream[3] == '\n') else False
            else:
                return False
        except IndexError:
            return False


    def __isWriteStopword(self, stream=str):
        try:
            if stream[0:7] == "escreva":
                if len(stream) == 7:
                    return True
                else:
                    return True if (stream[7] == ' ' or stream[7] == '\n') else False
            else:
                return False
        except IndexError:
            return False

    

    def __isReadStopword(self, stream=str):
        try:
            if stream[0:4] == "leia":
                if len(stream) == 4:
                    return True
                else:
                    return True if (stream[4] == ' ' or stream[4] == '\n') else False
            else:
                return False
        except IndexError:
            return False
    

    def __isReturnStopword(self, stream=str):
        try:
            if stream[0:7] == "retorna":
                if len(stream) == 7:
                    return True
                else:
                    return True if (stream[7] == ' ' or stream[7] == '\n') else False
            else:
                return False
        except IndexError:
            return False

    def __isInteiroStopword(self, stream=str):
        pass


                    

    def getTokenlist(self):
        pass
    
    
    


