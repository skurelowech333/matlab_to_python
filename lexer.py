from __future__ import annotations

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 17:41:35 2026

@author: Sarah
"""

"""
lexer.py

Lexical analyzer for the MATLAB-to-Python translator.

The lexer converts MATLAB source text into a stream of Token objects.

Responsibilities:
    - Read source characters
    - Recognize MATLAB language elements
    - Track source locations
    - Generate tokens for the parser

The lexer does NOT:
    - Understand program structure
    - Build an AST
    - Translate MATLAB syntax

Example:

Input:
    x = sin(t);

Output:
    IDENTIFIER(x)
    ASSIGN(=)
    IDENTIFIER(sin)
    LPAREN(()
    IDENTIFIER(t)
    RPAREN())
    SEMICOLON(;)

"""

from pathlib import Path

from tokens import (
    Token,
    TokenType,
    KEYWORDS,
    OPERATORS,
)


class Lexer:
    """
    MATLAB source code lexer.

    Parameters
    ----------
    source : str
        MATLAB source text.

    Attributes
    ----------
    source : str
        Entire source file.

    position : int
        Current character index.

    line : int
        Current source line.

    column : int
        Current source column.
    """

    def __init__(self, source: str):

        self.source = source

        self.position = 0

        self.line = 1
        self.column = 1

        self.length = len(source)


    # ======================================================
    # Character utilities
    # ======================================================
    def current(self):
        """
        Return current character.
        """

        if self.position >= self.length:
            return None

        return self.source[self.position]


    def peek(self, offset=1):
        """
        Look ahead without consuming.
        """

        index = self.position + offset

        if index >= self.length:
            return None

        return self.source[index]


    def advance(self):
        """
        Consume one character.
        """

        char = self.current()

        if char is None:
            return None

        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1

        else:
            self.column += 1

        return char


    def make_token(self, token_type, value):
        """
        Create a token at current location.
        """

        return Token(
            token_type,
            value,
            self.line,
            self.column
        )


    # ======================================================
    # Whitespace
    # ======================================================
    def skip_whitespace(self):

        while True:

            char = self.current()

            if char is None:
                break

            if char in " \t\r":

                self.advance()

            else:
                break

    # ======================================================
    # Identifiers / Keywords
    # ======================================================
    def read_identifier(self):

        start_line = self.line
        start_col = self.column

        value = ""

        while True:

            char = self.current()

            if char is None:
                break

            if char.isalnum() or char == "_":

                value += char
                self.advance()

            else:
                break


        token_type = KEYWORDS.get(
            value,
            TokenType.IDENTIFIER
        )

        return Token(
            token_type,
            value,
            start_line,
            start_col
        )



    # ======================================================
    # Numbers
    # ======================================================
    def read_number(self):

        start_line = self.line
        start_col = self.column

        value = ""

        decimal = False


        while True:

            char = self.current()

            if char is None:
                break


            if char.isdigit():

                value += char
                self.advance()


            elif char == "." and not decimal:

                decimal = True
                value += char
                self.advance()


            else:

                break


        # scientific notation

        if self.current() in ("e", "E"):

            value += self.advance()


            if self.current() in ("+", "-"):

                value += self.advance()


            while self.current() and self.current().isdigit():

                value += self.advance()



        return Token(
            TokenType.NUMBER,
            value,
            start_line,
            start_col
        )



    # ======================================================
    # Comments
    # ======================================================
    def read_comment(self):

        start_line = self.line
        start_col = self.column


        value = ""


        while True:

            char = self.current()


            if char is None or char == "\n":
                break


            value += char
            self.advance()



        return Token(
            TokenType.COMMENT,
            value,
            start_line,
            start_col
        )



    # ======================================================
    # Operators
    # ======================================================
    def read_operator(self):

        start_line = self.line
        start_col = self.column


        # longest operators first

        for length in (3, 2, 1):

            text = self.source[
                self.position:
                self.position + length
            ]


            if text in OPERATORS:

                for _ in range(length):
                    self.advance()


                return Token(
                    OPERATORS[text],
                    text,
                    start_line,
                    start_col
                )


        return None



    # ======================================================
    # Main tokenizer
    # ======================================================
    def tokenize(self):

        tokens = []


        while self.current() is not None:


            self.skip_whitespace()


            char = self.current()


            if char is None:
                break



            # newline

            if char == "\n":

                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\n",
                        self.line,
                        self.column
                    )
                )

                self.advance()

                continue



            # comments

            if char == "%":

                tokens.append(
                    self.read_comment()
                )

                continue



            # identifiers

            if char.isalpha() or char == "_":

                tokens.append(
                    self.read_identifier()
                )

                continue



            # numbers

            if char.isdigit():

                tokens.append(
                    self.read_number()
                )

                continue



            # operators

            token = self.read_operator()


            if token:

                tokens.append(token)

                continue



            # unknown character

            raise SyntaxError(
                f"Unknown character "
                f"{char!r} "
                f"at {self.line}:{self.column}"
            )


        tokens.append(
            Token(
                TokenType.EOF,
                "",
                self.line,
                self.column
            )
        )


        return tokens



# ==========================================================
# Convenience loader
# ==========================================================

def tokenize_file(filename):

    source = Path(filename).read_text()

    lexer = Lexer(source)

    return lexer.tokenize()