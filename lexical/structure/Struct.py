# -*- coding: utf-8 -*-
from enum import Enum

class Token(object):
    def __init__(self, lexeme=str, token_type=""):
        self.lexeme = lexeme
    
    
    def __setTokenValue(self, lexeme=str, token_type=""):
        if token_type == "":
            self.tokenval = TokenValue(lexeme)


class TokenValue(Enum):
    IF = 'se'
    ELSE = 'senão'
    THEN = "então"
    END = "fim"
    FOR = "repita"
    RETURN = "retorna"
    UNTIL = "até"
    READ = "leia"
    WRITE = "escreva"
    FLOAT_TYPE = "tipo_flutuante"
    INTEGER_TYPE = "tipo_inteiro"
    PLUS = "+"
    MINUS = "-"
    TIMES = "*"
    DIVISION = "/"
    LOGIC_EQUALS = "="
    COMMA = ","
    ASSIGNMENT = ":="
    LESS = "<"
    LESS_EQUALS = "<="
    HIGHER = ">"
    HIGHER_EQUALS = ">="
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    TWO_DOTS = ":"
    OPEN_BRACKETS = "["
    CLOSE_BRACKETS = "]"
    LOGIC_AND = "&&"
    LOGIC_OR = "||"
    LOGIC_NOT = "!"
    INTEGER_NUMBER = "numero_inteiro"
    FLOAT_NUMBER = "numero_flutuante"
    IDENTIFICATOR = "id"
    SCIENTIFIC_NOTATION = "notacao_cientifica"

