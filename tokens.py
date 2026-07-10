from __future__ import annotations

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:40:27 2026

@author: Sarah
"""

"""
tokens.py

Token definitions for the MATLAB-to-Python translator.

This module defines the token types produced by the lexer and consumed by the
parser. Tokens are the smallest meaningful units of MATLAB source code, such as
keywords, identifiers, operators, numbers, strings, and punctuation.

Translation Pipeline
--------------------
MATLAB Source
      │
      ▼
    Lexer
      │
      ▼
    Tokens (this module)
      │
      ▼
    Parser
      │
      ▼
      AST

The lexer converts raw source text into a sequence of Token objects. The parser
then analyzes these tokens to construct the Abstract Syntax Tree (AST).

Each token stores:
    - its type
    - its original text
    - the source line
    - the source column

This information is used for parsing, diagnostics, and error reporting.
"""

from dataclasses import dataclass
from enum import Enum, auto


# ==========================================================
# Token Types
# ==========================================================

class TokenType(Enum):
    """Enumeration of all MATLAB token types."""

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

    CLASSDEF = auto()
    PROPERTIES = auto()
    METHODS = auto()

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
    """
    Represents a single lexical token.

    Parameters
    ----------
    type : TokenType
        Token classification.

    value : str
        Original text of the token.

    line : int
        Source line number.

    column : int
        Source column number.
    """

    type: TokenType
    value: str
    line: int
    column: int

    def __str__(self) -> str:
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

    "classdef": TokenType.CLASSDEF,
    "properties": TokenType.PROPERTIES,
    "methods": TokenType.METHODS,
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

    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,

    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,

    ",": TokenType.COMMA,
    ";": TokenType.SEMICOLON,

    ".": TokenType.DOT,

    "@": TokenType.AT,
}