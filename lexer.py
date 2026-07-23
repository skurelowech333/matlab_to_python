from __future__ import annotations

# -*- coding: utf-8 -*-
"""
lexer.py

Lexical analyzer for the MATLAB-to-Python translator.

Responsibilities:
    - Read MATLAB source
    - Recognize tokens
    - Track source locations
    - Generate parser input
"""

from pathlib import Path

from tokens import (
    Token,
    TokenType,
    KEYWORDS,
    OPERATORS,
)


class Lexer:

    def __init__(self, source: str):

        self.source = source

        self.position = 0
        self.line = 1
        self.column = 1

        self.length = len(source)

        self.tokens = []


    # ======================================================
    # Character utilities
    # ======================================================

    def current(self):

        if self.position >= self.length:
            return None

        return self.source[self.position]


    def peek(self, offset=1):

        index = self.position + offset

        if index >= self.length:
            return None

        return self.source[index]


    def advance(self):

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


    def add_token(self, token):

        self.tokens.append(token)

        return token


    # ======================================================
    # Whitespace
    # ======================================================

    def skip_whitespace(self):

        while self.current() in (" ", "\t", "\r"):

            self.advance()


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


        if self.current() in ("e", "E"):

            value += self.advance()

            if self.current() in ("+", "-"):

                value += self.advance()


            while (
                self.current()
                and self.current().isdigit()
            ):

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
    # Tokenizer
    # ======================================================

    def tokenize(self):

        tokens = []

        while self.current() is not None:

            self.skip_whitespace()

            char = self.current()

            if char is None:
                break


            if char == "\n":

                token = Token(
                    TokenType.NEWLINE,
                    "\n",
                    self.line,
                    self.column
                )

                tokens.append(
                    self.add_token(token)
                )

                self.advance()

                continue


            if char == "%":

                tokens.append(
                    self.add_token(
                        self.read_comment()
                    )
                )

                continue


            if char.isalpha() or char == "_":

                tokens.append(
                    self.add_token(
                        self.read_identifier()
                    )
                )

                continue


            if char.isdigit():

                tokens.append(
                    self.add_token(
                        self.read_number()
                    )
                )

                continue
            
            # MATLAB strings use double quotes
            if char == '"':
            
                tokens.append(
                    self.add_token(
                        self.read_string()
                    )
                )
            
                continue


            token = self.read_operator()

            if token:

                tokens.append(
                    self.add_token(token)
                )

                continue


            raise SyntaxError(
                f"Unknown character {char!r} "
                f"at {self.line}:{self.column}"
            )


        tokens.append(
            self.add_token(
                Token(
                    TokenType.EOF,
                    "",
                    self.line,
                    self.column
                )
            )
        )

        return tokens


    # ======================================================
    # Strings
    # ======================================================

    def read_string(self):

        start_line = self.line
        start_col = self.column

        quote = self.current()

        value = ""

        # consume opening quote
        self.advance()


        while True:

            char = self.current()

            if char is None:
                raise SyntaxError(
                    f"Unterminated string at "
                    f"{start_line}:{start_col}"
                )


            # closing quote
            if char == quote:
                self.advance()
                break


            # MATLAB escaped quote:
            # 'don''t'
            
            if (
                char == quote
                and self.peek() == quote
            ):
            
                value += quote
                self.advance()
                self.advance()
                continue
            
            
            # closing quote
            if char == quote:
                self.advance()
                break


            value += char
            self.advance()


        return Token(
            TokenType.STRING,
            value,
            start_line,
            start_col
        )

# ==========================================================
# Convenience loader
# ==========================================================

def tokenize_file(filename):

    source = Path(filename).read_text()

    return Lexer(source).tokenize()