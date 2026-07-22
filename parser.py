from __future__ import annotations

# -*- coding: utf-8 -*-
"""
parser.py

Recursive descent parser for MATLAB source code.

Features:
    - Functions
    - Assignments
    - Expressions
    - Function calls
    - Array indexing
    - For loops
    - If statements
    - Matrices
    - Element-wise operators
    - Source tracking for error recovery
"""

from tokens import TokenType

from abstract_syntax_tree import (
    Program,
    Function,
    Assignment,
    ExpressionStatement,
    ClassDef,
    PropertyBlock,
    For,
    If,
    Comment,
    Identifier,
    Number,
    String,
    BinaryOp,
    UnaryOp,
    Call,
    Matrix,
    Index,
    Slice,
    End,
    FieldAccess
)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    # ======================================================
    # Token utilities
    # ======================================================

    def current(self):
        return self.tokens[self.position]

    def peek(self, offset=1):
        index = self.position + offset
        if index >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[index]

    def advance(self):
        token = self.current()
        self.position += 1
        return token

    def check(self, token_type):
        return self.current().type == token_type

    def match(self, token_type):
        if self.check(token_type):
            self.advance()
            return True
        return False

    def expect(self, token_type):
        if not self.check(token_type):
            raise SyntaxError(
                f"Expected {token_type}, got {self.current()}"
            )
        return self.advance()

    def skip_newlines(self):
        while self.match(TokenType.NEWLINE):
            pass

    def make_node(self, node, token=None):
        if token is None:
            token = self.current()
        node.line = getattr(
            token,
            "line",
            0
        )
        node.source = getattr(
            token,
            "value",
            ""
        )
        return node

    # ======================================================
    # Program
    # ======================================================

    def parse(self):
        statements = []
        self.skip_newlines()

        while not self.check(TokenType.EOF):
            try:
                statement = self.statement()
                if statement is not None:
                    statements.append(
                        statement
                    )
            except Exception as error:
                self.errors.append(
                    {
                        "line":
                            getattr(
                                self.current(),
                                "line",
                                0
                            ),
                        "error":
                            str(error)
                    }
                )
                self.recover_statement()

            self.skip_newlines()

        return self.make_node(
            Program(
                body=statements
            )
        )

    def recover_statement(self):
        """
        Skip tokens until the next MATLAB statement boundary.
        """
        while not self.check(TokenType.EOF):
            if self.check(TokenType.NEWLINE):
                self.advance()
                break
            if self.check(TokenType.SEMICOLON):
                self.advance()
                break
            self.advance()

    # ======================================================
    # Statements
    # ======================================================

    def statement(self):
        if self.check(TokenType.COMMENT):
            token = self.advance()
            return self.make_node(
                Comment(
                    text=token.value
                ),
                token
            )
        if self.check(TokenType.CLASSDEF):
            return self.classdef()

        if self.check(TokenType.SEMICOLON):
            self.advance()
            return None

        if self.check(TokenType.FUNCTION):
            return self.function()

        if self.check(TokenType.FOR):
            return self.for_loop()

        if self.check(TokenType.IF):
            return self.if_statement()

        return self.assignment_or_expression()

    # ======================================================
    # Function
    # ======================================================

    def function(self):
        token = self.expect(
            TokenType.FUNCTION
        )
        outputs = []
        function_name = None

        if self.check(TokenType.IDENTIFIER):
            first = self.advance().value

            if self.match(TokenType.ASSIGN):
                outputs.append(first)
            else:
                function_name = first

        elif self.match(TokenType.LBRACKET):
            while not self.check(TokenType.RBRACKET):
                outputs.append(
                    self.expect(
                        TokenType.IDENTIFIER
                    ).value
                )
                self.match(
                    TokenType.COMMA
                )

            self.expect(
                TokenType.RBRACKET
            )
            self.expect(
                TokenType.ASSIGN
            )
        else:
            raise SyntaxError(
                "Invalid MATLAB function declaration"
            )

        if function_name is None:
            function_name = self.expect(
                TokenType.IDENTIFIER
            ).value

        inputs = []

        self.expect(
            TokenType.LPAREN
        )

        while not self.check(TokenType.RPAREN):
            inputs.append(
                self.expect(
                    TokenType.IDENTIFIER
                ).value
            )
            if not self.match(TokenType.COMMA):
                break

        self.expect(
            TokenType.RPAREN
        )

        body = self.block()

        return self.make_node(
            Function(
                name=function_name,
                inputs=inputs,
                outputs=outputs,
                body=body
            ),
            token
        )

    # ======================================================
    # Blocks
    # ======================================================

    def block(self):
        body = []
        self.skip_newlines()

        while not (
            self.check(TokenType.END)
            or self.check(TokenType.EOF)
        ):
            statement = self.statement()

            if statement is not None:
                body.append(
                    statement
                )

            self.skip_newlines()

        if self.check(TokenType.END):
            self.advance()

        return body

    # ======================================================
    # For Loop
    # ======================================================

    def for_loop(self):
        token = self.expect(
            TokenType.FOR
        )

        variable = self.expect(
            TokenType.IDENTIFIER
        ).value

        self.expect(
            TokenType.ASSIGN
        )

        start = self.expression()

        self.expect(
            TokenType.COLON
        )

        stop = self.expression()

        body = self.block()

        return self.make_node(
            For(
                variable=variable,
                start=start,
                stop=stop,
                body=body
            ),
            token
        )

    # ======================================================
    # If
    # ======================================================

    def if_statement(self):
        token = self.expect(
            TokenType.IF
        )

        condition = self.expression()
        body = self.block()

        return self.make_node(
            If(
                condition=condition,
                body=body
            ),
            token
        )

    # ======================================================
    # Assignment
    # ======================================================

    def assignment_or_expression(self):
        expression = self.expression()

        if self.match(TokenType.ASSIGN):
            value = self.expression()

            return self.make_node(
                Assignment(
                    target=expression,
                    value=value
                )
            )

        return self.make_node(
            ExpressionStatement(
                expression=expression
            )
        )

    # ======================================================
    # Expressions
    # ======================================================

    def expression(self):
        return self.binary_expression(0)

    PRECEDENCE = {
        TokenType.OR: 1,
        TokenType.AND: 2,
        TokenType.EQUAL: 3,
        TokenType.NOT_EQUAL: 3,
        TokenType.LESS: 4,
        TokenType.LESS_EQUAL: 4,
        TokenType.GREATER: 4,
        TokenType.GREATER_EQUAL: 4,
        TokenType.PLUS: 5,
        TokenType.MINUS: 5,
        TokenType.TIMES: 6,
        TokenType.DIVIDE: 6,
        TokenType.ELEMENT_TIMES: 6,
        TokenType.ELEMENT_DIVIDE: 6,
        TokenType.POWER: 7,
        TokenType.ELEMENT_POWER: 7,
    }

    def binary_expression(self, minimum):
        left = self.unary()

        while True:
            operator_type = self.current().type

            if operator_type not in self.PRECEDENCE:
                break

            precedence = self.PRECEDENCE[
                operator_type
            ]

            if precedence < minimum:
                break

            token = self.advance()

            right = self.binary_expression(
                precedence + 1
            )

            left = self.make_node(
                BinaryOp(
                    operator=token.value,
                    left=left,
                    right=right
                ),
                token
            )

        return left

    def unary(self):

        if self.check(TokenType.MINUS):
    
            token = self.advance()
    
            return self.make_node(
                UnaryOp(
                    operator="-",
                    operand=self.unary()
                ),
                token
            )
    
    
        if self.check(TokenType.PLUS):
    
            token = self.advance()
    
            return self.make_node(
                UnaryOp(
                    operator="+",
                    operand=self.unary()
                ),
                token
            )
    
    
        return self.postfix()

    # ======================================================
    # Postfix (indexing)
    # ======================================================

    def postfix(self):

        node = self.primary()
    
        while True:
    
            # obj.field
            if self.check(TokenType.DOT):
    
                self.advance()
    
                field = self.expect(
                    TokenType.IDENTIFIER
                ).value
    
                node = self.make_node(
                    FieldAccess(
                        value=node,
                        field=field
                    )
                )
    
                continue
    
    
            # A(i,j)
            if self.check(TokenType.LPAREN):
    
                self.advance()
    
                indices = self.parse_indices()
    
                self.expect(
                    TokenType.RPAREN
                )
    
                node = self.make_node(
                    Index(
                        value=node,
                        indices=indices
                    )
                )
    
                continue
    
    
            break
    
    
        return node

    def parse_indices(self):
        """
        Parse MATLAB indexing expressions: A(1,2), A(:,end), A(1:5), etc.
        """
        indices = []

        while not self.check(TokenType.RPAREN):
            # Colon (slice)
            if self.check(TokenType.COLON):
                self.advance()
                # Start is empty
                stop = None
                step = None
                
                # Check for stop
                if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                    stop = self.expression()
                
                # Check for step
                if self.check(TokenType.COLON):
                    self.advance()
                    if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                        step = self.expression()
                
                indices.append(
                    Slice(start=None, stop=stop, step=step)
                )
            else:
                # Try to parse an expression
                expr = self.expression()
                
                # Check if it's a slice (start:stop:step)
                if self.check(TokenType.COLON):
                    self.advance()
                    stop = None
                    step = None
                    
                    if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                        stop = self.expression()
                    
                    if self.check(TokenType.COLON):
                        self.advance()
                        if not self.check(TokenType.COMMA) and not self.check(TokenType.RPAREN):
                            step = self.expression()
                    
                    indices.append(
                        Slice(start=expr, stop=stop, step=step)
                    )
                else:
                    # Regular index
                    indices.append(expr)
            
            if not self.match(TokenType.COMMA):
                break

        return indices

    # ======================================================
    # Primary Expressions
    # ======================================================

    def matrix_element(self):
        return self.binary_expression(8)
    
    def primary(self):
        token = self.advance()

        # -------------------------------
        # Matrix
        # -------------------------------

        if token.type == TokenType.LBRACKET:
            rows = []
            row = []

            while not self.check(TokenType.RBRACKET):
                if self.check(TokenType.NEWLINE):
                    self.advance()
                    continue

                if self.check(TokenType.SEMICOLON):
                    self.advance()

                    if row:
                        rows.append(row)
                        row = []

                    continue

                row.append(self.matrix_element())

                self.match(
                    TokenType.COMMA
                )

            self.expect(
                TokenType.RBRACKET
            )

            if row:
                rows.append(row)

            return self.make_node(
                Matrix(
                    rows=rows
                ),
                token
            )

        # -------------------------------
        # Number
        # -------------------------------

        if token.type == TokenType.NUMBER:
            return self.make_node(
                Number(
                    value=float(token.value)
                ),
                token
            )

        # -------------------------------
        # Identifier
        # -------------------------------

        if token.type == TokenType.IDENTIFIER:
            node = self.make_node(
                Identifier(
                    name=token.value
                ),
                token
            )

            # Check for function call
            if self.check(TokenType.LPAREN):
                # Peek ahead to distinguish function call from indexing
                # If we see an identifier followed by (, it could be:
                # 1. func(args) - function call
                # 2. A(i) - array index
                # The postfix() method will handle this after primary()
                pass

            return node

        # -------------------------------
        # Parentheses
        # -------------------------------

        if token.type == TokenType.LPAREN:
            expression = self.expression()
            self.expect(
                TokenType.RPAREN
            )
            return expression

        raise SyntaxError(
            f"Unexpected token {token}"
        )
        
    # ======================================================
    # MATLAB Class Definition
    # ======================================================
    
    def classdef(self):
    
        token = self.expect(
            TokenType.CLASSDEF
        )
    
        name = self.expect(
            TokenType.IDENTIFIER
        ).value
    
    
        properties = []
        methods = []
    
    
        self.skip_newlines()
    
    
        while not self.check(TokenType.END) and not self.check(TokenType.EOF):
    
    
            # ------------------------------
            # Properties block
            # ------------------------------
    
            if self.check(TokenType.PROPERTIES):
    
                self.advance()
    
                body = []
    
                self.skip_newlines()
    
                while (
                    not self.check(TokenType.END)
                    and
                    not self.check(TokenType.EOF)
                ):
    
                    stmt = self.assignment_or_expression()
    
                    if stmt:
                        body.append(stmt)
    
                    self.skip_newlines()
    
    
                self.expect(
                    TokenType.END
                )
    
    
                properties.append(
                    PropertyBlock(
                        body=body
                    )
                )
    
    
                continue
    
    
    
            # ------------------------------
            # Methods block
            # ------------------------------
    
            if self.check(TokenType.METHODS):
    
                self.advance()
    
                self.skip_newlines()
    
    
                while (
                    not self.check(TokenType.END)
                    and
                    not self.check(TokenType.EOF)
                ):
    
                    if self.check(TokenType.FUNCTION):
    
                        methods.append(
                            self.function()
                        )
    
                    else:
    
                        self.advance()
    
    
                    self.skip_newlines()
    
    
                self.expect(
                    TokenType.END
                )
    
    
                continue
    
    
    
            self.advance()
    
    
        self.expect(
            TokenType.END
        )
    
    
        return self.make_node(
            ClassDef(
                name=name,
                properties=properties,
                methods=methods
            ),
            token
        )
