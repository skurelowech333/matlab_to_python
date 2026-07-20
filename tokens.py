from __future__ import annotations

# -*- coding: utf-8 -*-

"""
tokens.py

Token definitions for the MATLAB-to-Python translator.

Defines:
    - TokenType enum
    - Token dataclass
    - MATLAB keyword lookup
    - Operator lookup
"""

from dataclasses import dataclass
from enum import Enum, auto


# ==========================================================
# Token Types
# ==========================================================

class TokenType(Enum):

    # ---------- Special ----------

    EOF = auto()
    NEWLINE = auto()


    # ---------- Identifiers ----------

    IDENTIFIER = auto()


    # ---------- Literals ----------

    NUMBER = auto()
    STRING = auto()


    # ---------- Keywords ----------

    FUNCTION = auto()

    IF = auto()
    ELSEIF = auto()
    ELSE = auto()

    FOR = auto()
    WHILE = auto()

    SWITCH = auto()
    CASE = auto()
    OTHERWISE = auto()

    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()

    END = auto()

    TRY = auto()
    CATCH = auto()

    GLOBAL = auto()
    PERSISTENT = auto()


    # ---------- Classes ----------

    CLASSDEF = auto()
    PROPERTIES = auto()
    METHODS = auto()
    EVENTS = auto()


    # ---------- Operators ----------

    PLUS = auto()
    MINUS = auto()

    TIMES = auto()
    DIVIDE = auto()
    POWER = auto()

    ELEMENT_TIMES = auto()
    ELEMENT_DIVIDE = auto()
    ELEMENT_POWER = auto()


    ASSIGN = auto()


    EQUAL = auto()
    NOT_EQUAL = auto()


    LESS = auto()
    LESS_EQUAL = auto()

    GREATER = auto()
    GREATER_EQUAL = auto()


    AND = auto()
    OR = auto()
    NOT = auto()


    TRANSPOSE = auto()

    COLON = auto()


    # ---------- Delimiters ----------

    LPAREN = auto()
    RPAREN = auto()

    LBRACKET = auto()
    RBRACKET = auto()

    LBRACE = auto()
    RBRACE = auto()


    COMMA = auto()
    SEMICOLON = auto()

    DOT = auto()

    AT = auto()


    # ---------- Comments ----------

    COMMENT = auto()



# ==========================================================
# Token
# ==========================================================

@dataclass(slots=True)
class Token:

    type: TokenType

    value: str

    line: int

    column: int


    def __str__(self):

        return (
            f"{self.type.name}"
            f"('{self.value}') "
            f"[{self.line}:{self.column}]"
        )


    __repr__ = __str__



# ==========================================================
# MATLAB Keywords
# ==========================================================

KEYWORDS = {

    "function": TokenType.FUNCTION,


    "if": TokenType.IF,
    "elseif": TokenType.ELSEIF,
    "else": TokenType.ELSE,


    "for": TokenType.FOR,
    "while": TokenType.WHILE,


    "switch": TokenType.SWITCH,
    "case": TokenType.CASE,
    "otherwise": TokenType.OTHERWISE,


    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,

    "return": TokenType.RETURN,


    "end": TokenType.END,


    "try": TokenType.TRY,
    "catch": TokenType.CATCH,


    "global": TokenType.GLOBAL,

    "persistent": TokenType.PERSISTENT,


    # MATLAB classes

    "classdef": TokenType.CLASSDEF,

    "properties": TokenType.PROPERTIES,

    "methods": TokenType.METHODS,

    "events": TokenType.EVENTS,

}



# ==========================================================
# Operator Lookup
# ==========================================================

OPERATORS = {

    "+": TokenType.PLUS,

    "-": TokenType.MINUS,


    "*": TokenType.TIMES,

    "/": TokenType.DIVIDE,

    "^": TokenType.POWER,


    ".*": TokenType.ELEMENT_TIMES,

    "./": TokenType.ELEMENT_DIVIDE,

    ".^": TokenType.ELEMENT_POWER,


    "=": TokenType.ASSIGN,


    "==": TokenType.EQUAL,

    "~=": TokenType.NOT_EQUAL,


    "<": TokenType.LESS,

    "<=": TokenType.LESS_EQUAL,


    ">": TokenType.GREATER,

    ">=": TokenType.GREATER_EQUAL,


    "&&": TokenType.AND,

    "||": TokenType.OR,


    "~": TokenType.NOT,


    "'": TokenType.TRANSPOSE,


    ":": TokenType.COLON,


    "(": TokenType.LPAREN,

    ")": TokenType.RPAREN,


    "[":

        TokenType.LBRACKET,

    "]":

        TokenType.RBRACKET,


    "{":

        TokenType.LBRACE,

    "}":

        TokenType.RBRACE,


    ",":

        TokenType.COMMA,


    ";":

        TokenType.SEMICOLON,


    ".":

        TokenType.DOT,


    "@":

        TokenType.AT,

}