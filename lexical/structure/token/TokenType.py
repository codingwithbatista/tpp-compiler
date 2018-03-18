from enum import Enum


class TokenType(Enum):
    IF = "PR",
    ELSE = "PR"
    THEN = "PR"
    END = "PR"
    FOR = "PR"
    RETURN = "PR"
    UNTIL = "PR"
    READ = "PR"
    WRITE = "PR"
    INTEGER_TYPE = "PR"
    FLOAT_TYPE = "PR"
    PLUS = "SB"
    MINUS = "SB"
    TIMES = "SB"
    DIVISION = "SB"
    LOGIC_EQUALS = "SB"
    COMMA = "SB"
    ASSIGNMENT = "SB"
    LESS = "SB"
    LESS_EQUALS = "SB"
    HIGHER = "SB"
    HIGHER_EQUALS = "SB"
    OPEN_PARENTHESES = "SB"
    CLOSE_PARENTHESES = "SB"
    TWO_DOTS = "SB"
    OPEN_BRACKETS = "SB"
    FLOAT_NUMBER = "NUM"
    CLOSE_BRACKETS = "SB"
    LOGIC_AND = "SB"
    LOGIC_OR = "SB"
    LOGIC_NOT = "SB"
    INTEGER_NUMBER = "NUM"
    